# Verificación de matematicas

Fecha: 2026-10-03

## Fuentes

| Archivo | SHA-256 |
|---|---|
| `estandares-matematicas.pdf` | `37a3bbc6e2a47508b48b691473936323964d76d5d57785f7068e5e8753fd57be` |
| `dba-matematicas.pdf` | `72f23359840f31d59b15057b8022a7872ef0b1cd9b50e3aa98d70a29b30d56ca` |

## Resultado

| Tipo | Textos |
|---|---|
| Estándar | 172 |
| DBA | 119 |
| Evidencia | 437 |

- Literales en el PDF: **728 de 728**
- Completos (frontera confirmada automáticamente): 726
- Completos (confirmados por revisión manual): 2
- Pendientes: **0**

## Confirmaciones manuales

- `MAT-DBA-6-05` (pág. 47): El enunciado termina en «para resolver problemas.»; en el flujo interno del PDF lo sigue el texto de la figura del ejemplo (cancha de fútbol), no la continuación de la frase.
- `MAT-DBA-9-03-E2` (pág. 67): La evidencia termina en «con otras sucesiones.»; en el flujo interno del PDF la sigue la tabla de la figura del ejemplo (cuadrados, lado, perímetro, área).

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
