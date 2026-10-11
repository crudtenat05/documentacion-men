"""Publica la transcripción legible en las carpetas DBA/ y ESTANDARES/ (un archivo por asignatura).

    python3 extraccion/publicar.py

Lee los datos verificados de datos/<area>/ y escribe:
  DBA/<Asignatura>.md         los Derechos Básicos de Aprendizaje por grado, con sus evidencias
  ESTANDARES/<Asignatura>.md  los Estándares Básicos de Competencias por grupo de grados
"""
import json
import os

AREAS = [('matematicas', 'Matematicas', 'Matemáticas'), ('lenguaje', 'Lenguaje', 'Lenguaje'),
         ('ciencias_naturales', 'Ciencias_Naturales', 'Ciencias Naturales'),
         ('ciencias_sociales', 'Ciencias_Sociales', 'Ciencias Sociales')]
# Inglés no se publica desde aquí: DBA/Ingles.md es la transcripción curada (enunciado exacto, habilidades y ejemplo explicado)


def grado(g):
    return 'Transición' if g == 0 else f'Grado {g}.°'


def dba(area, archivo, nombre):
    datos = json.load(open(f'_soporte/datos/{area}/dba.json', encoding='utf-8'))
    fuentes = ', '.join(dict.fromkeys(d['fuente'] for d in datos))
    L = [f'# Derechos Básicos de Aprendizaje · {nombre}', '',
         f'Fuente: MEN ({fuentes}). {len(datos)} DBA. Entre paréntesis, la página del PDF.', '']
    actual = None
    for d in datos:
        if d['grado'] != actual:
            actual = d['grado']
            L += [f'## {grado(actual)}', '']
        L += [f"**DBA {d['numero']}.** {d['enunciado']} *(pág. {d['pagina_pdf']} · {d['codigo']})*", '']
        if d['evidencias']:
            L += ['Evidencias de aprendizaje:', '']
            L += [f"{e['numero']}. {e['texto']}" for e in d['evidencias']]
            L += ['']
    open(f'DBA/{archivo}.md', 'w', encoding='utf-8').write('\n'.join(L))
    return len(datos)


def estandares(area, archivo, nombre):
    ruta = f'_soporte/datos/{area}/estandares.json'
    if not os.path.exists(ruta):
        return 0
    datos = json.load(open(ruta, encoding='utf-8'))
    if 'tipo' in datos[0]:
        return estandares_ciencias(datos, archivo, nombre)
    L = [f'# Estándares Básicos de Competencias · {nombre}', '',
         f"Fuente: MEN, Estándares Básicos de Competencias (2006) ({datos[0]['fuente']}). {len(datos)} estándares, "
         'organizados como en el documento: por grupo de grados y por eje. Entre paréntesis, la página del PDF.', '']
    grupo = eje = None
    for e in datos:
        g = (e['grado_desde'], e['grado_hasta'])
        if g != grupo:
            grupo, eje = g, None
            L += [f'## Grados {g[0]}.° a {g[1]}.°', '']
        if e['eje_nombre'] != eje:
            eje = e['eje_nombre']
            L += [f'### {eje[:1].upper() + eje[1:].lower()}', '']
        L += [f"{e['orden']}. {e['texto']} *(pág. {e['pagina_pdf']} · {e['codigo']})*"]
        for s in e.get('subprocesos', []):
            L += [f"   - {s['texto']}"]
    L += ['']
    open(f'ESTANDARES/{archivo}.md', 'w', encoding='utf-8').write('\n'.join(L))
    return len(datos)


def estandares_ciencias(datos, archivo, nombre):
    """Ciencias Sociales y Ciencias Naturales: por grupo de grados, los estándares y, debajo, las acciones
    concretas de pensamiento y de producción de cada columna. El documento no numera las acciones ni las
    asigna a un estándar; aquí van con viñeta y con su código para poder citarlas."""
    est = [d for d in datos if d['tipo'] == 'estandar']
    paginas = sorted({d['pagina_pdf'] for d in datos} | {d['continua_en_pagina_pdf'] for d in datos if d.get('continua_en_pagina_pdf')})
    salto = datos[0]['pagina_libro'] - datos[0]['pagina_pdf']
    L = [f'# Estándares Básicos de Competencias · {nombre}', '',
         f"Fuente: MEN, Estándares Básicos de Competencias (2006) ({datos[0]['fuente']}, páginas {paginas[0]} a "
         f'{paginas[-1]} del PDF; {paginas[0] + salto} a {paginas[-1] + salto} del libro). {len(est)} estándares y '
         f'{len(datos) - len(est)} acciones concretas de pensamiento y de producción, organizados como en el '
         'documento: por grupo de grados y por columna. Entre paréntesis, la página del PDF.', '',
         'Cada grupo de grados trae sus estándares y, debajo, las acciones con las que se alcanzan («Para '
         'lograrlo…»). El documento no asigna cada acción a un estándar ni las numera: las agrupa por columna.', '']
    grupo = eje = subtitulo = None
    for d in datos:
        g = (d['grado_desde'], d['grado_hasta'])
        if g != grupo:
            grupo, eje = g, None
            L += [f'## Grados {g[0]}.° a {g[1]}.°', '']
        if d['eje'] != eje:
            eje, subtitulo = d['eje'], None
            if L[-1] != '':
                L += ['']
            if d['tipo'] == 'estandar':
                L += [f"### Estándares · {d['columna']}", '']
            elif d['columna'].startswith('…manejo'):
                L += [f"### {d['columna']} · {d['eje_nombre']}", '']
            else:
                L += [f"### {d['columna']}", '']
        if d.get('subtitulo') != subtitulo:
            subtitulo = d.get('subtitulo')
            L += ['', f'**{subtitulo}**', '']
        cita = f"pág. {d['pagina_pdf']}" + (f" y {d['continua_en_pagina_pdf']}" if d.get('continua_en_pagina_pdf') else '')
        marca = f"{d['orden']}." if d['tipo'] == 'estandar' else '-'
        L += [f"{marca} {d['texto']} *({cita} · {d['codigo']})*"]
    L += ['']
    open(f'ESTANDARES/{archivo}.md', 'w', encoding='utf-8').write('\n'.join(L))
    return len(est)


if __name__ == '__main__':
    os.makedirs('DBA', exist_ok=True)  # se ejecuta desde la raíz del repositorio
    os.makedirs('ESTANDARES', exist_ok=True)
    for area, archivo, nombre in AREAS:
        print(f'{nombre}: {dba(area, archivo, nombre)} DBA, {estandares(area, archivo, nombre)} estándares')
