# Documentación MEN · Referentes curriculares verificados

Fuente única de los referentes oficiales (Estándares Básicos de Competencias y Derechos Básicos de
Aprendizaje) para ValorativoWeb, SIET y cualquier otro uso de Grafimática Digital.

Ningún texto de este repositorio se transcribe a mano ni con inteligencia artificial: se extrae del PDF
oficial con un programa, se verifica contra el mismo PDF por una vía independiente y queda registrado.

## Estructura

| Carpeta | Contenido |
|---|---|
| `fuentes/men/` | PDF originales del MEN, sin modificar. Ficha y huella digital en `fuentes/FUENTES.md`. |
| `extraccion/` | Programas que leen el PDF y producen los datos. Cualquiera puede volver a ejecutarlos y obtener lo mismo. |
| `datos/<area>/` | Resultado: `estandares.json`, `dba.json` (con evidencias), versiones `.csv` para hojas de cálculo y `.md` para lectura. |
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
6. **Salidas.** CSV y Markdown se generan desde los JSON verificados. Si algo se corrige, se corrige la
   extracción y se regenera todo.

## Uso

Requiere Python 3, `pdftotext` (poppler-utils) y `openpyxl`.

```
python3 extraccion/matematicas_estandares.py
python3 extraccion/matematicas_dba.py
python3 extraccion/verificar.py matematicas
python3 extraccion/generar_salidas.py matematicas

python3 extraccion/lenguaje_estandares.py
python3 extraccion/lenguaje_dba.py
python3 extraccion/verificar.py lenguaje
python3 extraccion/generar_salidas.py lenguaje
```

`extraccion/dba_men.py` es el extractor común de los DBA del MEN (serie 2016, dos columnas por página);
cada área lo invoca con su PDF y su rango de páginas.

## Códigos

- Estándares: `MAT-EBC-{grado inicial}.{grado final}-{pensamiento}-{nn}`, con PN numérico, PE espacial,
  PM métrico, PA aleatorio y PV variacional, numerados en el orden del documento.
- Estándares de Lenguaje: `LEN-EBC-{grado inicial}.{grado final}-{factor}-{nn}`, con PT producción textual,
  CI comprensión e interpretación textual, LI literatura, MC medios de comunicación y otros sistemas
  simbólicos y EC ética de la comunicación. Cada estándar tiene su enunciado identificador y sus
  subprocesos («Para lo cual,»): `LEN-EBC-…-nn-S{k}`. Según la Nota 1 del documento, el estándar
  comprende ambos.
- DBA: `{MAT|LEN}-DBA-{grado}-{nn}`; evidencias: `{MAT|LEN}-DBA-{grado}-{nn}-E{k}`.

## Estado

| Área | Estándares | DBA | Evidencias | Verificación |
|---|---|---|---|---|
| Matemáticas | 172 | 119 | 437 | 728 de 728 literales y completos (2 confirmados manualmente) |
| Lenguaje | 35 (con 177 subprocesos) | 88 | 333 | 633 de 633 literales y completos |
| Ciencias Naturales | — | — | — | Pendiente |
| Ciencias Sociales y Competencias Ciudadanas | — | — | — | Pendiente |
| Inglés | — | — | — | Pendiente |

Los ejemplos de los DBA se guardan como texto de apoyo (`ejemplo_texto_plano`). Pueden contener
fórmulas y figuras que el texto plano no reproduce, por eso no se usan como referente literal.
