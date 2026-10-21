"""Edição final: ordem aprovada, 15 inclusões, exclusão 7036 e foto 0616 corrigida."""
from pathlib import Path
from io import BytesIO
import sys, json, math, html, importlib.util

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'tmp/pdf-final-deps'))
import fitz
from PIL import Image, ImageDraw, ImageOps
spec=importlib.util.spec_from_file_location('base_final',OUT.parent/'revisao-03/gerar.py')
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

PDF=ROOT/'output/pdf'
ORDER=json.loads((OUT.parent/'revisao-04/ordem-diretoria.json').read_text(encoding='utf-8'))
for line in ORDER: line['codes']=[c for c in line['codes'] if c!='7036']
DATA={i['code'].split()[0]:i for i in base.items if i['catalog']=='geral'}
for code,oem in json.loads((OUT.parent/'revisao-04/codigos-originais-fichas.json').read_text(encoding='utf-8')).items():
    DATA[code]['originalCode']=oem
NEW=json.loads((OUT/'novas-fichas.json').read_text(encoding='utf-8'))
DATA.update({i['code'].split()[0]:i for i in NEW})
DATA['0616']['photoOverride']='revisao-02/recortes/0616A PU.png'
BRANDS=['Volkswagen','Mercedes-Benz','Ford','Toyota','Scania / DAF','Volvo / Scania / DAF',
        'Trucks e Carretas','Chevrolet','Iveco','Mitsubishi','Nissan']
REQUESTED=[c for line in ORDER for c in line['codes']]
assert len(REQUESTED)==len(set(REQUESTED))==141
assert all(c in DATA for c in REQUESTED)
original_para=base.para
def para(c,text,x,y,width,size=10,font='Arial',color=(0,0,0),align=0):
    if text.startswith('Cód. original:'): size,font,color=9,'Bold',(0,0,0)
    return original_para(c,text,x,y,width,size,font,color,align)
base.para=para
original_logo=base.logo
def logo(c,brand,x,y,w=29,h=17):
    if brand=='DAF':
        c.setFillColorRGB(*base.BLUE);c.setFont('Bold',7)
        c.drawCentredString(x+w/2,base.H-y-h/2-2.5,'DAF')
    else: original_logo(c,brand,x,y,w,h)
base.logo=logo

# Enquadramento no PDF das fotografias originais; nenhum produto é redesenhado.
# Coordenadas normalizadas da área fotográfica, com margem em torno de cada peça.
FRAMES={
 '2062B':(.14,.12,.80,.83),'2081C':(.19,.16,.80,.90),'2119':(.13,.15,.85,.86),
 '8010':(.08,.22,.90,.84),'2066':(.26,.25,.74,.76),'0613':(.20,.20,.78,.82),
 '2068':(.20,.28,.80,.77),'2051':(.24,.24,.76,.78),'7034':(.20,.24,.80,.81),
 '1056':(.23,.25,.77,.79),'2065':(.23,.27,.77,.80),'7038':(.22,.25,.76,.79),
 '6056':(.20,.22,.78,.80),'7039':(.24,.22,.72,.90),'7035':(.15,.18,.81,.84),
}
checks=[]
def draw_photo(c,file,x,y,width,height):
    # Respeita a orientação registrada pela câmera antes da incorporação ao PDF.
    with Image.open(file) as source:
        im=ImageOps.exif_transpose(source).convert('RGB')
        im.thumbnail((round(width*450/72),round(height*450/72)),Image.Resampling.LANCZOS)
        stream=BytesIO();im.save(stream,format='JPEG',quality=95)
    c.drawImage(ImageReader(stream),x,y,width=width,height=height)

def new_body(c,item,x,y):
    escape=lambda s:html.escape(s).replace(' | ','<br/>')
    blocks=[(escape(item['name']),'Bold',0),(escape(item['specs']),'Arial',4),
            (escape(item['application']),'Arial',5)]
    if item.get('secondTitle'):
        blocks += [(escape(item['secondTitle']),'Bold',8),(escape(item['secondApplication']),'Arial',4)]
    blocks=[b for b in blocks if b[0]]
    size=9.4
    while True:
        measured=[]
        for text,font,gap in blocks:
            sz=size if font=='Bold' else size-.4
            p=Paragraph(text,ParagraphStyle('measure',fontName=font,fontSize=sz,leading=sz*1.13))
            measured.append(p.wrap(161,800)[1]+gap)
        if sum(measured)<=99: break
        size-=.1
        assert size>=7.7,(item['code'],measured)
    top=y+21
    for text,font,gap in blocks:
        top+=gap
        top+=para(c,text,x+96,top,161,size if font=='Bold' else size-.4,font,align=1)
    checks.append(dict(code=item['code'],body_bottom=round(top-y,2),font_size=round(size,2)))
    assert top<=y+121,item['code']

def card(c,item,x,y):
    code=item['code'].split()[0]
    if code not in FRAMES and not item.get('photoOverride'):
        return base.card(c,item,x,y)
    base.tag(c,item,x,y)
    if item.get('photoOverride'):
        f=OUT.parent/item['photoOverride']
        with Image.open(f) as im:
            iw,ih=im.size
            bounds=im.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox() if im.mode=='RGBA' else (0,0,iw,ih)
        bx,by,br,bb=bounds
        vw,vh=br-bx,bb-by
        s=min(91/vw,94/vh)
        vx=x+(92-vw*s)/2;vy=y+22+(96-vh*s)/2
        base.draw_img(c,str(f),vx-bx*s,base.H-(vy-by*s)-ih*s,width=iw*s,height=ih*s,mask='auto')
    else:
        f=ROOT/'assets/img/Peças de PU'/item['image']
        with Image.open(f) as im: iw,ih=im.size
        l,t,r,b=FRAMES[code]
        vw,vh=iw*(r-l),ih*(b-t)
        s=min(91/vw,94/vh)
        dw,dh=vw*s,vh*s
        vx=x+(92-dw)/2;vy=y+22+(96-dh)/2
        c.saveState()
        clip=c.beginPath();clip.rect(vx,base.H-vy-dh,dw,dh)
        c.clipPath(clip,stroke=0,fill=0)
        draw_photo(c,str(f),vx-iw*l*s,base.H-vy-ih*(1-t)*s,width=iw*s,height=ih*s)
        c.restoreState()
    new_body(c,item,x,y)
    if item.get('originalCode'):
        para(c,'Cód. original: '+html.escape(item['originalCode']),x,y+124,257,align=1)
    c.setStrokeColorRGB(.88,.9,.95);c.setLineWidth(.4)
    c.line(x,base.H-y-136,x+257,base.H-y-136)

def export_versions(doc,toc):
    name='Catalogo-PU-2026-Final'
    doc.save(PDF/(name+'-A4.pdf'),garbage=4,deflate=True)
    light=fitz.open()
    for source in doc:
        page=light.new_page(width=base.W,height=base.H)
        pix=source.get_pixmap(dpi=170)
        page.insert_image(page.rect,stream=pix.tobytes('jpeg',jpg_quality=88))
        for block in source.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    page.insert_text((span['bbox'][0],min(base.H-3,max(8,span['bbox'][3]))),span['text'],fontsize=5,fontname='helv',render_mode=3)
    for i,source in enumerate(doc):
        for link in source.get_links():
            if link['kind']==fitz.LINK_GOTO:
                light[i].insert_link({'kind':fitz.LINK_GOTO,'from':link['from'],'page':link['page']})
    light.set_toc(toc);light.set_metadata(doc.metadata)
    light.save(PDF/(name+'-Clientes.pdf'),garbage=4,deflate=True)
    bleed=3*72/25.4;press=fitz.open();W,H=base.W,base.H
    for i,source in enumerate(doc):
        pg=press.new_page(width=W+2*bleed,height=H+2*bleed)
        for target,clip in [([bleed,0,W+bleed,bleed],[0,0,W,.5]),([bleed,H+bleed,W+bleed,H+2*bleed],[0,H-.5,W,H]),([0,bleed,bleed,H+bleed],[0,0,.5,H]),([W+bleed,bleed,W+2*bleed,H+bleed],[W-.5,0,W,H])]:
            pg.show_pdf_page(fitz.Rect(target),doc,i,clip=fitz.Rect(clip),keep_proportion=False)
        for xx in [0,1]:
            for yy in [0,1]:
                target=fitz.Rect(0 if xx==0 else W+bleed,0 if yy==0 else H+bleed,bleed if xx==0 else W+2*bleed,bleed if yy==0 else H+2*bleed)
                clip=fitz.Rect(0 if xx==0 else W-.5,0 if yy==0 else H-.5,.5 if xx==0 else W,.5 if yy==0 else H)
                pg.show_pdf_page(target,doc,i,clip=clip,keep_proportion=False)
        pg.show_pdf_page(fitz.Rect(bleed,bleed,W+bleed,H+bleed),doc,i)
        pg.set_trimbox(fitz.Rect(bleed,bleed,W+bleed,H+bleed));pg.set_bleedbox(pg.rect)
    press.set_metadata(doc.metadata);press.set_toc(toc)
    press.save(PDF/(name+'-Sangria-3mm.pdf'),garbage=4,deflate=True)

def main():
    plan=[]
    for line,brand in zip(ORDER,BRANDS):
        for start in range(0,len(line['codes']),10):
            plan.append(dict(line=line['line'],brand=brand,codes=line['codes'][start:start+10],
                             part=start//10+1,parts=math.ceil(len(line['codes'])/10),page=len(plan)+3))
    page_for={code:p['page'] for p in plan for code in p['codes']}
    stream=BytesIO();c=base.Canvas(stream,pagesize=(base.W,base.H),initialFontName='Arial')
    x=base.chrome(c,2,'Encontre sua peça','ÍNDICE POR LINHA E APLICAÇÃO  |  EDIÇÃO 2026')
    para(c,'141 referências de PU',x,94,520,11,'Bold')
    para(c,'Leia de cima para baixo na coluna esquerda e depois na direita.',x,116,520,9)
    y=152
    for line,brand in zip(ORDER,BRANDS):
        pages=[p['page'] for p in plan if p['line']==line['line']]
        label=f'{pages[0]:02}' if len(pages)==1 else f'{pages[0]:02}-{pages[-1]:02}'
        para(c,'Linha '+line['line']+' - '+brand,x,y,440,11,'Bold')
        para(c,label,x+450,y,66,11,'Bold',base.BLUE,2)
        c.setStrokeColorRGB(.89,.91,.95);c.line(x,base.H-y-24,x+517,base.H-y-24);y+=38
    para(c,'APLICAÇÕES COMPARTILHADAS',x,y+18,520,10,'Bold',base.BLUE)
    para(c,f'DAF: 6054 PU na página {page_for["6054"]}; 7033 PU e 7038 PU na página {page_for["7038"]}.',x,y+40,520,9)
    para(c,'As variantes e suas medidas estão reunidas na ficha da referência principal.<br/>Buchas do amortecedor: consulte o catálogo específico.',x,y+68,520,9)
    c.showPage();manifest=[]
    for p in plan:
        x=base.chrome(c,p['page'],p['brand'],f'LINHA PU  |  LINHA {p["line"]}  |  {p["part"]}/{p["parts"]}')
        for j,code in enumerate(p['codes']):
            card(c,DATA[code],x+270*(j//5),94+142*(j%5))
            manifest.append(dict(code=code,line=p['line'],page=p['page'],slot=j+1))
        if p['line']=='7000' and p['part']==p['parts']:
            para(c,f'Também se aplica a Volvo: 8012 PU e 8013 PU - página {page_for["8012"]}.',x,803,520,8)
        c.showPage()
    c.save();doc=fitz.open()
    doc.insert_pdf(base.approved,from_page=0,to_page=0)
    interior=fitz.open(stream=stream.getvalue(),filetype='pdf');doc.insert_pdf(interior)
    doc.insert_pdf(base.approved,from_page=len(base.approved)-1,to_page=len(base.approved)-1)
    toc=[[1,'Capa',1],[1,'Índice',2]]
    for line,brand in zip(ORDER,BRANDS):
        label='Linha '+line['line'];page=next(p['page'] for p in plan if p['line']==line['line'])
        toc.append([1,label+' - '+brand,page])
        for rect in doc[1].search_for(label): doc[1].insert_link({'kind':fitz.LINK_GOTO,'from':rect,'page':page-1})
    toc.append([1,'Contato',len(doc)]);doc.set_toc(toc)
    doc.set_metadata(dict(title='Catálogo PU 2026 | Borrachas Rocha',author='Borrachas Rocha',
                          subject='Edição final de 21/10/2026 - 141 referências'))
    export_versions(doc,toc)
    (OUT/'produtos.json').write_text(json.dumps([DATA[c] for c in REQUESTED],ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'ordem-final.json').write_text(json.dumps(ORDER,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'conferencia.json').write_text(json.dumps(dict(paginas=len(doc),referencias=manifest,
        excluidas=['7036'],foto_corrigida={'0616':'0616A'},novas=[i['code'] for i in NEW],
        fonte_codigo_original_pt=9,pendentes=[],textos=checks+base.checks),ensure_ascii=False,indent=2),encoding='utf-8')
    previews=OUT/'previas';previews.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(4*312,math.ceil(len(doc)/4)*445),'#ddd')
    for i,page in enumerate(doc):
        page.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(previews/f'pagina-{i+1:02}.png')
        pix=page.get_pixmap(matrix=fitz.Matrix(.5,.5));im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        xx,yy=i%4*312+6,i//4*445+5;sheet.paste(im,(xx,yy));ImageDraw.Draw(sheet).text((xx,yy+422),str(i+1),fill='black')
    sheet.save(OUT/'visao-geral.jpg',quality=92)
    print(f'{len(doc)} páginas; {len(REQUESTED)} referências; 15 inclusões; 0616 com foto da 0616A.')

if __name__=='__main__': main()
