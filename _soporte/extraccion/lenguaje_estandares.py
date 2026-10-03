"""Extrae los Estándares Básicos de Competencias del Lenguaje (MEN, 2006) desde el PDF oficial.

Cada ciclo ocupa dos páginas con columnas. Cada columna es un estándar: un enunciado identificador,
la expresión «Para lo cual,» y sus subprocesos en viñetas. Según la Nota 1 del documento, el estándar
comprende el enunciado y sus subprocesos. Un factor puede tener más de una columna (más de un
estándar) bajo un mismo título; en ese caso la columna sin título hereda el de su vecina.

    python3 extraccion/lenguaje_estandares.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfutil import palabras, lineas, unir_lineas, tipografia, texto_linea

PDF = 'fuentes/men/estandares-lengua-castellana.pdf'
CICLOS = {(1, 3): (15, 16), (4, 5): (17, 18), (6, 7): (19, 20), (8, 9): (21, 22), (10, 11): (23, 24)}
FACTORES = [  # (código, palabra que identifica el título del factor)
    ('PT', 'PRODUCCIÓN'), ('CI', 'COMPRENSIÓN'), ('LI', 'LITERATURA'), ('MC', 'MEDIOS'), ('EC', 'ÉTICA'),
]
MAYUS = set('ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚÜ')


def es_titulo(w):
    letras = [c for c in w[4] if c.isalpha()]
    return letras and all(c in MAYUS for c in letras)


def titulos(ws, y_para):
    """Bloques de título: palabras en mayúscula sobre las columnas, agrupadas por línea y por cercanía.
    Cada bloque devuelve su centro horizontal y su texto."""
    cand = sorted((w for w in ws if es_titulo(w) and y_para - 200 < w[1] < y_para - 10 and 45 < w[0] < 575),
                  key=lambda w: (round(w[1]), w[0]))
    segmentos = []
    for w in cand:
        s = next((s for s in segmentos if abs(s['y'] - w[1]) < 3 and 0 <= w[0] - s['x1'] < 12), None)
        if s:
            s['ws'].append(w); s['x1'] = w[2]
        else:
            segmentos.append({'y': w[1], 'x0': w[0], 'x1': w[2], 'ws': [w]})
    bloques = []
    for s in sorted(segmentos, key=lambda s: s['y']):
        c = (s['x0'] + s['x1']) / 2
        b = next((b for b in bloques if 0 < s['y'] - b['y'] < 20 and abs(b['c'] - c) < 60), None)
        if b:
            b['texto'] += ' ' + ' '.join(w[4] for w in s['ws']); b['y'] = s['y']
            b['c'] = (min(b['x0'], s['x0']) + max(b['x1'], s['x1'])) / 2
            b['x0'], b['x1'] = min(b['x0'], s['x0']), max(b['x1'], s['x1'])
        else:
            bloques.append({'y': s['y'], 'x0': s['x0'], 'x1': s['x1'], 'c': c, 'texto': ' '.join(w[4] for w in s['ws'])})
    return bloques


def columnas(pagina, factor_previo=None):
    ws = palabras(PDF, pagina)
    anclas = sorted((w for i, w in enumerate(ws) if w[4] == 'Para' and i + 1 < len(ws) and ws[i + 1][4] == 'lo'),
                    key=lambda w: w[0])
    y_para = anclas[0][1]
    bloques = titulos(ws, y_para)
    y_titulos = max((b['y'] for b in bloques), default=y_para - 140) + 8
    salida = []
    for i, a in enumerate(anclas):
        x0 = a[0] - 3
        x1 = anclas[i + 1][0] - 3 if i + 1 < len(anclas) else 10_000
        col = [w for w in ws if x0 <= w[0] < x1]
        # el título de una columna es el bloque más cercano a su centro; un título centrado sobre dos
        # columnas queda como el más cercano de ambas
        centro = (x0 + min(x1, 575)) / 2
        propio = min(bloques, key=lambda b: abs(b['c'] - centro)) if bloques else None
        titulo = tipografia(propio['texto']) if propio else ''
        factor = next((c for c, clave in FACTORES if clave in titulo.upper()), None) or factor_previo
        if factor is None:
            raise RuntimeError(f'Columna sin factor en la página {pagina}, x={x0:.0f}')
        factor_previo = factor
        enunciado = [texto_linea(f) for y, f in lineas([w for w in col if y_titulos < w[1] < a[1] - 1])]
        subs, actual, previo_y = [], None, None
        for y, fila in lineas([w for w in col if w[1] > a[1] + 5]):
            if previo_y is not None and y - previo_y > 20:
                break
            previo_y = y
            if fila[0][4] == '•':
                actual = [texto_linea(fila[1:])]
                subs.append(actual)
            elif actual:
                actual.append(texto_linea(fila))
        salida.append((factor, titulo, enunciado, subs, pagina))
    return salida, factor_previo


def extraer():
    datos, cortes, contador = [], [], {}
    for (g1, g2), paginas in CICLOS.items():
        nombres, previo = {}, None
        for pagina in paginas:
            cols, previo = columnas(pagina, previo)
            for factor, titulo, enunciado, subs, pag in cols:
                if titulo:
                    nombres[factor] = titulo
                n = contador[(g1, factor)] = contador.get((g1, factor), 0) + 1
                cod = f'LEN-EBC-{g1}.{g2}-{factor}-{n:02d}'
                texto, cs = unir_lineas([tipografia(l) for l in enunciado])
                cortes += [{'codigo': cod, 'palabra': c} for c in cs]
                sub = []
                for k, s in enumerate(subs, 1):
                    t, cs = unir_lineas([tipografia(l) for l in s])
                    cortes += [{'codigo': f'{cod}-S{k}', 'palabra': c} for c in cs]
                    sub.append({'codigo': f'{cod}-S{k}', 'numero': k, 'texto': t})
                datos.append({'codigo': cod, 'area': 'lenguaje', 'grado_desde': g1, 'grado_hasta': g2, 'eje': factor,
                              'eje_nombre': nombres.get(factor, titulo), 'orden': n, 'texto': texto, 'subprocesos': sub,
                              'fuente': os.path.basename(PDF), 'pagina_pdf': pag})
    return datos, cortes


if __name__ == '__main__':
    datos, cortes = extraer()
    os.makedirs('_soporte/datos/lenguaje', exist_ok=True)
    with open('_soporte/datos/lenguaje/estandares.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    with open('_soporte/datos/lenguaje/estandares_cortes_de_palabra.json', 'w', encoding='utf-8') as f:
        json.dump(cortes, f, ensure_ascii=False, indent=1)
    print(len(datos), 'estándares;', sum(len(d['subprocesos']) for d in datos), 'subprocesos;', len(cortes), 'cortes')
