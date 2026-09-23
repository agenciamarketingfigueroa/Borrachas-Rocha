"""Monta PDF por marca e versão com sangria. Python + PyMuPDF/Pillow/ReportLab."""
from pathlib import Path
from io import BytesIO
import json, math, html, sys
import fitz
from PIL import Image, ImageDraw
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
RECALL='--revisao-02' in sys.argv
OUT=HERE/'revisao-02' if RECALL else HERE
OUT.mkdir(exist_ok=True)
W,H=595.2,841.92
BLUE=(2/255,24/255,1)
RED=(.75,0,.075)
FONTS=Path('/System/Library/Fonts/Supplemental')
for name,file in [('Arial','Arial.ttf'),('Bold','Arial Bold.ttf'),('Black','Arial Black.ttf'),('Rounded','Arial Rounded Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTS/file)))
items=json.loads((HERE/'produtos.json').read_text())
brands=['Chevrolet','Ford','Iveco','Mercedes-Benz','Mitsubishi','Nissan','Scania','Toyota','Volkswagen','Volvo',
        'HBZ','JOST','Randon','Rodoviária','Suspensys']
groups={b:sorted([i for i in items if i['brand']==b],key=lambda i:i['code']) for b in brands}
plan=[]
for b in brands:
    count=math.ceil(len(groups[b])/8)
    size,extra=divmod(len(groups[b]),count)
    offset=0
    for j in range(count):
        n=size+(j<extra)
        plan.append(dict(brand=b,items=groups[b][offset:offset+n],part=j+1,parts=count,page=len(plan)+3))
        offset+=n
page_for={i['code']:p['page'] for p in plan for i in p['items']}
manifest=[]
checks=[]

def para(c,text,x,y,width,size=10,font='Arial',color=(0,0,0),align=0):
    p=Paragraph(text,ParagraphStyle('p',fontName=font,fontSize=size,leading=size*1.13,textColor=color,alignment=align))
    _,height=p.wrap(width,800)
    p.drawOn(c,x,H-y-height)
    return height

def brand_logo(c,b,x,y,w=29,h=17):
    f=HERE/'logos'/f'{b}.png'
    if f.exists(): c.drawImage(str(f),x,H-y-h,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')
    else:
        c.setFillColorRGB(.12,.16,.4);c.setFont('Bold',4.8);c.drawCentredString(x+w/2,H-y-h/2-1.8,'RODOVIÁRIA')

def chrome(c,page,title,subtitle):
    # Faixa na borda externa; páginas pares têm faixa à esquerda.
    left=page%2==0
    px=40 if left else 0
    c.setFillColorRGB(*BLUE);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColorRGB(1,1,1);c.roundRect(px,23,W-40,H-46,11,fill=1,stroke=0)
    c.rect(px,23,W-40,30,fill=1,stroke=0)
    c.rect(W-18 if left else 0,23,18,H-57,fill=1,stroke=0)
    c.saveState();c.setFillColorRGB(1,1,1);c.setFont('Rounded',11)
    c.translate(25 if left else W-15,288);c.rotate(90)
    c.drawString(0,0,'BORRACHAS ROCHA | CATÁLOGO 2026');c.restoreState()
    c.setFont('Bold',18);c.setFillColorRGB(1,1,1)
    c.drawCentredString(20 if left else W-20,30,str(page).zfill(2))
    x=px+14
    c.setFillColorRGB(*RED);c.rect(x,H-77,527,3,fill=1,stroke=0)
    para(c,title.upper(),x,35,465,22,'Rounded',BLUE)
    para(c,subtitle,x,62,525,8,'Arial',(.3,.3,.3))
    return x

def tag(c,item,x,y):
    c.setFillColorRGB(*RED)
    path=c.beginPath();path.moveTo(x,H-y);path.lineTo(x+94,H-y);path.lineTo(x+89,H-y-17);path.lineTo(x,H-y-17);path.close()
    c.drawPath(path,fill=1,stroke=0)
    c.setFillColorRGB(1,1,1);c.rect(x+.5,H-y-16.5,29,16,fill=1,stroke=0)
    brand_logo(c,item['brand'],x+1,y+1,27,14)
    c.setFillColorRGB(1,1,1);c.setFont('Bold',9.2);c.drawCentredString(x+59,H-y-11.5,item['code'])

def card(c,item,x,y):
    width,height=257,160
    if item['original']:
        file=HERE/item['image']
        with Image.open(file) as im: iw,ih=im.size
        # Não aumentar além da escala original. O original é uma imagem a 300 dpi.
        scale=min(width/iw,height/ih,72/300)
        dw,dh=iw*scale,ih*scale
        c.drawImage(str(file),x,H-y-dh,width=dw,height=dh)
        # Corrige somente a etiqueta duplicada no original.
        if item['code']=='0912A PU':
            c.setFillColorRGB(1,1,1);c.rect(x,H-y-19,96,19,fill=1,stroke=0)
            tag(c,item,x,y)
        # O título já vinha truncado nestas três fichas; restaura o texto
        # completo confirmado no cadastro, preservando foto, medidas e aplicação.
        if item['code'] in ['5021 PU','5022 PU','5023 PU']:
            c.setFillColorRGB(1,1,1);c.rect(x+96,H-y-48,160,31,fill=1,stroke=0)
            para(c,'Bucha inferior do<br/>amortecedor dianteiro',x+98,y+20,157,10.1,'Bold',align=1)
        if item['code']=='0633 PU':
            # A aplicação encostava na faixa azul no original; mesma lista,
            # recomposta dentro da ficha para tornar todas as letras legíveis.
            c.setFillColorRGB(1,1,1);c.rect(x+96,H-y-160,161,75,fill=1,stroke=0)
            application=('Iveco Daily 35-10 / 35-13 / 38-13<br/>'
                '40-12 / 40-13 / 49-10 / 49-12<br/>'
                '50-13 / 59-12 / 60-12 / 60-13<br/>'
                '70-12 / 70-13 / 35S14 / 35S14 HD<br/>'
                '40S14 / 40S16 / 45S14 / 45S16<br/>'
                '45S17 / 55C16 / 50C17 / 55C17')
            para(c,application,x+96,y+87,161,7.8,'Arial',align=1)
        c.saveState()
        text=c.beginText(x+36,H-y-10);text.setFont('Arial',8);text.setTextRenderMode(3);text.textOut(item['code']);c.drawText(text)
        c.restoreState()
        checks.append(dict(code=item['code'],effective_dpi=round(72/scale,1),height_pt=round(dh,1)))
    else:
        tag(c,item,x,y)
        if RECALL:
            file=OUT/'recortes'/f'{item["code"]}.png'
            with Image.open(file) as im:
                assert im.mode=='RGBA',(item['code'],'Recorte sem transparência')
                iw,ih=im.size
                bounds=im.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox()
            assert bounds,(item['code'],'Imagem vazia')
            bx,by,br,bb=bounds
            visible_w,visible_h=br-bx,bb-by
            # Dimensiona pelo produto visível, não pelas margens do arquivo.
            # Caixa comum próxima às fotos antigas; sem deformar a peça.
            s=min(91/visible_w,104/visible_h)
            vx=x+(92-visible_w*s)/2
            vy=y+27+(108-visible_h*s)/2
            c.drawImage(str(file),vx-bx*s,H-(vy-by*s)-ih*s,width=iw*s,height=ih*s,mask='auto')
        else:
            file=ROOT/'assets/img/Peças de PU'/item['image']
            with Image.open(file) as im: iw,ih=im.size
            s=min(87/iw,96/ih)
            c.drawImage(str(file),x+(87-iw*s)/2,H-y-29-ih*s,width=iw*s,height=ih*s,mask='auto')
        tx,tw=x+96,161
        bottom=y+23+para(c,html.escape(item['name']),tx,y+23,tw,10.3,'Bold',align=1)
        if item['specs']:
            bottom+=7
            bottom+=para(c,html.escape(item['specs']).replace(' | ','<br/>'),tx,bottom,tw,9,'Arial',align=1)
        if item['application']:
            bottom+=9
            bottom+=para(c,html.escape(item['application']),tx,bottom,tw,9.3,'Arial',align=1)
        assert bottom<=y+height,(item['code'],bottom-y)
        checks.append(dict(code=item['code'],effective_dpi=round(72/s,1),height_pt=round(bottom-y,1)))
    c.setStrokeColorRGB(.88,.9,.95);c.setLineWidth(.4);c.line(x,H-y-height-4,x+width,H-y-height-4)

refs={
 'Ford':[('0911 PU','Ranger 2012 em diante'),('9027 PU','F250'),('8012 PU','Tensor Suspensys com pino'),('8013 PU','Tensor Suspensys sem pino')],
 'Mercedes-Benz':[('1030 PU','Calço de molas • Accelo'),('8012 PU','Tensor Suspensys com pino'),('8013 PU','Tensor Suspensys sem pino')],
 'Volkswagen':[('8012 PU','Tensor Suspensys com pino'),('8013 PU','Tensor Suspensys sem pino')],
 'Volvo':[('8012 PU','Tensor Suspensys com pino'),('8013 PU','Tensor Suspensys sem pino')]
}

stream=BytesIO();c=Canvas(stream,pagesize=(W,H),initialFontName='Arial')
x=chrome(c,2,'Encontre sua peça','ÍNDICE POR MONTADORA E FABRICANTE  •  EDIÇÃO 2026')
para(c,'Escolha a marca. Dentro de cada seção, consulte as peças em ordem de código.',x,94,520,10)
y=131
for section,bs in [('MONTADORAS',brands[:10]),('IMPLEMENTOS E COMPONENTES',brands[10:])]:
    para(c,section,x,y,500,10,'Bold',BLUE);y+=24
    for b in bs:
        pages=[p['page'] for p in plan if p['brand']==b]
        label=str(pages[0]).zfill(2) if len(pages)==1 else f'{pages[0]:02}–{pages[-1]:02}'
        brand_logo(c,b,x+3,y,29,17)
        para(c,b,x+47,y,340,11,'Bold')
        para(c,label,x+450,y,66,11,'Bold',BLUE,2)
        c.setStrokeColorRGB(.89,.91,.95);c.line(x+47,H-y-21,x+517,H-y-21)
        y+=29
    y+=18
para(c,'APLICAÇÕES COMPARTILHADAS',x,y,500,9,'Bold',BLUE);y+=18
para(c,f'DAF: consulte 6054 PU na página {page_for["6054 PU"]} e 7033 PU na página {page_for["7033 PU"]}.<br/>'
       'Outras aplicações compartilhadas estão indicadas nas respectivas seções.<br/>'
       'As variantes e suas medidas permanecem reunidas na ficha da referência principal.',x,y,520,9)
c.showPage()

for p in plan:
    b=p['brand'];subset=p['items']
    subtitle=f'LINHA PU  •  {len(groups[b])} REFERÊNCIAS'
    if p['parts']>1: subtitle+=f'  •  {p["part"]}/{p["parts"]}'
    if b in brands[10:]: subtitle='IMPLEMENTOS E COMPONENTES  •  LINHA PU'
    x=chrome(c,p['page'],b,subtitle)
    for j,item in enumerate(subset):
        col,row=j%2,j//2
        card(c,item,x+col*270,101+row*172)
        manifest.append(dict(code=item['code'],brand=b,page=p['page'],source='PDF 2025' if item['original'] else 'catalog.js'))
    notes=refs.get(b,[]) if p['part']==p['parts'] else []
    if notes:
        note_y=101+math.ceil(len(subset)/2)*172+8
        assert note_y+26+len(notes)*13<811
        para(c,'TAMBÉM SE APLICA A '+b.upper(),x,note_y,520,9,'Bold',BLUE)
        for k,(code,app) in enumerate(notes):
            para(c,f'{code}  •  {app}  —  página {page_for[code]}',x,note_y+20+k*13,520,8.5)
    c.showPage()
c.save()
interior=fitz.open(stream=stream.getvalue(),filetype='pdf')
original=fitz.open(json.loads((HERE/'fontes.json').read_text())['original'])
doc=fitz.open();doc.insert_pdf(original,from_page=0,to_page=0)
# Arte original da capa; ano vetorial nas mesmas posições da revisão anterior.
doc[0].draw_rect(fitz.Rect(41,590,291,672),color=None,fill=(254/255,0,0))
year=BytesIO();yc=Canvas(year,pagesize=(W,H),initialFontName='Arial')
yc.setFont('Black',89)
yc.setFillColorRGB(.63,0,0);yc.drawString(44,179,'2026')
yc.setFillColorRGB(1,1,1);yc.drawString(42,182,'2026');yc.save()
yd=fitz.open(stream=year.getvalue(),filetype='pdf');doc[0].show_pdf_page(doc[0].rect,yd,0)
doc.insert_pdf(interior);doc.insert_pdf(original,from_page=len(original)-1,to_page=len(original)-1)
assert len(doc)==len(plan)+3
doc.set_metadata(dict(title='Catálogo PU 2026 por montadora | Borrachas Rocha',author='Borrachas Rocha',subject='135 referências • índice por marca • edição 2026'))
toc=[[1,'Capa',1],[1,'Índice por marca',2]]
for b in brands:
    pages=[p['page'] for p in plan if p['brand']==b]
    toc.append([1,b,pages[0]])
toc.append([1,'Contato',len(doc)])
doc.set_toc(toc)
# Links internos no índice, preservados na versão digital.
for b in brands:
    for rect in doc[1].search_for(b):
        doc[1].insert_link({'kind':fitz.LINK_GOTO,'from':rect,'page':min(p['page'] for p in plan if p['brand']==b)-1})
out=OUT/'Catalogo-PU-2026-Por-Montadora-A4.pdf'
doc.save(out,garbage=4,deflate=True)

bleed=3*72/25.4
press=fitz.open()
for i,source in enumerate(doc):
    pg=press.new_page(width=W+2*bleed,height=H+2*bleed)
    for target,clip in [
        ([bleed,0,W+bleed,bleed],[0,0,W,.5]),
        ([bleed,H+bleed,W+bleed,H+2*bleed],[0,H-.5,W,H]),
        ([0,bleed,bleed,H+bleed],[0,0,.5,H]),
        ([W+bleed,bleed,W+2*bleed,H+bleed],[W-.5,0,W,H])]:
        pg.show_pdf_page(fitz.Rect(target),doc,i,clip=fitz.Rect(clip),keep_proportion=False)
    for xx in [0,1]:
        for yy in [0,1]:
            target=fitz.Rect(0 if xx==0 else W+bleed,0 if yy==0 else H+bleed,bleed if xx==0 else W+2*bleed,bleed if yy==0 else H+2*bleed)
            clip=fitz.Rect(0 if xx==0 else W-.5,0 if yy==0 else H-.5,.5 if xx==0 else W,.5 if yy==0 else H)
            pg.show_pdf_page(target,doc,i,clip=clip,keep_proportion=False)
    pg.show_pdf_page(fitz.Rect(bleed,bleed,W+bleed,H+bleed),doc,i)
    pg.set_trimbox(fitz.Rect(bleed,bleed,W+bleed,H+bleed));pg.set_bleedbox(pg.rect)
press.set_metadata(doc.metadata);press.set_toc(toc)
press.save(OUT/'Catalogo-PU-2026-Por-Montadora-Sangria-3mm.pdf',garbage=4,deflate=True)
(OUT/'conferencia.json').write_text(json.dumps(dict(paginas=len(doc),referencias=manifest,pendentes=['1013A PU'],imagens=checks),ensure_ascii=False,indent=2))
thumbs=[]
for i,pg in enumerate(doc):
    pix=pg.get_pixmap(matrix=fitz.Matrix(.6,.6))
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    thumbs.append(im)
    if i in [0,1,3,4,12,16,18,23,25]: pg.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(OUT/f'previa-{i+1:02}.png')
sheet=Image.new('RGB',(4*378,math.ceil(len(doc)/4)*532),'#e2e2e2');draw=ImageDraw.Draw(sheet)
for i,im in enumerate(thumbs):
    x=(i%4)*378+10;y=(i//4)*532+5;sheet.paste(im,(x,y));draw.text((x,y+508),f'{i+1:02}',fill='black')
sheet.save(OUT/'visao-geral.jpg',quality=85)
print('Gerados',len(doc),'páginas e',len(manifest),'referências. A4:',round(out.stat().st_size/1024/1024,1),'MB')
