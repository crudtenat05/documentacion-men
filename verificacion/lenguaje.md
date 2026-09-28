# Verificación de lenguaje

Fecha: 2026-09-28

## Fuentes

| Archivo | SHA-256 |
|---|---|
| `estandares-lengua-castellana.pdf` | `2475062ca03b4c90801643bcee58cf5e8bb81aaa929a286b4506b30ca83b8695` |
| `dba-lenguaje.pdf` | `9918e0e7f44121d32efb652204e7a5f59a9d4b4abf86e47aec09bacf66946f44` |

## Resultado

| Tipo | Textos |
|---|---|
| Estándar | 35 |
| Subproceso | 177 |
| DBA | 88 |
| Evidencia | 333 |

- Literales en el PDF: **633 de 633**
- Completos (frontera confirmada automáticamente): 633
- Completos (confirmados por revisión manual): 0
- Pendientes: **0**

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
