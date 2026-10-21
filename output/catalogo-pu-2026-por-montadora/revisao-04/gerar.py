"""Prévia da ordem da direção; fichas ausentes ficam explicitamente pendentes.

Reutiliza a composição aprovada da revisão 03, sem alterar os PDFs publicados.
"""
from pathlib import Path
from io import BytesIO
import importlib.util
import json
import math
import fitz
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
spec = importlib.util.spec_from_file_location('revisao03', OUT.parent/'revisao-03/gerar.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
ORDER = json.loads((OUT/'ordem-diretoria.json').read_text(encoding='utf-8'))
DATA = {i['code'].split()[0]: i for i in base.items if i['catalog'] == 'geral'}
for code, oem in json.loads((OUT/'codigos-originais-fichas.json').read_text(encoding='utf-8')).items():
    DATA[code]['originalCode'] = oem
BRANDS = ['Volkswagen','Mercedes-Benz','Ford','Toyota','Scania','Volvo',
          'Trucks e Carretas','Chevrolet','Iveco','Mitsubishi','Nissan']
REQUESTED = [c for line in ORDER for c in line['codes']]
MISSING = [c for c in REQUESTED if c not in DATA]
assert len(REQUESTED) == len(set(REQUESTED)) == 142

# Código original: 7 pt cinza -> 9 pt preto em negrito, sempre vetorial.
original_para = base.para
def para(c, text, x, y, width, size=10, font='Arial', color=(0,0,0), align=0):
    if text.startswith('Cód. original:'):
        size, font, color = 9, 'Bold', (0,0,0)
    return original_para(c, text, x, y, width, size, font, color, align)
base.para = para

def pending_card(c, code, brand, x, y):
    base.tag(c, {'code':code+' PU', 'brand':brand}, x, y)
    c.setStrokeColorRGB(.78,.80,.85)
    c.setLineWidth(.6)
    c.roundRect(x, base.H-y-121, 257, 98, 5, stroke=1, fill=0)
    para(c, 'FICHA PENDENTE', x+8, y+43, 241, 11, 'Bold', base.RED, 1)
    para(c, 'Posição reservada conforme a lista da direção.<br/>'
         'Aguardando foto e dados técnicos de PU.', x+12, y+65, 233, 9, align=1)
    c.setStrokeColorRGB(.88,.9,.95)
    c.line(x,base.H-y-136,x+257,base.H-y-136)

def main():
    plan=[]
    for line,brand in zip(ORDER,BRANDS):
        codes=line['codes']
        for start in range(0,len(codes),10):
            plan.append(dict(line=line['line'],brand=brand,codes=codes[start:start+10],
                             part=start//10+1,parts=math.ceil(len(codes)/10),page=len(plan)+3))
    page_for={code:p['page'] for p in plan for code in p['codes']}
    stream=BytesIO()
    c=base.Canvas(stream,pagesize=(base.W,base.H),initialFontName='Arial')
    x=base.chrome(c,2,'Encontre sua peça','ORDEM DA DIREÇÃO - PRÉVIA DE CONFERÊNCIA')
    para(c, f'{len(REQUESTED)} posições: {len(REQUESTED)-len(MISSING)} fichas disponíveis e '
         f'{len(MISSING)} pendentes.',x,94,520,10,'Bold')
    para(c,'Leia de cima para baixo na coluna esquerda e depois na direita.',x,115,520,9)
    y=150
    for line,brand in zip(ORDER,BRANDS):
        pages=[p['page'] for p in plan if p['line']==line['line']]
        label=f'{pages[0]:02}' if len(pages)==1 else f'{pages[0]:02}-{pages[-1]:02}'
        para(c,'Linha '+line['line']+' - '+brand,x,y,420,11,'Bold')
        para(c,label,x+450,y,66,11,'Bold',base.BLUE,2)
        c.setStrokeColorRGB(.89,.91,.95)
        c.line(x,base.H-y-24,x+517,base.H-y-24)
        y+=38
    para(c,'CONFERÊNCIA ANTES DA IMPRESSÃO',x,y+8,520,10,'Bold',base.RED)
    para(c,'Fichas pendentes: '+', '.join(MISSING)+'.',x,y+30,520,9)
    para(c,'A 7036 também está ausente na base. A foto do 8016 ainda precisa ser '
         'conferida no arquivo de origem; essa referência não consta nesta lista.',x,y+67,520,9)
    para(c,'DAF: 6054 PU na página '+str(page_for['6054'])+' e 7033 PU na página '+
         str(page_for['7033'])+'. Buchas do amortecedor: catálogo específico.',x,y+104,520,9)
    c.showPage()
    manifest=[]
    for p in plan:
        subtitle=f'PRÉVIA - FICHAS PENDENTES SINALIZADAS - {p["part"]}/{p["parts"]}'
        x=base.chrome(c,p['page'],p['brand'],subtitle)
        # Identifica a linha sem disputar espaço com o cabeçalho aprovado.
        para(c,'LINHA '+p['line'],x+390,41,134,11,'Bold',base.BLUE,2)
        for j,code in enumerate(p['codes']):
            col,row=j//5,j%5
            xx,yy=x+270*col,94+142*row
            if code in DATA:
                base.card(c,DATA[code],xx,yy)
            else:
                pending_card(c,code,p['brand'],xx,yy)
            manifest.append(dict(code=code,line=p['line'],page=p['page'],slot=j+1,
                                 status='disponível' if code in DATA else 'pendente'))
        if p['line']=='7000' and p['part']==p['parts']:
            para(c, f'Também se aplica a Volvo: 8012 PU e 8013 PU - página {page_for["8012"]}.',
                 x,803,520,8)
        c.showPage()
    c.save()
    doc=fitz.open()
    doc.insert_pdf(base.approved,from_page=0,to_page=0)
    cover=BytesIO()
    cc=base.Canvas(cover,pagesize=(base.W,base.H),initialFontName='Arial')
    cc.setFillColorRGB(1,1,1)
    cc.rect(0,base.H-73,base.W,45,fill=1,stroke=0)
    para(cc,'PRÉVIA DE CONFERÊNCIA',18,34,560,16,'Bold',base.RED,1)
    para(cc,f'{len(MISSING)} fichas pendentes - não enviar para impressão final',18,55,560,9,'Bold',base.RED,1)
    cc.save()
    overlay=fitz.open(stream=cover.getvalue(),filetype='pdf')
    doc[0].show_pdf_page(doc[0].rect,overlay,0)
    interior=fitz.open(stream=stream.getvalue(),filetype='pdf')
    doc.insert_pdf(interior)
    doc.insert_pdf(base.approved,from_page=len(base.approved)-1,to_page=len(base.approved)-1)
    toc=[[1,'Capa - prévia',1],[1,'Índice e pendências',2]]
    for line in ORDER:
        label='Linha '+line['line']
        page=next(p['page'] for p in plan if p['line']==line['line'])
        toc.append([1,label,page])
        for rect in doc[1].search_for(label):
            doc[1].insert_link({'kind':fitz.LINK_GOTO,'from':rect,'page':page-1})
    toc.append([1,'Contato',len(doc)])
    doc.set_toc(toc)
    doc.set_metadata(dict(title='Catálogo PU 2026 - Prévia da ordem da direção',
                          author='Borrachas Rocha',subject='142 posições; 16 fichas pendentes. Revisão 04.'))
    target=ROOT/'output/pdf/Catalogo-PU-2026-Revisao-04-PREVIA.pdf'
    doc.save(target,garbage=4,deflate=True)
    (OUT/'conferencia.json').write_text(json.dumps(dict(paginas=len(doc),referencias=manifest,
        fonte_codigo_original_pt=9,pendentes=MISSING),ensure_ascii=False,indent=2),encoding='utf-8')
    preview=OUT/'previas'
    preview.mkdir(exist_ok=True)
    thumbs=[]
    for i,page in enumerate(doc):
        page.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(preview/f'pagina-{i+1:02}.png')
        pix=page.get_pixmap(matrix=fitz.Matrix(.5,.5))
        thumbs.append(Image.frombytes('RGB',(pix.width,pix.height),pix.samples))
    sheet=Image.new('RGB',(4*312,math.ceil(len(doc)/4)*445),'#ddd')
    for i,im in enumerate(thumbs):
        x,y=i%4*312+6,i//4*445+5
        sheet.paste(im,(x,y))
        ImageDraw.Draw(sheet).text((x,y+422),str(i+1),fill='black')
    sheet.save(OUT/'visao-geral.jpg',quality=90)
    print(f'{len(doc)} páginas; {len(REQUESTED)} posições; {len(MISSING)} pendentes.')

if __name__=='__main__':
    main()
