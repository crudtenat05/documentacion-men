"""Extractor común de los Derechos Básicos de Aprendizaje del MEN (serie 2016: dos columnas por página).

Cada página tiene dos columnas. Un DBA se reconoce por su número en tipografía grande; su enunciado
son las líneas contiguas al número hasta «Evidencias de aprendizaje». Las evidencias empiezan con la
viñeta «m» y terminan en «Ejemplo». El ejemplo se conserva como texto de apoyo: puede contener
fórmulas y figuras que el texto plano no reproduce, por eso no se usa como referente literal.

    Lo usan extraccion/<area>_dba.py.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfutil import palabras, lineas, unir_lineas, tipografia, texto_linea

CORTE_COLUMNA = 325              # frontera horizontal entre columnas
Y_MIN, Y_MAX = 100, 780          # fuera de este rango: encabezado y pie de página


def grado_de_pagina(ws):
    """Grado del encabezado («… • Grado 3º»). Algunos PDF parten la palabra («G» «rado»)."""
    cab = sorted([w for w in ws if w[1] < 70 and w[3] - w[1] >= 10], key=lambda w: w[0])  # sin adornos pequeños
    m = re.search(r'Grado\s*(\d{1,2})', ' '.join(w[4] for w in cab).replace('G rado', 'Grado'))
    return int(m.group(1)) if m else None


def flujo(PDF, PRIMERA, ULTIMA, VINETA='m', corte=CORTE_COLUMNA):
    """Líneas del documento en orden de lectura: página por página, columna izquierda y luego derecha."""
    salida, grado = [], None
    for p in range(PRIMERA, ULTIMA + 1):
        ws = palabras(PDF, p)
        propio = grado_de_pagina(ws)
        grado = propio or grado
        c = corte
        if corte == 'auto':
            # fuera la rosa de los vientos decorativa de Sociales: rumbos (0–330) y letras cardinales sueltas, en tipografía
            # de hasta 10 puntos; el texto del documento mide 12 o 13
            ws = [w for w in ws if w[3] - w[1] >= 6 and not (re.fullmatch(r'[0-9NSOE]{1,3}', w[4]) and w[3] - w[1] <= 10.5)]
            ws = [w for w in ws if not (w[4].isdigit() and w[1] > 755)]   # número de página al pie
            # la columna derecha empieza donde está su número de DBA o su «Evidencias»; varía por página
            # el corte es el centro del canal vacío entre columnas: la franja vertical que ninguna palabra cruza
            cuerpo = [w for w in ws if Y_MIN < w[1] < Y_MAX]
            libres = [x for x in range(260, 380) if not any(w[0] - 1 < x < w[2] + 1 for w in cuerpo)]
            if libres:
                tramos, ini = [], libres[0]
                for a_, b_ in zip(libres, libres[1:] + [None]):
                    if b_ != a_ + 1:
                        tramos.append((ini, a_)); ini = b_
                x0, x1 = max(tramos, key=lambda t: t[1] - t[0])
                c = (x0 + x1) / 2
            else:
                c = 310
        for col, (x0, x1) in enumerate([(0, c), (c, 10_000)]):
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
                salida.append({'pagina': p, 'col': col, 'y': y, 'x': limpia[0][0], 'grado': grado, 'encabezado': propio is not None,
                               'texto': tipografia(texto_linea(limpia)), 'numero': None, 'nota': es_nota})
            for n in numeros:  # el número se ancla a la línea más cercana verticalmente
                cand = [l for l in salida if l['pagina'] == p and l['col'] == col]
                if cand:
                    mas_cerca = min(cand, key=lambda l: abs(l['y'] - (n[1] + 8)))
                    mas_cerca['numero'] = int(n[4][:-1])
    return salida


def extraer(PDF, PRIMERA, ULTIMA, prefijo, area, VINETA='m', por_reinicio=False, corte=CORTE_COLUMNA):
    """VINETA: letra con que el PDF codifica la viñeta de las evidencias (m en Matemáticas y Lenguaje)."""
    L = flujo(PDF, PRIMERA, ULTIMA, corte=corte)
    # 1) enunciado: líneas contiguas al número, hacia arriba y hacia abajo, hasta «Evidencias de aprendizaje»
    rol = [None] * len(L)
    for i, l in enumerate(L):
        if l['numero'] is None:
            continue
        a = i
        while a - 1 >= 0 and L[a - 1]['pagina'] == l['pagina'] and L[a - 1]['col'] == l['col'] \
                and L[a]['y'] - L[a - 1]['y'] < 16 and not re.match(r'(Evidencias|Ejemplo|' + VINETA + r' ?[A-ZÁÉÍÓÚÑ])', L[a - 1]['texto']):
            a -= 1
        b = i
        while b + 1 < len(L) and not L[b + 1]['texto'].startswith('Evidencias de aprendi'):
            b += 1
        for k in range(a, b + 1):
            rol[k] = ('enunciado', l['numero'])
    # 2) recorrido secuencial
    dbas, actual, seccion = [], None, None
    for i, l in enumerate(L):
        if rol[i] and rol[i][0] == 'enunciado':
            if actual is None or actual['numero'] != rol[i][1] or actual['grado'] != l['grado'] or seccion != 'enunciado':
                actual = {'grado': l['grado'], 'encabezado': l['encabezado'], 'numero': rol[i][1], 'enunciado': [], 'evidencias': [], 'ejemplo': [], 'notas': [],
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
        if t.startswith('Evidencias de aprendi'):   # a veces el PDF parte la palabra («aprendi zaje»)
            seccion = 'evidencias'
        elif t.startswith('Ejemplo'):
            seccion = 'ejemplo'
            if t.strip() != 'Ejemplo':
                actual['ejemplo'].append(t[len('Ejemplo'):].strip())
        elif seccion == 'evidencias':
            vineta = re.match(VINETA + r'\s*(?=[A-ZÁÉÍÓÚÑ¿¡(])', t)  # la viñeta «m» puede venir pegada a la palabra
            previa = L[i - 1] if i else None
            salto = previa and previa['pagina'] == l['pagina'] and previa['col'] == l['col'] and l['y'] - previa['y'] > 20
            if vineta:
                actual['evidencias'].append([t[vineta.end():]])
            elif salto:
                seccion = None  # tras un espacio grande sin viñeta viene una figura o recuadro del ejemplo
            elif actual['evidencias']:
                actual['evidencias'][-1].append(t)
        elif seccion == 'ejemplo':
            actual['ejemplo'].append(t)
    if por_reinicio:
        # El encabezado «Grado N» solo está en algunas páginas: el grado avanza cuando la numeración vuelve
        # a empezar (aparece un DBA cuyo número ya existe en el grado actual). Los encabezados que sí están
        # sirven de control: si no coinciden, se detiene la extracción.
        grado, vistos = dbas[0]['grado'], set()
        for d in dbas:
            if d['numero'] in vistos:
                grado, vistos = grado + 1, set()
            vistos.add(d['numero'])
            if d['grado'] is not None and d['grado'] != grado and d.get('encabezado'):
                raise SystemExit(f"Grado inconsistente en la página {d['pagina_pdf']}: encabezado {d['grado']}, numeración {grado}")
            d['grado'] = grado
    salida, cortes = [], []
    for d in dbas:
        cod = f"{prefijo}-DBA-{d['grado']}-{d['numero']:02d}"
        enunciado, cs = unir_lineas(d['enunciado'])
        cortes += [{'codigo': cod, 'palabra': c} for c in cs]
        evid = []
        for k, ev in enumerate(d['evidencias'], 1):
            texto, cs = unir_lineas(ev)
            cortes += [{'codigo': f'{cod}-E{k}', 'palabra': c} for c in cs]
            evid.append({'codigo': f'{cod}-E{k}', 'numero': k, 'texto': texto})
        ejemplo, _ = unir_lineas(d['ejemplo'])
        salida.append({'codigo': cod, 'area': area, 'grado': d['grado'], 'numero': d['numero'],
                       'enunciado': enunciado, 'evidencias': evid, 'ejemplo_texto_plano': ejemplo or None,
                       'notas_al_pie': [unir_lineas(n[1])[0] for n in d['notas']],
                       'fuente': os.path.basename(PDF), 'pagina_pdf': d['pagina_pdf']})
    return salida, cortes



def guardar(area, datos, cortes):
    os.makedirs(f'datos/{area}', exist_ok=True)
    with open(f'datos/{area}/dba.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    with open(f'datos/{area}/dba_cortes_de_palabra.json', 'w', encoding='utf-8') as f:
        json.dump(cortes, f, ensure_ascii=False, indent=1)
    print(len(datos), 'DBA;', sum(len(d['evidencias']) for d in datos), 'evidencias;', len(cortes), 'cortes')
