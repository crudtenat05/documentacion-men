"""Extrae los Derechos Básicos de Aprendizaje de Ciencias Naturales V.1 (MEN, 2016) desde el PDF oficial.

    python3 extraccion/naturales_dba.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from dba_men import extraer, guardar

# Defectos de la lectura del PDF, confirmados contra la página. Se registran en datos/…/correcciones_tipograficas.json.
CORRECCIONES = {
    # el subíndice de H₂O es un carácter pequeño en otra línea: la extracción lo dejó al final de la frase
    'CN-DBA-6-03-E2': [('(NaCl, H O, Cu). 2', '(NaCl, H2O, Cu).')],
    # «arena-gravilla» cae partido al final de línea; el guion es parte del término, no un corte de palabra
    'CN-DBA-4-05-E3': [('arenagravilla', 'arena-gravilla')],
    # espacio intruso dentro de la palabra (el PDF separa las letras al justificar la línea)
    'CN-DBA-1-01-E4': [('obser vaciones', 'observaciones')],
}


def corregir(datos, correcciones):
    aplicadas = []
    for d in datos:
        for item, campo in [(d, 'enunciado')] + [(e, 'texto') for e in d['evidencias']]:
            for antes, despues in correcciones.get(item['codigo'], []):
                if antes not in item[campo]:
                    raise SystemExit(f"Corrección sin efecto en {item['codigo']}: «{antes}»")
                item[campo] = item[campo].replace(antes, despues)
                aplicadas.append({'codigo': item['codigo'], 'antes': antes, 'despues': despues})
    return aplicadas


if __name__ == '__main__':
    # las evidencias usan la viñeta «q»; el grado se sigue por la numeración (el encabezado no está en todas las páginas)
    datos, cortes = extraer('fuentes/men/dba-naturales.pdf', 8, 38, 'CN', 'ciencias_naturales', VINETA='q', por_reinicio=True)
    aplicadas = corregir(datos, CORRECCIONES)
    guardar('ciencias_naturales', datos, cortes)
    with open('_soporte/datos/ciencias_naturales/correcciones_tipograficas.json', 'w', encoding='utf-8') as f:
        json.dump(aplicadas, f, ensure_ascii=False, indent=1)
    print(len(aplicadas), 'correcciones tipográficas')
