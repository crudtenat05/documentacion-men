"""Convierte los DBA verificados de Matemáticas (6.° a 11.°) en la malla común que usan los sistemas.

El MEN no publicó un esquema por módulos para Matemáticas: la unidad de la malla es el DBA. Cada unidad lleva:
- el enunciado exacto del DBA (como meta) y sus evidencias de aprendizaje;
- el ejemplo del MEN;
- el pensamiento matemático y un título corto (solo etiquetas, criterio editorial);
- los estándares del mismo pensamiento y grupo de grados (Estándares Básicos de Competencias, 2006).

Entradas: _soporte/datos/matematicas/dba.json y estandares.json (extracción verificada).
Salidas:  _soporte/datos/matematicas/malla.json y estandares_malla.json (formato común con Inglés).

Uso: python3 _soporte/extraccion/matematicas_malla.py
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / '_soporte' / 'datos' / 'matematicas'

PENSAMIENTOS = {
    'PN': 'Pensamiento numérico',
    'PE': 'Pensamiento espacial',
    'PM': 'Pensamiento métrico',
    'PA': 'Pensamiento aleatorio',
    'PV': 'Pensamiento variacional',
}

# Código del DBA: (pensamiento, título corto). El título es una etiqueta para navegar; el enunciado no cambia.
UNIDADES = {
    'MAT-DBA-6-01': ('PN', 'Números enteros y racionales en contexto'),
    'MAT-DBA-6-02': ('PN', 'Propiedades de las operaciones con enteros y racionales'),
    'MAT-DBA-6-03': ('PN', 'Orden y equivalencia entre números'),
    'MAT-DBA-6-04': ('PE', 'Construcción de figuras planas y cuerpos'),
    'MAT-DBA-6-05': ('PM', 'Estimación y medición de ángulos, longitudes, áreas y volúmenes'),
    'MAT-DBA-6-06': ('PE', 'Formas bidimensionales y tridimensionales'),
    'MAT-DBA-6-07': ('PE', 'El plano cartesiano'),
    'MAT-DBA-6-08': ('PV', 'Variación directa e inversa'),
    'MAT-DBA-6-09': ('PV', 'Operaciones con números desconocidos'),
    'MAT-DBA-6-10': ('PA', 'Interpretación de información estadística'),
    'MAT-DBA-6-11': ('PA', 'Comparación de poblaciones y muestras'),
    'MAT-DBA-6-12': ('PA', 'Frecuencias en experimentos aleatorios'),
    'MAT-DBA-7-01': ('PN', 'Problemas con números racionales'),
    'MAT-DBA-7-02': ('PN', 'Algoritmos para operar con racionales'),
    'MAT-DBA-7-03': ('PN', 'Racionales y cantidades desconocidas'),
    'MAT-DBA-7-04': ('PM', 'Escalas en planos, mapas y maquetas'),
    'MAT-DBA-7-05': ('PE', 'Objetos tridimensionales y sus transformaciones'),
    'MAT-DBA-7-06': ('PV', 'Variación de áreas y perímetros en el plano cartesiano'),
    'MAT-DBA-7-07': ('PV', 'Ecuaciones y situaciones de variación'),
    'MAT-DBA-7-08': ('PA', 'Estudios estadísticos y gráficos'),
    'MAT-DBA-7-09': ('PA', 'Principio multiplicativo y probabilidad'),
    'MAT-DBA-8-01': ('PN', 'Números irracionales'),
    'MAT-DBA-8-02': ('PN', 'Propiedades de los racionales e irracionales'),
    'MAT-DBA-8-03': ('PV', 'El signo igual, equivalencias y sistemas de ecuaciones'),
    'MAT-DBA-8-04': ('PM', 'Atributos medibles de los sólidos'),
    'MAT-DBA-8-05': ('PM', 'Volumen de objetos regulares e irregulares'),
    'MAT-DBA-8-06': ('PE', 'Congruencia y semejanza'),
    'MAT-DBA-8-07': ('PE', 'Teoremas y propiedades de figuras geométricas'),
    'MAT-DBA-8-08': ('PV', 'Gráficas y expresiones algebraicas'),
    'MAT-DBA-8-09': ('PV', 'Conjeturas con lenguaje algebraico'),
    'MAT-DBA-8-10': ('PV', 'Modelos funcionales y covariación'),
    'MAT-DBA-8-11': ('PA', 'Datos agrupados y medidas de tendencia central'),
    'MAT-DBA-8-12': ('PA', 'Probabilidad de eventos compuestos'),
    'MAT-DBA-9-01': ('PN', 'Números reales y expresiones polinómicas'),
    'MAT-DBA-9-02': ('PV', 'Expresiones algebraicas, igualdad y orden'),
    'MAT-DBA-9-03': ('PN', 'Números reales y procesos infinitos'),
    'MAT-DBA-9-04': ('PM', 'Volumen y capacidad de cilindros, conos y esferas'),
    'MAT-DBA-9-05': ('PE', 'Teoremas de Thales y Pitágoras'),
    'MAT-DBA-9-06': ('PE', 'Semejanza y congruencia en dos y tres dimensiones'),
    'MAT-DBA-9-07': ('PE', 'Trayectorias y desplazamientos'),
    'MAT-DBA-9-08': ('PV', 'Modelos numéricos, algebraicos y gráficos para decidir'),
    'MAT-DBA-9-09': ('PV', 'Procesos inductivos y conjeturas'),
    'MAT-DBA-9-10': ('PA', 'Comparación de distribuciones de dos grupos'),
    'MAT-DBA-9-11': ('PA', 'Técnicas de conteo'),
    'MAT-DBA-10-01': ('PN', 'Propiedades de los números reales'),
    'MAT-DBA-10-02': ('PN', 'Orden en los reales e intervalos'),
    'MAT-DBA-10-03': ('PM', 'Velocidad media y aceleración media'),
    'MAT-DBA-10-04': ('PV', 'Funciones periódicas'),
    'MAT-DBA-10-05': ('PE', 'Lugares geométricos y transformaciones'),
    'MAT-DBA-10-06': ('PV', 'Razón de cambio'),
    'MAT-DBA-10-07': ('PV', 'Propiedades de las funciones'),
    'MAT-DBA-10-08': ('PA', 'Muestras aleatorias e inferencia'),
    'MAT-DBA-10-09': ('PA', 'Medidas de tendencia central y de dispersión'),
    'MAT-DBA-10-10': ('PA', 'Experimentos aleatorios y predicción'),
    'MAT-DBA-11-01': ('PN', 'Los sistemas numéricos'),
    'MAT-DBA-11-02': ('PN', 'Orden en los reales e inecuaciones'),
    'MAT-DBA-11-03': ('PM', 'Medición, estimación y razón de cambio'),
    'MAT-DBA-11-04': ('PM', 'Precisión en las mediciones'),
    'MAT-DBA-11-05': ('PV', 'La derivada como razón de cambio y pendiente'),
    'MAT-DBA-11-06': ('PE', 'Sistemas de coordenadas'),
    'MAT-DBA-11-07': ('PV', 'Modelos funcionales y variación'),
    'MAT-DBA-11-08': ('PV', 'Derivadas de funciones'),
    'MAT-DBA-11-09': ('PA', 'Asociación y correlación entre variables'),
    'MAT-DBA-11-10': ('PA', 'Eventos independientes y probabilidad condicional'),
}

GRUPOS = {6: (6, 7), 7: (6, 7), 8: (8, 9), 9: (8, 9), 10: (10, 11), 11: (10, 11)}


def main():
    dba = [d for d in json.loads((DATOS / 'dba.json').read_text(encoding='utf-8')) if d['grado'] >= 6]
    estandares = json.loads((DATOS / 'estandares.json').read_text(encoding='utf-8'))

    errores = [f'Falta título/pensamiento para {d["codigo"]}' for d in dba if d['codigo'] not in UNIDADES]
    errores += [f'{c} no existe en dba.json' for c in UNIDADES if c not in {d['codigo'] for d in dba}]
    if errores:
        sys.exit('\n'.join(errores))

    # Estándares en el formato común: código, «habilidad» (aquí el pensamiento) y texto.
    comunes = [{
        'codigo': e['codigo'], 'nivel': f"{e['grado_desde']}-{e['grado_hasta']}",
        'grados': f"{e['grado_desde']}.° a {e['grado_hasta']}.°", 'habilidad': PENSAMIENTOS[e['eje']],
        'numero': e['orden'], 'texto': e['texto'], 'pagina': e['pagina_pdf'], 'competencias': [],
    } for e in estandares]

    malla = []
    for d in sorted(dba, key=lambda x: (x['grado'], x['numero'])):
        pens, titulo = UNIDADES[d['codigo']]
        desde, hasta = GRUPOS[d['grado']]
        relacionados = [e['codigo'] for e in estandares
                        if e['eje'] == pens and e['grado_desde'] == desde and e['grado_hasta'] == hasta]
        if not relacionados:
            sys.exit(f'{d["codigo"]}: sin estándares de {pens} en {desde}-{hasta}')
        malla.append({
            'codigo': d['codigo'],
            'area': 'matematicas',
            'unidad': 'DBA',
            'grado': d['grado'],
            'modulo': d['numero'],
            'eje': PENSAMIENTOS[pens],
            'tema': titulo,
            'horas': None,
            'nivel_mcer': None,
            'meta': d['enunciado'],
            'meta_en': None,
            'ruta': (d.get('ejemplo_texto_plano') or '').strip(),
            'evidencias': [{'codigo': ev['codigo'], 'texto': ev['texto']} for ev in d['evidencias']],
            'estandares': relacionados,
            'fuente_pagina': d.get('pagina_pdf'),
        })

    (DATOS / 'malla.json').write_text(json.dumps(malla, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    (DATOS / 'estandares_malla.json').write_text(json.dumps(comunes, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{len(malla)} DBA de 6.° a 11.° en la malla común; {len(comunes)} estándares; '
          f'{sum(len(m["estandares"]) for m in malla)} relaciones DBA-estándar verificadas.')


if __name__ == '__main__':
    main()
