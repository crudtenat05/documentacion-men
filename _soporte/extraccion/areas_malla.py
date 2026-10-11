"""Convierte los DBA verificados de Lenguaje, Ciencias Naturales y Ciencias Sociales (6.° a 11.°) en la malla común
que usan los sistemas, igual que matematicas_malla.py.

Cada unidad de la malla es un DBA y lleva:
- el enunciado exacto del DBA (como meta), sus evidencias de aprendizaje y el ejemplo del MEN si lo hay;
- el eje y un título corto (solo etiquetas para navegar, criterio editorial; el enunciado no cambia);
- la página del documento del MEN de donde sale.

Los estándares no se relacionan todavía: en Lenguaje el cruce DBA-estándar no es uno a uno y en Ciencias los
estándares aún no están extraídos. La lista va vacía y se completa cuando se haga ese trabajo.

Entradas: _soporte/datos/{area}/dba.json (extracción verificada).
Salidas:  _soporte/datos/{area}/malla.json.

Uso: python3 _soporte/extraccion/areas_malla.py
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / '_soporte' / 'datos'

EJES = {
    'lenguaje': {
        'ME': 'Medios de comunicación', 'SS': 'Otros sistemas simbólicos', 'LI': 'Literatura',
        'OR': 'Oralidad', 'CO': 'Comprensión e interpretación textual', 'PT': 'Producción textual',
    },
    'ciencias_naturales': {
        'FI': 'Entorno físico', 'QU': 'Entorno químico', 'VI': 'Entorno vivo',
    },
    'ciencias_sociales': {
        'ES': 'Relaciones espaciales y ambientales', 'HI': 'Relaciones con la historia y la cultura',
        'EP': 'Relaciones ético-políticas',
    },
}

# Código del DBA: (eje, título corto).
UNIDADES = {
    'LEN-DBA-6-01': ('ME', 'Información de los medios de comunicación'),
    'LEN-DBA-6-02': ('SS', 'Organizadores gráficos'),
    'LEN-DBA-6-03': ('LI', 'La obra literaria y la imaginación'),
    'LEN-DBA-6-04': ('LI', 'Expresiones regionales en la literatura'),
    'LEN-DBA-6-05': ('LI', 'Obras de la tradición popular'),
    'LEN-DBA-6-06': ('CO', 'Comprensión de tipos de texto'),
    'LEN-DBA-6-07': ('OR', 'Discursos orales según el contexto'),
    'LEN-DBA-6-08': ('PT', 'Producción de textos según el destinatario'),
    'LEN-DBA-7-01': ('ME', 'Clasificación de la información de los medios'),
    'LEN-DBA-7-02': ('SS', 'Sistemas verbales y no verbales'),
    'LEN-DBA-7-03': ('LI', 'Literatura e historia'),
    'LEN-DBA-7-04': ('LI', 'Géneros literarios'),
    'LEN-DBA-7-05': ('OR', 'Comprensión de discursos orales'),
    'LEN-DBA-7-06': ('CO', 'Interpretación de tipologías textuales'),
    'LEN-DBA-7-07': ('OR', 'Narraciones orales'),
    'LEN-DBA-7-08': ('PT', 'Planificación textual'),
    'LEN-DBA-8-01': ('ME', 'Discursos en los medios de comunicación'),
    'LEN-DBA-8-02': ('SS', 'Manifestaciones artísticas y culturas'),
    'LEN-DBA-8-03': ('LI', 'Estructura de cuentos, relatos y novelas'),
    'LEN-DBA-8-04': ('LI', 'El género lírico'),
    'LEN-DBA-8-05': ('OR', 'Escucha atenta en el diálogo'),
    'LEN-DBA-8-06': ('CO', 'Sentidos de un texto'),
    'LEN-DBA-8-07': ('OR', 'El sentido de los textos en las intervenciones'),
    'LEN-DBA-8-08': ('PT', 'Textos para ámbitos públicos y privados'),
    'LEN-DBA-9-01': ('ME', 'Confrontación de los discursos de los medios'),
    'LEN-DBA-9-02': ('SS', 'Símbolos en los discursos'),
    'LEN-DBA-9-03': ('LI', 'El lenguaje literario'),
    'LEN-DBA-9-04': ('LI', 'Literatura y producciones audiovisuales'),
    'LEN-DBA-9-05': ('OR', 'Opiniones en debates de actualidad'),
    'LEN-DBA-9-06': ('CO', 'Estrategias de lectura'),
    'LEN-DBA-9-07': ('OR', 'Exposición oral de argumentos'),
    'LEN-DBA-9-08': ('PT', 'Planes textuales y corrección lingüística'),
    'LEN-DBA-10-01': ('ME', 'Lectura crítica de los medios masivos'),
    'LEN-DBA-10-02': ('SS', 'Producción de textos audiovisuales'),
    'LEN-DBA-10-03': ('LI', 'La literatura en su momento histórico'),
    'LEN-DBA-10-04': ('LI', 'Literatura y artes visuales'),
    'LEN-DBA-10-05': ('OR', 'Evaluación de discursos orales'),
    'LEN-DBA-10-06': ('CO', 'Lectura crítica y argumentada'),
    'LEN-DBA-10-07': ('OR', 'Ponencias, relatorías y entrevistas'),
    'LEN-DBA-10-08': ('PT', 'Estrategias de producción y corrección'),
    'LEN-DBA-11-01': ('ME', 'Posición crítica ante los medios'),
    'LEN-DBA-11-02': ('SS', 'Códigos verbales y no verbales en la cultura'),
    'LEN-DBA-11-03': ('LI', 'Elección y abordaje de lecturas'),
    'LEN-DBA-11-04': ('LI', 'Temas de la literatura clásica'),
    'LEN-DBA-11-05': ('OR', 'Comprensión de los argumentos del otro'),
    'LEN-DBA-11-06': ('CO', 'Comparación crítica de textos'),
    'LEN-DBA-11-07': ('OR', 'Dominio oral de un tema'),
    'LEN-DBA-11-08': ('PT', 'Textos académicos'),

    'CN-DBA-6-01': ('FI', 'Carga eléctrica, atracción y repulsión'),
    'CN-DBA-6-02': ('QU', 'Temperatura, presión y propiedades de las sustancias'),
    'CN-DBA-6-03': ('QU', 'Sustancias y mezclas'),
    'CN-DBA-6-04': ('VI', 'Funciones de la célula'),
    'CN-DBA-6-05': ('VI', 'Clasificación de los seres vivos'),
    'CN-DBA-7-01': ('FI', 'Energía en los sistemas mecánicos'),
    'CN-DBA-7-02': ('QU', 'Elementos, sustancias y tabla periódica'),
    'CN-DBA-7-03': ('VI', 'Cadenas y redes tróficas'),
    'CN-DBA-7-04': ('VI', 'Ciclos del carbono, el nitrógeno y el agua'),
    'CN-DBA-8-01': ('FI', 'Máquinas térmicas y termodinámica'),
    'CN-DBA-8-02': ('QU', 'Reacciones químicas y enlaces'),
    'CN-DBA-8-03': ('QU', 'Comportamiento de los gases'),
    'CN-DBA-8-04': ('VI', 'Sistemas de órganos y regulación'),
    'CN-DBA-8-05': ('VI', 'Reproducción de los seres vivos'),
    'CN-DBA-9-01': ('FI', 'Descripción del movimiento'),
    'CN-DBA-9-02': ('QU', 'Ácidos y bases'),
    'CN-DBA-9-03': ('QU', 'Soluciones'),
    'CN-DBA-9-04': ('VI', 'Genética mendeliana y herencia'),
    'CN-DBA-9-05': ('VI', 'Expresión de la información genética'),
    'CN-DBA-9-06': ('VI', 'Origen de las especies'),
    'CN-DBA-10-01': ('FI', 'Fuerzas y movimiento'),
    'CN-DBA-10-02': ('FI', 'Conservación de la energía mecánica'),
    'CN-DBA-10-03': ('QU', 'Reacciones de compuestos inorgánicos'),
    'CN-DBA-10-04': ('VI', 'Biotecnología'),
    'CN-DBA-11-01': ('FI', 'Ondas: el sonido y la luz'),
    'CN-DBA-11-02': ('FI', 'Fuerzas eléctricas y magnéticas'),
    'CN-DBA-11-03': ('FI', 'Circuitos eléctricos'),
    'CN-DBA-11-04': ('QU', 'Reacciones de compuestos orgánicos'),

    'CS-DBA-6-01': ('ES', 'Origen del universo'),
    'CS-DBA-6-02': ('ES', 'La Tierra en transformación'),
    'CS-DBA-6-03': ('HI', 'Hominización y prehistoria'),
    'CS-DBA-6-04': ('HI', 'Las primeras ciudades'),
    'CS-DBA-6-05': ('HI', 'Legados de las sociedades prehispánicas'),
    'CS-DBA-6-06': ('EP', 'Formas de gobierno en la antigüedad'),
    'CS-DBA-6-07': ('EP', 'Intereses en la democracia'),
    'CS-DBA-6-08': ('EP', 'Democracia y no discriminación'),
    'CS-DBA-7-01': ('ES', 'Representaciones del mundo'),
    'CS-DBA-7-02': ('ES', 'Población, ciudades y problemas sociales'),
    'CS-DBA-7-03': ('HI', 'El Imperio romano y su legado'),
    'CS-DBA-7-04': ('HI', 'La Edad Media'),
    'CS-DBA-7-05': ('HI', 'El Renacimiento'),
    'CS-DBA-7-06': ('HI', 'Conquista y colonización de América'),
    'CS-DBA-7-07': ('EP', 'Democracia y derechos fundamentales'),
    'CS-DBA-7-08': ('EP', 'Mediación de conflictos'),
    'CS-DBA-8-01': ('ES', 'Cooperación entre Estados'),
    'CS-DBA-8-02': ('ES', 'Migraciones en el mundo'),
    'CS-DBA-8-03': ('HI', 'El capitalismo'),
    'CS-DBA-8-04': ('HI', 'Imperialismo y expansión europea'),
    'CS-DBA-8-05': ('HI', 'Independencias americanas'),
    'CS-DBA-8-06': ('HI', 'Tecnología y desarrollo en la Colombia del siglo XIX'),
    'CS-DBA-8-07': ('EP', 'Dignidad humana y discriminación'),
    'CS-DBA-8-08': ('EP', 'Organizaciones y derechos colectivos'),
    'CS-DBA-9-01': ('ES', 'Geosistemas biodiversos de Colombia'),
    'CS-DBA-9-02': ('ES', 'Migraciones en Colombia'),
    'CS-DBA-9-03': ('HI', 'Crisis económicas en Colombia'),
    'CS-DBA-9-04': ('HI', 'Colombia en el siglo XX'),
    'CS-DBA-9-05': ('EP', 'Estado social de derecho'),
    'CS-DBA-9-06': ('EP', 'Las mujeres y la igualdad de derechos'),
    'CS-DBA-9-07': ('EP', 'Solución de conflictos mediante acuerdos'),
    'CS-DBA-9-08': ('ES', 'Desigualdad económica entre regiones'),
    'CS-DBA-10-01': ('ES', 'Conflictos territoriales en Colombia'),
    'CS-DBA-10-02': ('HI', 'La violencia en la Colombia del siglo XX'),
    'CS-DBA-10-03': ('EP', 'Diversidad cultural y exclusión'),
    'CS-DBA-10-04': ('EP', 'Organismos internacionales'),
    'CS-DBA-10-05': ('HI', 'Conflictos bélicos contemporáneos'),
    'CS-DBA-11-01': ('ES', 'Ambiente y supervivencia de la humanidad'),
    'CS-DBA-11-02': ('EP', 'Solución negociada de los conflictos armados'),
    'CS-DBA-11-03': ('HI', 'Conflictos geopolíticos recientes'),
    'CS-DBA-11-04': ('HI', 'La Guerra Fría'),
    'CS-DBA-11-05': ('ES', 'Globalización'),
}


def main():
    total = 0
    for area, ejes in EJES.items():
        dba = [d for d in json.loads((DATOS / area / 'dba.json').read_text(encoding='utf-8')) if d['grado'] >= 6]
        propios = {c: v for c, v in UNIDADES.items() if c.split('-')[0] == dba[0]['codigo'].split('-')[0]}

        errores = [f'Falta título/eje para {d["codigo"]}' for d in dba if d['codigo'] not in propios]
        errores += [f'{c} no existe en dba.json de {area}' for c in propios if c not in {d['codigo'] for d in dba}]
        errores += [f'{c}: eje {e} desconocido' for c, (e, _) in propios.items() if e not in ejes]
        if errores:
            sys.exit('\n'.join(errores))

        malla = []
        for d in sorted(dba, key=lambda x: (x['grado'], x['numero'])):
            eje, titulo = propios[d['codigo']]
            malla.append({
                'codigo': d['codigo'],
                'area': area,
                'unidad': 'DBA',
                'grado': d['grado'],
                'modulo': d['numero'],
                'eje': ejes[eje],
                'tema': titulo,
                'horas': None,
                'nivel_mcer': None,
                'meta': d['enunciado'],
                'meta_en': None,
                'ruta': (d.get('ejemplo_texto_plano') or '').strip(),
                'evidencias': [{'codigo': ev['codigo'], 'texto': ev['texto']} for ev in d['evidencias']],
                'estandares': [],
                'fuente': d.get('fuente'),
                'fuente_pagina': d.get('pagina_pdf'),
            })

        (DATOS / area / 'malla.json').write_text(json.dumps(malla, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        evidencias = sum(len(m['evidencias']) for m in malla)
        print(f'{area}: {len(malla)} DBA de 6.° a 11.° en la malla común, con {evidencias} evidencias.')
        total += len(malla)
    print(f'Total: {total} DBA.')


if __name__ == '__main__':
    main()
