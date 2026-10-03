# Verificación ICFES · Matemáticas

Fecha: 2026-09-29

## Fuente

| Archivo | SHA-256 |
|---|---|
| `fuentes/icfes/guia-orientacion-saber11-2026-2.pdf` | `9022a58a6ab2ff9d488b5c94be3392acf9da3433038de1ede3f822fa55d2eeb3` |

## Resultado

| Tipo | Textos |
|---|---|
| Competencia | 3 |
| Afirmación | 3 |
| Evidencia | 8 |
| Contenido | 23 |

- Literales en el PDF: **37 de 37** (descripción de cada competencia, afirmaciones, evidencias y contenidos). El extractor se detiene sin escribir si uno solo no aparece literal.
- Única corrección tipográfica: la maquetación deja un espacio antes del punto final de dos descripciones («EBC .»); se quita.

## Método

1. `extraccion/icfes_matematicas.py` lee el PDF con la posición de cada palabra y separa las columnas de la tabla de cada competencia (afirmación y evidencias) y las columnas de la figura de contenidos.
2. La descripción de cada competencia, cada afirmación y cada evidencia deben aparecer literales en el texto de su página, y cada contenido en el texto de su columna, leídos por otra vía (`pdftotext` sin posiciones). Solo se toleran espacios y cortes de palabra con guion.
3. `extraccion/icfes_salidas.py` genera las salidas desde el JSON verificado.

## Pendiente

- **Niveles de desempeño de Matemáticas** (rangos de puntaje y descriptores). No están en esta guía: vienen en el documento «Niveles de desempeño · Prueba Matemáticas Saber 11°» del ICFES. Falta el PDF original para extraerlos y verificarlos. Hasta entonces, ValorativoWeb los carga desde una transcripción no verificada.
