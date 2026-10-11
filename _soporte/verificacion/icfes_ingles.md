# Verificación ICFES · Inglés

Fecha: 2026-10-10

## Fuente

| Archivo | SHA-256 |
|---|---|
| `fuentes/icfes/guia-orientacion-saber11-2026-2.pdf` | `9022a58a6ab2ff9d488b5c94be3392acf9da3433038de1ede3f822fa55d2eeb3` |

## Resultado

| Tipo | Elementos |
|---|---|
| Parte de la prueba, con su habilidad y descripción | 7 |
| Nivel de desempeño | 4 |

- Comprobaciones literales contra el PDF: **17 de 17** (los tres párrafos de presentación, la habilidad y descripción de cada parte, y la fila de cada parte en la tabla 32).
- Los porcentajes de las siete partes (11, 11, 11, 18, 16, 11 y 22) suman 100.
- **Leído de la imagen, no del texto:** el número de cada parte (págs. 64 y 65) y los rótulos de los niveles (figura 5) están dibujados; se tomaron de la página convertida en imagen con `pdftoppm`. La correspondencia entre número y habilidad coincide con el orden en que el texto las presenta.
- El número de opciones de respuesta de cada parte se tomó de su propia descripción.

## Diferencias con las otras pruebas

- La guía no da competencias, afirmaciones ni evidencias para Inglés: la describe por partes y por niveles.
- La guía nombra los cuatro niveles pero no los describe: remite a un «Documento de consulta».

## Pendiente

- **Marco de referencia de la prueba Inglés** y el **«Documento de consulta» de los niveles** (descriptores de Pre A1, A1, A2 y B1): no están en `fuentes/icfes/`.
- La guía dice que la prueba se alinea con los Estándares Básicos de Competencias en Lenguas Extranjeras: Inglés (ya procesados en `datos/ingles/estandares.json`). El cruce entre partes de la prueba y estándares no está hecho.
