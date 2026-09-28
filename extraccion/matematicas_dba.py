"""Extrae los Derechos Básicos de Aprendizaje de Matemáticas V.2 (MEN, 2016) desde el PDF oficial.

    python3 extraccion/matematicas_dba.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from dba_men import extraer, guardar

if __name__ == '__main__':
    # páginas 7 a 88: las demás son presentación y contraportada
    guardar('matematicas', *extraer('fuentes/men/dba-matematicas.pdf', 7, 88, 'MAT', 'matematicas'))
