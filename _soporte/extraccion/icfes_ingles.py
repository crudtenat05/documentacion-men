"""Estructura de la prueba Inglés (Saber 11°): Guía de orientación 2026-2 del ICFES, páginas 63 a 65.

Uso (desde la raíz del repositorio):  python _soporte/extraccion/icfes_ingles.py

Esta prueba no trae competencias, afirmaciones ni evidencias en la guía: se describe por sus siete partes, cada una
con la habilidad que evalúa, y por cuatro niveles de desempeño. Por eso no usa `publicar()` y arma sus propias salidas,
con la misma regla: no se escribe nada si un texto no aparece literal en su página.
"""
import csv
import hashlib
import json
import sys
from datetime import date

from icfes_transcrito import DOCUMENTO, PDF, RAIZ, _plano, pagina

DESCRIPCION = ('De acuerdo con el Marco de referencia, esta prueba evalúa la competencia para comunicarse efectivamente en inglés. '
               'La evaluación realizada a través de la prueba Inglés se alinea con los Estándares Básicos de Competencias en Lenguas '
               'Extranjeras: Inglés del MEN. A su vez, en relación con el Marco Común Europeo de Referencia para las lenguas (MCER), '
               'los evaluados se clasifican en cuatro niveles de desempeño.')
PRE_A1 = ('Teniendo en cuenta que, en Colombia, existe población que está por debajo del nivel del MCER (A1), en esta prueba se incluyó '
          'el nivel Pre A1, que representa un paso a medio camino del Nivel A1, donde los estudiantes aún no pueden producir discurso, '
          'pero son capaces de comprender algunas palabras y expresiones fijas.')
PROPOSITO = ('La prueba busca que los evaluados demuestren sus habilidades comunicativas en lectura y uso de la lengua inglesa. Para '
             'ello, cada una de las siete partes que componen la prueba Inglés evalúa una habilidad específica relacionada:')

# El número de cada parte está dibujado en la página (no es texto del PDF): se leyó de la imagen de las págs. 64 y 65.
PARTES = [
    (1, 11, 64, 3, 'Evalúa el conocimiento lexical', 'En esta parte, los evaluados deben comprender una serie de descripciones con el fin de relacionarlas con una lista de palabras. Dicha lista consta de siete palabras disponibles, clasificadas de la letra A a la letra G, y las cinco descripciones con las que deben relacionarlas. Cabe indicar que al haber cinco enunciados y siete opciones de respuesta, sobran dos opciones al final.'),
    (2, 11, 64, 3, 'Indaga por el conocimiento pragmático', 'Los evaluados deben reconocer el propósito comunicativo de un aviso y el lugar donde este puede aparecer. Para ello, los evaluados deben leer el aviso y escoger entre las tres opciones de respuesta disponibles (A, B o C) el lugar más apropiado y marcarlo en la hoja de respuestas.'),
    (3, 11, 64, 3, 'Evalúa el conocimiento comunicativo', 'Los evaluados deben elegir la intervención más adecuada que un interlocutor 2 haría frente a lo dicho por un interlocutor 1. Lo anterior se relaciona con la pertinencia del lenguaje usado en situaciones particulares, recreadas en pequeñas conversaciones. En consecuencia, en esta parte, el evaluado debe completar conversaciones cortas, seleccionando la respuesta correcta entre las tres opciones de la hoja de respuestas.'),
    (4, 18, 64, 3, 'Con base en un texto, evalúa el conocimiento gramatical', 'Los evaluados deben elegir las palabras más adecuadas para completar un texto. Para ello, los evaluados deben leer y prestar atención a una serie de espacios, puesto que, para cada uno de estos, se debe seleccionar la palabra gramaticalmente correcta entre las tres opciones presentadas (A, B o C) y marcarla en la hoja de respuestas.'),
    (5, 16, 65, 3, 'Evalúa la comprensión de lectura literal de un texto', 'Este ejercicio consiste en que los evaluados seleccionen la paráfrasis que permite responder correctamente a cada pregunta planteada en un texto. Los evaluados deben seleccionar la respuesta correcta, para cada pregunta, entre tres opciones (A, B o C) y señalarla en la hoja de respuestas.'),
    (6, 11, 65, 4, 'Evalúa el proceso de lectura inferencial', 'En esta parte se plantean distintas preguntas sobre la intención del autor y los aspectos generales y particulares destacables del texto. El evaluado debe seleccionar la respuesta correcta, para cada pregunta, entre cuatro opciones (A, B, C o D) y marcarla en su hoja de respuestas.'),
    (7, 22, 65, 4, 'Con base en un texto, evalúa el conocimiento gramatical y lexical', 'El ejercicio consiste en elegir las palabras más adecuadas para completar el texto. Para ello, se debe seleccionar la palabra correcta, es decir, aquella que completa cada uno de los espacios en el texto presentado, entre cuatro opciones dadas (A, B, C o D) y marcarla en la hoja de respuestas.'),
]
# Figura 5 (pág. 63), de menor a mayor. Es un dibujo: los rótulos se leyeron de la imagen de la página.
NIVELES = ['Pre A1', 'A1', 'A2', 'B1']

fallos, n = [], 0


def revisar(texto, pag):
    global n
    n += 1
    if _plano(texto) not in pagina(pag):
        fallos.append(f'[pág. {pag}] {texto[:100]}')


for t in (DESCRIPCION, PRE_A1, PROPOSITO):
    revisar(t, 63)
for num, pct, pag, _, habilidad, descripcion in PARTES:
    revisar(f'{habilidad} {descripcion}', pag)
    revisar(f'{num} {pct} %', 63)
if sum(p[1] for p in PARTES) != 100:
    fallos.append('Los porcentajes de las partes no suman 100.')
if fallos:
    sys.exit('NO se escribió nada. Textos que no aparecen literales en el PDF:\n- ' + '\n- '.join(fallos))

salida = RAIZ / '_soporte/datos/icfes/ingles'
salida.mkdir(parents=True, exist_ok=True)
partes = [{'codigo': f'ING-P{num}', 'numero': num, 'habilidad': hab, 'descripcion': des, 'porcentaje_preguntas': pct,
           'opciones_de_respuesta': 'Siete palabras (A a G) para cinco descripciones' if num == 1 else f'{op} opciones',
           'pagina': pag} for num, pct, pag, op, hab, des in PARTES]
datos = {'documento': DOCUMENTO, 'prueba': 'ingles', 'descripcion': DESCRIPCION, 'pagina': 63, 'proposito': PROPOSITO,
         'niveles_de_desempeno': [{'codigo': 'ING-N' + nv.replace(' ', ''), 'nivel': nv, 'orden': i, 'pagina': 63} for i, nv in enumerate(NIVELES, 1)],
         'nota_pre_a1': PRE_A1, 'partes': partes}
(salida / 'taxonomia.json').write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
with open(salida / 'partes.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['parte', 'numero', 'habilidad', 'porcentaje_preguntas', 'opciones_de_respuesta', 'descripcion', 'pagina_pdf'])
    w.writerows([[p['codigo'], p['numero'], p['habilidad'], p['porcentaje_preguntas'], p['opciones_de_respuesta'], p['descripcion'], p['pagina']] for p in partes])

md = ['# Inglés · Saber 11° · estructura de la prueba según el ICFES', '',
      f"Fuente: {DOCUMENTO['titulo']} (`{PDF}`). Textos literales del PDF, con su página.", '', f'{DESCRIPCION} (pág. 63)', '',
      '## Niveles de desempeño (figura 5, pág. 63)', '', ' → '.join(NIVELES), '', PRE_A1, '',
      '## Las siete partes de la prueba', '', PROPOSITO, '']
for p in partes:
    md += [f"### `{p['codigo']}` Parte {p['numero']} · {p['habilidad']} · {p['porcentaje_preguntas']} % de las preguntas (pág. {p['pagina']})", '',
           p['descripcion'], '', f"Respuesta: {p['opciones_de_respuesta']}.", '']
(salida / 'ingles.md').write_text('\n'.join(md), encoding='utf-8')

sha = hashlib.sha256((RAIZ / PDF).read_bytes()).hexdigest()
ver = ['# Verificación ICFES · Inglés', '', f'Fecha: {date.today().isoformat()}', '', '## Fuente', '', '| Archivo | SHA-256 |', '|---|---|',
       f'| `{PDF}` | `{sha}` |', '', '## Resultado', '', '| Tipo | Elementos |', '|---|---|', '| Parte de la prueba, con su habilidad y descripción | 7 |',
       '| Nivel de desempeño | 4 |', '',
       f'- Comprobaciones literales contra el PDF: **{n} de {n}** (los tres párrafos de presentación, la habilidad y descripción de cada parte, y la fila de cada parte en la tabla 32).',
       '- Los porcentajes de las siete partes (11, 11, 11, 18, 16, 11 y 22) suman 100.',
       '- **Leído de la imagen, no del texto:** el número de cada parte (págs. 64 y 65) y los rótulos de los niveles (figura 5) están dibujados; se tomaron de la página convertida en imagen con `pdftoppm`. La correspondencia entre número y habilidad coincide con el orden en que el texto las presenta.',
       '- El número de opciones de respuesta de cada parte se tomó de su propia descripción.', '',
       '## Diferencias con las otras pruebas', '',
       '- La guía no da competencias, afirmaciones ni evidencias para Inglés: la describe por partes y por niveles.',
       '- La guía nombra los cuatro niveles pero no los describe: remite a un «Documento de consulta».', '',
       '## Pendiente', '',
       '- **Marco de referencia de la prueba Inglés** y el **«Documento de consulta» de los niveles** (descriptores de Pre A1, A1, A2 y B1): no están en `fuentes/icfes/`.',
       '- La guía dice que la prueba se alinea con los Estándares Básicos de Competencias en Lenguas Extranjeras: Inglés (ya procesados en `datos/ingles/estandares.json`). El cruce entre partes de la prueba y estándares no está hecho.', '']
(RAIZ / '_soporte/verificacion/icfes_ingles.md').write_text('\n'.join(ver), encoding='utf-8')
print(f'Inglés: {n} de {n} comprobaciones literales. 7 partes y 4 niveles.')
