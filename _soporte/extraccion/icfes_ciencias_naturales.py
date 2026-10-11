"""Taxonomía de la prueba Ciencias Naturales (Saber 11°): Guía de orientación 2026-2 del ICFES, páginas 54 a 62.

Uso (desde la raíz del repositorio):  python _soporte/extraccion/icfes_ciencias_naturales.py
"""
from icfes_transcrito import publicar

DESCRIPCION = ('De acuerdo con el Marco de referencia, esta prueba evalúa la capacidad que tienen los evaluados para comprender y usar '
               'nociones, conceptos y teorías de las ciencias naturales en la solución de problemas. Evalúa también la habilidad de los '
               'evaluados para explicar cómo ocurren algunos fenómenos de la naturaleza, con base en observaciones, patrones y conceptos '
               'propios del conocimiento científico. La prueba, además, involucra en la evaluación el proceso de indagación, que incluye '
               'observar y relacionar patrones en los datos para llegar a conclusiones sobre fenómenos naturales. La prueba Ciencias '
               'Naturales no pretende evaluar conocimientos científicos en sentido estricto, sino la capacidad para reconstruir '
               'significativamente el conocimiento existente, razonar, tomar decisiones, resolver problemas, pensar con rigurosidad y '
               'valorar de manera crítica el conocimiento y sus consecuencias en la sociedad y en el ambiente.')

COMPETENCIAS = [
    {
        'nombre': 'Explicación de fenómenos', 'porcentaje': 30, 'pagina': 55, 'pagina_porcentaje': 62,
        'rotulo_porcentaje': 'b. Explicación de fenómenos 9 % 9 % 9 % 3 %',
        'descripcion': 'Es la capacidad de construir explicaciones y comprender argumentos y modelos que den razón de fenómenos, así como de establecer la validez o coherencia de una afirmación o de un argumento relacionados con un fenómeno o problema científico.',
        'afirmaciones': [
            {'numero': 1, 'pagina': 55, 'texto': 'Analiza el potencial del uso de recursos naturales o artefactos y sus efectos sobre el entorno y la salud, así como las posibilidades de desarrollo para las comunidades.', 'evidencias': {
                '1.1': 'Explica algunos principios para mantener la salud individual y la pública basado en principios biológicos, químicos y físicos.',
                '1.2': 'Explica cómo la explotación de un recurso o el uso de una tecnología tiene efectos positivos o negativos en las personas y en el entorno.',
                '1.3': 'Explica el uso correcto y seguro de una tecnología o artefacto en un contexto específico.',
            }},
            {'numero': 2, 'pagina': 55, 'texto': 'Explica cómo ocurren algunos fenómenos de la naturaleza basado en observaciones, patrones y conceptos propios del conocimiento científico.', 'evidencias': {
                '2.1': 'Da las razones por las cuales una reacción describe un fenómeno y justifica las relaciones cuantitativas existentes, teniendo en cuenta la ley de conservación de la masa y carga.',
                '2.2': 'Reconoce las razones por las cuales la materia se puede diferenciar, según su estructura y propiedades, y justifica las diferencias existentes entre distintos elementos, compuestos y mezclas.',
                '2.3': 'Reconoce los atributos que definen ciertos procesos fisicoquímicos simples (separación de mezclas, solubilidad, gases ideales, cambios de fase) y da razón de la manera en que ocurren.',
                '2.4': 'Elabora explicaciones al relacionar las variables de estado que describen un sistema electrónico, argumentando a partir de los modelos básicos de circuitos.',
                '2.5': 'Elabora explicaciones al relacionar las variables de estado que describen un sistema, argumentando a partir de los modelos básicos de cinemática y dinámica newtoniana.',
                '2.6': ('Elabora explicaciones al relacionar las variables de estado que describen un sistema, argumentando a partir de los modelos básicos de la termodinámica.', 56),
                '2.7': ('Elabora explicaciones al relacionar las variables de estado que describen un sistema, argumentando a partir de los modelos básicos de ondas.', 56),
                '2.8': ('Analiza aspectos de los ecosistemas y da razón de cómo funcionan, de sus interrelaciones con los factores bióticos y abióticos y de sus efectos al modificarse alguna variable interna.', 56),
                '2.9': ('Analiza la dinámica interna de los organismos y da razón de cómo funcionan sus componentes por separado y en conjunto para mantener la vida en el organismo.', 56),
            }},
            {'numero': 3, 'pagina': 56, 'texto': 'Modela fenómenos de la naturaleza basado en el análisis de variables, la relación entre dos o más conceptos del conocimiento científico y de la evidencia derivada de investigaciones científicas.', 'evidencias': {
                '3.1': 'Usa modelos físicos basados en dinámica clásica para comprender un fenómeno particular en un sistema.',
                '3.2': 'Identifica y usa modelos químicos para comprender fenómenos particulares de la naturaleza.',
                '3.3': 'Analiza y usa modelos biológicos para comprender la dinámica que se da en lo vivo y en el entorno.',
            }},
        ],
    },
    {
        'nombre': 'Uso comprensivo del conocimiento científico', 'porcentaje': 30, 'pagina': 57, 'pagina_porcentaje': 62,
        'rotulo_porcentaje': 'a. Uso comprensivo del pensamiento científico 9 % 9 % 9 % 3 %',
        'descripcion': 'Es la capacidad para comprender y usar nociones, conceptos y teorías de las ciencias naturales en la solución de problemas, y de establecer relaciones entre conceptos y conocimientos adquiridos y fenómenos que se observan con frecuencia.',
        'afirmaciones': [
            {'numero': 4, 'pagina': 57, 'texto': 'Asocia fenómenos naturales con conceptos propios del conocimiento científico.', 'evidencias': {
                '4.1': 'Relaciona los componentes de un circuito en serie y en paralelo con sus respectivos voltajes y corrientes.',
                '4.2': 'Relaciona los distintos factores que determinan la dinámica de un sistema o fenómeno (condiciones iniciales, parámetros y constantes) para identificar su comportamiento, teniendo en cuenta las leyes de la física.',
                '4.3': 'Relaciona los tipos de energía presentes en un objeto con las interacciones que presenta el sistema con su entorno.',
                '4.4': 'Establece relaciones entre fenómenos biológicos para comprender la dinámica de lo vivo.',
                '4.5': 'Establece relaciones entre fenómenos biológicos para comprender su entorno.',
                '4.6': 'Diferencia distintos tipos de reacciones químicas y realiza de manera adecuada cálculos teniendo en cuenta la ley de conservación de la masa y carga.',
                '4.7': 'Establece relaciones entre conceptos fisicoquímicos simples (separación de mezclas, solubilidad, gases ideales) con distintos fenómenos naturales.',
                '4.8': 'Establece relaciones entre las propiedades y estructura de la materia con la formación de iones y moléculas.',
            }},
            {'numero': 5, 'pagina': 58, 'texto': 'Identifica las características de algunos fenómenos de la naturaleza basado en el análisis de información y conceptos propios del conocimiento científico.', 'evidencias': {
                '5.1': 'Identifica las características fundamentales de las ondas, así como las variables y parámetros que afectan estas características en un medio de propagación.',
                '5.2': 'Identifica las formas de energía presentes en un fenómeno físico y las transformaciones que se dan entre ellas.',
                '5.3': 'Identifica los diferentes tipos de fuerzas que actúan sobre los cuerpos que conforman un sistema.',
                '5.4': 'Identifica características de algunos procesos que se da en los ecosistemas para comprender la dinámica que se dan a su interior.',
                '5.5': 'Identifica características de algunos procesos que se dan en los organismos para comprender la dinámica de lo vivo.',
                '5.6': 'Identifica las propiedades y estructura de la materia y diferencia elementos, compuestos y mezclas.',
                '5.7': 'Reconoce posibles cambios en el entorno por la explotación de un recurso o el uso de una tecnología.',
            }},
        ],
    },
    {
        'nombre': 'Indagación', 'porcentaje': 40, 'pagina': 59, 'pagina_porcentaje': 62,
        'rotulo_porcentaje': 'c. Indagación 12 % 12 % 12 % 4 %',
        'descripcion': 'Vincular a los estudiantes con la forma como se amplía y modifica el conocimiento científico es esencial para formar ciudadanos alfabetizados científicamente. Esta competencia se define como la capacidad para comprender que, a partir de la investigación científica, se construyen explicaciones del mundo natural. Además, involucra los procedimientos o metodologías que se aplican para generar más preguntas o intentar dar respuestas a estas. El proceso de indagación en ciencias incluye, entre otras cosas, observar detenidamente la situación planteada, formular preguntas, recurrir a libros u otras fuentes de información, hacer predicciones, plantear experimentos, identificar variables, realizar mediciones y organizar y analizar resultados. En el aula de clases no se trata de que el alumno repita un protocolo ya establecido o elaborado por el docente, sino que el estudiante formule sus propias preguntas y diseñe su propio procedimiento.',
        'afirmaciones': [
            {'numero': 6, 'pagina': 59, 'texto': 'Comprende que a partir de la investigación científica se construyen explicaciones sobre el mundo natural.', 'evidencias': {
                '6.1': 'Analiza qué tipo de pregunta puede ser contestada a partir del contexto de una investigación científica.',
                '6.2': 'Reconoce la importancia de la evidencia para comprender fenómenos naturales.',
            }},
            {'numero': 7, 'pagina': 59, 'texto': 'Deriva conclusiones para algunos fenómenos de la naturaleza, basándose en conocimientos científicos y en la evidencia de su propia investigación y la de otros.', 'evidencias': {
                '7.1': 'Comunica de forma apropiada el proceso y los resultados de investigación en ciencias naturales.',
                '7.2': 'Determina si los resultados derivados de una investigación son suficientes y pertinentes para sacar conclusiones en una situación dada.',
                '7.3': ('Elabora conclusiones a partir de información o evidencias que las respalden.', 60),
                '7.4': ('Hace predicciones basado en información, patrones y regularidades.', 60),
            }},
            {'numero': 8, 'pagina': 60, 'texto': 'Observa y relaciona patrones en los datos para evaluar las predicciones.', 'evidencias': {
                '8.1': 'Interpreta y analiza datos representados en texto, gráficas, dibujos, diagramas o tablas.',
                '8.2': 'Representa datos en gráficas y tablas.',
            }},
            {'numero': 9, 'pagina': 60, 'texto': 'Utiliza algunas habilidades de pensamiento y de procedimiento para evaluar predicciones.', 'evidencias': {
                '9.1': 'Da posibles explicaciones de eventos o fenómenos consistentes con conceptos de la ciencia.',
                '9.2': 'Diseña experimentos para dar respuesta a sus preguntas.',
                '9.3': 'Elige y utiliza instrumentos adecuados para reunir datos.',
                '9.4': 'Reconoce la necesidad de registrar y clasificar la información para realizar un buen análisis.',
                '9.5': 'Usa información adicional para evaluar una predicción.',
            }},
        ],
    },
]

# Componentes evaluados (pág. 61) y su peso en cada competencia (tabla 31, pág. 62).
COMPONENTES = [
    {'codigo': 'NAT-CP-BIO', 'nombre': 'Conceptos del componente biológico', 'porcentaje_preguntas': 30,
     'texto': 'Homeostasis en los seres vivos, la herencia y la reproducción, las relaciones ecológicas, la evolución y transformación de la vida en el planeta, la conservación de la energía.'},
    {'codigo': 'NAT-CP-FIS', 'nombre': 'Conceptos del componente físico', 'porcentaje_preguntas': 30,
     'texto': 'Cinemática, dinámica, electromagnetismo, energía mecánica, ondas, energía térmica, campo gravitacional, transformación y conservación de la energía.'},
    {'codigo': 'NAT-CP-QUI', 'nombre': 'Conceptos del componente químico', 'porcentaje_preguntas': 30,
     'texto': 'Cambios químicos, el átomo, tipos de enlaces, propiedades de la materia, estequiometría, separación de mezclas, solubilidad, gases ideales, transformación y conservación de la energía.'},
    {'codigo': 'NAT-CP-CTS', 'nombre': 'Temáticas del componente de Ciencia, Tecnología y Sociedad (CTS)', 'porcentaje_preguntas': 10,
     'texto': 'Se trata de temáticas interdisciplinares relacionadas con las ciencias naturales. Algunas son globales, como la deforestación, el efecto invernadero y la producción de transgénicos; y otras son locales, como la explotación de recursos y el tratamiento de basuras. No se requiere un conocimiento previo de estas temáticas.'},
]
DISTRIBUCION = [  # competencia (como la nombra la tabla 31), biológico, físico, químico, CTS, total
    ['Uso comprensivo del pensamiento científico', 9, 9, 9, 3, 30],
    ['Explicación de fenómenos', 9, 9, 9, 3, 30],
    ['Indagación', 12, 12, 12, 4, 40],
]
assert all(sum(f[1:5]) == f[5] for f in DISTRIBUCION) and [sum(f[i] for f in DISTRIBUCION) for i in range(1, 6)] == [30, 30, 30, 10, 100]

letras = 'abcd'
COMPROBACIONES = [(f"{letras[i]}. {c['nombre']} {c['texto']}", 61) for i, c in enumerate(COMPONENTES)] + [('Total 30 % 30 % 30 % 10 % 100 %', 62)]

EXTRA_MD = '\n'.join(
    ['## Componentes evaluados (pág. 61)', ''] + [f"- `{c['codigo']}` **{c['nombre']}** · {c['porcentaje_preguntas']} % de las preguntas. {c['texto']}" for c in COMPONENTES]
    + ['', '## Distribución de preguntas por competencia y componente (tabla 31, pág. 62)', '', '| Competencia | Biológico | Físico | Químico | CTS | Total |', '|---|---|---|---|---|---|']
    + [f'| {f[0]} | {f[1]} % | {f[2]} % | {f[3]} % | {f[4]} % | {f[5]} % |' for f in DISTRIBUCION] + ['| **Total** | 30 % | 30 % | 30 % | 10 % | 100 % |'])

NOTAS = [
    'La tabla 31 nombra la segunda competencia «Uso comprensivo del pensamiento científico» y la pone primera; en el resto de la guía se llama «Uso comprensivo del conocimiento científico» y va segunda. Aquí se usa el nombre y el orden del desarrollo (págs. 55 a 60), y la tabla se guarda con su propio rótulo.',
    'Sin correcciones tipográficas. La evidencia 5.4 dice «procesos que se da en los ecosistemas» y «la dinámica que se dan a su interior»: se deja como está en el PDF.',
    'Las tablas de las afirmaciones 2 y 7 continúan en la página siguiente: cada evidencia lleva la página donde está.',
    'Esta prueba no desagrega habilidades por competencia, como sí lo hace Sociales y Ciudadanas.',
]
PENDIENTES = [
    '**Marco de referencia de la prueba**, que la guía cita como origen: no está en `fuentes/icfes/`.',
    '**Niveles de desempeño de Ciencias Naturales**: no están en esta guía.',
    'La guía remite a los Estándares Básicos de Competencias de Ciencias Naturales: ese PDF está en `fuentes/men/` sin procesar.',
]

publicar('ciencias_naturales', 'Ciencias Naturales', 'NAT', DESCRIPCION, 54, COMPETENCIAS, NOTAS, PENDIENTES, EXTRA_MD,
         extra={'componentes': [c | {'pagina': 61} for c in COMPONENTES],
                'distribucion_por_competencia_y_componente': [dict(zip(['competencia_segun_tabla', 'biologico', 'fisico', 'quimico', 'cts', 'total'], f)) | {'pagina': 62} for f in DISTRIBUCION]},
         comprobaciones=COMPROBACIONES)
