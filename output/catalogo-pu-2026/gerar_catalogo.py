"""Gera a edição 2026 preservando as páginas do PDF fornecido pelo cliente.

Uso: python gerar_catalogo.py '/caminho/[CATÁLOGO 2025][PU][DIGITAL].pdf'
Dependências: pymupdf, pillow, reportlab. Fontes: Arial do macOS.
"""
from pathlib import Path
from io import BytesIO
import ast
import hashlib
import json
import re
import sys

import pymupdf as fitz
from PIL import Image, ImageChops
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen.canvas import Canvas

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = Path(sys.argv[1])
W, H = 595.2, 841.92
MM = 72 / 25.4
BLUE = (2 / 255, 24 / 255, 1)
RED = (190 / 255, 0, 20 / 255)
FONTS = Path('/System/Library/Fonts/Supplemental')
for name, filename in [('Arial', 'Arial.ttf'), ('Bold', 'Arial Bold.ttf'),
                       ('Black', 'Arial Black.ttf'), ('Rounded', 'Arial Rounded Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))

# Inventário conferido visualmente no original; ordem por coluna.
ORIGINAL_CODES = [
    '1020 1021 1026 1026A 1027 1030 1033 1046A 1048 1048A',
    '1050 1053 1061 1062 1065 1066 2015 2048 2048A 2049',
    '2062 2063A 2063B 2063C 2074A 2074B 2074C 2078 2078A 2081B',
    '2108 2112 2114 5007 5008 5019 5024 5025 6002 6051',
    '6052 6053 6054 7010 7010A 7012 7014 7014A 7015 7017A',
    '7019 7020 7025 7025A 7033 7037 8011 8012 8013 8024',
    '9017 9020 9022 9023 9024 9026 9027 0610 0611 0614',
    '0614A 0614B 0615 0627 0628 0630 0631 0632 0633 0805',
    '0806 0807 0813 0825 0904 0905 0906 0911 0913 0914',
    '3056 3058 5021 5022 5023 5029 9028 0828 0828A 0836',
    '0912 0912A',
]
existing = {code + ' PU' for line in ORIGINAL_CODES for code in line.split()}
raw = ast.literal_eval(re.search(r'const PU_PRODUCTS = (\[.*?\n\])',
                                (ROOT / 'catalog.js').read_text(), re.S)[1])
products = [dict(code=r[0], brand=r[1], name=r[2], application=r[3],
                 specs=r[4] if len(r) > 4 else '',
                 image=r[5] if len(r) > 5 else r[0] + '.png') for r in raw]
new = [p for p in products if p['code'] not in existing]
brand_order = ['Volkswagen', 'Mercedes', 'Iveco', 'Scania', 'Ford', 'Toyota',
               'Mitsubishi', 'Randon', 'Jost', 'Rodoviária']
new.sort(key=lambda p: (brand_order.index(p['brand']), p['code']))
assert len(new) == 34
assert len(existing) == 102
assert '0836 PU' not in {p['code'] for p in new}


def text_pdf(text, font='Black', color=(1, 1, 1)):
    """Texto vetorial recortado nos limites visíveis, sem rasterizar a fonte."""
    stream = BytesIO()
    c = Canvas(stream, pagesize=(600, 200), initialFontName='Arial')
    c.setFillColorRGB(*color)
    c.setFont(font, 100)
    c.drawString(20, 50, text)
    c.save()
    doc = fitz.open(stream=stream.getvalue(), filetype='pdf')
    pix = doc[0].get_pixmap(alpha=True)
    alpha = Image.frombytes('RGBA', (pix.width, pix.height), pix.samples).getchannel('A')
    return doc, fitz.Rect(alpha.getbbox())


def place_text(page, text, rect, font='Black', color=(1, 1, 1)):
    doc, clip = text_pdf(text, font, color)
    page.show_pdf_page(rect, doc, 0, clip=clip, keep_proportion=False)


def update_rail(page, number):
    # Atualiza apenas o ano na tarja lateral, preservando o restante do original.
    # A tarja é redesenhada porque as páginas fornecidas são imagens a 300 dpi.
    left = number % 2 == 1
    rect = fitz.Rect(13, 205, 35, 543) if left else fitz.Rect(560, 205, 582, 543)
    page.draw_rect(rect, color=None, fill=BLUE)
    stream = BytesIO()
    c = Canvas(stream, pagesize=(W, H), initialFontName='Arial')
    c.setFillColorRGB(1, 1, 1)
    c.setFont('Rounded', 13.1)
    c.translate(30.8 if left else 577.8, 314)
    c.rotate(90)
    c.drawString(0, 0, 'BORRACHAS ROCHA | CATÁLOGO 2026')
    c.save()
    overlay = fitz.open(stream=stream.getvalue(), filetype='pdf')
    page.show_pdf_page(page.rect, overlay, 0)


def paragraph(c, text, x, top, width, size, font, color=(0, 0, 0), leading=None):
    style = ParagraphStyle('item', fontName=font, fontSize=size,
                           leading=leading or size * 1.13, alignment=1,
                           textColor=color, spaceAfter=0)
    para = Paragraph(text.replace('&', '&amp;'), style)
    _, height = para.wrap(width, H)
    para.drawOn(c, x, H - top - height)
    return height


def card(c, item, x, y, width, height):
    code, brand = item['code'], item['brand']
    # Bandeira vermelha e campo branco para a marca, como no catálogo de origem.
    c.setFillColorRGB(*RED)
    p = c.beginPath()
    p.moveTo(x, H-y); p.lineTo(x+143, H-y)
    p.lineTo(x+137, H-y-17); p.lineTo(x, H-y-17); p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.rect(x+.5, H-y-16.5, 46, 16, fill=1, stroke=0)
    c.setFillColorRGB(.04, .12, .45)
    short = {'Volkswagen': 'VW', 'Mercedes': 'MB', 'Mitsubishi': 'MITSUBISHI',
             'Rodoviária': 'RODOVIÁRIA'}.get(brand, brand.upper())
    c.setFont('Bold', 6.6 if len(short)>7 else 8)
    c.drawCentredString(x+23, H-y-11.5, short)
    c.setFillColorRGB(1, 1, 1)
    c.setFont('Bold', 10.3)
    c.drawCentredString(x+94, H-y-12, code)
    image_size = 86
    if item['image']:
        image_path = ROOT / 'assets/img/Peças de PU' / item['image']
        assert image_path.exists(), image_path
        c.drawImage(str(image_path), x, H-y-24-image_size,
                    width=image_size, height=image_size,
                    preserveAspectRatio=True, anchor='c', mask='auto')
    else:
        paragraph(c, 'Imagem não<br/>disponível', x+2, y+58, 82, 7, 'Arial', (.42,.42,.42))
    tx, tw = x+94, width-94
    title_h = paragraph(c, item['name'], tx, y+23, tw, 9.1, 'Bold')
    specs = item['specs'].replace(' | ', '<br/>')
    top = y+23+title_h+6
    if specs:
        top += paragraph(c, specs, tx, top, tw, 7.6, 'Arial') + 7
    if item['application']:
        top += paragraph(c, item['application'], tx, top, tw, 8.2, 'Arial')
    assert top <= y+height-3, (code, top, y+height)


def addition_page(items, number):
    stream = BytesIO()
    c = Canvas(stream, pagesize=(W,H), initialFontName='Arial')
    c.setFillColorRGB(*BLUE); c.rect(0,0,W,H,fill=1,stroke=0)
    left = number % 2 == 1
    panel_x = 47 if left else 0
    c.setFillColorRGB(1,1,1)
    c.roundRect(panel_x,24,W-47,H-48,12,fill=1,stroke=0)
    # Suprime os cantos arredondados inferiores e externos.
    c.rect(panel_x,24,W-47,40,fill=1,stroke=0)
    c.rect(W-20 if left else 0,24,20,H-60,fill=1,stroke=0)
    c.setFillColorRGB(*BLUE); c.setFont('Rounded',13)
    c.drawCentredString(panel_x+(W-47)/2,H-49,'NOVAS REFERÊNCIAS • LINHA PU')
    c.saveState(); c.setFillColorRGB(1,1,1);c.setFont('Rounded',13.1)
    c.translate(30.8 if left else 577.8,314);c.rotate(90)
    c.drawString(0,0,'BORRACHAS ROCHA | CATÁLOGO 2026');c.restoreState()
    c.setFillColorRGB(1,1,1)
    p=c.beginPath()
    if left:
        p.moveTo(2,2);p.lineTo(58,2);p.lineTo(56,58);p.lineTo(2,98)
    else:
        p.moveTo(W-2,2);p.lineTo(W-58,2);p.lineTo(W-56,58);p.lineTo(W-2,98)
    p.close();c.drawPath(p,fill=1,stroke=0)
    c.setFillColorRGB(0,0,0);c.setFont('Arial',25)
    c.drawCentredString(28 if left else W-28,23,str(number))
    rows = (len(items)+1)//2
    cell_h = 121 if rows == 6 else 143
    x0 = panel_x+12
    for i,item in enumerate(items):
        # Leitura de cima para baixo por coluna, seguindo o PDF original.
        col,row = divmod(i,rows)
        card(c,item,x0+col*264,68+row*cell_h,250,cell_h)
    c.save()
    return fitz.open(stream=stream.getvalue(),filetype='pdf')


original = fitz.open(SOURCE)
assert len(original)==13
doc = fitz.open()
doc.insert_pdf(original, from_page=0, to_page=11)

# Capa: mesma arte; somente a área do ano recebe a atualização.
year_rect = fitz.Rect(41,590,291,672)
doc[0].draw_rect(year_rect,color=None,fill=(254/255,0,0))
place_text(doc[0],'2026',fitz.Rect(46,596,288,667),color=(.63,0,0))
place_text(doc[0],'2026',fitz.Rect(44,592,286,663))
for number in range(1,12):
    update_rail(doc[number],number)

# O PDF imprime 0912 duas vezes. A segunda é a variante de 41,5 mm,
# cadastrada no site como 0912A; corrige-se só a etiqueta dessa variante.
label=fitz.Rect(87,205,138,221)
doc[11].draw_rect(label,color=None,fill=(178/255,9/255,24/255))
place_text(doc[11],'0912A PU',fitz.Rect(89,208,134,216),font='Bold')

for i,batch in enumerate([new[:12],new[12:24],new[24:]]):
    extra=addition_page(batch,12+i)
    doc.insert_pdf(extra)
doc.insert_pdf(original,from_page=12,to_page=12)
assert len(doc)==16
doc.set_metadata(dict(title='Catálogo PU 2026 — Borrachas Rocha',
                      author='Borrachas Rocha',subject='Peças em poliuretano — edição para impressão'))
doc.set_toc([[1,'Capa',1],[1,'Catálogo de peças',2],
             [1,'Buchas do amortecedor',11],[1,'Novas referências',13],[1,'Contato',16]])
a4_path=HERE/'Catalogo-PU-2026-A4.pdf'
doc.save(a4_path,garbage=4,deflate=True)

# Versão de gráfica: 3 mm de sangria por extensão das bordas, mantendo
# escala e área de corte. Sem perfil CMYK inventado ou imposição de cadernos.
bleed=3*MM
press=fitz.open()
for i,source_page in enumerate(doc):
    page=press.new_page(width=W+2*bleed,height=H+2*bleed)
    # Extensão apenas dos 0,5 pt externos: nenhuma parte do miolo é ampliada.
    strips=[(fitz.Rect(bleed,0,W+bleed,bleed),fitz.Rect(0,0,W,.5)),
            (fitz.Rect(bleed,H+bleed,W+bleed,H+2*bleed),fitz.Rect(0,H-.5,W,H)),
            (fitz.Rect(0,bleed,bleed,H+bleed),fitz.Rect(0,0,.5,H)),
            (fitz.Rect(W+bleed,bleed,W+2*bleed,H+bleed),fitz.Rect(W-.5,0,W,H))]
    for target,clip in strips:page.show_pdf_page(target,doc,i,clip=clip,keep_proportion=False)
    for x in [0,1]:
        for y in [0,1]:
            target=fitz.Rect(0 if x==0 else W+bleed,0 if y==0 else H+bleed,
                             bleed if x==0 else W+2*bleed,bleed if y==0 else H+2*bleed)
            clip=fitz.Rect(0 if x==0 else W-.5,0 if y==0 else H-.5,
                           .5 if x==0 else W,.5 if y==0 else H)
            page.show_pdf_page(target,doc,i,clip=clip,keep_proportion=False)
    page.show_pdf_page(fitz.Rect(bleed,bleed,W+bleed,H+bleed),doc,i)
    page.set_trimbox(fitz.Rect(bleed,bleed,W+bleed,H+bleed))
    page.set_bleedbox(page.rect)
press.set_metadata(doc.metadata)
press.save(HERE/'Catalogo-PU-2026-Grafica-Sangria-3mm.pdf',garbage=4,deflate=True)

manifest=dict(original=str(SOURCE),sha256_original=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              cadastro='https://borrachasrocha.com.br/catalog.js',
              sha256_cadastro=hashlib.sha256((ROOT/'catalog.js').read_bytes()).hexdigest(),
              paginas=16,referencias_originais=102,referencias_adicionadas=34,
              referencias_por_pagina_original=ORIGINAL_CODES,novos_produtos=new,
              decisao_0836='Manter a aplicação Pajero do PDF, por instrução do cliente.',
              ajustes=['Ano da capa e das tarjas: 2026.',
                       'Segunda etiqueta 0912 PU corrigida para 0912A PU (41,5 mm).'],
              sem_foto=['1013A PU'])
(HERE/'conferencia.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
for i in [0,12,13,14]:
    doc[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(HERE/f'previa-pagina-{i+1:02}.png')
print(f'Gerados {len(doc)} páginas, {len(existing)+len(new)} referências; {len(new)} adições.')
