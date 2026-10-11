"""Extrae los Estándares Básicos de Competencias en Ciencias Sociales y en Ciencias Naturales (MEN, 2006)
desde el PDF oficial.

Cada grupo de grados ocupa una doble página. En la franja superior están los estándares («Al terminar
tercer grado…»). Debajo, en columnas, las acciones concretas de pensamiento y de producción con las que
se alcanzan («Para lograrlo…»): «…me aproximo al conocimiento como científico(a) social/natural»,
«…manejo conocimientos propios de las ciencias sociales/naturales» (tres columnas) y «…desarrollo
compromisos personales y sociales». En el documento las acciones no cuelgan de un estándar en particular,
sino de su columna; así se conservan aquí.

Las palabras se leen con PyMuPDF (posición de cada palabra en la página).

    python3 extraccion/ciencias_estandares.py
"""
import json
import os
import sys

import pymupdf

sys.path.insert(0, os.path.dirname(__file__))
from pdfutil import lineas, unir_lineas, tipografia, texto_linea

PDF = 'fuentes/men/estandares-ciencias-sociales-naturales.pdf'
PAGINA_LIBRO = 95   # la página 1 del PDF es la 96 del libro
GRUPOS = [(1, 3), (4, 5), (6, 7), (8, 9), (10, 11)]
AREAS = {  # área: (prefijo del código, primera página, nombre de la ciencia en las columnas)
    'ciencias_sociales': ('CS', 27, 'sociales'),
    'ciencias_naturales': ('CN', 37, 'naturales'),
}
# (palabra que identifica el título de la columna, código, nombre). El orden importa: «biológicos» antes de «vivo».
COLUMNAS = {
    'ciencias_sociales': [
        ('aproximo', 'AC', 'Me aproximo al conocimiento como científico(a) social'),
        ('historia', 'HC', 'Relaciones con la historia y las culturas'),
        ('espaciales', 'EA', 'Relaciones espaciales y ambientales'),
        ('ético', 'EP', 'Relaciones ético-políticas'),
        ('compromisos', 'CP', 'Desarrollo compromisos personales y sociales'),
    ],
    'ciencias_naturales': [
        ('aproximo', 'AC', 'Me aproximo al conocimiento como científico(a) natural'),
        ('biológicos', 'PB', 'Entorno vivo · Procesos biológicos'),
        ('químicos', 'PQ', 'Entorno físico · Procesos químicos'),
        ('físicos', 'PF', 'Entorno físico · Procesos físicos'),
        ('vivo', 'EV', 'Entorno vivo'),
        ('físico', 'EF', 'Entorno físico'),
        ('tecnología', 'CT', 'Ciencia, tecnología y sociedad'),
        ('compromisos', 'CP', 'Desarrollo compromisos personales y sociales'),
    ],
}
# Defectos de la lectura del PDF, confirmados contra la página. Se registran en
# datos/…/estandares_correcciones_tipograficas.json.
CORRECCIONES = {
    # «Europa-América-África» cae partido al final de línea; el guion es parte del término, no un corte de palabra
    'CS-EBC-6.7-EA-11': [('Europa-América- África', 'Europa-América-África')],
}
MANEJO = {'HC', 'EA', 'EP', 'PB', 'PQ', 'PF', 'EV', 'EF', 'CT'}


def palabras(doc, pagina):
    """Palabras del cuerpo de la página (x0, y0, x1, y1, texto). Se descartan la marca de agua
    («Ciencias Sociales 1º - 3º», letras de más de 30 puntos) y el rótulo vertical del margen."""
    return [w[:5] for w in doc[pagina - 1].get_text('words') if w[3] - w[1] < 30 and 60 <= w[0] and w[2] <= 562]


def unir(textos):
    return unir_lineas([tipografia(t) for t in textos])


def pagina(doc, n, area):
    """Devuelve (encabezado, estándares, columnas) de una página.
    estándares: lista de (empieza con flecha, líneas); columnas: lista de (código, nombre, título leído,
    viñetas), y cada viñeta es (subtítulo o None, líneas)."""
    ws = palabras(doc, n)
    y_manejo = min(w[1] for w in ws if w[4] in ('…manejo', 'propios'))
    vinetas = sorted((w for w in ws if w[4] == '•'), key=lambda w: w[0])
    xs = []
    for w in vinetas:
        if not xs or w[0] - xs[-1] > 20:
            xs.append(w[0])
    y_vinetas = min(w[1] for w in vinetas)

    # Franja superior: el encabezado en letra grande y los estándares en letra pequeña
    franja = [w for w in ws if 140 < w[1] < y_manejo - 8]
    grande = [w for w in franja if w[3] - w[1] > 13]
    encabezado = ' '.join(texto_linea(f) for y, f in lineas(grande))
    # Cada estándar es un bloque de texto que empieza con una punta de flecha (un signo, no una letra).
    # Un bloque sin flecha es la continuación del estándar que empezó en la página anterior.
    pequenas = [w for w in franja if w[3] - w[1] <= 13]
    cajas = sorted(b for b in doc[n - 1].get_text('blocks')
                   if any(b[0] - 1 <= w[0] and w[2] <= b[2] + 1 and b[1] - 1 <= w[1] and w[3] <= b[3] + 1 for w in pequenas))
    bloques = []
    for b in cajas:
        flecha = not b[4][:1].isalnum()
        if bloques and b[0] < bloques[-1]['x1']:
            bloques[-1]['x1'] = max(bloques[-1]['x1'], b[2])
            bloques[-1]['flecha'] |= flecha
        else:
            bloques.append({'x0': b[0], 'x1': b[2], 'flecha': flecha})
    estandares = []
    for b in bloques:
        suyas = [w for w in pequenas if b['x0'] - 1 <= (w[0] + w[2]) / 2 <= b['x1'] + 1]
        estandares.append((b['flecha'], [texto_linea(f) for y, f in lineas(suyas)]))

    columnas = []
    for i, x in enumerate(xs):
        x0, x1 = x - 3, (xs[i + 1] - 3 if i + 1 < len(xs) else 10_000)
        col = [w for w in ws if x0 <= w[0] < x1]
        titulo = ' '.join(texto_linea(f) for y, f in lineas([w for w in col if y_manejo + 8 < w[1] < y_vinetas - 5]))
        titulo = tipografia(titulo)
        clave = next((c for c in COLUMNAS[area] if c[0] in titulo), None)
        if clave is None:
            raise RuntimeError(f'Columna sin título reconocido en la página {n}: «{titulo}»')
        # Una línea sin viñeta separada de la anterior por un espacio en blanco es un subtítulo de la columna
        items, actual, previo_y, subtitulo = [], None, None, None
        for y, fila in lineas([w for w in col if w[1] >= y_vinetas - 2]):
            salto = previo_y is not None and y - previo_y > 15
            previo_y = y
            if fila[0][4] == '•':
                actual = [texto_linea(fila[1:])]
                items.append((subtitulo, actual))
            elif salto:
                subtitulo, actual = tipografia(texto_linea(fila)), None
            elif actual:
                actual.append(texto_linea(fila))
            else:
                raise RuntimeError(f'Línea sin viñeta ni subtítulo en la página {n}: «{texto_linea(fila)}»')
        columnas.append((clave[1], clave[2], titulo, items))
    return encabezado, estandares, columnas


def extraer(area):
    prefijo, primera, ciencia = AREAS[area]
    doc = pymupdf.open(PDF)
    datos, cortes, titulos = [], [], []

    def registro(cod, g1, g2, tipo, eje, nombre, grupo_col, orden, lineas_texto, pag, **extra):
        texto, cs = unir(lineas_texto)
        cortes.extend({'codigo': cod, 'palabra': c} for c in cs)
        datos.append({'codigo': cod, 'area': area, 'grado_desde': g1, 'grado_hasta': g2, 'tipo': tipo, 'eje': eje,
                      'eje_nombre': nombre, 'columna': grupo_col, 'orden': orden, 'texto': texto, **extra,
                      'fuente': os.path.basename(PDF), 'pagina_pdf': pag, 'pagina_libro': pag + PAGINA_LIBRO})

    for k, (g1, g2) in enumerate(GRUPOS):
        paginas = (primera + 2 * k, primera + 2 * k + 1)
        leidas = [pagina(doc, n, area) for n in paginas]
        encabezado = tipografia(leidas[0][0]).replace('Para lograrlo...', '').strip()
        generales = []   # [página, líneas, página donde continúa]
        for pag, (_, estandares, _) in zip(paginas, leidas):
            for flecha, ls in estandares:
                if flecha:
                    generales.append([pag, list(ls), None])
                else:   # continuación del estándar que empezó en la página anterior
                    generales[-1][1] += ls
                    generales[-1][2] = pag
        for n, (pag, ls, sigue) in enumerate(generales, 1):
            extra = {'continua_en_pagina_pdf': sigue} if sigue else {}
            registro(f'{prefijo}-EBC-{g1}.{g2}-EG-{n:02d}', g1, g2, 'estandar', 'EG', 'Estándares', encabezado,
                     n, ls, pag, **extra)
        for pag, (_, _, columnas) in zip(paginas, leidas):
            for eje, nombre, titulo, items in columnas:
                titulos.append({'pagina_pdf': pag, 'eje': eje, 'titulo_leido': titulo})
                grupo_col = (f'…manejo conocimientos propios de las ciencias {ciencia}' if eje in MANEJO
                             else '…' + nombre[:1].lower() + nombre[1:])
                for i, (subtitulo, ls) in enumerate(items, 1):
                    extra = {'subtitulo': subtitulo} if subtitulo else {}
                    registro(f'{prefijo}-EBC-{g1}.{g2}-{eje}-{i:02d}', g1, g2, 'accion', eje, nombre, grupo_col,
                             i, ls, pag, **extra)
    aplicadas = []
    for d in datos:
        for antes, despues in CORRECCIONES.get(d['codigo'], []):
            if antes not in d['texto']:
                raise SystemExit(f"Corrección sin efecto en {d['codigo']}: «{antes}»")
            d['texto'] = d['texto'].replace(antes, despues)
            aplicadas.append({'codigo': d['codigo'], 'antes': antes, 'despues': despues})
    return datos, cortes, titulos, aplicadas


if __name__ == '__main__':
    for area in AREAS:
        datos, cortes, titulos, aplicadas = extraer(area)
        os.makedirs(f'_soporte/datos/{area}', exist_ok=True)
        with open(f'_soporte/datos/{area}/estandares.json', 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=1)
        with open(f'_soporte/datos/{area}/estandares_cortes_de_palabra.json', 'w', encoding='utf-8') as f:
            json.dump(cortes, f, ensure_ascii=False, indent=1)
        with open(f'_soporte/datos/{area}/estandares_correcciones_tipograficas.json', 'w', encoding='utf-8') as f:
            json.dump(aplicadas, f, ensure_ascii=False, indent=1)
        print(area, sum(d['tipo'] == 'estandar' for d in datos), 'estándares;',
              sum(d['tipo'] == 'accion' for d in datos), 'acciones;', len(cortes), 'cortes;', len(aplicadas), 'correcciones tipográficas')
