# Verificación de ingles

Fecha: 2026-10-03

## Fuentes

| Archivo | SHA-256 |
|---|---|
| `dba-transicion-y-primaria_ingles.pdf` | `9f5dba10ef169fd88afae060826bdc6a596948bf0cea8267dcde9cfa0d28254a` |
| `dba-ingles.pdf` | `623646ed1bb7bfa82d4e99e44c52a35065456b23bebb7c12bcf2596c5fca6cf0` |

## Resultado

| Tipo | Textos |
|---|---|
| DBA | 71 |

- Literales en el PDF: **71 de 71**
- Completos (frontera confirmada automáticamente): 71
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
