"""
Extrae de la Guía de orientación Saber 11° 2026-2 (PDF original del ICFES, fuentes/icfes/) la
taxonomía de la prueba de Matemáticas: competencias (con su descripción y % de preguntas),
afirmaciones, evidencias y contenidos genéricos/no genéricos, cada uno con su página.
Requiere pdftotext (poppler-utils).

Verifica que cada texto extraído aparezca literal en el PDF (leído por otra vía: el texto de la
página o de la columna completa); si alguno no aparece, se detiene sin escribir nada.

    python3 extraccion/icfes_matematicas.py
"""
import subprocess, re, sys, html
from collections import defaultdict
import os
PDF=os.environ.get('GUIA_PDF','fuentes/icfes/guia-orientacion-saber11-2026-2.pdf')
def palabras(p):
    out = subprocess.run(['pdftotext','-f',str(p),'-l',str(p),'-bbox',PDF,'-'],capture_output=True,text=True).stdout
    return [(float(a),float(b),float(c),float(d),html.unescape(w)) for a,b,c,d,w in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', out)]
def lineas(ws):
    filas = defaultdict(list)
    for w in ws: filas[round(w[1]/3)].append(w)
    return [' '.join(x[4] for x in sorted(f, key=lambda z: z[0])) for _, f in sorted(filas.items())]
def tabla(p):
    ws = palabras(p)
    hA = next(w for w in ws if w[4]=='Afirmación'); hE = next(w for w in ws if w[4]=='Evidencias')
    y0 = hA[3]
    pie = min([w[1] for w in ws if w[1]>y0 and re.fullmatch(r'\d{1,2}', w[4]) and w[0]>500] or [9999])
    cuerpo = [w for w in ws if w[1]>y0 and w[1]<pie and w[0] >= hA[0]-40]
    xa = min(w[0] for w in cuerpo if re.fullmatch(r'\d\.', w[4])) - 1
    xe = min(w[0] for w in cuerpo if re.fullmatch(r'\d\.\d+', w[4])) - 1
    cuerpo = [w for w in cuerpo if w[0] >= xa]
    afi = ' '.join(lineas([w for w in cuerpo if xa <= w[0] < xe]))
    evi = ' '.join(lineas([w for w in cuerpo if w[0] >= xe]))
    return afi, evi

import json, re, subprocess
norm=lambda s: re.sub(r'\s+',' ',s).strip()
def texto_pagina(p): return norm(subprocess.run(['pdftotext','-f',str(p),'-l',str(p),PDF,'-'],capture_output=True,text=True).stdout)

def descripcion(p):
    ws = palabras(p)
    hA = next(w for w in ws if w[4]=='Afirmación')
    tit = next(w for w in ws if w[4] in ('a.','b.','c.'))
    pie = min([w[1] for w in ws if re.fullmatch(r'\d{1,2}', w[4]) and w[0]>500 and w[1]>tit[1]] or [9999])
    izq = [w for w in ws if w[0] < hA[0]-40 and w[1] > tit[3]+2 and w[1] < pie]
    # La maquetación deja un espacio antes de algunos signos de puntuación («EBC .»): se quita
    return re.sub(r'\s+([.,;:])', r'\1', norm(' '.join(lineas(izq))))

comp = [('MAT-C1','Interpretación y representación',31,34),('MAT-C2','Formulación y ejecución',32,43),('MAT-C3','Argumentación',33,23)]
datos = {'documento': {'codigo':'ICFES-GUIA-S11-2026-2','entidad':'ICFES','titulo':'Guía de orientación del Examen Saber 11º 2026-2 (Calendario A)',
          'version':'2026-2','anio':2026,'archivo':'fuentes/icfes/guia-orientacion-saber11-2026-2.pdf'},
         'prueba':'matematicas','competencias':[], 'contenidos':[]}
for i,(cod,nombre,p,pct) in enumerate(comp, start=1):
    afi, evi = tabla(p)
    m = re.match(r'(\d)\.\s+(.*)', afi); num, afi_txt = int(m.group(1)), norm(m.group(2))
    evs = [(n, norm(t)) for n, t in re.findall(r'(\d\.\d+)\s+(.*?)(?=\s\d\.\d+\s|$)', evi)]
    datos['competencias'].append({'codigo':cod,'nombre':nombre,'descripcion':descripcion(p),'porcentaje_preguntas':pct,'orden':i,'pagina':p,
        'afirmaciones':[{'codigo':f'MAT-A{num}','numero':num,'texto':afi_txt,'pagina':p,
            'evidencias':[{'codigo':f'MAT-E{n}','numero':n,'texto':t} for n,t in evs]}]})

# Contenidos (figura 5, pp. 35–36): cada ítem va de su viñeta » a la siguiente viñeta o encabezado
def items_columna(ws):
    marcas = sorted([(w[1], 'bullet', w) for w in ws if w[4] == '»'] +
                    [(w[1], 'generico' if nxt == 'genéricos' else 'no_generico', w) for w, nxt in
                     ((w, next((v[4] for v in ws if abs(v[1]-w[1]) < 2 and v[0] > w[0]), '')) for w in ws if w[4] == 'Contenidos')
                     if nxt in ('genéricos', 'no')], key=lambda m: m[0])
    salida, tipo = [], None
    for i, (y, clase, w) in enumerate(marcas):
        if clase != 'bullet':
            tipo = clase; continue
        y_fin = marcas[i+1][0] - 3.5 if i+1 < len(marcas) else 9999
        cuerpo = [v for v in ws if v[1] >= y-3.5 and v[1] < y_fin and v[0] > w[0] + 2 and not re.fullmatch(r'\d{1,2}', v[4]) and v[4] != 'Continúa']
        texto = norm(' '.join(lineas(cuerpo)))
        texto = re.sub(r'\s*Continúa en la siguiente página.*$', '', texto)
        salida.append((tipo, texto))
    return salida
def region(p, x0, x1, y0=0, y1=2000):
    return [w for w in palabras(p) if x0 <= w[0] < x1 and y0 <= w[1] < y1]
w36 = palabras(36)
xal = next(w for w in w36 if w[4] == 'Álgebra')[0]
fin35 = next(w for w in palabras(35) if w[4] == 'Continúa')[1]
columnas = {'Estadística': (35, 0, 2000, 0, fin35), 'Geometría': (36, 0, xal - 5, 0, 2000), 'Álgebra y cálculo': (36, xal - 5, 2000, 0, 2000)}
sig = {'Estadística': 'EST', 'Geometría': 'GEO', 'Álgebra y cálculo': 'ALG'}
cortes = {}
for cat, (p, x0, x1, y0, y1) in columnas.items():
    cortes[cat] = (p, x0, x1)
    cont = {'generico': 0, 'no_generico': 0}
    for tipo, t in items_columna(region(p, x0, x1, y0, y1)):
        cont[tipo] += 1
        datos['contenidos'].append({'codigo': f"MAT-CT-{sig[cat]}-{'G' if tipo == 'generico' else 'NG'}-{cont[tipo]:02d}",
            'categoria': cat, 'tipo': tipo, 'texto': t, 'orden': cont[tipo], 'pagina': p})

# Verificación: todo texto debe aparecer literal en el texto de su página
fallas=[]
for c in datos['competencias']:
    tp = texto_pagina(c['pagina'])
    if norm(c['descripcion']) not in tp.replace('- ',''): fallas.append((c['pagina'], 'descripción', c['codigo']))
    for a in c['afirmaciones']:
        for t in [a['texto']]+[e['texto'] for e in a['evidencias']]:
            if norm(t) not in tp.replace('- ',''): fallas.append((c['pagina'],t[:60]))
def texto_columna(p, x0, x1):
    ancho = int(min(x1, 1400) - x0)
    return norm(subprocess.run(['pdftotext','-f',str(p),'-l',str(p),'-x',str(int(x0)),'-y','0','-W',str(ancho),'-H','2000',PDF,'-'],capture_output=True,text=True).stdout)
for ct in datos['contenidos']:
    p, x0, x1 = cortes[ct['categoria']]
    if not ct['texto'] or norm(ct['texto']) not in texto_columna(p, x0, x1): fallas.append((ct['pagina'], ct['categoria'], ct['texto'][:70]))
if fallas:
    raise SystemExit(f'Textos que no aparecen literales en el PDF: {fallas}')
json.dump(datos, open(os.environ.get('SALIDA','_soporte/datos/icfes/matematicas/taxonomia.json'),'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('competencias', len(datos['competencias']), 'evidencias', sum(len(a['evidencias']) for c in datos['competencias'] for a in c['afirmaciones']), 'contenidos', len(datos['contenidos']))
print('FALLAS de verificación literal:', fallas)
for c in datos['competencias']: print(c['codigo'], c['nombre'], c['porcentaje_preguntas'], '| desc:', c['descripcion'][:110])
for ct in datos['contenidos']: print(ct['codigo'], '|', ct['texto'])
