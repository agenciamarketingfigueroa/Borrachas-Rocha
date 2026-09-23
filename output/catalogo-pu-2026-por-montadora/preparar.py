"""Extrai fichas do original, preservando os pixels e dados técnicos."""
from pathlib import Path
import ast, re, json, hashlib
import fitz
from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = Path('/Users/felipefigueroa/Desktop/[CATÁLOGO 2025][PU][DIGITAL].pdf')
ASSETS = HERE / 'fichas'
LOGOS = HERE / 'logos'
ASSETS.mkdir(exist_ok=True)
LOGOS.mkdir(exist_ok=True)
previous = json.loads((ROOT/'output/catalogo-pu-2026/conferencia.json').read_text())
doc = fitz.open(SOURCE)
items = []
logos = {}

def brand(code):
    if code == '1046A': return 'HBZ'
    if code in ['8012','8013','8024']: return 'Suspensys'
    return {'10':'Volkswagen','20':'Mercedes-Benz','21':'Mercedes-Benz',
            '06':'Iveco','08':'Mitsubishi','09':'Nissan','30':'Ford',
            '50':'Toyota','60':'Scania','70':'Volvo','80':'Randon','90':'Chevrolet'}[code[:2]]

for n, codes in enumerate(previous['referencias_por_pagina_original'], 1):
    pix = doc[n].get_pixmap()
    small = Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    pix = doc[n].get_pixmap(matrix=fitz.Matrix(300/72,300/72))
    full = Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    split = 304 if n == 1 else (318 if n%2 else 297)
    cols = [(48,split),(split,590)] if n%2 else [(27,split),(split,549)]
    scans = [(50,145),(305,407)] if n%2 else [(30,120),(292,380)]
    code_list=codes.split()
    idx=0
    for col, (sx,ex) in enumerate(scans):
        rows=[y for y in range(55,790) if sum(1 for x in range(sx,ex)
              if (lambda v:v[0]>130 and v[1]<85 and v[2]<100)(small.getpixel((x,y))))>16]
        runs=[]
        for y in rows:
            if not runs or y>runs[-1][-1]+8: runs.append([y])
            else: runs[-1].append(y)
        runs=[r for r in runs if len(r)>5]
        for row,run in enumerate(runs):
            code=code_list[idx]; idx+=1
            x0,x1=cols[col]
            if code in ['8012','8013']: x0=288
            if code=='1027': x1=318
            if code=='1048A': x0=318
            if code in ['2062','7010A']: x1=315
            if code in ['2074B','7017A']: x0=315
            if code=='7019': x1=287
            if code=='7037': x0=288
            if code=='7025': x1=289
            if code=='0633': x1=551
            y0=run[0]-2
            y1=(runs[row+1][0]-3) if row+1<len(runs) else (335 if n==11 else 781)
            rect=[x0,y0,x1,y1]
            crop=full.crop(tuple(round(v*300/72) for v in rect))
            from PIL import ImageDraw
            pen=ImageDraw.Draw(crop)
            if col==0:
                # Uma ficha vizinha pode começar antes do fim dos textos;
                # limpa somente a faixa do cabeçalho vizinho, nunca o corpo.
                pen.rectangle((round((x1-x0-9)*300/72),0,crop.width,round(20*300/72)),fill='white')
            if row==4:
                # Exclui apenas os fragmentos da moldura/numeração antiga.
                if n%2 and col==0:
                    pen.rectangle((0,round((740-y0)*300/72),round((61-x0)*300/72),crop.height),fill='white')
                elif not n%2 and col==1:
                    pen.rectangle((round((537-x0)*300/72),round((769-y0)*300/72),crop.width,crop.height),fill='white')
            if code=='0633':
                for yy in range(crop.height):
                    for xx in range(round((548-x0)*300/72),crop.width):
                        rr,gg,bb=crop.getpixel((xx,yy))
                        if bb>170 and rr<100 and gg<120: crop.putpixel((xx,yy),(255,255,255))
            # Mantém 2 px brancos de margem após aparar apenas o fundo vazio.
            diff=ImageChops.difference(crop,Image.new('RGB',crop.size,'white')).convert('L')
            bbox=diff.point(lambda v:255 if v>35 else 0).getbbox()
            bbox=(max(0,bbox[0]-2),max(0,bbox[1]-2),min(crop.width,bbox[2]+2),min(crop.height,bbox[3]+2))
            crop=crop.crop(bbox)
            crop.save(ASSETS/f'{code}.png',dpi=(300,300))
            b=brand(code)
            # Campo de marca à esquerda da faixa vermelha, sem bordas.
            labelx=min(x for y in range(run[0],run[-1]+1) for x in range(sx,ex)
                       if (lambda v:v[0]>140 and v[1]<85 and v[2]<100)(small.getpixel((x,y))))
            if b not in logos:
                logo_rect=[labelx+1,run[0]+1,labelx+23,run[-1]-1]
                logo=full.crop(tuple(round(v*300/72) for v in logo_rect))
                logo.save(LOGOS/f'{b}.png',dpi=(300,300))
                logos[b]={'pagina_original':n+1,'recorte_pt':logo_rect}
            items.append(dict(code=code+' PU',brand=b,original=True,image=f'fichas/{code}.png',
                              source_page=n+1,source_rect=rect,crop_pixels=list(crop.size)))
    assert idx==len(code_list),(n,idx,len(code_list))

raw=ast.literal_eval(re.search(r'const PU_PRODUCTS = (\[.*?\n\])',(ROOT/'catalog.js').read_text(),re.S)[1])
existing={i['code'] for i in items}
for r in raw:
    if r[0] in existing or r[0]=='1013A PU': continue
    b={'Mercedes':'Mercedes-Benz','Jost':'JOST'}.get(r[1],r[1])
    items.append(dict(code=r[0],brand=b,name=r[2],application=r[3],specs=r[4] if len(r)>4 else '',
                      image=r[5] if len(r)>5 else r[0]+'.png',original=False))
assert len(items)==135 and len({i['code'] for i in items})==135
# Recortes conferidos visualmente: algumas bordas finas vermelhas se perdem
# na detecção automática, por isso as marcas usam coordenadas explícitas.
logo_clips={
 'Volkswagen':(1,[60,72,82,84]), 'HBZ':(1,[325,346,350,358]),
 'Mercedes-Benz':(2,[301,207,325,219]), 'Toyota':(4,[40,493,65,505]),
 'Scania':(4,[299,493,324,505]), 'Volvo':(5,[324,72,348,84]),
 'Randon':(6,[299,206,324,218]), 'Suspensys':(6,[299,344,324,357]),
 'Chevrolet':(7,[60,73,84,86]), 'Iveco':(7,[324,352,349,365]),
 'Mitsubishi':(8,[299,643,323,656]), 'Nissan':(9,[324,72,349,85]),
 'Ford':(10,[40,66,65,78])}
for b,(p,r) in logo_clips.items():
    doc[p].get_pixmap(matrix=fitz.Matrix(300/72,300/72),clip=fitz.Rect(r)).save(LOGOS/f'{b}.png')
    if b!='Mitsubishi':
        logo=Image.open(LOGOS/f'{b}.png').convert('RGB')
        for yy in range(logo.height):
            for xx in range(logo.width-12,logo.width):
                rr,gg,bb=logo.getpixel((xx,yy))
                if rr>110 and rr>gg*1.5 and rr>bb*1.3: logo.putpixel((xx,yy),(255,255,255))
        logo.save(LOGOS/f'{b}.png')
    logos[b]={'pagina_original':p+1,'recorte_pt':r}
(LOGOS/'JOST.svg').write_text(re.sub(r'<!DOCTYPE[^>]*>','',Path('/private/tmp/rocha-jost-logo.svg').read_text()))
svg=fitz.open(LOGOS/'JOST.svg')
svg[0].get_pixmap(matrix=fitz.Matrix(4,4)).save(LOGOS/'JOST.png')
logos['JOST']={'url':'https://service-and-parts.jost-world.com/fileadmin/templates/jostworld_t3bootstrap/images/logos/JOST_Dachmarke_Logo_mit_Flaeche.svg',
               'validacao':'Somente svg, rect e path; sem scripts, eventos ou referências externas. DTD removido.'}
(HERE/'produtos.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
(HERE/'fontes.json').write_text(json.dumps(dict(original=str(SOURCE),sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    cadastro='catalog.js',sha256_cadastro=hashlib.sha256((ROOT/'catalog.js').read_bytes()).hexdigest(),logos=logos,
    decisoes={'0836 PU':'Mitsubishi Pajero TR4 / IO, como no PDF; confirmado pelo usuário.',
              '6054 PU':'Manter em Scania e preservar aplicação DAF escrita no original; confirmado pelo usuário.',
              '1046A PU':'HBZ, como no PDF; confirmado pelo usuário.',
              '1013A PU':'Não incluir até o usuário fornecer foto.',
              '0912A PU':'Corrigir a segunda etiqueta 0912 para 0912A, variante de 41,5 mm conforme cadastro e revisão anterior.'}),ensure_ascii=False,indent=2))
print('Preparadas',len(items),'fichas; logos:',list(logos))
