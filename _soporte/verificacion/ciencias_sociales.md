# Verificación de ciencias_sociales

Fecha: 2026-10-03

## Fuentes

| Archivo | SHA-256 |
|---|---|
| `dba-sociales.pdf` | `f816ba011a0c6041fbe9e72644832fbaa217340748dcdcd29aad3e7a3188870e` |

## Resultado

| Tipo | Textos |
|---|---|
| DBA | 82 |
| Evidencia | 328 |

- Literales en el PDF: **410 de 410**
- Completos (frontera confirmada automáticamente): 394
- Completos (confirmados por revisión manual): 16
- Pendientes: **0**

## Confirmaciones manuales

- `CS-DBA-1-02-E1` (pág. 8): La evidencia continúa en la parte superior de la columna derecha; en el flujo del PDF ambas mitades están separadas por el DBA siguiente. Confirmada contra la página.
- `CS-DBA-2-02-E1` (pág. 12): La evidencia continúa en la parte superior de la columna derecha; en el flujo del PDF ambas mitades están separadas por el DBA siguiente. Confirmada contra la página.
- `CS-DBA-6-05-E3` (pág. 31): La página 31 está impresa en diagonal y el flujo interno del PDF guarda esta evidencia con los caracteres al revés; se leyó por la posición de cada palabra y se confirmó contra la página.
- `CS-DBA-1-03-E3` (pág. 8): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-1-07-E4` (pág. 10): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-2-03-E3` (pág. 12): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-2-03-E4` (pág. 12): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-3-08-E4` (pág. 20): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-5-03-E4` (pág. 26): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-6-02-E4` (pág. 29): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-6-05-E2` (pág. 31): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-6-06-E4` (pág. 31): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-7-04-E4` (pág. 35): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-7-05-E4` (pág. 35): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-9-06-E4` (pág. 44): La evidencia termina antes de una imagen, un pie de foto o un espacio en blanco; en el flujo del PDF sigue ese otro texto. Confirmada contra la página.
- `CS-DBA-6-05-E1` (pág. 31): La ligadura «fi» de «geográficos» no existe en el texto interno del PDF; se restituyó como se lee en la página.

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
