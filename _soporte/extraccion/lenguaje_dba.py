"""Extrae los Derechos Básicos de Aprendizaje de Lenguaje (MEN, 2016) desde el PDF oficial.

    python3 extraccion/lenguaje_dba.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from dba_men import extraer, guardar

if __name__ == '__main__':
    # páginas 8 a 52: las demás son presentación y contraportada
    guardar('lenguaje', *extraer('fuentes/men/dba-lenguaje.pdf', 8, 52, 'LEN', 'lenguaje'))
