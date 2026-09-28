"""Verificación independiente de los textos extraídos de un área.

Dos comprobaciones por cada estándar, enunciado de DBA y evidencia:

1. Literalidad: el texto aparece, carácter por carácter, en el texto plano del PDF obtenido por otra
   vía (pdftotext -raw, orden del flujo interno del PDF). Solo se ignoran diferencias tipográficas:
   espacios y saltos de línea, guiones de corte de palabra al final de línea, ligaduras (ﬁ → fi) y
   llamadas de nota al pie en superíndice. Cualquier otra diferencia hace fallar la verificación.
2. Completitud: lo que sigue al texto en el PDF es el inicio de otro elemento (viñeta, encabezado,
   número de DBA, pie de página), no la continuación de la misma frase. Así se detecta un texto al que
   le falte su final.

Los casos que la máquina no puede confirmar se revisan contra el PDF y se registran en
verificacion/<area>_confirmaciones_manuales.json con la razón.

    python3 extraccion/verificar.py matematicas
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import date

SIGUIENTES = ('•', 'm', 'Evidenciasdeaprendizaje', 'Ejemplo', 'PENSAMIENTO', 'Matemáticas', 'MatematicasDBA',
              'Derechos', 'Nota', 'Estándares', 'Paralocual', 'Lenguaje', 'LENGUAJE')


def compacto(s):
    s = unicodedata.normalize('NFC', unicodedata.normalize('NFKC', s))
    s = re.sub(r'-\s*\n\s*(?=[a-záéíóúñ])', '', s)   # corte de palabra al final de línea
    return re.sub(r'\s+', '', s)


def texto_pdf(pdf):
    raw = subprocess.run(['pdftotext', '-raw', pdf, '-'], capture_output=True, text=True, check=True).stdout
    return compacto(raw)


_cache = {}


def sin_llamadas(fuente):
    """Texto del PDF sin llamadas de nota al pie: un dígito suelto pegado a una letra o a un paréntesis."""
    if fuente not in _cache:
        _cache[fuente] = re.sub(r'(?<=[A-Za-záéíóúñ)])\d(?=[^\d])', '', fuente)
    return _cache[fuente]


def aparece(texto, fuente):
    t = compacto(texto)
    return t in fuente or t in sin_llamadas(fuente)


def completo(texto, fuente, inicios=()):
    """Lo que sigue al texto debe ser el inicio de otro elemento: una viñeta, un encabezado, un título
    en mayúsculas, un número, o el comienzo de otro texto extraído del mismo documento (en páginas a
    varias columnas, el flujo interno del PDF pasa de un enunciado al de la columna vecina)."""
    t = compacto(texto)
    for f in (fuente, sin_llamadas(fuente)):
        i = f.find(t)
        while i >= 0:
            despues = f[i + len(t):i + len(t) + 40]
            if (despues.startswith(SIGUIENTES) or re.match(r'\d', despues) or despues == ''
                    or re.match(r'[A-ZÁÉÍÓÚÑ]{4,}', despues) or any(despues.startswith(x) for x in inicios)):
                return True
            i = f.find(t, i + 1)
    return False


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, 'rb') as f:
        for bloque in iter(lambda: f.read(1 << 20), b''):
            h.update(bloque)
    return h.hexdigest()


def textos(area):
    for archivo, tipo in [('estandares.json', 'Estándar'), ('dba.json', 'DBA')]:
        for d in json.load(open(f'datos/{area}/{archivo}', encoding='utf-8')):
            pdf = f"fuentes/men/{d['fuente']}"
            yield tipo, d['codigo'], d.get('texto') or d.get('enunciado'), pdf, d['pagina_pdf']
            for e in d.get('subprocesos', []):
                yield 'Subproceso', e['codigo'], e['texto'], pdf, d['pagina_pdf']
            for e in d.get('evidencias', []):
                yield 'Evidencia', e['codigo'], e['texto'], pdf, d['pagina_pdf']


def main(area):
    fuentes, filas = {}, []
    todos = list(textos(area))
    inicios = {pdf: {compacto(t)[:15] for _, _, t, p, _ in todos if p == pdf} for _, _, _, pdf, _ in todos}
    for tipo, cod, texto, pdf, pag in todos:
        if pdf not in fuentes:
            fuentes[pdf] = texto_pdf(pdf)
        filas.append({'tipo': tipo, 'codigo': cod, 'pagina_pdf': pag, 'fuente': pdf,
                      'literal': aparece(texto, fuentes[pdf]), 'completo': completo(texto, fuentes[pdf], inicios[pdf])})
    ruta_manual = f'verificacion/{area}_confirmaciones_manuales.json'
    manuales = {m['codigo']: m for m in json.load(open(ruta_manual, encoding='utf-8'))} if os.path.exists(ruta_manual) else {}
    for f in filas:
        if not f['completo'] and f['codigo'] in manuales:
            f['completo_por'] = 'revisión manual'
    no_literales = [f for f in filas if not f['literal']]
    sin_frontera = [f for f in filas if not f['completo'] and 'completo_por' not in f]
    resumen = {'area': area, 'fecha': date.today().isoformat(), 'total': len(filas),
               'literales': len(filas) - len(no_literales),
               'completos_automatico': sum(1 for f in filas if f['completo']),
               'completos_manual': sum(1 for f in filas if f.get('completo_por')),
               'pendientes': [f['codigo'] for f in no_literales + sin_frontera],
               'fuentes': {os.path.basename(p): sha256(p) for p in fuentes}}
    os.makedirs('verificacion', exist_ok=True)
    with open(f'verificacion/{area}.json', 'w', encoding='utf-8') as f:
        json.dump({'resumen': resumen, 'textos': filas}, f, ensure_ascii=False, indent=1)

    conteo = {}
    for f in filas:
        conteo[f['tipo']] = conteo.get(f['tipo'], 0) + 1
    L = [f'# Verificación de {area}', '',
         f"Fecha: {resumen['fecha']}", '',
         '## Fuentes', '', '| Archivo | SHA-256 |', '|---|---|']
    L += [f'| `{a}` | `{h}` |' for a, h in resumen['fuentes'].items()]
    L += ['', '## Resultado', '', '| Tipo | Textos |', '|---|---|']
    L += [f'| {t} | {n} |' for t, n in conteo.items()]
    L += ['', f"- Literales en el PDF: **{resumen['literales']} de {resumen['total']}**",
          f"- Completos (frontera confirmada automáticamente): {resumen['completos_automatico']}",
          f"- Completos (confirmados por revisión manual): {resumen['completos_manual']}",
          f"- Pendientes: **{len(resumen['pendientes'])}**", '']
    if manuales:
        L += ['## Confirmaciones manuales', '']
        L += [f"- `{c}` (pág. {m['pagina_pdf']}): {m['razon']}" for c, m in manuales.items()]
        L += ['']
    if resumen['pendientes']:
        L += ['## Pendientes', ''] + [f'- `{c}`' for c in resumen['pendientes']] + ['']
    L += ['## Método', '', (__doc__ or '').strip().split('\n\n    python3')[0]]
    with open(f'verificacion/{area}.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print(f"{resumen['total']} textos; {resumen['literales']} literales; "
          f"{resumen['completos_automatico']} completos automático; {resumen['completos_manual']} manual; "
          f"{len(resumen['pendientes'])} pendientes")
    return 1 if resumen['pendientes'] else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
