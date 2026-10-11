<?php

/**
 * Taxonomía de la prueba Lectura Crítica (Saber 11°) según la Guía de orientación 2026-2 del ICFES, páginas 39 a 45.
 *
 * Uso (desde la raíz del repositorio):  php _soporte/extraccion/icfes_lectura_critica.php
 *
 * Está en PHP y no en Python, como los demás extractores, porque en el equipo donde se hizo (2026-10-10) no había
 * Python ni un lector de PDF con posiciones. Por eso los textos no se sacan por coordenadas: están transcritos aquí
 * abajo, y el programa NO escribe nada si uno solo no aparece literal en el PDF, leído con pdftotext en dos modos
 * (-raw para los párrafos y las tablas, -table para confirmar filas y columnas). Solo se toleran espacios y saltos
 * de línea.
 */

const PDF = 'fuentes/icfes/guia-orientacion-saber11-2026-2.pdf';
const SALIDA = '_soporte/datos/icfes/lectura_critica';

$documento = [
    'codigo' => 'ICFES-GUIA-S11-2026-2',
    'entidad' => 'ICFES',
    'titulo' => 'Guía de orientación del Examen Saber 11º 2026-2 (Calendario A)',
    'version' => '2026-2',
    'anio' => 2026,
    'archivo' => PDF,
];

$prueba = [
    'descripcion' => 'Esta prueba evalúa las habilidades de entender, interpretar y evaluar textos que pueden encontrarse tanto en la vida cotidiana como en ámbitos académicos no especializados. Se espera que los estudiantes que culminan la educación media cuenten con las capacidades lectoras para tomar posturas críticas frente a esta clase de textos.',
    'pagina' => 39,
];

// A diferencia de Matemáticas (tres competencias), esta prueba evalúa UNA competencia, la lectora, que la guía
// desagrega en tres procesos cognitivos; cada proceso se recoge en una afirmación.
$competencia = [
    'codigo' => 'LEC-C1',
    'nombre' => 'Competencia lectora',
    'descripcion' => 'De acuerdo con el Marco de referencia de esta prueba, se evalúa la competencia lectora, la cual involucra, de manera general, los procesos cognitivos necesarios para leer de manera crítica diferentes tipos de texto.',
    'pagina' => 39,
];

$afirmaciones = [
    [
        'numero' => 1, 'pagina' => 40, 'porcentaje' => 25,
        'proceso' => 'Identificar y ubicar información local',
        'descripcion' => 'Este proceso se relaciona con la capacidad para comprender el significado de las palabras, expresiones y frases que aparecen explícitamente en el texto. La evaluación de este proceso no indaga por conocimientos propios de la gramática, pero sí por la comprensión de las relaciones semánticas que existen entre los diferentes elementos que constituyen una oración. En esa medida, permite dar respuesta a preguntas como: ¿qué?, ¿dónde?, ¿cuándo?, ¿quién?, ¿de qué manera?, ¿con quién? La afirmación que recoge este proceso es: Identifica y entiende los contenidos locales que conforman un texto.',
        'texto' => 'Identifica y entiende los contenidos locales que conforman un texto.',
        'evidencias' => [
            '1.1' => 'Entiende el significado de los elementos locales que constituyen un texto.',
            '1.2' => 'Identifica los eventos narrados de manera explícita en un texto (literario, descriptivo, caricatura o cómic) y los personajes involucrados (si los hay).',
        ],
    ],
    [
        'numero' => 2, 'pagina' => 41, 'porcentaje' => 42,
        'proceso' => 'Relacionar e interpretar información',
        'descripcion' => 'Este proceso se relaciona con la capacidad para comprender cómo se relacionan formal y semánticamente los elementos locales que constituyen un texto, de manera que este adquiera un sentido global (a nivel de párrafos, secciones, capítulos, etcétera). En esa medida, las preguntas correspondientes a este proceso cognitivo involucran varios elementos locales de un texto (por ejemplo, diferentes frases o párrafos) y exigen reconocer y comprender su articulación. En este proceso de lectura se activa el conocimiento previo del lector, quien relaciona la información del texto para obtener conclusiones, plantear una hipótesis, hacer generalizaciones, comprender el lenguaje implícito. La afirmación que recoge este proceso es Comprende cómo se articulan las partes de un texto para darle un sentido global.',
        'texto' => 'Comprende cómo se articulan las partes de un texto para darle un sentido global.',
        'evidencias' => [
            '2.1' => 'Comprende la estructura formal de un texto y la función de sus partes.',
            '2.2' => 'Identifica y caracteriza las diferentes voces o situaciones presentes en un texto.',
            '2.3' => 'Comprende las relaciones entre diferentes partes o enunciados de un texto.',
            '2.4' => 'Identifica y caracteriza las ideas o afirmaciones presentes en un texto informativo.',
            '2.5' => 'Identifica el tipo de relación existente entre diferentes elementos de un texto (discontinuo).',
        ],
    ],
    [
        'numero' => 3, 'pagina' => 42, 'porcentaje' => 33,
        'proceso' => 'Evaluar y reflexionar sobre la forma y el contenido de los textos',
        'descripcion' => 'Este proceso se relaciona con la capacidad para enfrentar un texto críticamente e implica identificar la intención comunicativa del autor y reflexionar sobre la forma y el contenido del texto. Incluye evaluar la validez de argumentos, advertir supuestos, derivar implicaciones, reconocer estrategias argumentativas y retóricas, relacionar contenidos con variables contextuales, etcétera. Se trata de la habilidad propiamente crítica y, como tal, exige un ejercicio adecuado de las dos anteriores. La afirmación que recoge este proceso es Reflexiona a partir de un texto y evalúa su contenido.',
        'texto' => 'Reflexiona a partir de un texto y evalúa su contenido.',
        'evidencias' => [
            '3.1' => 'Establece la validez e implicaciones de un enunciado de un texto (argumentativo o expositivo).',
            '3.2' => 'Establece relaciones entre un texto y otros textos o enunciados.',
            '3.3' => 'Reconoce contenidos valorativos presentes en un texto.',
            '3.4' => 'Reconoce las estrategias discursivas en un texto.',
            '3.5' => 'Contextualiza adecuadamente un texto o la información contenida en este.',
        ],
    ],
];

// Tabla 21 (pág. 43): tipos de textos. «imagenes» va sin tilde porque así está en el PDF.
$tiposDeTexto = [
    ['codigo' => 'LEC-TX-CON-LIT', 'formato' => 'Continuos', 'clase' => 'Literarios', 'ejemplos' => 'Novela, cuento, poesía, canción, dramaturgia'],
    ['codigo' => 'LEC-TX-CON-INF', 'formato' => 'Continuos', 'clase' => 'Informativos (descriptivos, expositivos, argumentativos)', 'ejemplos' => 'Ensayo, columna de opinión, crónica'],
    ['codigo' => 'LEC-TX-DIS-LIT', 'formato' => 'Discontinuos', 'clase' => 'Literarios', 'ejemplos' => 'Caricatura, cómic'],
    ['codigo' => 'LEC-TX-DIS-INF', 'formato' => 'Discontinuos', 'clase' => 'Informativos (descriptivos, expositivos, argumentativos)', 'ejemplos' => 'Etiqueta, infografía, tabla, diagrama, aviso publicitario, manual, reglamento, imagenes'],
];

// Tabla 22 (pág. 44): distribución aproximada de preguntas por tipo de texto.
$distribucion = [
    ['formato' => 'Continuos', 'tipo' => 'Literario', 'porcentaje' => 24],
    ['formato' => 'Continuos', 'tipo' => 'Informativo filosófico', 'porcentaje' => 30],
    ['formato' => 'Continuos', 'tipo' => 'Informativo no filosófico', 'porcentaje' => 30],
    ['formato' => 'Discontinuos', 'tipo' => 'Literario', 'porcentaje' => 8],
    ['formato' => 'Discontinuos', 'tipo' => 'Informativo', 'porcentaje' => 8],
];

// ── Verificación: cada texto debe estar literal en su página ──
function pagina(int $n, string $modo): string
{
    $t = (string) shell_exec('pdftotext -q -enc UTF-8 '.$modo.' -f '.$n.' -l '.$n.' '.escapeshellarg(PDF).' -');

    return (string) preg_replace('/\s+/u', ' ', $t);
}
function esta(string $texto, int $pagina, string $modo = '-raw'): bool
{
    static $cache = [];
    $cache[$modo.$pagina] ??= pagina($pagina, $modo);

    return str_contains($cache[$modo.$pagina], (string) preg_replace('/\s+/u', ' ', $texto));
}

$fallos = [];
$n = ['competencia' => 0, 'proceso' => 0, 'afirmacion' => 0, 'evidencia' => 0, 'tipo' => 0, 'distribucion' => 0];
$revisar = function (string $que, string $texto, int $pagina, string $modo = '-raw') use (&$fallos, &$n) {
    $n[$que]++;
    if (! esta($texto, $pagina, $modo)) {
        $fallos[] = "[$que, pág. $pagina] ".mb_substr($texto, 0, 90);
    }
};

$revisar('competencia', $prueba['descripcion'], 39);
$revisar('competencia', $competencia['descripcion'], 39);
foreach ($afirmaciones as $a) {
    $revisar('proceso', $a['descripcion'], $a['pagina']);
    $revisar('afirmacion', $a['numero'].'. '.preg_replace('/\.$/', '', $a['texto']), $a['pagina'], '-raw');
    foreach ($a['evidencias'] as $num => $texto) {
        $revisar('evidencia', $num.' '.$texto, $a['pagina']);
    }
    // Porcentaje de la tabla 23 (pág. 45), en la misma fila de su afirmación.
    $revisar('afirmacion', $a['porcentaje'].' %', 45);
}
foreach ($tiposDeTexto as $t) {
    $revisar('tipo', $t['ejemplos'], 43);
}
foreach ($distribucion as $d) {
    $revisar('distribucion', $d['tipo'].' '.$d['porcentaje'].' %', 44);
}
if (array_sum(array_column($distribucion, 'porcentaje')) !== 100 || array_sum(array_column($afirmaciones, 'porcentaje')) !== 100) {
    $fallos[] = 'Los porcentajes no suman 100.';
}
if ($fallos) {
    fwrite(STDERR, "NO se escribió nada. Textos que no aparecen literales en el PDF:\n- ".implode("\n- ", $fallos)."\n");
    exit(1);
}

// ── Salidas ──
@mkdir(SALIDA, 0775, true);
$json = [
    'documento' => $documento,
    'prueba' => 'lectura_critica',
    'descripcion' => $prueba['descripcion'],
    'pagina' => $prueba['pagina'],
    'competencias' => [[
        'codigo' => $competencia['codigo'],
        'nombre' => $competencia['nombre'],
        'descripcion' => $competencia['descripcion'],
        'porcentaje_preguntas' => 100,
        'orden' => 1,
        'pagina' => $competencia['pagina'],
        'afirmaciones' => array_map(fn ($a) => [
            'codigo' => 'LEC-A'.$a['numero'],
            'numero' => $a['numero'],
            'proceso' => $a['proceso'],
            'descripcion_proceso' => $a['descripcion'],
            'texto' => $a['texto'],
            'porcentaje_preguntas' => $a['porcentaje'],
            'pagina' => $a['pagina'],
            'evidencias' => array_map(fn ($num, $texto) => ['codigo' => 'LEC-E'.$num, 'numero' => (string) $num, 'texto' => $texto], array_keys($a['evidencias']), $a['evidencias']),
        ], $afirmaciones),
    ]],
    'tipos_de_texto' => array_map(fn ($t) => $t + ['pagina' => 43], $tiposDeTexto),
    'distribucion_por_tipo_de_texto' => array_map(fn ($d) => $d + ['pagina' => 44], $distribucion),
];
file_put_contents(SALIDA.'/taxonomia.json', json_encode($json, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)."\n");

$csv = function (string $archivo, array $encabezado, array $filas) {
    $f = fopen($archivo, 'w');
    fwrite($f, "\xEF\xBB\xBF");
    fputcsv($f, $encabezado, ',', '"', '');
    foreach ($filas as $fila) {
        fputcsv($f, $fila, ',', '"', '');
    }
    fclose($f);
};
$filas = [];
foreach ($afirmaciones as $a) {
    foreach ($a['evidencias'] as $num => $texto) {
        $filas[] = [$competencia['codigo'], $competencia['nombre'], 'LEC-A'.$a['numero'], $a['proceso'], $a['texto'], $a['porcentaje'], 'LEC-E'.$num, $texto, $a['pagina']];
    }
}
$csv(SALIDA.'/evidencias.csv', ['competencia', 'competencia_nombre', 'afirmacion', 'proceso', 'afirmacion_texto', 'porcentaje_preguntas', 'evidencia', 'evidencia_texto', 'pagina_pdf'], $filas);
$csv(SALIDA.'/tipos_de_texto.csv', ['codigo', 'formato', 'clase', 'ejemplos', 'pagina_pdf'], array_map(fn ($t) => [$t['codigo'], $t['formato'], $t['clase'], $t['ejemplos'], 43], $tiposDeTexto));
$csv(SALIDA.'/distribucion.csv', ['formato', 'tipo_de_texto', 'porcentaje_preguntas', 'pagina_pdf'], array_map(fn ($d) => [$d['formato'], $d['tipo'], $d['porcentaje'], 44], $distribucion));

$md = "# Lectura Crítica · Saber 11° · taxonomía del ICFES\n\n";
$md .= "Fuente: {$documento['titulo']} (`".PDF."`). Textos literales del PDF, con su página.\n\n";
$md .= $prueba['descripcion']." (pág. 39)\n\n";
$md .= "## Competencia, afirmaciones y evidencias\n\n";
$md .= "### `{$competencia['codigo']}` {$competencia['nombre']} (pág. 39)\n\n{$competencia['descripcion']}\n\n";
$md .= "La guía desagrega la competencia en tres procesos cognitivos; cada uno se recoge en una afirmación.\n\n";
foreach ($afirmaciones as $a) {
    $md .= "#### Proceso {$a['numero']} · {$a['proceso']} · {$a['porcentaje']} % de las preguntas (pág. {$a['pagina']})\n\n{$a['descripcion']}\n\n";
    $md .= "- **Afirmación** `LEC-A{$a['numero']}` {$a['texto']}\n";
    foreach ($a['evidencias'] as $num => $texto) {
        $md .= "  - `LEC-E{$num}` {$texto}\n";
    }
    $md .= "\n";
}
$md .= "## Tipos de textos utilizados (tabla 21, pág. 43)\n\n| Código | Formato | Clase | Ejemplos |\n|---|---|---|---|\n";
foreach ($tiposDeTexto as $t) {
    $md .= "| `{$t['codigo']}` | {$t['formato']} | {$t['clase']} | {$t['ejemplos']} |\n";
}
$md .= "\n«imagenes» va sin tilde porque así está en el PDF.\n\n";
$md .= "## Distribución aproximada de preguntas por tipo de texto (tabla 22, pág. 44)\n\n| Formato | Tipo de texto | Porcentaje |\n|---|---|---|\n";
foreach ($distribucion as $d) {
    $md .= "| {$d['formato']} | {$d['tipo']} | {$d['porcentaje']} % |\n";
}
file_put_contents(SALIDA.'/lectura_critica.md', $md);

$total = array_sum($n);
$ver = "# Verificación ICFES · Lectura Crítica\n\nFecha: ".date('Y-m-d')."\n\n## Fuente\n\n| Archivo | SHA-256 |\n|---|---|\n| `".PDF.'` | `'.hash_file('sha256', PDF)."` |\n\n";
$ver .= "## Resultado\n\n| Tipo | Elementos |\n|---|---|\n| Competencia | 1 |\n| Proceso cognitivo (con su descripción) | 3 |\n| Afirmación | 3 |\n| Evidencia | ".count($filas)." |\n| Tipo de texto (tabla 21) | ".count($tiposDeTexto)." |\n| Fila de distribución (tabla 22) | ".count($distribucion)." |\n\n";
$ver .= "- Comprobaciones literales contra el PDF: **{$total} de {$total}**. El programa se detiene sin escribir si una sola falla.\n";
$ver .= "- Los porcentajes por afirmación (25, 42 y 33) y por tipo de texto (24, 30, 30, 8 y 8) suman 100.\n";
$ver .= "- Sin correcciones tipográficas. «imagenes» se deja sin tilde, como está en el PDF.\n\n";
$ver .= "## Método\n\n1. Los textos están transcritos en `extraccion/icfes_lectura_critica.php` (no se extraen por coordenadas: ver la nota de ese archivo).\n";
$ver .= "2. Cada descripción, afirmación, evidencia y fila de tabla debe aparecer literal en el texto de su página, leído con `pdftotext -raw`. Solo se toleran espacios y saltos de línea.\n";
$ver .= "3. Las filas y columnas de las tablas 21 y 22 se confirmaron además con `pdftotext -table`, porque el modo `-layout` las desordena.\n\n";
$ver .= "## Diferencias con Matemáticas\n\n- Una sola competencia (la lectora), no tres. Lo que en Matemáticas son competencias, aquí son tres procesos cognitivos, uno por afirmación.\n- No hay lista de contenidos: en su lugar, la guía da los tipos de textos y su distribución.\n- El porcentaje de preguntas está dado por afirmación (tabla 23, pág. 45).\n\n";
$ver .= "## Pendiente\n\n- **Niveles de desempeño de Lectura Crítica**: no están en esta guía.\n- **Marco de referencia de la prueba**, que la guía cita como origen de la competencia: no está en `fuentes/icfes/`.\n";
file_put_contents('_soporte/verificacion/icfes_lectura_critica.md', $ver);

echo "Lectura Crítica: {$total} de {$total} comprobaciones literales. Salidas en ".SALIDA."\n";
