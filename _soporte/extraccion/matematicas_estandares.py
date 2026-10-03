"""Extrae los Estándares Básicos de Competencias en Matemáticas (MEN, 2006) desde el PDF oficial.

Cada ciclo ocupa dos páginas: la izquierda con dos pensamientos y la derecha con tres, en columnas
con viñetas. Las columnas se delimitan por la posición horizontal de sus viñetas; el texto de cada
estándar se reconstruye uniendo sus líneas. No se escribe ni corrige ningún texto a mano.

    python3 extraccion/matematicas_estandares.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfutil import palabras, lineas, unir_lineas, tipografia, texto_linea

PDF = 'fuentes/men/estandares-matematicas.pdf'
CICLOS = {(1, 3): (35, 36), (4, 5): (37, 38), (6, 7): (39, 40), (8, 9): (41, 42), (10, 11): (43, 44)}
EJES = [  # (código, palabra que identifica el encabezado)
    ('PN', 'NUMÉRICO'), ('PE', 'ESPACIAL'), ('PM', 'MÉTRICO'), ('PA', 'ALEATORIO'), ('PV', 'VARIACIONAL'),
]


def columnas(pdf, pagina):
    ws = palabras(pdf, pagina)
    xs = sorted({round(w[0]) for w in ws if w[4] == '•'})
    bordes = []
    for x in xs:  # agrupa viñetas casi alineadas
        if not bordes or x - bordes[-1] > 30:
            bordes.append(x)
    resultado = []
    for i, x0 in enumerate(bordes):
        x1 = bordes[i + 1] - 3 if i + 1 < len(bordes) else 10_000
        col = [w for w in ws if x0 - 3 <= w[0] < x1]
        vinetas = [w for w in col if w[4] == '•']
        y_ini = min(v[1] for v in vinetas)
        encabezado = ' '.join(w[4] for w in sorted([w for w in ws if x0 - 25 <= w[0] < x1 and y_ini - 70 < w[1] < y_ini - 2 and w[4].isupper()], key=lambda z: (round(z[1]), z[0])))
        cuerpo = lineas([w for w in col if w[1] >= y_ini - 1])
        items, actual, previo_y = [], None, None
        for y, fila in cuerpo:
            if previo_y is not None and y - previo_y > 20:  # salto grande: termina la columna
                break
            previo_y = y
            if fila[0][4] == '•':
                actual = {'lineas': [texto_linea(fila[1:])], 'y': y}
                items.append(actual)
            elif actual:
                actual['lineas'].append(texto_linea(fila))
        resultado.append((tipografia(encabezado), items))
    return resultado


def extraer():
    salida, cortes = [], []
    for (g1, g2), paginas in CICLOS.items():
        for pagina in paginas:
            for encabezado, items in columnas(PDF, pagina):
                eje = next(c for c, clave in EJES if clave in encabezado.upper())
                for n, it in enumerate(items, 1):
                    texto, cs = unir_lineas([tipografia(l) for l in it['lineas']])
                    codigo = f'MAT-EBC-{g1}.{g2}-{eje}-{n:02d}'
                    salida.append({'codigo': codigo, 'area': 'matematicas', 'grado_desde': g1, 'grado_hasta': g2,
                                   'eje': eje, 'eje_nombre': encabezado, 'orden': n, 'texto': texto,
                                   'fuente': os.path.basename(PDF), 'pagina_pdf': pagina})
                    cortes += [{'codigo': codigo, 'palabra': c} for c in cs]
    return salida, cortes


if __name__ == '__main__':
    datos, cortes = extraer()
    os.makedirs('_soporte/datos/matematicas', exist_ok=True)
    with open('_soporte/datos/matematicas/estandares.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    with open('_soporte/datos/matematicas/estandares_cortes_de_palabra.json', 'w', encoding='utf-8') as f:
        json.dump(cortes, f, ensure_ascii=False, indent=1)
    print(len(datos), 'estándares;', len(cortes), 'palabras reconstruidas en cortes de línea')
