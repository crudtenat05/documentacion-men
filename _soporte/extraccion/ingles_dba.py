"""Extrae los Derechos Básicos de Aprendizaje de Inglés (MEN, 2016) desde los PDF oficiales: 6.° a 11.° aquí, y
Transición a 5.° con extraccion/ingles_primaria_dba.py. Todo queda en datos/ingles/dba.json.

    python3 extraccion/ingles_dba.py

Formato distinto de la serie 2016 de las otras áreas: cada página tiene dos columnas y en cada una hay DBA
encabezados por su número en tipografía grande (32 pt). El DBA no trae «evidencias de aprendizaje»: su enunciado
termina en «Por ejemplo», y lo que sigue es un ejemplo (diálogos, textos o imágenes en inglés) que se conserva solo
como texto de apoyo, no como referente literal.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pdfutil import palabras, lineas, unir_lineas, tipografia, texto_linea

PDF = 'fuentes/men/dba-ingles.pdf'
CORTE = 330          # canal entre columnas
PIE = 690            # número de página


def grado_de_pagina(ws):
    m = re.search(r'Grado\s*(\d{1,2})', ' '.join(w[4] for w in sorted(ws, key=lambda w: (w[1], w[0])) if w[1] < 130))
    return int(m.group(1)) if m else None


def main():
    dbas, cortes = [], []
    for p in range(1, 37):
        ws = [w for w in palabras(PDF, p) if w[1] < PIE]
        grado = grado_de_pagina(ws)
        if not grado:
            continue
        numeros = [w for w in ws if re.fullmatch(r'\d{1,2}', w[4]) and w[3] - w[1] > 25]
        for n in numeros:
            # un DBA ocupa todo el ancho de la página solo si sus primeras líneas cruzan el canal entre columnas
            # (una palabra pisa el canal, o dos palabras consecutivas de la misma línea quedan a cada lado y casi juntas)
            cruza = False
            for _, fila in lineas([w for w in ws if n[1] - 4 <= w[1] < n[1] + 70]):
                if any(w[0] < CORTE < w[2] for w in fila) or any(
                        a_[2] <= CORTE <= b_[0] and b_[0] - a_[2] < 10 for a_, b_ in zip(fila, fila[1:])):
                    cruza = True
            vecino = not cruza
            col = ((0, CORTE) if n[0] < CORTE else (CORTE, 10_000)) if vecino else (0, 10_000)
            debajo = [m[1] for m in numeros if m is not n and m[1] > n[1] + 5
                      and (not vecino or col[0] <= m[0] < col[1])]
            hasta = min(debajo) if debajo else PIE
            celda = [w for w in ws if w is not n and col[0] <= w[0] < col[1] and n[1] - 4 <= w[1] < hasta - 2]
            texto = [tipografia(texto_linea(f)) for _, f in lineas(celda)]
            enunciado, resto = [], []
            for t in texto:
                # el ejemplo empieza en «Por ejemplo», o —cuando no hay esa frase en la celda— en la primera línea en
                # inglés que sigue a un enunciado ya cerrado con punto
                ingles = bool(re.search(r"\b(I|I'm|I’m|you|is|are|the|my|your|What|Where|How|Hello|Hi|Name|This)\b", t)) \
                    and not re.search(r'\b(de|la|el|que|los|las|en|y|para|con)\b', t)
                if not resto and enunciado and enunciado[-1].rstrip().endswith('.') and ingles:
                    resto.append(t)
                    continue
                if resto or re.search(r'\bPor\b', t) and (re.search(r'Por ejemplo', t) or t.rstrip().endswith('Por')):
                    corte = t.find('Por')
                    if not resto and t[:corte].strip():
                        enunciado.append(t[:corte].strip())
                    resto.append(t if resto else t[corte:])
                else:
                    enunciado.append(t)
            enun, cs = unir_lineas(enunciado)
            if not re.search(r'[a-záéíóúñ]{3}', enun):
                continue   # casilla en blanco con renglones para que el docente escriba (no es un DBA oficial)
            cod = f'ING-DBA-{grado}-{int(n[4]):02d}'
            cortes += [{'codigo': cod, 'palabra': c} for c in cs]
            dbas.append({'codigo': cod, 'area': 'ingles', 'grado': grado, 'numero': int(n[4]), 'enunciado': enun,
                         'evidencias': [], 'ejemplo_texto_plano': unir_lineas(resto)[0] or None,
                         'fuente': os.path.basename(PDF), 'pagina_pdf': p})
    # Transición (grado 0) a 5.° vienen de otro PDF con otro formato: extraccion/ingles_primaria_dba.py
    import ingles_primaria_dba
    primaria, aplicadas = ingles_primaria_dba.main()
    dbas += primaria
    dbas.sort(key=lambda d: (d['grado'], d['numero']))
    os.makedirs('_soporte/datos/ingles', exist_ok=True)
    json.dump(aplicadas, open('_soporte/datos/ingles/correcciones_tipograficas.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(dbas, open('_soporte/datos/ingles/dba.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(cortes, open('_soporte/datos/ingles/dba_cortes_de_palabra.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(dbas), 'DBA;', len(cortes), 'cortes')


if __name__ == '__main__':
    main()
