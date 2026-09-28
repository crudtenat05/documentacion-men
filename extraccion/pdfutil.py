"""Utilidades comunes: lectura de palabras con su posición (pdftotext -bbox) y normalización.

La normalización solo deshace efectos tipográficos del PDF (ligaduras como «ﬁ», espacios repetidos);
nunca cambia palabras.
"""
import html
import re
import subprocess
import unicodedata


def palabras(pdf, pagina):
    """Palabras de una página como tuplas (x0, y0, x1, y1, texto)."""
    out = subprocess.run(['pdftotext', '-f', str(pagina), '-l', str(pagina), '-bbox', pdf, '-'],
                         capture_output=True, text=True, check=True).stdout
    return [(float(a), float(b), float(c), float(d), html.unescape(w))
            for a, b, c, d, w in re.findall(
                r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', out)]


def tipografia(s):
    """Deshace ligaduras y caracteres de compatibilidad (ﬁ → fi) sin tocar tildes ni signos."""
    return unicodedata.normalize('NFC', unicodedata.normalize('NFKC', s))


def lineas(ws, tolerancia=3.0):
    """Agrupa palabras en líneas por su coordenada vertical y las ordena de izquierda a derecha."""
    ws = sorted(ws, key=lambda w: (w[1], w[0]))
    filas = []
    for w in ws:
        if filas and abs(filas[-1][0] - w[1]) <= tolerancia:
            filas[-1][1].append(w)
        else:
            filas.append([w[1], [w]])
    return [(y, sorted(f, key=lambda z: z[0])) for y, f in filas]


def unir_lineas(textos):
    """Une líneas de un mismo párrafo. Un guion al final de línea seguido de minúscula es corte de
    palabra y se elimina; cualquier otro guion se conserva. Devuelve (texto, cortes) donde cortes
    lista las palabras reconstruidas para revisión humana."""
    texto, cortes = '', []
    for t in textos:
        t = t.strip()
        if not t:
            continue
        if texto.endswith('-') and t[:1].islower() and not texto.endswith(' -'):
            previa = texto.rsplit(' ', 1)[-1]
            texto = texto[:-1] + t
            cortes.append(previa[:-1] + t.split(' ', 1)[0])
        else:
            texto = (texto + ' ' + t) if texto else t
    return re.sub(r'\s+', ' ', texto).strip(), cortes


def texto_plano(pdf, primera=None, ultima=None):
    """Texto completo (o de un rango de páginas) para verificar coincidencias literales."""
    args = ['pdftotext']
    if primera:
        args += ['-f', str(primera)]
    if ultima:
        args += ['-l', str(ultima)]
    return subprocess.run(args + [pdf, '-'], capture_output=True, text=True, check=True).stdout


def texto_linea(fila, pegado=0.8):
    """Texto de una línea de palabras. Dos fragmentos sin separación horizontal (por ejemplo, una
    palabra partida en la ligadura «ﬁ») se unen sin espacio."""
    out = ''
    for i, w in enumerate(fila):
        if i and w[0] - fila[i - 1][2] > pegado:
            out += ' '
        out += w[4]
    return out
