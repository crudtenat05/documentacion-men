"""Salidas de lectura para áreas que por ahora solo tienen DBA (los estándares se extraen después).

    python3 extraccion/salidas_dba.py ciencias_naturales

Genera desde datos/<area>/dba.json verificado: dba.csv, evidencias.csv y <area>.md.
"""
import csv
import json
import sys

NOMBRES = {'ciencias_naturales': 'Ciencias Naturales', 'ciencias_sociales': 'Ciencias Sociales'}


def main(area):
    base = f'datos/{area}'
    dba = json.load(open(f'{base}/dba.json', encoding='utf-8'))
    with open(f'{base}/dba.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['codigo', 'grado', 'numero', 'enunciado', 'fuente', 'pagina_pdf'])
        for d in dba:
            w.writerow([d['codigo'], d['grado'], d['numero'], d['enunciado'], d['fuente'], d['pagina_pdf']])
    with open(f'{base}/evidencias.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['codigo', 'dba', 'grado', 'numero', 'texto', 'fuente', 'pagina_pdf'])
        for d in dba:
            for e in d['evidencias']:
                w.writerow([e['codigo'], d['codigo'], d['grado'], e['numero'], e['texto'], d['fuente'], d['pagina_pdf']])
    nombre = NOMBRES.get(area, area)
    L = [f'# {nombre} · Derechos Básicos de Aprendizaje', '',
         f"Fuente: `fuentes/men/{dba[0]['fuente']}` (MEN, V.1, 2016). Texto extraído del PDF y verificado "
         f"(`verificacion/{area}.md`). {len(dba)} DBA y {sum(len(d['evidencias']) for d in dba)} evidencias.", '']
    grado = None
    for d in dba:
        if d['grado'] != grado:
            grado = d['grado']
            L += [f'## Grado {grado}', '']
        L += [f"### {d['codigo']} · DBA {d['numero']} (pág. {d['pagina_pdf']})", '', d['enunciado'], '',
              '**Evidencias de aprendizaje**', '']
        L += [f"- `{e['codigo']}` {e['texto']}" for e in d['evidencias']]
        L += ['']
    with open(f'{base}/{area}.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    print(nombre, len(dba), 'DBA →', f'{base}/dba.csv, evidencias.csv, {area}.md')


if __name__ == '__main__':
    main(sys.argv[1])
