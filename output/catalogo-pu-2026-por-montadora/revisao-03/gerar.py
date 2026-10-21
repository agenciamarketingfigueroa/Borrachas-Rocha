"""Revisão 21/10/2026. Preserva capa, moldura, paleta, fontes e fichas aprovadas.
Execução: python gerar.py (PyMuPDF, Pillow, ReportLab).
"""
from pathlib import Path
from io import BytesIO
import json, html, math
import fitz
from PIL import Image, ImageDraw
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader

OUT=Path(__file__).resolve().parent
BASE=OUT.parent
ROOT=BASE.parent.parent
W,H=595.2,841.92
BLUE=(2/255,24/255,1)
RED=(.75,0,.075)
FONT_DIR=Path('C:/Windows/Fonts') if Path('C:/Windows/Fonts').exists() else Path('/System/Library/Fonts/Supplemental')
for name,win,mac in [('Arial','arial.ttf','Arial.ttf'),('Bold','arialbd.ttf','Arial Bold.ttf'),('Black','ariblk.ttf','Arial Black.ttf'),('Rounded','ARLRDBD.TTF','Arial Rounded Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT_DIR/(win if (FONT_DIR/win).exists() else mac))))
items=json.loads((OUT/'produtos.json').read_text(encoding='utf-8'))
approved=fitz.open(BASE/'revisao-02/Catalogo-PU-2026-Por-Montadora-A4.pdf')
checks=[]

def draw_img(c,file,x,y,width,height,**kwargs):
    # Otimiza antes de incorporar, sem reescrever máscaras/xrefs de um PDF pronto.
    with Image.open(file) as source:
        im=source.copy()
        im.thumbnail((max(1,round(width*450/72)),max(1,round(height*450/72))),Image.Resampling.LANCZOS)
        stream=BytesIO()
        if im.mode=='RGBA': im.save(stream,format='PNG')
        else: im.convert('RGB').save(stream,format='JPEG',quality=95)
    c.drawImage(ImageReader(stream),x,y,width=width,height=height,**kwargs)

def para(c,text,x,y,width,size=10,font='Arial',color=(0,0,0),align=0):
    p=Paragraph(text,ParagraphStyle('p',fontName=font,fontSize=size,leading=size*1.13,textColor=color,alignment=align))
    _,height=p.wrap(width,800)
    p.drawOn(c,x,H-y-height)
    return height

def logo(c,brand,x,y,w=29,h=17):
    f=BASE/'logos'/f'{brand}.png'
    if f.exists(): c.drawImage(str(f),x,H-y-h,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')
    elif brand=='Rodoviária':
        c.setFillColorRGB(*BLUE);c.setFont('Bold',3.8);c.drawCentredString(x+w/2,H-y-h/2-1.3,'RODOVIÁRIA')
    # 8027: o documento não informa fabricante; não inventar logo.

def chrome(c,page,title,subtitle):
    left=page%2==0;px=40 if left else 0
    c.setFillColorRGB(*BLUE);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColorRGB(1,1,1);c.roundRect(px,23,W-40,H-46,11,fill=1,stroke=0)
    c.rect(px,23,W-40,30,fill=1,stroke=0);c.rect(W-18 if left else 0,23,18,H-57,fill=1,stroke=0)
    c.saveState();c.setFillColorRGB(1,1,1);c.setFont('Rounded',11)
    c.translate(25 if left else W-15,288);c.rotate(90);c.drawString(0,0,'BORRACHAS ROCHA | CATÁLOGO 2026');c.restoreState()
    c.setFont('Bold',18);c.setFillColorRGB(1,1,1);c.drawCentredString(20 if left else W-20,30,str(page).zfill(2))
    x=px+14;c.setFillColorRGB(*RED);c.rect(x,H-77,527,3,fill=1,stroke=0)
    para(c,title.upper(),x,35,527,22 if len(title)<23 else 20,'Rounded',BLUE)
    para(c,subtitle,x,62,525,8,'Arial',(.3,.3,.3))
    return x

def tag(c,item,x,y):
    c.setFillColorRGB(*RED);p=c.beginPath();p.moveTo(x,H-y);p.lineTo(x+94,H-y);p.lineTo(x+89,H-y-17);p.lineTo(x,H-y-17);p.close();c.drawPath(p,fill=1,stroke=0)
    c.setFillColorRGB(1,1,1);c.rect(x+.5,H-y-16.5,29,16,fill=1,stroke=0)
    logo(c,item['brand'],x+1,y+1,27,14)
    c.setFillColorRGB(1,1,1);c.setFont('Bold',9.2);c.drawCentredString(x+59,H-y-11.5,item['code'])

def text_body(c,item,x,y):
    name=html.escape(item['name']);spec=html.escape(item.get('specs','')).replace(' | ','<br/>');app=html.escape(item.get('application',''))
    # A mesma composição foto à esquerda / descrição centralizada à direita.
    size=9.4
    while True:
        blocks=[(name,size,'Bold',0),(spec,size-.8,'Arial',5),(app,size-.5,'Arial',7)]
        heights=[]
        for text,sz,font,gap in blocks:
            if not text: heights.append(0);continue
            p=Paragraph(text,ParagraphStyle('m',fontName=font,fontSize=sz,leading=sz*1.13))
            heights.append(p.wrap(161,800)[1]+gap)
        if sum(heights)<=98: break
        size-=.15
        assert size>=7.4,(item['code'],heights)
    top=y+21
    for text,sz,font,gap in blocks:
        if text: top+=gap+para(c,text,x+96,top+gap,161,sz,font,align=1)
    checks.append(dict(code=item['code'],body_bottom=top-y,font_size=round(size,2)))

def card(c,item,x,y):
    code=item['code']
    if item['original'] and not item.get('recompose'):
        f=BASE/item['image']
        with Image.open(f) as im: iw,ih=im.size
        s=min(257/iw,118/ih,72/300);dw,dh=iw*s,ih*s
        draw_img(c,str(f),x,H-y-dh,width=dw,height=dh)
        # Mantém correções de etiqueta/título já aprovadas na revisão 02.
        if code=='0912A PU':
            c.setFillColorRGB(1,1,1);c.rect(x,H-y-19,96,19,fill=1,stroke=0);tag(c,item,x,y)
        if code in ['5021 PU','5022 PU','5023 PU','3056 PU','3058 PU']:
            factor=s/.24
            c.setFillColorRGB(1,1,1);c.rect(x+96*factor,H-y-50*factor,161*factor,33*factor,fill=1,stroke=0)
            para(c,'Bucha inferior do<br/>amortecedor dianteiro',x+98*factor,y+20*factor,157*factor,10.1*factor,'Bold',align=1)
        if code=='0633 PU':
            factor=s/.24
            c.setFillColorRGB(1,1,1);c.rect(x+96*factor,H-y-160*factor,161*factor,75*factor,fill=1,stroke=0)
            app='Iveco Daily 35-10 / 35-13 / 38-13<br/>40-12 / 40-13 / 49-10 / 49-12<br/>50-13 / 59-12 / 60-12 / 60-13<br/>70-12 / 70-13 / 35S14 / 35S14 HD<br/>40S14 / 40S16 / 45S14 / 45S16<br/>45S17 / 55C16 / 50C17 / 55C17'
            para(c,app,x+96*factor,y+87*factor,161*factor,7.8*factor,align=1)
        c.saveState();t=c.beginText(x,H-y-10);t.setFont('Arial',8);t.setTextRenderMode(3);t.textOut(code);c.drawText(t);c.restoreState()
    else:
        tag(c,item,x,y)
        if item['original']:
            # Foto recortada da ficha original pelo motor PDF, preservada sem geração.
            f=ROOT/'assets/img/Peças de PU/fotos-catalogo'/f'{code}.png'
            if not f.exists():
                src=BASE/item['image'];pix=fitz.Pixmap(str(src));d=fitz.open();pg=d.new_page(width=pix.width*.24,height=pix.height*.24);pg.insert_image(pg.rect,filename=str(src))
                pg.get_pixmap(matrix=fitz.Matrix(3,3),clip=fitz.Rect(0,20,min(94,pg.rect.width*.39),pg.rect.height)).save(f)
        elif item.get('new'):
            f=ROOT/'assets/img/Peças de PU/recortes'/f'{code}.png'
            if not f.exists(): f=ROOT/'assets/img/Peças de PU'/item['image']
        else: f=BASE/'revisao-02/recortes'/f'{code}.png'
        with Image.open(f) as im:
            iw,ih=im.size
            bounds=im.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox() if im.mode=='RGBA' else (0,0,iw,ih)
        bx,by,br,bb=bounds;vw,vh=br-bx,bb-by;s=min(91/vw,94/vh)
        vx=x+(92-vw*s)/2;vy=y+22+(96-vh*s)/2
        draw_img(c,str(f),vx-bx*s,H-(vy-by*s)-ih*s,width=iw*s,height=ih*s,mask='auto')
        text_body(c,item,x,y)
    if item.get('originalCode'):
        para(c,'Cód. original: '+html.escape(item['originalCode']),x,y+124,257,7,'Arial',(.35,.35,.35),1)
    c.setStrokeColorRGB(.88,.9,.95);c.setLineWidth(.4);c.line(x,H-y-136,x+257,H-y-136)

def codekey(item):
    code=item['code'];return (code.startswith('0'),code)

def make(kind):
    subset=[i for i in items if i['catalog']==kind]
    sections=['Volkswagen','Mercedes-Benz','Ford','Toyota','Scania','Volvo','Trucks e Carretas','Chevrolet','Iveco','Mitsubishi','Nissan'] if kind=='geral' else ['Buchas do amortecedor']
    plan=[]
    for section in sections:
        group=[i for i in subset if i['section']==section] if kind=='geral' else sorted(subset,key=codekey)
        if kind=='geral':
            if section=='Trucks e Carretas':
                order={'HBZ':0,'Rodoviária':1,'Randon':2,'Suspensys':3,'JOST':4,'Truck':5}
                group.sort(key=lambda i:(order[i['brand']],codekey(i)))
            else: group.sort(key=codekey)
        for start in range(0,len(group),10):
            plan.append(dict(section=section,items=group[start:start+10],part=start//10+1,parts=math.ceil(len(group)/10),total=len(group),page=len(plan)+(3 if kind=='geral' else 2)))
    stream=BytesIO();c=Canvas(stream,pagesize=(W,H),initialFontName='Arial')
    page_for={i['code']:p['page'] for p in plan for i in p['items']}
    if kind=='geral':
        x=chrome(c,2,'Encontre sua peça','ÍNDICE POR MONTADORA E APLICAÇÃO  •  EDIÇÃO 2026')
        para(c,'Escolha a seção. As referências estão em ordem crescente de código.',x,94,520,10)
        y=132
        for section in sections:
            pages=[p['page'] for p in plan if p['section']==section]
            if section!='Trucks e Carretas': logo(c,section,x+3,y,29,17)
            para(c,section,x+47,y,370,11,'Bold')
            label=f'{pages[0]:02}' if len(pages)==1 else f'{pages[0]:02}-{pages[-1]:02}'
            para(c,label,x+450,y,66,11,'Bold',BLUE,2)
            c.setStrokeColorRGB(.89,.91,.95);c.line(x+47,H-y-24,x+517,H-y-24);y+=38
        para(c,'APLICAÇÕES COMPARTILHADAS',x,y+22,500,9,'Bold',BLUE)
        para(c,f'DAF: consulte 6054 PU na página {page_for["6054 PU"]} e 7033 PU na página {page_for["7033 PU"]}.<br/>As variantes e suas medidas permanecem reunidas na ficha da referência principal.',x,y+42,520,9)
        para(c,'Buchas e borrachas do amortecedor estão reunidas no catálogo específico.',x,y+90,520,9)
        c.showPage()
    manifest=[]
    for p in plan:
        subtitle=f'LINHA PU  •  {p["total"]} REFERÊNCIAS'
        if p['parts']>1: subtitle+=f'  •  {p["part"]}/{p["parts"]}'
        x=chrome(c,p['page'],p['section'],subtitle)
        for j,item in enumerate(p['items']):
            col,row=j//5,j%5
            card(c,item,x+col*270,94+row*142)
            manifest.append(dict(code=item['code'],brand=item['brand'],section=p['section'],page=p['page'],slot=j+1))
        if kind=='geral' and p['section']=='Volvo' and p['part']==p['parts']:
            note_y=94+min(5,len(p['items']))*142+12
            para(c,'TAMBÉM SE APLICA A VOLVO',x,note_y,520,9,'Bold',BLUE)
            for k,(code,label) in enumerate([('8012 PU','Tensor Suspensys com pino'),('8013 PU','Tensor Suspensys sem pino')]):
                para(c,f'{code}  •  {label}  -  página {page_for[code]}',x,note_y+20+k*13,520,8.5)
        c.showPage()
    c.save();interior=fitz.open(stream=stream.getvalue(),filetype='pdf')
    doc=fitz.open();doc.insert_pdf(approved,from_page=0,to_page=0)
    if kind=='amortecedor':
        # Somente a identificação da linha muda na área azul da capa aprovada.
        cover=BytesIO();cc=Canvas(cover,pagesize=(W,H),initialFontName='Arial')
        cc.setFillColorRGB(*BLUE);cc.rect(313,H-812,264,122,fill=1,stroke=0)
        para(cc,'BUCHAS DO',314,692,258,27,'Black',(1,1,1))
        para(cc,'AMORTECEDOR',314,728,258,23,'Black',(1,1,1))
        para(cc,'LINHA PU  •  2026',314,774,258,12,'Bold',(1,1,1));cc.save()
        cd=fitz.open(stream=cover.getvalue(),filetype='pdf');doc[0].show_pdf_page(doc[0].rect,cd,0)
    doc.insert_pdf(interior);doc.insert_pdf(approved,from_page=len(approved)-1,to_page=len(approved)-1)
    toc=[[1,'Capa',1]]+([[1,'Índice',2]] if kind=='geral' else [])
    for section in sections: toc.append([1,section,next(p['page'] for p in plan if p['section']==section)])
    toc.append([1,'Contato',len(doc)]);doc.set_toc(toc)
    if kind=='geral':
        for section in sections:
            for rect in doc[1].search_for(section): doc[1].insert_link({'kind':fitz.LINK_GOTO,'from':rect,'page':next(p['page'] for p in plan if p['section']==section)-1})
    name='Catalogo-PU-2026' if kind=='geral' else 'Catalogo-Buchas-do-Amortecedor-2026'
    doc.set_metadata(dict(title=('Catálogo PU 2026' if kind=='geral' else 'Buchas do amortecedor 2026')+' | Borrachas Rocha',author='Borrachas Rocha',subject=f'Revisão 21/10/2026 - {len(subset)} referências'))
    # Limita imagens superdimensionadas a resolução de impressão, sem rasterizar texto.
    doc.save(OUT/(name+'-A4.pdf'),garbage=4,deflate=True)
    # Versão leve renderizada a 200 dpi; camada pesquisável e links preservados.
    light=fitz.open()
    for source in doc:
        page=light.new_page(width=W,height=H)
        pix=source.get_pixmap(dpi=200)
        page.insert_image(page.rect,stream=pix.tobytes('jpeg',jpg_quality=88))
        for block in source.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    page.insert_text((span['bbox'][0],min(H-3,max(8,span['bbox'][3]))),span['text'],fontsize=5,fontname='helv',render_mode=3)
    for i,source in enumerate(doc):
        for link in source.get_links():
            if link['kind']==fitz.LINK_GOTO: light[i].insert_link({'kind':fitz.LINK_GOTO,'from':link['from'],'page':link['page']})
    light.set_toc(toc);light.set_metadata(doc.metadata)
    light.save(OUT/(name+'-Clientes.pdf'),garbage=4,deflate=True)
    bleed=3*72/25.4;press=fitz.open()
    for i,source in enumerate(doc):
        pg=press.new_page(width=W+2*bleed,height=H+2*bleed)
        # A moldura azul chega à borda; a capa é estendida a partir de suas próprias bordas.
        for target,clip in [([bleed,0,W+bleed,bleed],[0,0,W,.5]),([bleed,H+bleed,W+bleed,H+2*bleed],[0,H-.5,W,H]),([0,bleed,bleed,H+bleed],[0,0,.5,H]),([W+bleed,bleed,W+2*bleed,H+bleed],[W-.5,0,W,H])]: pg.show_pdf_page(fitz.Rect(target),doc,i,clip=fitz.Rect(clip),keep_proportion=False)
        for xx in [0,1]:
            for yy in [0,1]:
                target=fitz.Rect(0 if xx==0 else W+bleed,0 if yy==0 else H+bleed,bleed if xx==0 else W+2*bleed,bleed if yy==0 else H+2*bleed)
                clip=fitz.Rect(0 if xx==0 else W-.5,0 if yy==0 else H-.5,.5 if xx==0 else W,.5 if yy==0 else H)
                pg.show_pdf_page(target,doc,i,clip=clip,keep_proportion=False)
        pg.show_pdf_page(fitz.Rect(bleed,bleed,W+bleed,H+bleed),doc,i)
        pg.set_trimbox(fitz.Rect(bleed,bleed,W+bleed,H+bleed));pg.set_bleedbox(pg.rect)
    press.set_metadata(doc.metadata);press.set_toc(toc);press.save(OUT/(name+'-Sangria-3mm.pdf'),garbage=4,deflate=True)
    (OUT/(kind+'-conferencia.json')).write_text(json.dumps(dict(paginas=len(doc),referencias=manifest),ensure_ascii=False,indent=2),encoding='utf-8')
    thumbs=[]
    preview=OUT/'previas';preview.mkdir(exist_ok=True)
    for i,pg in enumerate(doc):
        pg.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(preview/f'{kind}-{i+1:02}.png')
        pix=pg.get_pixmap(matrix=fitz.Matrix(.5,.5));thumbs.append(Image.frombytes('RGB',(pix.width,pix.height),pix.samples))
    sheet=Image.new('RGB',(4*312,math.ceil(len(doc)/4)*445),'#ddd')
    for i,im in enumerate(thumbs):
        x=i%4*312+6;y=i//4*445+5;sheet.paste(im,(x,y));ImageDraw.Draw(sheet).text((x,y+422),str(i+1),fill='black')
    sheet.save(OUT/f'{kind}-visao-geral.jpg',quality=88)
    print(kind,len(subset),'referências',len(doc),'páginas')

if __name__=='__main__':
    make('geral');make('amortecedor')
    (OUT/'conferencia-textos.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
