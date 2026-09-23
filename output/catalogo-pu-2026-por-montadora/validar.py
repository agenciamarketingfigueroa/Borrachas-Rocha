from pathlib import Path
import json, re, sys
import fitz
from PIL import Image, ImageChops, ImageDraw

HERE=Path(__file__).resolve().parent
RECALL='--revisao-02' in sys.argv
OUT=HERE/'revisao-02' if RECALL else HERE
doc=fitz.open(OUT/'Catalogo-PU-2026-Por-Montadora-A4.pdf')
press=fitz.open(OUT/'Catalogo-PU-2026-Por-Montadora-Sangria-3mm.pdf')
data=json.loads((HERE/'produtos.json').read_text())
manifest=json.loads((OUT/'conferencia.json').read_text())
original=fitz.open(json.loads((HERE/'fontes.json').read_text())['original'])
assert len(doc)==len(press)==28
assert len(data)==len(manifest['referencias'])==135
assert sum(not i['original'] for i in data)==33
assert len({i['code'] for i in data})==135
for entry in manifest['referencias']:
    assert entry['code'] in doc[entry['page']-1].get_text(),entry
for p in doc:
    assert abs(p.rect.width-595.2)<.02 and abs(p.rect.height-841.92)<.02
    assert '2024' not in p.get_text() and '2025' not in p.get_text()
assert '1013A PU' not in ''.join(p.get_text() for p in doc)
for item in data:
    if item['original']: continue
    entry=next(m for m in manifest['referencias'] if m['code']==item['code'])
    page=doc[entry['page']-1]
    visible=' '.join(''.join(chr(ch[0]) for ch in span['chars']) for span in page.get_texttrace() if span['type']==0)
    assert item['code'] in visible,('Código invisível',item['code'])
    normalized=lambda s: re.sub(r'\s+','',s)
    assert normalized(item['name']) in normalized(visible),('Descrição ausente',item['code'])
embedded={}
for p in doc:
    for font in p.get_fonts():
        if font[0] not in embedded:
            extracted=doc.extract_font(font[0]);assert extracted[3],font
            embedded[font[0]]=font[3]
links=list(doc[1].get_links());assert len(links)==15
for link in links: assert 2<=link['page']<=26
assert len(doc.get_toc())==18
bleed=3*72/25.4
for p in press:
    assert abs(p.trimbox.width-595.2)<.02 and abs(p.trimbox.height-841.92)<.02
    assert abs(p.trimbox.x0-bleed)<.02

def render(page):
    pix=page.get_pixmap(matrix=fitz.Matrix(1,1))
    return Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
assert ImageChops.difference(render(original[-1]),render(doc[-1])).getbbox() is None
coverdiff=ImageChops.difference(render(original[0]),render(doc[0]))
ImageDraw.Draw(coverdiff).rectangle((40,589,293,675),fill='black')
assert coverdiff.getbbox() is None,'Mudança na capa fora do ano'
old=[i for i in manifest['imagens'] if next(d for d in data if d['code']==i['code'])['original']]
assert min(i['effective_dpi'] for i in old)>=300
report=dict(paginas=28,fichas_originais=102,fichas_novas=33,total=135,marcas=15,
    codigos_na_pagina_correta=True,codigos_e_descricoes_novos_visiveis=True,indice_links=15,
    fontes_incorporadas=list(embedded.values()),contracapa_identica_ao_original=True,
    capa_preservada_fora_do_ano=True,sangria_mm=3,formato_mm=[209.97,297.01],
    fichas_originais_dpi_minimo=min(i['effective_dpi'] for i in old),
    pendente='1013A PU: não incluída, aguardando fotografia do usuário',
    cor='RGB, como o original; sem certificação PDF/X ou perfil CMYK')
if RECALL:
    previous=fitz.open(HERE/'Catalogo-PU-2026-Por-Montadora-A4.pdf')
    # A revisão altera somente fotografias e seu enquadramento.
    assert [p.get_text() for p in previous]==[p.get_text() for p in doc]
    recortes=[]
    for item in data:
        if item['original']: continue
        with Image.open(OUT/'recortes'/f'{item["code"]}.png') as im:
            assert im.mode=='RGBA',item['code']
            alpha=im.getchannel('A')
            assert alpha.getextrema()==(0,255),item['code']
            # Algumas saídas têm resíduo de 1/255 em um canto (0,39% de opacidade).
            # Aceita esse arredondamento, mas rejeita fundo visível nos cantos.
            assert all(alpha.getpixel(pt)<=1 for pt in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)]),item['code']
            box=alpha.point(lambda a:255 if a>16 else 0).getbbox()
            vw,vh=box[2]-box[0],box[3]-box[1]
            scale=min(91/vw,104/vh)
            recortes.append(dict(code=item['code'],visible_width_pt=round(vw*scale,2),visible_height_pt=round(vh*scale,2)))
    report.update(revisao=2,fotos_com_transparencia=len(recortes),conteudo_textual_identico=True,escala_proporcional=recortes)
(OUT/'validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
