# Verificación de ciencias_naturales

Fecha: 2026-10-03

## Fuentes

| Archivo | SHA-256 |
|---|---|
| `dba-naturales.pdf` | `3156475f8a0cc988080dc71c49b722f9f125726591adafd66f45a78d5e8a3f4d` |

## Resultado

| Tipo | Textos |
|---|---|
| DBA | 53 |
| Evidencia | 180 |

- Literales en el PDF: **233 de 233**
- Completos (frontera confirmada automáticamente): 229
- Completos (confirmados por revisión manual): 4
- Pendientes: **0**

## Confirmaciones manuales

- `CN-DBA-4-05-E3` (pág. 16): La evidencia empieza al pie de la columna derecha de la página 16 y continúa en la 17; entre ambas el flujo del PDF intercala el encabezado. Además se conserva el guion de «arena-gravilla», que el PDF parte al final de línea.
- `CN-DBA-6-03-E2` (pág. 22): Símbolo «H2O»: el subíndice 2 es un carácter pequeño en otra línea; se ubicó en su lugar, como se ve en la página.
- `CN-DBA-6-03-E4` (pág. 22): La evidencia termina al pie de la columna izquierda; en el flujo del PDF sigue el texto del ejemplo de la página siguiente.
- `CN-DBA-8-04-E4` (pág. 28): La evidencia termina al pie de la columna derecha; en el flujo del PDF sigue el ejemplo del DBA vecino.
- `CN-DBA-9-04-E4` (pág. 31): La evidencia termina al pie de la columna derecha; en el flujo del PDF sigue la continuación de un texto de la columna vecina.

## Método

Verificación independiente de los textos extraídos de un área.

Dos comprobaciones por cada estándar, enunciado de DBA y evidencia:

1. Literalidad: el texto aparece, carácter por carácter, en el texto plano del PDF obtenido por otra
   vía (pdftotext -raw, orden del flujo interno del PDF). Solo se ignoran diferencias tipográficas:
   espacios y saltos de línea, guiones de corte de palabra al final de línea, ligaduras (ﬁ → fi) y
   llamadas de nota al pie en superíndice. Cualquier otra diferencia hace fallar la verificación.
2. Completitud: lo que sigue al texto en el PDF es el inicio de otro elemento (viñeta, encabezado,
   número de DBA, pie de página), no la continuación de la misma frase. Así se detecta un texto al que
   le falte su final.

Los casos que la máquina no puede confirmar se revisan contra el PDF y se registran en
verificacion/<area>_confirmaciones_manuales.json con la razón.
