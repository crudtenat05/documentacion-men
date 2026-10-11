# Verificación ICFES · Ciencias Naturales

Fecha: 2026-10-10

## Fuente

| Archivo | SHA-256 |
|---|---|
| `fuentes/icfes/guia-orientacion-saber11-2026-2.pdf` | `9022a58a6ab2ff9d488b5c94be3392acf9da3433038de1ede3f822fa55d2eeb3` |

## Resultado

| Tipo | Elementos |
|---|---|
| Competencia | 3 |
| Habilidad (con su descripción) | 0 |
| Afirmación | 9 |
| Evidencia | 43 |

- Comprobaciones literales contra el PDF: **64 de 64** (descripción de la prueba y de cada competencia, habilidades, afirmaciones, evidencias y porcentajes). El programa se detiene sin escribir si una sola falla.
- Los porcentajes de las competencias suman 100.

- La tabla 31 nombra la segunda competencia «Uso comprensivo del pensamiento científico» y la pone primera; en el resto de la guía se llama «Uso comprensivo del conocimiento científico» y va segunda. Aquí se usa el nombre y el orden del desarrollo (págs. 55 a 60), y la tabla se guarda con su propio rótulo.
- Sin correcciones tipográficas. La evidencia 5.4 dice «procesos que se da en los ecosistemas» y «la dinámica que se dan a su interior»: se deja como está en el PDF.
- Las tablas de las afirmaciones 2 y 7 continúan en la página siguiente: cada evidencia lleva la página donde está.
- Esta prueba no desagrega habilidades por competencia, como sí lo hace Sociales y Ciudadanas.

## Método

1. Los textos están transcritos en `extraccion/icfes_ciencias_naturales.py`, leídos del PDF y contrastados con la imagen de cada página (`pdftoppm`).
2. `extraccion/icfes_transcrito.py` comprueba que cada uno aparezca literal en el texto de su página (`pdftotext -raw`). Solo se toleran espacios y saltos de línea.
3. Si todo coincide, genera el JSON, el CSV y la versión legible.

## Pendiente

- **Marco de referencia de la prueba**, que la guía cita como origen: no está en `fuentes/icfes/`.
- **Niveles de desempeño de Ciencias Naturales**: no están en esta guía.
- La guía remite a los Estándares Básicos de Competencias de Ciencias Naturales: ese PDF está en `fuentes/men/` sin procesar.
