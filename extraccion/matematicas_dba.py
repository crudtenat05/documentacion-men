"""Extrae los Derechos Básicos de Aprendizaje de Matemáticas V.2 (MEN, 2016) desde el PDF oficial.

Cada página tiene dos columnas. Un DBA se reconoce por su número en tipografía grande; su enunciado
son las líneas contiguas al número hasta «Evidencias de aprendizaje». Las evidencias empiezan con la
viñeta «m» y terminan en «Ejemplo». El ejemplo se conserva como texto de apoyo: puede contener
fórmulas y figuras que el texto plano no reproduce, por eso no se usa como referente literal.

    python3 extraccion/matematicas_dba.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfutil import palabras, lineas, unir_lineas, tipografia, texto_linea

PDF = 'fuentes/men/dba-matematicas.pdf'
PRIMERA, ULTIMA = 7, 88          # páginas con DBA; las demás son presentación y contraportada
CORTE_COLUMNA = 325              # frontera horizontal entre columnas
Y_MIN, Y_MAX = 100, 780          # fuera de este rango: encabezado y pie de página


def grado_de_pagina(ws):
    cab = sorted([w for w in ws if w[1] < 70], key=lambda w: w[0])
    for i, w in enumerate(cab):
        if w[4] == 'Grado':
            resto = ''.join(x[4] for x in cab[i + 1:i + 3])
            m = re.match(r'(\d{1,2})', resto)
            if m:
                return int(m.group(1))
    return None


def flujo():
    """Líneas del documento en orden de lectura: página por página, columna izquierda y luego derecha."""
    salida, grado = [], None
    for p in range(PRIMERA, ULTIMA + 1):
        ws = palabras(PDF, p)
        grado = grado_de_pagina(ws) or grado
        for col, (x0, x1) in enumerate([(0, CORTE_COLUMNA), (CORTE_COLUMNA, 10_000)]):
            cw = [w for w in ws if x0 <= w[0] < x1 and Y_MIN < w[1] < Y_MAX]
            numeros = [w for w in cw if re.fullmatch(r'\d{1,2}\.', w[4]) and w[3] - w[1] > 20]
            resto = [w for w in cw if w not in numeros]
            nota_alto = None
            for y, fila in lineas(resto):
                llamada = (fila[0][3] - fila[0][1] < 8.5 and fila[0][4].isdigit()
                           and sum(1 for w in fila[1:] if re.search(r'[a-záéíóúñ]{3}', w[4])) >= 4)
                alto = sorted(w[3] - w[1] for w in fila)[len(fila) // 2]
                previa = salida[-1] if salida and salida[-1]['pagina'] == p and salida[-1]['col'] == col else None
                if llamada:                       # empieza una nota al pie
                    nota_alto = fila[1][3] - fila[1][1] if len(fila) > 1 else alto
                    es_nota = True
                elif nota_alto and previa and previa['nota'] and y - previa['y'] < 16 and abs(alto - nota_alto) < 0.4:
                    es_nota = True                # continúa la nota al pie
                else:
                    es_nota, nota_alto = False, None
                # llamadas de nota en superíndice dentro del texto: se retiran del texto literal
                if llamada:
                    limpia = fila[1:]
                else:  # la llamada ocupa su propio espacio: el siguiente fragmento se pega al anterior
                    limpia = []
                    for w in fila:
                        if w[4].isdigit() and w[3] - w[1] < 8.5 and limpia:
                            ultimo = limpia[-1]
                            limpia[-1] = (ultimo[0], ultimo[1], w[2], ultimo[3], ultimo[4])
                        else:
                            limpia.append(w)
                if not limpia:
                    continue
                salida.append({'pagina': p, 'col': col, 'y': y, 'x': limpia[0][0], 'grado': grado,
                               'texto': tipografia(texto_linea(limpia)), 'numero': None, 'nota': es_nota})
            for n in numeros:  # el número se ancla a la línea más cercana verticalmente
                cand = [l for l in salida if l['pagina'] == p and l['col'] == col]
                if cand:
                    mas_cerca = min(cand, key=lambda l: abs(l['y'] - (n[1] + 8)))
                    mas_cerca['numero'] = int(n[4][:-1])
    return salida


def extraer():
    L = flujo()
    # 1) enunciado: líneas contiguas al número, hacia arriba y hacia abajo, hasta «Evidencias de aprendizaje»
    rol = [None] * len(L)
    for i, l in enumerate(L):
        if l['numero'] is None:
            continue
        a = i
        while a - 1 >= 0 and L[a - 1]['pagina'] == l['pagina'] and L[a - 1]['col'] == l['col'] \
                and L[a]['y'] - L[a - 1]['y'] < 16 and not re.match(r'(Evidencias|Ejemplo|m ?[A-ZÁÉÍÓÚÑ])', L[a - 1]['texto']):
            a -= 1
        b = i
        while b + 1 < len(L) and not L[b + 1]['texto'].startswith('Evidencias de aprendizaje'):
            b += 1
        for k in range(a, b + 1):
            rol[k] = ('enunciado', l['numero'])
    # 2) recorrido secuencial
    dbas, actual, seccion = [], None, None
    for i, l in enumerate(L):
        if rol[i] and rol[i][0] == 'enunciado':
            if actual is None or actual['numero'] != rol[i][1] or actual['grado'] != l['grado'] or seccion != 'enunciado':
                actual = {'grado': l['grado'], 'numero': rol[i][1], 'enunciado': [], 'evidencias': [], 'ejemplo': [], 'notas': [],
                          'pagina_pdf': l['pagina']}
                dbas.append(actual)
            actual['enunciado'].append(l['texto'])
            seccion = 'enunciado'
            continue
        if actual is None:
            continue
        if l['nota']:
            if actual['notas'] and actual['notas'][-1][0] == (l['pagina'], l['col']) and not l.get('inicio'):
                actual['notas'][-1][1].append(l['texto'])
            else:
                actual['notas'].append([(l['pagina'], l['col']), [l['texto']]])
            continue
        t = l['texto']
        if t.startswith('Evidencias de aprendizaje'):
            seccion = 'evidencias'
        elif t.startswith('Ejemplo'):
            seccion = 'ejemplo'
            if t.strip() != 'Ejemplo':
                actual['ejemplo'].append(t[len('Ejemplo'):].strip())
        elif seccion == 'evidencias':
            vineta = re.match(r'm ?(?=[A-ZÁÉÍÓÚÑ¿¡(])', t)  # la viñeta «m» puede venir pegada a la palabra
            if vineta:
                actual['evidencias'].append([t[vineta.end():]])
            elif actual['evidencias']:
                actual['evidencias'][-1].append(t)
        elif seccion == 'ejemplo':
            actual['ejemplo'].append(t)
    salida, cortes = [], []
    for d in dbas:
        cod = f"MAT-DBA-{d['grado']}-{d['numero']:02d}"
        enunciado, cs = unir_lineas(d['enunciado'])
        cortes += [{'codigo': cod, 'palabra': c} for c in cs]
        evid = []
        for k, ev in enumerate(d['evidencias'], 1):
            texto, cs = unir_lineas(ev)
            cortes += [{'codigo': f'{cod}-E{k}', 'palabra': c} for c in cs]
            evid.append({'codigo': f'{cod}-E{k}', 'numero': k, 'texto': texto})
        ejemplo, _ = unir_lineas(d['ejemplo'])
        salida.append({'codigo': cod, 'area': 'matematicas', 'grado': d['grado'], 'numero': d['numero'],
                       'enunciado': enunciado, 'evidencias': evid, 'ejemplo_texto_plano': ejemplo or None,
                       'notas_al_pie': [unir_lineas(n[1])[0] for n in d['notas']],
                       'fuente': os.path.basename(PDF), 'pagina_pdf': d['pagina_pdf']})
    return salida, cortes


if __name__ == '__main__':
    datos, cortes = extraer()
    os.makedirs('datos/matematicas', exist_ok=True)
    with open('datos/matematicas/dba.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    with open('datos/matematicas/dba_cortes_de_palabra.json', 'w', encoding='utf-8') as f:
        json.dump(cortes, f, ensure_ascii=False, indent=1)
    print(len(datos), 'DBA;', sum(len(d['evidencias']) for d in datos), 'evidencias;', len(cortes), 'cortes')
