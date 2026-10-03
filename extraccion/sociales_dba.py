"""Extrae los Derechos Básicos de Aprendizaje de Ciencias Sociales V.1 (MEN, 2016) desde el PDF oficial.

    python3 extraccion/sociales_dba.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from dba_men import extraer, guardar

# Defectos tipográficos del PDF: solo espacios mal puestos, nunca palabras distintas. El verificador compara sin
# espacios, así que el texto corregido sigue coincidiendo con el PDF. Se registran en datos/…/correcciones_tipograficas.json.
CORRECCIONES = {
    'CS-DBA-8-08': [('Comprendelaimportanciadelasasociaciones,', 'Comprende la importancia de las asociaciones,')],
    # espacios intrusos dentro de palabras (letras separadas al justificar, o la página 31 impresa en diagonal)
    'CS-DBA-6-05-E3': [('l a est r uct ur a soci al, pol í t i ca', 'la estructura social, política')],
    'CS-DBA-6-06-E4': [('obser van', 'observan')],
    'CS-DBA-7-07': [('Co mprende', 'Comprende')],
    # la ligadura «fi» no está en el texto del PDF; en la página se lee «geográficos»
    'CS-DBA-6-05-E1': [('geográ cos', 'geográficos')],
}

if __name__ == '__main__':
    # las evidencias usan la viñeta «l»; la columna derecha cambia de posición según la página
    datos, cortes = extraer('fuentes/men/dba-sociales.pdf', 8, 51, 'CS', 'ciencias_sociales', VINETA='l',
                            por_reinicio=True, corte='auto')
    aplicadas = []
    for d in datos:
        for item, campo in [(d, 'enunciado')] + [(e, 'texto') for e in d['evidencias']]:
            for antes, despues in CORRECCIONES.get(item['codigo'], []):
                if antes not in item[campo]:
                    raise SystemExit(f"Corrección sin efecto en {item['codigo']}: «{antes}»")
                item[campo] = item[campo].replace(antes, despues)
                aplicadas.append({'codigo': item['codigo'], 'antes': antes, 'despues': despues})
    guardar('ciencias_sociales', datos, cortes)
    with open('datos/ciencias_sociales/correcciones_tipograficas.json', 'w', encoding='utf-8') as f:
        json.dump(aplicadas, f, ensure_ascii=False, indent=1)
    print(len(aplicadas), 'correcciones tipográficas')
