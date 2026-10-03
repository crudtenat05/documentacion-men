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


if __name__ == '__main__':
    os.makedirs('DBA', exist_ok=True)  # se ejecuta desde la raíz del repositorio
    os.makedirs('ESTANDARES', exist_ok=True)
    for area, archivo, nombre in AREAS:
        print(f'{nombre}: {dba(area, archivo, nombre)} DBA, {estandares(area, archivo, nombre)} estándares')
