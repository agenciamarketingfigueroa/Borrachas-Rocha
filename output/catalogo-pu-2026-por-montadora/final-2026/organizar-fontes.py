"""Conserva fontes mínimas e centraliza os PDFs vigentes antes da limpeza."""
from pathlib import Path
import sys,shutil,json
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'tmp/pdf-final-deps'))
import fitz
from PIL import Image,ImageDraw
fontes=OUT.parent/'fontes';fontes.mkdir(exist_ok=True)
target=fontes/'capas-aprovadas.pdf'
if not target.exists():
    original=fitz.open(ROOT/'output/pdf/Catalogo-PU-2026-Final-A4.pdf')
    cover=fitz.open()
    cover.insert_pdf(original,from_page=0,to_page=0)
    cover.insert_pdf(original,from_page=len(original)-1,to_page=len(original)-1)
    cover.save(target,garbage=4,deflate=True)
for suffix in ['A4','Clientes','Sangria-3mm']:
    name=f'Catalogo-Buchas-do-Amortecedor-2026-{suffix}.pdf'
    src=OUT.parent/'revisao-03'/name
    dest=ROOT/'output/pdf'/name
    if src.exists(): shutil.copy2(src,dest)
    assert dest.is_file()
    assert len(fitz.open(dest))==4
items=json.loads((OUT/'edicao-imagens.json').read_text(encoding='utf-8'))['images']
sheet=Image.new('RGB',(1500,1000),'white')
draw=ImageDraw.Draw(sheet)
for n,item in enumerate(items):
    with Image.open(ROOT/item['output']) as source:
        assert source.mode=='RGBA',item['code']
        alpha=source.getchannel('A')
        assert alpha.getextrema()==(0,255),item['code']
        assert all(alpha.getpixel(point)==0 for point in [(0,0),(0,source.height-1),(source.width-1,0),(source.width-1,source.height-1)])
        # Apenas folha de inspeção: os PNGs incorporados permanecem intactos.
        preview=source.copy();preview.thumbnail((270,285))
        x,y=(n%5)*300,(n//5)*333
        sheet.paste(preview,(x+(300-preview.width)//2,y+30),preview)
        draw.text((x+10,y+10),item['code']+' PU',fill='black')
sheet.save(OUT/'recortes-conferencia.jpg',quality=93)
print('15 PNGs RGBA com transparencia; capas preservadas; 3 PDFs de amortecedor centralizados.')
