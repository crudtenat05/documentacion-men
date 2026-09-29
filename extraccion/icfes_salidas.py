"""Genera, a partir de datos/icfes/<prueba>/taxonomia.json (extraído y verificado), las salidas de
lectura y de sistemas, y el reporte de verificación. Nunca se editan a mano.

- datos/icfes/<prueba>/<prueba>.md            (lectura)
- datos/icfes/<prueba>/evidencias.csv          (competencia → afirmación → evidencia)
- datos/icfes/<prueba>/contenidos.csv
- verificacion/icfes_<prueba>.md

    python3 extraccion/icfes_salidas.py matematicas
"""
import csv, hashlib, json, sys
from datetime import date

NOMBRES = {'matematicas': 'Matemáticas'}


def main(prueba):
    base = f'datos/icfes/{prueba}'
    d = json.load(open(f'{base}/taxonomia.json', encoding='utf-8'))
    doc = d['documento']

    with open(f'{base}/evidencias.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['competencia', 'competencia_nombre', 'porcentaje_preguntas', 'afirmacion', 'afirmacion_texto', 'evidencia', 'evidencia_texto', 'pagina_pdf'])
        for c in d['competencias']:
            for a in c['afirmaciones']:
                for e in a['evidencias']:
                    w.writerow([c['codigo'], c['nombre'], c['porcentaje_preguntas'], a['codigo'], a['texto'], e['codigo'], e['texto'], a['pagina']])
    with open(f'{base}/contenidos.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['codigo', 'categoria', 'tipo', 'orden', 'texto', 'pagina_pdf'])
        for ct in d['contenidos']:
            w.writerow([ct['codigo'], ct['categoria'], ct['tipo'], ct['orden'], ct['texto'], ct['pagina']])

    L = [f"# {NOMBRES[prueba]} · Saber 11° · taxonomía del ICFES", '',
         f"Fuente: {doc['titulo']} (`{doc['archivo']}`). Textos literales del PDF, con su página.", '',
         '## Competencias, afirmaciones y evidencias', '']
    for c in d['competencias']:
        L += [f"### `{c['codigo']}` {c['nombre']} · {c['porcentaje_preguntas']} % de las preguntas (pág. {c['pagina']})", '', c['descripcion'], '']
        for a in c['afirmaciones']:
            L += [f"- **Afirmación** `{a['codigo']}` {a['texto']}"]
            L += [f"  - `{e['codigo']}` {e['texto']}" for e in a['evidencias']]
        L.append('')
    L += ['## Contenidos', '']
    for cat in dict.fromkeys(ct['categoria'] for ct in d['contenidos']):
        L += [f"### {cat}", '']
        for tipo, titulo in (('generico', 'Genéricos'), ('no_generico', 'No genéricos')):
            items = [ct for ct in d['contenidos'] if ct['categoria'] == cat and ct['tipo'] == tipo]
            if items:
                L += [f"**{titulo}**", ''] + [f"- `{ct['codigo']}` {ct['texto']} (pág. {ct['pagina']})" for ct in items] + ['']
    open(f'{base}/{prueba}.md', 'w', encoding='utf-8').write('\n'.join(L))

    sha = hashlib.sha256(open(doc['archivo'], 'rb').read()).hexdigest()
    n_af = sum(len(c['afirmaciones']) for c in d['competencias'])
    n_ev = sum(len(a['evidencias']) for c in d['competencias'] for a in c['afirmaciones'])
    total = len(d['competencias']) + n_af + n_ev + len(d['contenidos'])
    R = [f"# Verificación ICFES · {NOMBRES[prueba]}", '', f"Fecha: {date.today().isoformat()}", '',
         '## Fuente', '', '| Archivo | SHA-256 |', '|---|---|', f"| `{doc['archivo']}` | `{sha}` |", '',
         '## Resultado', '', '| Tipo | Textos |', '|---|---|',
         f"| Competencia | {len(d['competencias'])} |", f"| Afirmación | {n_af} |", f"| Evidencia | {n_ev} |", f"| Contenido | {len(d['contenidos'])} |", '',
         f"- Literales en el PDF: **{total} de {total}** (descripción de cada competencia, afirmaciones, evidencias y contenidos). "
         "El extractor se detiene sin escribir si uno solo no aparece literal.",
         '- Única corrección tipográfica: la maquetación deja un espacio antes del punto final de dos descripciones («EBC .»); se quita.', '',
         '## Método', '',
         '1. `extraccion/icfes_matematicas.py` lee el PDF con la posición de cada palabra y separa las columnas de la tabla de cada competencia (afirmación y evidencias) y las columnas de la figura de contenidos.',
         '2. La descripción de cada competencia, cada afirmación y cada evidencia deben aparecer literales en el texto de su página, y cada contenido en el texto de su columna, leídos por otra vía (`pdftotext` sin posiciones). Solo se toleran espacios y cortes de palabra con guion.',
         '3. `extraccion/icfes_salidas.py` genera las salidas desde el JSON verificado.', '',
         '## Pendiente', '',
         '- **Niveles de desempeño de Matemáticas** (rangos de puntaje y descriptores). No están en esta guía: vienen en el documento «Niveles de desempeño · Prueba Matemáticas Saber 11°» del ICFES. '
         'Falta el PDF original para extraerlos y verificarlos. Hasta entonces, ValorativoWeb los carga desde una transcripción no verificada.']
    open(f'verificacion/icfes_{prueba}.md', 'w', encoding='utf-8').write('\n'.join(R) + '\n')
    print('ok', total, 'textos;', sha[:16])


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'matematicas')
