"""Verifica y publica la taxonomía de una prueba del ICFES transcrita a mano desde la guía de orientación.

Lo usan los extractores de las pruebas cuya taxonomía no se saca por coordenadas (Sociales y Ciudadanas, Ciencias
Naturales, Inglés). Cada extractor declara los textos y llama a `publicar()`. La regla es la misma de todo el
repositorio: NO se escribe nada si un solo texto no aparece literal en su página del PDF.

Cómo se comprueba: el texto de cada página se lee con `pdftotext -raw` (orden del contenido, que respeta columnas y
filas de tabla) y se compara ignorando solo espacios y saltos de línea.
"""
import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PDF = 'fuentes/icfes/guia-orientacion-saber11-2026-2.pdf'
DOCUMENTO = {
    'codigo': 'ICFES-GUIA-S11-2026-2',
    'entidad': 'ICFES',
    'titulo': 'Guía de orientación del Examen Saber 11º 2026-2 (Calendario A)',
    'version': '2026-2',
    'anio': 2026,
    'archivo': PDF,
}

_paginas = {}


def _plano(texto):
    return re.sub(r'\s+', ' ', texto).strip()


def pagina(n):
    if n not in _paginas:
        r = subprocess.run(['pdftotext', '-q', '-enc', 'UTF-8', '-raw', '-f', str(n), '-l', str(n), str(RAIZ / PDF), '-'],
                           capture_output=True, check=True)
        _paginas[n] = _plano(r.stdout.decode('utf-8'))
    return _paginas[n]


def publicar(prueba, nombre, prefijo, descripcion, pagina_prueba, competencias, notas=(), pendientes=(), extra_md='', extra=None, comprobaciones=()):
    """`competencias`: lista de dicts con nombre, descripcion, porcentaje, pagina, pagina_porcentaje, rotulo_porcentaje,
    habilidades (opcional: numero, nombre, descripcion, pagina) y afirmaciones (numero, texto, pagina, evidencias:
    {numero: texto} o {numero: (texto, pagina)} cuando la tabla sigue en otra página).
    `extra`: datos propios de la prueba que se agregan al JSON; `comprobaciones`: sus textos, como (texto, pagina)."""
    fallos, cuenta = [], {'descripcion': 0, 'habilidad': 0, 'afirmacion': 0, 'evidencia': 0, 'porcentaje': 0, 'extra': 0}
    for c in competencias:
        for a in c['afirmaciones']:
            a['evidencias'] = {n: (v if isinstance(v, tuple) else (v, a['pagina'])) for n, v in a['evidencias'].items()}

    def revisar(tipo, texto, pag):
        cuenta[tipo] += 1
        if _plano(texto) not in pagina(pag):
            fallos.append(f'[{tipo}, pág. {pag}] {texto[:100]}')

    revisar('descripcion', descripcion, pagina_prueba)
    for c in competencias:
        revisar('descripcion', c['descripcion'], c['pagina'])
        revisar('porcentaje', f"{c['rotulo_porcentaje']} {c['porcentaje']} %", c['pagina_porcentaje'])
        for h in c.get('habilidades', []):
            revisar('habilidad', f"{h['numero']}. {h['nombre']} {h['descripcion']}", h['pagina'])
        for a in c['afirmaciones']:
            revisar('afirmacion', f"{a['numero']}. {a['texto']}", a['pagina'])
            for num, (texto, pag) in a['evidencias'].items():
                revisar('evidencia', f'{num} {texto}', pag)
    for texto, pag in comprobaciones:
        revisar('extra', texto, pag)
    if sum(c['porcentaje'] for c in competencias) != 100:
        fallos.append('Los porcentajes de las competencias no suman 100.')
    if fallos:
        sys.exit('NO se escribió nada. Textos que no aparecen literales en el PDF:\n- ' + '\n- '.join(fallos))

    salida = RAIZ / '_soporte/datos/icfes' / prueba
    salida.mkdir(parents=True, exist_ok=True)
    arbol, filas = [], []
    for i, c in enumerate(competencias, 1):
        cc = f'{prefijo}-C{i}'
        nodo = {'codigo': cc, 'nombre': c['nombre'], 'descripcion': c['descripcion'], 'porcentaje_preguntas': c['porcentaje'],
                'orden': i, 'pagina': c['pagina']}
        if c.get('habilidades'):
            nodo['habilidades'] = [{'codigo': f"{prefijo}-H{i}.{h['numero']}", **h} for h in c['habilidades']]
        nodo['afirmaciones'] = []
        for a in c['afirmaciones']:
            ca = f"{prefijo}-A{a['numero']}"
            evs = [{'codigo': f'{prefijo}-E{num}', 'numero': num, 'texto': t, 'pagina': pg} for num, (t, pg) in a['evidencias'].items()]
            nodo['afirmaciones'].append({'codigo': ca, 'numero': a['numero'], 'texto': a['texto'], 'pagina': a['pagina'], 'evidencias': evs})
            for e in evs:
                filas.append([cc, c['nombre'], c['porcentaje'], ca, a['texto'], e['codigo'], e['texto'], e['pagina']])
        arbol.append(nodo)

    datos = {'documento': DOCUMENTO, 'prueba': prueba, 'descripcion': descripcion, 'pagina': pagina_prueba, 'competencias': arbol}
    datos.update(extra or {})
    (salida / 'taxonomia.json').write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    with open(salida / 'evidencias.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['competencia', 'competencia_nombre', 'porcentaje_preguntas', 'afirmacion', 'afirmacion_texto', 'evidencia', 'evidencia_texto', 'pagina_pdf'])
        w.writerows(filas)

    md = [f'# {nombre} · Saber 11° · taxonomía del ICFES', '',
          f"Fuente: {DOCUMENTO['titulo']} (`{PDF}`). Textos literales del PDF, con su página.", '',
          f'{descripcion} (pág. {pagina_prueba})', '', '## Competencias, afirmaciones y evidencias', '']
    for nodo in arbol:
        md += [f"### `{nodo['codigo']}` {nodo['nombre']} · {nodo['porcentaje_preguntas']} % de las preguntas (pág. {nodo['pagina']})", '', nodo['descripcion'], '']
        for h in nodo.get('habilidades', []):
            md += [f"**Habilidad** `{h['codigo']}` {h['nombre']} (pág. {h['pagina']})", '', h['descripcion'], '']
        for a in nodo['afirmaciones']:
            md.append(f"- **Afirmación** `{a['codigo']}` {a['texto']} (pág. {a['pagina']})")
            md += [f"  - `{e['codigo']}` {e['texto']}" for e in a['evidencias']]
        md.append('')
    if extra_md:
        md += [extra_md, '']
    if notas:
        md += ['## Notas de transcripción', ''] + [f'- {n}' for n in notas] + ['']
    (salida / f'{prueba}.md').write_text('\n'.join(md), encoding='utf-8')

    total = sum(cuenta.values())
    n_af = sum(len(c['afirmaciones']) for c in competencias)
    n_hab = sum(len(c.get('habilidades', [])) for c in competencias)
    sha = hashlib.sha256((RAIZ / PDF).read_bytes()).hexdigest()
    ver = [f'# Verificación ICFES · {nombre}', '', f'Fecha: {date.today().isoformat()}', '', '## Fuente', '',
           '| Archivo | SHA-256 |', '|---|---|', f'| `{PDF}` | `{sha}` |', '', '## Resultado', '', '| Tipo | Elementos |', '|---|---|',
           f'| Competencia | {len(competencias)} |', f'| Habilidad (con su descripción) | {n_hab} |', f'| Afirmación | {n_af} |',
           f'| Evidencia | {len(filas)} |', '',
           f'- Comprobaciones literales contra el PDF: **{total} de {total}** (descripción de la prueba y de cada competencia, habilidades, afirmaciones, evidencias y porcentajes). El programa se detiene sin escribir si una sola falla.',
           '- Los porcentajes de las competencias suman 100.', '']
    if notas:
        ver += [f'- {n}' for n in notas] + ['']
    ver += ['## Método', '',
            f'1. Los textos están transcritos en `extraccion/icfes_{prueba}.py`, leídos del PDF y contrastados con la imagen de cada página (`pdftoppm`).',
            '2. `extraccion/icfes_transcrito.py` comprueba que cada uno aparezca literal en el texto de su página (`pdftotext -raw`). Solo se toleran espacios y saltos de línea.',
            '3. Si todo coincide, genera el JSON, el CSV y la versión legible.', '']
    if pendientes:
        ver += ['## Pendiente', ''] + [f'- {p}' for p in pendientes] + ['']
    (RAIZ / '_soporte/verificacion' / f'icfes_{prueba}.md').write_text('\n'.join(ver), encoding='utf-8')
    print(f'{nombre}: {total} de {total} comprobaciones literales. {len(competencias)} competencias, {n_hab} habilidades, {n_af} afirmaciones, {len(filas)} evidencias.')
