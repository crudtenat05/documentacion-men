# Verificación ICFES · Niveles de desempeño (Saber 11°)

Fecha: 2026-10-11

## Fuentes

| Archivo | SHA-256 |
|---|---|
| `fuentes/icfes/22-septiembre-nd-prueba-matematicas-saber-11.pdf` | `9aeae147442f0af64f9e6d71e935fcd89db0caa9a15b36f34c1767afe9bcc147` |
| `fuentes/icfes/22-septiembre-nd-prueba-lectura-critica-saber-11.pdf` | `8079b3753feb2f7da8677a557942c182ff196de033cd0b3fe83e2dfaea2a2dee` |
| `fuentes/icfes/22-septiembre-nd-prueba-sociales-y-ciudadanas-saber-11.pdf` | `056387daff4eed3d39d6801f82bc54f01b527681c312453e3eee083af20d0161` |
| `fuentes/icfes/22-septiembre-nd-prueba-ciencias-naturales-saber-11.pdf` | `3acaf55ea67f8e70122bec505bee314f8b9e16d96c93323ea796c65226bcf79c` |
| `fuentes/icfes/22-septiembre-nd-prueba-ingles-saber-11.pdf` | `849a23cd5e7c2813cf5ee67e727d21ab6461f6bce7df0fef85b42794db868e8f` |

## Resultado

| Prueba | Rangos de puntaje | Descriptores por nivel | Total |
|---|---|---|---|
| Matemáticas | 0 a 35 · 36 a 50 · 51 a 70 · 71 a 100 | 1 · 6 · 12 · 10 | 29 |
| Lectura Crítica | 0 a 35 · 36 a 50 · 51 a 65 · 66 a 100 | 1 · 8 · 10 · 8 | 27 |
| Sociales y Ciudadanas | 0 a 40 · 41 a 55 · 56 a 70 · 71 a 100 | 3 · 6 · 8 · 6 | 23 |
| Ciencias Naturales | 0 a 40 · 41 a 55 · 56 a 70 · 71 a 100 | 1 · 4 · 6 · 6 | 17 |
| Inglés | 0 a 36 · 37 a 57 · 58 a 70 · 71 a 100 | 2 · 2 · 4 · 3 | 11 |

## Método

1. El texto se lee del PDF con `pdftotext -raw`; no hay transcripción a mano.
2. Se quitan los rótulos de navegación que se repiten en cada página y se separa por nivel y por viñeta.
3. El programa se detiene si una prueba no tiene exactamente cuatro niveles o si sus cuatro rangos no cubren de 0 a 100 sin huecos.
4. En Matemáticas el nivel 3 ocupa dos páginas: sus descriptores se juntan en un solo nivel.

## Notas

- Erratas del PDF que se conservan: «presensentadas» (Matemáticas, nivel 2) y un paréntesis sin cerrar en el primer descriptor del nivel 3 de Matemáticas.
- Inglés: el documento define cuatro niveles (Pre A1, A1, A2, B1). El reporte de resultados por establecimiento de 2025 usa cinco (A-, A1, A2, B1, B+), con otros cortes: no son comparables entre sí.
- Cada prueba tiene sus propios cortes de puntaje.
