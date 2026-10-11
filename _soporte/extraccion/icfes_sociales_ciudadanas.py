"""Taxonomía de la prueba Sociales y Ciudadanas (Saber 11°): Guía de orientación 2026-2 del ICFES, páginas 46 a 53.

Uso (desde la raíz del repositorio):  python _soporte/extraccion/icfes_sociales_ciudadanas.py
"""
from icfes_transcrito import publicar

DESCRIPCION = ('De acuerdo con el Marco de referencia, esta prueba evalúa los conocimientos y habilidades que les permiten a los '
               'evaluados comprender el mundo social a partir de las ciencias sociales y establecer esa comprensión como referente '
               'para su ejercicio ciudadano. Asimismo, evalúa la habilidad para analizar distintos eventos, argumentos, posturas, '
               'conceptos, modelos, dimensiones y contextos, al igual que la capacidad para reflexionar y emitir juicios críticos de '
               'estos. En concordancia, la prueba no les pide a los evaluados que respondan desde su opinión, ni desde lo que se '
               'considera “políticamente correcto” o desde el “deber ser”, entendido este último como una forma correcta de actuar o '
               'pensar, que es aceptada o valorada positivamente por la sociedad.')

COMPETENCIAS = [
    {
        'nombre': 'Pensamiento social', 'porcentaje': 30, 'pagina': 47, 'pagina_porcentaje': 53, 'rotulo_porcentaje': 'a. Pensamiento social',
        'descripcion': 'Esta competencia evalúa la capacidad de los evaluados para usar y apropiarse de categorías básicas de las ciencias sociales; así como el conocimiento que tienen de principios constitucionales, del ordenamiento político colombiano y de los mecanismos constitucionales de participación.',
        'habilidades': [
            {'numero': 1, 'pagina': 47, 'nombre': 'Capacidad para identificar y usar conceptos básicos de las ciencias sociales',
             'descripcion': 'Para evaluar esta habilidad se plantean preguntas que se deben analizar a través de conceptos básicos de las ciencias sociales. Se evalúan los conocimientos referidos a la Constitución, en especial, sus fundamentos, los derechos y deberes de los ciudadanos y la organización del Estado. Así mismo, se evalúan los conocimientos en torno a los mecanismos de participación que los ciudadanos tienen a su disposición para velar por el cumplimiento de sus derechos y principios, como la defensa de la diversidad étnica y cultural. También se evalúan conceptos básicos de las ciencias sociales, que no están ligados al conocimiento de la Constitución.'},
            {'numero': 2, 'pagina': 47, 'nombre': 'Capacidad para identificar dimensiones temporales y espaciales de eventos y problemáticas sociales',
             'descripcion': 'Esta habilidad evalúa la comprensión de dimensiones temporales y espaciales de eventos y prácticas sociales; así como la capacidad para analizar las dimensiones históricas de eventos o problemáticas, y para relacionarlos con contextos geográficos y sus características, es decir, para conectar eventos e identificar razones que justifiquen esas conexiones.'},
        ],
        'afirmaciones': [
            {'numero': 1, 'pagina': 48, 'texto': 'Comprende modelos conceptuales, sus características y contextos de aplicación.', 'evidencias': {
                '1.1': 'Identifica y usa conceptos sociales básicos (económicos, políticos, culturales y geográficos).',
                '1.2': 'Conoce el modelo de Estado Social de Derecho y su aplicación en Colombia.',
                '1.3': 'Conoce la organización del Estado: Conoce las funciones y alcances de las ramas del poder y de los organismos de control.',
                '1.4': 'Conoce los mecanismos que los ciudadanos tienen a su disposición para participar activamente en la democracia y para garantizar el respeto de sus derechos.',
            }},
            {'numero': 2, 'pagina': 48, 'texto': 'Comprende dimensiones espaciales y temporales de eventos, problemáticas y prácticas sociales.', 'evidencias': {
                '2.1': 'Localiza en el tiempo y en el espacio eventos históricos y prácticas sociales.',
                '2.2': 'Relaciona dimensiones históricas y geográficas de eventos y problemáticas sociales.',
                '2.3': 'Relaciona problemáticas o prácticas sociales con características del espacio geográfico.',
            }},
        ],
    },
    {
        'nombre': 'Interpretación y análisis de perspectivas', 'porcentaje': 40, 'pagina': 49, 'pagina_porcentaje': 53,
        'rotulo_porcentaje': 'b. Interpretación y análisis de perspectivas',
        'descripcion': 'Esta competencia evalúa la habilidad de los evaluados para analizar críticamente la información que circula en la sociedad acerca de asuntos políticos, económicos y culturales, con la intención de valorar argumentos y explicaciones sobre problemáticas sociales e identificar diversos intereses, opiniones y perspectivas de personas y grupos sociales que interactúan en un momento dado. Esta competencia se fundamenta en procesos cognitivos de identificación, comprensión; análisis y evaluación de sentido, pertinencia y solidez de enunciados o planteamientos (capacidad de emitir y valorar juicios).',
        'habilidades': [
            {'numero': 1, 'pagina': 49, 'nombre': 'Reconocimiento de diversas opiniones, posturas e intereses',
             'descripcion': 'En esta habilidad se evalúa la capacidad de los evaluados para analizar una problemática según las perspectivas de diferentes actores sociales o colectivos involucrados. Las preguntas correspondientes a esta habilidad requieren que los evaluados, a partir de un conflicto, comprendan su origen, entiendan qué buscan los diferentes actores, identifiquen las coincidencias y diferencias entre sus intereses y valoren la reacción (por ejemplo, de aceptación o rechazo) de las partes ante una propuesta de solución.'},
            {'numero': 2, 'pagina': 49, 'nombre': 'Análisis crítico de fuentes y argumentos',
             'descripcion': 'En esta habilidad se evalúa la capacidad de los evaluados para valorar fuentes primarias y secundarias, corroborar y contextualizar la información suministrada y la pertinencia y solidez de los enunciados o argumentos expuestos. Se espera que los evaluados estén en capacidad de identificar prejuicios presentes en discursos; comprender las intenciones implícitas en un determinado acto comunicativo; establecer relaciones entre diferentes argumentos; evaluar la validez de generalizaciones y la confiabilidad de un enunciado, así como de las fuentes en las que este se sustenta o pretende sustentarse. También se valora la capacidad para anticipar el efecto de un determinado discurso en individuos o grupos de personas.'},
        ],
        'afirmaciones': [
            {'numero': 3, 'pagina': 50, 'texto': 'Contextualiza y evalúa usos de fuentes y argumentos.', 'evidencias': {
                '3.1': 'Inscribe una fuente primaria dada en un contexto económico, político o cultural.',
                '3.2': 'Evalúa posibilidades y limitaciones del uso de una fuente para apoyar argumentos o explicaciones.',
                '3.3': 'Devela prejuicios e intenciones en enunciados o argumentos.',
            }},
            {'numero': 4, 'pagina': 50, 'texto': 'Comprende perspectivas de distintos actores y grupos sociales.', 'evidencias': {
                '4.1': 'Reconoce y compara perspectivas de actores y grupos sociales.',
                '4.2': 'Reconoce que las cosmovisiones, ideologías y roles sociales influyen en diferentes argumentos, posiciones y conductas.',
                '4.3': 'Establece relaciones entre las perspectivas de los individuos en una situación conflictiva y las propuestas de solución.',
            }},
        ],
    },
    {
        'nombre': 'Pensamiento reflexivo y sistémico', 'porcentaje': 30, 'pagina': 51, 'pagina_porcentaje': 53,
        'rotulo_porcentaje': 'c. Pensamiento reflexivo y sistémico',
        'descripcion': 'Esta competencia evalúa la capacidad de los evaluados para identificar las diferentes dimensiones presentes en una problemática social y las relaciones que se dan entre ellas, así como la capacidad para comprender y evaluar el uso de modelos conceptuales en la toma de decisiones en contextos sociales.',
        'habilidades': [
            {'numero': 1, 'pagina': 51, 'nombre': 'Identificar modelos conceptuales que orientan decisiones sociales',
             'descripcion': 'Esta habilidad hace referencia al conocimiento de modelos conceptuales y de sus posibles usos en determinados contextos. Evalúa la capacidad para identificar las características de un modelo y de los principios que lo sustentan, así como y posibilidad de valorar decisiones, como coherentes o incoherentes, acerca de y en relación con los objetivos o postulados del modelo.'},
            {'numero': 2, 'pagina': 51, 'nombre': 'Establecer relaciones entre dimensiones presentes en una situación problemática y sus posibles alternativas de solución',
             'descripcion': 'Esta habilidad evalúa la capacidad de los evaluados para identificar distintas dimensiones de la vida social y analizar los posibles efectos que una intervención tiene en tales dimensiones. Esto implica el reconocimiento de las relaciones entre los ámbitos (social, económico, ambiental y político, entre otros) que están presentes en un problema o decisión. Cabe indicar que, para entender una situación problemática, es necesario identificar su contexto y reconocer que en cada caso particular pueden presentarse diferentes valores o ideas que se privilegian en un momento dado. Se espera, en consecuencia, que los evaluados comprendan que cada situación involucra diferentes dimensiones y que, en ocasiones, estas pueden contraponerse entre sí. Por ende, se debe comprender que las decisiones que se toman pueden favorecer unas dimensiones e ir en detrimento de otras.'},
        ],
        'afirmaciones': [
            {'numero': 5, 'pagina': 52, 'texto': 'Evalúa usos sociales de las ciencias sociales.', 'evidencias': {
                '5.1': 'Analiza modelos conceptuales y sus usos en decisiones sociales.',
            }},
            {'numero': 6, 'pagina': 52, 'texto': 'Comprende que los problemas y sus soluciones involucran distintas dimensiones y reconoce relaciones entre estas.', 'evidencias': {
                '6.1': 'Establece relaciones que hay entre dimensiones presentes en una situación problemática.',
                '6.2': 'Analiza los efectos en distintas dimensiones que tendría una posible intervención.',
            }},
        ],
    },
]

NOTAS = [
    'Sin correcciones tipográficas. En la habilidad 1 de la tercera competencia el PDF dice «así como y posibilidad de valorar decisiones» y «acerca de y en relación con»: se dejan como están.',
    'La guía no dice qué afirmación corresponde a cada habilidad. En la segunda competencia el orden está cruzado: la habilidad 1 es el reconocimiento de posturas y la 2 el análisis de fuentes, pero la afirmación 3 trata de fuentes y la 4 de perspectivas. Por eso las habilidades se guardan junto a su competencia, sin enlazarlas a una afirmación.',
    'Las comillas de «políticamente correcto» y «deber ser» son las curvas del PDF (“ ”).',
]
PENDIENTES = [
    '**Marco de referencia de la prueba**, que la guía cita como origen: no está en `fuentes/icfes/`.',
    '**Niveles de desempeño de Sociales y Ciudadanas**: no están en esta guía.',
    'La guía dice que las competencias están «alineadas con lo propuesto en los Estándares Básicos de Competencias en Ciencias Sociales y Competencias Ciudadanas, publicados por el MEN en 2006»: esos dos PDF están en `fuentes/men/` sin procesar.',
]

publicar('sociales_ciudadanas', 'Sociales y Ciudadanas', 'SOC', DESCRIPCION, 46, COMPETENCIAS, NOTAS, PENDIENTES)
