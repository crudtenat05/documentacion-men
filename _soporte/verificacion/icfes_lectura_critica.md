# Verificación ICFES · Lectura Crítica

Fecha: 2026-10-11

## Fuente

| Archivo | SHA-256 |
|---|---|
| `fuentes/icfes/guia-orientacion-saber11-2026-2.pdf` | `9022a58a6ab2ff9d488b5c94be3392acf9da3433038de1ede3f822fa55d2eeb3` |

## Resultado

| Tipo | Elementos |
|---|---|
| Competencia | 1 |
| Proceso cognitivo (con su descripción) | 3 |
| Afirmación | 3 |
| Evidencia | 12 |
| Tipo de texto (tabla 21) | 4 |
| Fila de distribución (tabla 22) | 5 |

- Comprobaciones literales contra el PDF: **32 de 32**. El programa se detiene sin escribir si una sola falla.
- Los porcentajes por afirmación (25, 42 y 33) y por tipo de texto (24, 30, 30, 8 y 8) suman 100.
- Sin correcciones tipográficas. «imagenes» se deja sin tilde, como está en el PDF.

## Método

1. Los textos están transcritos en `extraccion/icfes_lectura_critica.php` (no se extraen por coordenadas: ver la nota de ese archivo).
2. Cada descripción, afirmación, evidencia y fila de tabla debe aparecer literal en el texto de su página, leído con `pdftotext -raw`. Solo se toleran espacios y saltos de línea.
3. Las filas y columnas de las tablas 21 y 22 se confirmaron además con `pdftotext -table`, porque el modo `-layout` las desordena.

## Diferencias con Matemáticas

- Una sola competencia (la lectora), no tres. Lo que en Matemáticas son competencias, aquí son tres procesos cognitivos, uno por afirmación.
- No hay lista de contenidos: en su lugar, la guía da los tipos de textos y su distribución.
- El porcentaje de preguntas está dado por afirmación (tabla 23, pág. 45).

## Pendiente

- **Niveles de desempeño de Lectura Crítica**: no están en esta guía.
- **Marco de referencia de la prueba**, que la guía cita como origen de la competencia: no está en `fuentes/icfes/`.
