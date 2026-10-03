"""Convierte la malla y los estándares de inglés (Markdown curado) en datos JSON.

Fuentes: MALLAS/Ingles.md y ESTANDARES/Ingles.md (transcripción revisada por Julio).
Salidas: _soporte/datos/ingles/estandares.json y _soporte/datos/ingles/malla.json.

Uso: python3 _soporte/extraccion/ingles_malla.py
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / '_soporte' / 'datos' / 'ingles'

HABILIDADES = {
    'Escucha': 'ES', 'Lectura': 'LE', 'Escritura': 'ESC', 'Monólogo': 'MO', 'Conversación': 'CO',
}

# Etiqueta del Markdown → campo del JSON. El orden importa: «Saber hacer» antes que «Saber».
CAMPOS = [
    ('Funciones de lengua', 'funciones'),
    ('Objetivos', 'objetivos'),
    ('Saber hacer', 'saber_hacer'),
    ('Saber ser', 'saber_ser'),
    ('Saber', 'saber'),
    ('Léxico', 'lexico'),
    ('Expresiones', 'expresiones'),
    ('Gramática', 'gramatica'),
    ('Pronunciación', 'pronunciacion'),
    ('Discursivo', 'discursivo'),
    ('Sociolingüístico', 'sociolinguistico'),
    ('Evaluación para el aprendizaje', 'evaluacion_para'),
    ('Evaluación del aprendizaje', 'evaluacion_del'),
]


def limpiar(texto):
    """Quita el marcado de Markdown (negrita, cursiva) y espacios sobrantes."""
    texto = re.sub(r'\*\*(.+?)\*\*', r'\1', texto)
    texto = re.sub(r'\*(.+?)\*', r'\1', texto)
    return re.sub(r'\s+', ' ', texto).strip()


def leer_estandares():
    estandares = []
    nivel = grados = None
    habilidad = None
    for linea in (RAIZ / 'ESTANDARES' / 'Ingles.md').read_text(encoding='utf-8').splitlines():
        m = re.match(r'## Grados (.+?) · .*\((A1|A2\.1|A2\.2|B1\.1|B1\.2)\)', linea)
        if m:
            grados, nivel = m.group(1), m.group(2)
            continue
        m = re.match(r'### (\S+)', linea)
        if m and m.group(1) in HABILIDADES:
            habilidad = m.group(1)
            continue
        m = re.match(r'(\d+)\. (.+) \*\(pág\. (\d+) · (ING-EBC-[^ ]+?)(?: · ([\d, ]+))?\)\*$', linea)
        if m:
            estandares.append({
                'codigo': m.group(4),
                'nivel': nivel,
                'grados': grados,
                'habilidad': habilidad,
                'numero': int(m.group(1)),
                'texto': limpiar(m.group(2)),
                'pagina': int(m.group(3)),
                'competencias': [int(c) for c in re.findall(r'\d', m.group(5) or '')],
            })
    return estandares


def nuevo_modulo(grado, numero):
    modulo = {
        'codigo': f'ING-MALLA-{grado}-M{numero}',
        'area': 'ingles',
        'grado': grado,
        'modulo': numero,
        'eje': None, 'tema': None, 'horas': None, 'nivel_mcer': None,
        'meta': None, 'meta_en': None,
        'ruta': '',
        'estandares': [],
    }
    for _, campo in CAMPOS:
        modulo[campo] = []
    return modulo


def leer_malla(por_codigo):
    modulos = []
    grado = modulo = None
    seccion = None      # 'contexto' | 'nucleo'
    campo = None
    niveles = []
    ruta = []

    def cerrar():
        if modulo is not None:
            modulo['ruta'] = '\n'.join(ruta).strip()
            modulos.append(modulo)

    for linea in (RAIZ / 'MALLAS' / 'Ingles.md').read_text(encoding='utf-8').splitlines():
        if linea.startswith('---'):
            campo = None
            continue
        m = re.match(r'## Grado (\d+)', linea)
        if m:
            cerrar()
            grado, modulo, ruta = int(m.group(1)), None, []
            continue
        m = re.match(r'### Módulo (\d+)', linea)
        if m:
            cerrar()
            modulo, ruta, seccion, campo = nuevo_modulo(grado, int(m.group(1))), [], None, None
            continue
        if modulo is None:
            continue
        if linea.startswith('#### Contexto'):
            seccion, campo = 'contexto', None
            continue
        if linea.startswith('#### Núcleo'):
            seccion, campo = 'nucleo', None
            continue

        if seccion is None:
            for etiqueta, clave in (('Eje', 'eje'), ('Tema', 'tema'), ('Tiempo', 'horas'), ('Nivel MCER', 'nivel_mcer')):
                if linea.startswith(etiqueta + ': '):
                    modulo[clave] = limpiar(linea[len(etiqueta) + 2:]).replace(' horas', '')
            continue

        if seccion == 'contexto':
            if linea.startswith('Meta (inglés): '):
                modulo['meta_en'] = limpiar(linea[15:])
            elif linea.startswith('Meta: '):
                modulo['meta'] = limpiar(linea[6:])
            elif linea.startswith('Saber ser:'):
                campo = 'saber_ser'
            elif campo == 'saber_ser' and linea.startswith('- '):
                modulo['saber_ser'].append(limpiar(linea[2:]))
            elif linea.strip():
                campo = None
                ruta.append(limpiar(linea) if not linea.startswith((' ', '-')) else linea.rstrip())
            continue

        # Núcleo de lengua
        m = re.match(r'Estándares \(Guía 22, nivel ([A-Z0-9.]+)', linea)
        if m:
            niveles, campo = [m.group(1)], 'estandares'
            continue
        if linea.startswith('Estándares (Guía 22)'):
            niveles, campo = [], 'estandares'
            continue
        if campo == 'estandares':
            m = re.match(r'\| Habilidad \| (.+) \|$', linea)
            if m and 'Estándares' not in m.group(1):
                niveles = [re.match(r'([A-Z0-9.]+)', c.strip()).group(1) for c in m.group(1).split('|')]
                continue
            m = re.match(r'\| (\S+) \| (.+) \|$', linea)
            if m and m.group(1) in HABILIDADES:
                for nivel, celda in zip(niveles, m.group(2).split('|')):
                    for numero in re.findall(r'\d+', celda):
                        codigo = f'ING-EBC-{nivel}-{HABILIDADES[m.group(1)]}-{int(numero):02d}'
                        if codigo not in por_codigo:
                            sys.exit(f'Estándar citado que no existe: {codigo} en {modulo["codigo"]}')
                        modulo['estandares'].append(codigo)
                continue
            if linea.startswith('|') or not linea.strip():
                continue

        encontrado = False
        for etiqueta, clave in CAMPOS:
            if linea.startswith(etiqueta) and linea.rstrip().endswith(':'):
                campo, encontrado = clave, True
                # «Evaluación para el aprendizaje (ruta 2):» conserva la ruta en cada ítem.
                m = re.search(r'\((ruta \d)\)', linea)
                modulo.setdefault('_prefijo', {})[clave] = f'{m.group(1).capitalize()}: ' if m else ''
                break
        if encontrado:
            continue
        m = re.match(r'\s*(?:-|\d+\.) (.+)', linea)
        if m and campo and campo != 'estandares':
            prefijo = modulo.get('_prefijo', {}).get(campo, '')
            modulo[campo].append(prefijo + limpiar(m.group(1)))

    cerrar()
    for modulo in modulos:
        modulo.pop('_prefijo', None)
    return modulos


def main():
    estandares = leer_estandares()
    por_codigo = {e['codigo']: e for e in estandares}
    modulos = leer_malla(por_codigo)

    errores = []
    if len(estandares) != 218:
        errores.append(f'Se esperaban 218 estándares y hay {len(estandares)}')
    if len(modulos) != 24:
        errores.append(f'Se esperaban 24 módulos y hay {len(modulos)}')
    for m in modulos:
        for clave in ('eje', 'tema', 'meta', 'meta_en', 'nivel_mcer', 'horas'):
            if not m[clave]:
                errores.append(f'{m["codigo"]}: falta {clave}')
        for clave in ('funciones', 'objetivos', 'saber', 'saber_hacer', 'saber_ser', 'gramatica', 'estandares', 'evaluacion_del'):
            if not m[clave]:
                errores.append(f'{m["codigo"]}: {clave} vacío')
        if not m['ruta']:
            errores.append(f'{m["codigo"]}: sin ruta (tareas, proyecto o problema)')
    if errores:
        sys.exit('\n'.join(errores))

    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / 'estandares.json').write_text(json.dumps(estandares, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    (SALIDA / 'malla.json').write_text(json.dumps(modulos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    citas = sum(len(m['estandares']) for m in modulos)
    print(f'{len(estandares)} estándares, {len(modulos)} módulos, {citas} citas de estándares verificadas.')


if __name__ == '__main__':
    main()
