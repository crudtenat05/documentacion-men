"""Niveles de desempeño de las cinco pruebas de Saber 11° (documentos del ICFES de septiembre de 2025).

Uso (desde la raíz del repositorio):  python _soporte/extraccion/icfes_niveles_desempeno.py

A diferencia de la taxonomía, aquí no hay transcripción a mano: los descriptores se toman directamente del texto del
PDF (`pdftotext -raw`), separando por la frase «El evaluado que se ubica en el nivel …» y por la viñeta «»» de cada
descriptor. Solo se unen los renglones cortados y se quitan los rótulos de navegación de cada página.
"""
import csv
import hashlib
import json
import re
import subprocess
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PRUEBAS = [  # carpeta de datos, nombre, prefijo, archivo
    ('matematicas', 'Matemáticas', 'MAT', '22-septiembre-nd-prueba-matematicas-saber-11.pdf'),
    ('lectura_critica', 'Lectura Crítica', 'LEC', '22-septiembre-nd-prueba-lectura-critica-saber-11.pdf'),
    ('sociales_ciudadanas', 'Sociales y Ciudadanas', 'SOC', '22-septiembre-nd-prueba-sociales-y-ciudadanas-saber-11.pdf'),
    ('ciencias_naturales', 'Ciencias Naturales', 'NAT', '22-septiembre-nd-prueba-ciencias-naturales-saber-11.pdf'),
    ('ingles', 'Inglés', 'ING', '22-septiembre-nd-prueba-ingles-saber-11.pdf'),
]
ROTULOS = re.compile(r'^(Puntaje|Niveles|Niveles Puntaje|Saber 11º|Niveles de Desempeño|» Ir a página principal|Prueba .+|Continúan en la siguiente página.*)$')
RANGO = re.compile(r'^(\d+) a (\d+)$')
resumen = []

for carpeta, nombre, prefijo, archivo in PRUEBAS:
    pdf = RAIZ / 'fuentes/icfes' / archivo
    crudo = subprocess.run(['pdftotext', '-q', '-enc', 'UTF-8', '-raw', str(pdf), '-'], capture_output=True, check=True).stdout.decode('utf-8')
    lineas = [l.strip() for l in crudo.splitlines() if l.strip()]
    rangos = []
    for l in lineas:  # los cuatro rangos, en el orden en que aparecen la primera vez
        m = RANGO.match(l)
        if m and (int(m[1]), int(m[2])) not in rangos:
            rangos.append((int(m[1]), int(m[2])))
    assert len(rangos) == 4 and rangos[0][0] == 0 and rangos[-1][1] == 100 and all(rangos[i][1] + 1 == rangos[i + 1][0] for i in range(3)), (nombre, rangos)

    texto = ' '.join(l for l in lineas if not ROTULOS.match(l) and not RANGO.match(l))
    presentacion = texto.split('El evaluado que se ubica en el nivel')[0]
    niveles = {}
    for bloque in texto.split('El evaluado que se ubica en el nivel')[1:]:
        clave = re.match(r'\s*(Pre A1|A1|A2|B1|[1-4])\b', bloque)[1]
        cabeza, *vinetas = bloque.split('»')
        intro = re.sub(r'\s+', ' ', 'El evaluado que se ubica en el nivel' + cabeza).strip()
        n = niveles.setdefault(clave, {'nivel': clave, 'introduccion': intro, 'descriptores': []})
        n['descriptores'] += [re.sub(r'\s+', ' ', v).strip() for v in vinetas if v.strip()]
    assert len(niveles) == 4, (nombre, list(niveles))
    lista = []
    for i, (clave, n) in enumerate(niveles.items()):
        n.update({'codigo': f"{prefijo}-N{clave.replace(' ', '')}", 'orden': i + 1, 'puntaje_desde': rangos[i][0], 'puntaje_hasta': rangos[i][1]})
        n['descriptores'] = [{'codigo': f"{n['codigo']}.{j}", 'texto': d} for j, d in enumerate(n['descriptores'], 1)]
        lista.append(n)

    salida = RAIZ / '_soporte/datos/icfes' / carpeta
    salida.mkdir(parents=True, exist_ok=True)
    datos = {'documento': {'entidad': 'ICFES', 'titulo': f'Saber 11º · Niveles de Desempeño · Prueba {nombre}', 'anio': 2025,
                           'archivo': f'fuentes/icfes/{archivo}', 'origen': f'https://www.icfes.gov.co/wp-content/uploads/2025/09/{archivo}'},
             'prueba': carpeta, 'niveles': lista}
    (salida / 'niveles_desempeno.json').write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    with open(salida / 'niveles_desempeno.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['nivel', 'codigo_nivel', 'puntaje_desde', 'puntaje_hasta', 'codigo_descriptor', 'descriptor'])
        for n in lista:
            w.writerows([[n['nivel'], n['codigo'], n['puntaje_desde'], n['puntaje_hasta'], d['codigo'], d['texto']] for d in n['descriptores']])
    md = [f'# {nombre} · Saber 11° · niveles de desempeño', '', f'Fuente: ICFES, 2025 (`fuentes/icfes/{archivo}`). Textos literales del PDF.', '']
    for n in lista:
        md += [f"## Nivel {n['nivel']} · puntaje {n['puntaje_desde']} a {n['puntaje_hasta']}", '', n['introduccion'], ''] + [f"- `{d['codigo']}` {d['texto']}" for d in n['descriptores']] + ['']
    (salida / 'niveles_desempeno.md').write_text('\n'.join(md), encoding='utf-8')
    resumen.append((nombre, archivo, hashlib.sha256(pdf.read_bytes()).hexdigest(), lista))
    print(f"{nombre}: " + ' · '.join(f"{n['nivel']} ({n['puntaje_desde']}-{n['puntaje_hasta']}): {len(n['descriptores'])}" for n in lista))

ver = ['# Verificación ICFES · Niveles de desempeño (Saber 11°)', '', f'Fecha: {date.today().isoformat()}', '', '## Fuentes', '', '| Archivo | SHA-256 |', '|---|---|']
ver += [f'| `fuentes/icfes/{a}` | `{h}` |' for _, a, h, _ in resumen]
ver += ['', '## Resultado', '', '| Prueba | Rangos de puntaje | Descriptores por nivel | Total |', '|---|---|---|---|']
ver += [f"| {nom} | {' · '.join(str(n['puntaje_desde']) + ' a ' + str(n['puntaje_hasta']) for n in l)} | {' · '.join(str(len(n['descriptores'])) for n in l)} | {sum(len(n['descriptores']) for n in l)} |" for nom, _, _, l in resumen]
ver += ['', '## Método', '',
        '1. El texto se lee del PDF con `pdftotext -raw`; no hay transcripción a mano.',
        '2. Se quitan los rótulos de navegación que se repiten en cada página y se separa por nivel y por viñeta.',
        '3. El programa se detiene si una prueba no tiene exactamente cuatro niveles o si sus cuatro rangos no cubren de 0 a 100 sin huecos.',
        '4. En Matemáticas el nivel 3 ocupa dos páginas: sus descriptores se juntan en un solo nivel.', '',
        '## Notas', '',
        '- Erratas del PDF que se conservan: «presensentadas» (Matemáticas, nivel 2) y un paréntesis sin cerrar en el primer descriptor del nivel 3 de Matemáticas.',
        '- Inglés: el documento define cuatro niveles (Pre A1, A1, A2, B1). El reporte de resultados por establecimiento de 2025 usa cinco (A-, A1, A2, B1, B+), con otros cortes: no son comparables entre sí.',
        '- Cada prueba tiene sus propios cortes de puntaje.', '']
(RAIZ / '_soporte/verificacion/icfes_niveles_desempeno.md').write_text('\n'.join(ver), encoding='utf-8')
