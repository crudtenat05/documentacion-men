# Verificación ICFES · Sociales y Ciudadanas

Fecha: 2026-10-10

## Fuente

| Archivo | SHA-256 |
|---|---|
| `fuentes/icfes/guia-orientacion-saber11-2026-2.pdf` | `9022a58a6ab2ff9d488b5c94be3392acf9da3433038de1ede3f822fa55d2eeb3` |

## Resultado

| Tipo | Elementos |
|---|---|
| Competencia | 3 |
| Habilidad (con su descripción) | 6 |
| Afirmación | 6 |
| Evidencia | 16 |

- Comprobaciones literales contra el PDF: **35 de 35** (descripción de la prueba y de cada competencia, habilidades, afirmaciones, evidencias y porcentajes). El programa se detiene sin escribir si una sola falla.
- Los porcentajes de las competencias suman 100.

- Sin correcciones tipográficas. En la habilidad 1 de la tercera competencia el PDF dice «así como y posibilidad de valorar decisiones» y «acerca de y en relación con»: se dejan como están.
- La guía no dice qué afirmación corresponde a cada habilidad. En la segunda competencia el orden está cruzado: la habilidad 1 es el reconocimiento de posturas y la 2 el análisis de fuentes, pero la afirmación 3 trata de fuentes y la 4 de perspectivas. Por eso las habilidades se guardan junto a su competencia, sin enlazarlas a una afirmación.
- Las comillas de «políticamente correcto» y «deber ser» son las curvas del PDF (“ ”).

## Método

1. Los textos están transcritos en `extraccion/icfes_sociales_ciudadanas.py`, leídos del PDF y contrastados con la imagen de cada página (`pdftoppm`).
2. `extraccion/icfes_transcrito.py` comprueba que cada uno aparezca literal en el texto de su página (`pdftotext -raw`). Solo se toleran espacios y saltos de línea.
3. Si todo coincide, genera el JSON, el CSV y la versión legible.

## Pendiente

- **Marco de referencia de la prueba**, que la guía cita como origen: no está en `fuentes/icfes/`.
- **Niveles de desempeño de Sociales y Ciudadanas**: no están en esta guía.
- La guía dice que las competencias están «alineadas con lo propuesto en los Estándares Básicos de Competencias en Ciencias Sociales y Competencias Ciudadanas, publicados por el MEN en 2006»: esos dos PDF están en `fuentes/men/` sin procesar.
