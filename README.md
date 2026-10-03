# Documentación MEN · Referentes curriculares transcritos

## Dónde está cada cosa

| Carpeta | Qué contiene |
|---|---|
| **`DBA/`** | Los Derechos Básicos de Aprendizaje transcritos, un archivo por asignatura, organizados por grado. |
| **`ESTANDARES/`** | Los Estándares Básicos de Competencias transcritos, un archivo por asignatura. El MEN los define por grupos de grados (1.° a 3.°, 4.° a 5.°, 6.° a 7.°, 8.° a 9.°, 10.° a 11.°), y así se organizan. |

| Asignatura | DBA | Estándares |
|---|---|---|
| Matemáticas | 1.° a 11.° | 1.° a 11.° |
| Lenguaje | 1.° a 11.° | 1.° a 11.° |
| Ciencias Naturales | 1.° a 11.° | pendiente |
| Ciencias Sociales | 1.° a 11.° | pendiente |
| Inglés | Transición a 11.° | pendiente |

Todo se transcribe desde los PDF oficiales de `fuentes/` con un programa y se verifica contra el mismo PDF.
Las demás carpetas son el soporte de ese proceso; no hace falta abrirlas para usar la transcripción.

## Proceso (soporte)

| Carpeta | Contenido |
|---|---|
| `fuentes/men/`, `fuentes/icfes/` | PDF originales del MEN y del ICFES, sin modificar. Ficha y huella digital en `fuentes/FUENTES.md`. |
| `extraccion/` | Programas que leen el PDF y producen los datos. Cualquiera puede volver a ejecutarlos y obtener lo mismo. |
| `datos/icfes/<prueba>/` | Taxonomía Saber 11°: `taxonomia.json`, `evidencias.csv`, `contenidos.csv` y `.md` de lectura. |
| `datos/<area>/` | Los mismos datos en JSON (`estandares.json`, `dba.json`), para los sistemas (ValorativoWeb, SIET, DocenteWeb). |
| `verificacion/` | Reporte por área: cuántos textos, cuántos literales, cuántos completos, confirmaciones manuales y pendientes. |
| `revision/` | Planilla para la revisión humana, página por página. |

## Proceso por documento

1. **Fuente.** El PDF original se guarda en `fuentes/men/` y se registra su huella SHA-256.
2. **Extracción.** Un programa lee el texto incrustado del PDF con la posición de cada palabra, separa
   columnas, viñetas y secciones, y asigna a cada estándar, DBA y evidencia su código, grado y página.
3. **Verificación automática.** Cada texto debe aparecer literal en el PDF (leído por otra vía) y
   terminar donde empieza el siguiente elemento. Solo se toleran diferencias tipográficas: espacios,
   cortes de palabra con guion al final de línea, ligaduras y llamadas de nota al pie en superíndice.
4. **Confirmación manual.** Lo que la máquina no puede confirmar se revisa contra la página y se
   registra con la razón en `verificacion/<area>_confirmaciones_manuales.json`.
5. **Revisión humana.** La planilla de `revision/` permite a una persona confirmar, página por
   página, que cada texto quedó bien separado y con el código correcto.
6. **Publicación.** `extraccion/publicar.py` escribe `DBA/` y `ESTANDARES/` desde los JSON verificados. Si algo
   se corrige, se corrige la extracción y se vuelve a publicar.

## Uso

Requiere Python 3, `pdftotext` (poppler-utils) y `openpyxl`.

```
python3 extraccion/matematicas_estandares.py
python3 extraccion/matematicas_dba.py
python3 extraccion/verificar.py matematicas
python3 extraccion/generar_salidas.py matematicas

python3 extraccion/icfes_matematicas.py
python3 extraccion/icfes_salidas.py matematicas

python3 extraccion/lenguaje_estandares.py
python3 extraccion/lenguaje_dba.py
python3 extraccion/verificar.py lenguaje
python3 extraccion/generar_salidas.py lenguaje

python3 extraccion/naturales_dba.py
python3 extraccion/verificar.py ciencias_naturales
python3 extraccion/publicar.py

python3 extraccion/sociales_dba.py
python3 extraccion/verificar.py ciencias_sociales


python3 extraccion/ingles_dba.py          # 6.° a 11.° y, con ingles_primaria_dba.py, Transición a 5.°
python3 extraccion/verificar.py ingles

```

`extraccion/dba_men.py` es el extractor común de los DBA del MEN (serie 2016, dos columnas por página);
cada área lo invoca con su PDF y su rango de páginas, la letra con que el PDF codifica la viñeta de las
evidencias y, si hace falta, el corte de columnas por página y el grado por numeración (cuando el
encabezado «Grado N» no está en todas las páginas).

Los defectos de tipografía del PDF que la extracción no puede resolver sola (espacios dentro de una palabra,
una ligadura «fi» que no está en el texto interno, un subíndice desplazado) se corrigen en el programa del
área con una lista explícita y quedan registrados en `datos/<area>/correcciones_tipograficas.json`.

## Códigos

- Estándares: `MAT-EBC-{grado inicial}.{grado final}-{pensamiento}-{nn}`, con PN numérico, PE espacial,
  PM métrico, PA aleatorio y PV variacional, numerados en el orden del documento.
- Estándares de Lenguaje: `LEN-EBC-{grado inicial}.{grado final}-{factor}-{nn}`, con PT producción textual,
  CI comprensión e interpretación textual, LI literatura, MC medios de comunicación y otros sistemas
  simbólicos y EC ética de la comunicación. Cada estándar tiene su enunciado identificador y sus
  subprocesos («Para lo cual,»): `LEN-EBC-…-nn-S{k}`. Según la Nota 1 del documento, el estándar
  comprende ambos.
- DBA: `{MAT|LEN}-DBA-{grado}-{nn}`; evidencias: `{MAT|LEN}-DBA-{grado}-{nn}-E{k}`.
- Saber 11° (ICFES): competencias `MAT-C{n}`, afirmaciones `MAT-A{n}`, evidencias `MAT-E{n.m}` con la
  numeración de la guía, y contenidos `MAT-CT-{EST|GEO|ALG}-{G|NG}-{nn}` (categoría, genérico o no
  genérico, orden en la figura de la guía).

## Estado

| Área | Estándares | DBA | Evidencias | Verificación |
|---|---|---|---|---|
| Matemáticas | 172 | 119 | 437 | 728 de 728 literales y completos (2 confirmados manualmente) |
| Lenguaje | 35 (con 177 subprocesos) | 88 | 333 | 633 de 633 literales y completos |
| Ciencias Naturales | — | — | — | Pendiente |
| Ciencias Sociales y Competencias Ciudadanas | — | — | — | Pendiente |
| Inglés | — | — | — | Pendiente |

| ICFES Saber 11° | Taxonomía | | | Verificación |
|---|---|---|---|---|
| Matemáticas | 3 competencias · 3 afirmaciones | 8 evidencias | 23 contenidos | 37 de 37 literales (guía 2026-2) |
| Matemáticas · niveles de desempeño | — | — | — | Pendiente: falta el PDF original |

Los ejemplos de los DBA se guardan como texto de apoyo (`ejemplo_texto_plano`). Pueden contener
fórmulas y figuras que el texto plano no reproduce, por eso no se usan como referente literal.
