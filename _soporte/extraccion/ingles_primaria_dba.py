"""Extrae los Derechos Básicos de Aprendizaje de Inglés de Transición a 5.° (MEN, 2016) desde el PDF oficial.

    python3 extraccion/ingles_primaria_dba.py

El PDF trae páginas dobles (dos páginas impresas por página del archivo). Cada grado ocupa una doble página: la
izquierda con el número grande del grado («Tr» en Transición) y una cuadrícula de 2 × 2 DBA; la derecha con más
DBA o con casillas en blanco para el docente (que no son DBA oficiales). Cada DBA tiene su número (27,7 pt), un
enunciado que termina en «Por ejemplo» / «como en el siguiente ejemplo» y un ejemplo ilustrado en inglés.
El grado se escribe 0 para Transición.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfutil import palabras, lineas, unir_lineas, tipografia, texto_linea

PDF = 'fuentes/men/dba-transicion-y-primaria_ingles.pdf'
MITAD = 589              # borde entre las dos páginas impresas
FIN = re.compile(r'(,?;?\s*(así\s+)?(como|tal como)\s+(se\s+)?(muestra\s+)?(en\s+)?el\s+(siguiente\s+ejemplo|texto\s+siguiente)'
                 r'|(?<=\.)\s*Por\s+ejemplo|\s+Por\s+ejemplo|\s*Puede,\s+por\s+ejemplo)')   # conserva el punto propio
ES = re.compile(r'\b(de|la|el|que|los|las|en|y|para|con|sobre|su|sus|a|un|una)\b')
EN = re.compile(r"\b(I|I'm|you|is|are|the|my|your|What|Where|How|this|This|have|it|It|and|do|don’t)\b")


def enunciado_de(bloque):
    """Texto en español hasta donde empieza el ejemplo: el marcador («Por ejemplo», «como en el siguiente
    ejemplo»…) o, si no lo hay, la primera oración que ya está en inglés."""
    m = FIN.search(bloque)
    if m:
        return bloque[:m.start()]
    oraciones = re.split(r'(?<=[.!?])\s+', bloque)
    salida = []
    for o in oraciones:
        if salida and (EN.search(o) or not ES.search(o)):
            break
        salida.append(o)
    return ' '.join(salida)


# Un globo de diálogo del ejemplo se cruza con el enunciado y la lectura por posición intercala sus palabras.
# Se fija el enunciado como se lee en la página (pág. 13); queda registrado en correcciones_tipograficas.json.
CORRECCIONES = {
    'ING-DBA-5-03': 'Intercambia información sobre hábitos, gustos y preferencias acerca de temas conocidos, '
                    'siguiendo modelos provistos por el profesor.',
}


def main():
    dbas, grado = [], None
    for p in range(8, 15):
        ws = [w for w in palabras(PDF, p) if 60 < w[1] < 690]
        grande = [w for w in ws if w[3] - w[1] > 45 and w[0] < MITAD]
        if grande:
            grado = 0 if grande[0][4] == 'Tr' else int(grande[0][4])
        for x0, x1 in [(0, MITAD), (MITAD, 10_000)]:
            pagina = [w for w in ws if x0 <= w[0] < x1 and w[3] - w[1] < 45]
            numeros = [w for w in pagina if re.fullmatch(r'\d{1,2}', w[4]) and 20 < w[3] - w[1] < 35]
            dos = [w for w in numeros if w[4] == '2']
            if x0 == 0 and dos and not any(w[4] == '1' for w in numeros):
                # el «1» de la página izquierda está dibujado como imagen: ocupa la celda superior izquierda,
                # a la altura del DBA 2
                numeros.append((75, dos[0][1], 85, dos[0][3], '1'))
            numeros.sort(key=lambda w: (round(w[1] / 150), w[0]))
            for n in numeros:
                # celda: desde el número hacia la derecha hasta la columna vecina y hacia abajo hasta la fila siguiente
                derecha = min([m[0] for m in numeros if m[0] > n[0] + 50 and abs(m[1] - n[1]) < 60] + [x1])
                abajo = min([m[1] for m in numeros if m[1] > n[1] + 100 and abs(m[0] - n[0]) < 120] + [690])
                celda = [w for w in pagina if n[0] - 5 <= w[0] < derecha - 5 and n[1] - 10 <= w[1] < abajo - 10 and w is not n]
                texto = [tipografia(texto_linea(f)) for _, f in lineas(celda)]
                bloque = unir_lineas(texto)[0]
                enun = enunciado_de(bloque).strip().rstrip(',;: ')   # literal: sin agregar punto final
                if not ES.search(enun):
                    continue   # casilla en blanco para el docente
                cod = f'ING-DBA-{grado}-{int(n[4]):02d}'
                dbas.append({'codigo': cod, 'area': 'ingles', 'grado': grado, 'numero': int(n[4]), 'enunciado': enun,
                             'evidencias': [], 'fuente': os.path.basename(PDF), 'pagina_pdf': p})
    aplicadas = []
    for d in dbas:
        if d['codigo'] in CORRECCIONES:
            aplicadas.append({'codigo': d['codigo'], 'antes': d['enunciado'], 'despues': CORRECCIONES[d['codigo']]})
            d['enunciado'] = CORRECCIONES[d['codigo']]
    dbas.sort(key=lambda d: (d['grado'], d['numero']))
    return dbas, aplicadas


if __name__ == '__main__':
    d, a = main()
    print(len(d), 'DBA de Transición a 5.°;', len(a), 'corrección')
