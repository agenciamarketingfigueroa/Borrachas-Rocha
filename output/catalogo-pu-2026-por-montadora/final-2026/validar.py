"""Valida a edição final e os requisitos específicos da atualização."""
from pathlib import Path
import json,re,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'tmp/pdf-final-deps'))
import fitz
from PIL import Image

manifest=json.loads((OUT/'conferencia.json').read_text(encoding='utf-8'))
entries=manifest['referencias']
data={i['code'].split()[0]:i for i in json.loads((OUT/'produtos.json').read_text(encoding='utf-8'))}
order=json.loads((OUT.parent/'revisao-04/ordem-diretoria.json').read_text(encoding='utf-8'))
expected=[c for line in order for c in line['codes'] if c!='7036']
assert [e['code'] for e in entries]==expected
assert len(expected)==len(set(expected))==141
assert manifest['pendentes']==[]
assert data['0616']['photoOverride']=='revisao-02/recortes/0616A PU.png'
assert data['0616']['specs'].startswith('Comprimento: 70 mm')
norm=lambda t:re.sub(r'\s+','',t).casefold()
doc=fitz.open(ROOT/'output/pdf/Catalogo-PU-2026-Final-A4.pdf')
assert len(doc)==22==manifest['paginas']
assert len(doc[1].get_links())==11
assert len(doc.get_toc())==14
full='\n'.join(p.get_text() for p in doc)
assert 'FICHA PENDENTE' not in full and 'PRÉVIA' not in full and '7036 PU' not in full
new={i['code'].split()[0]:i for i in json.loads((OUT/'novas-fichas.json').read_text(encoding='utf-8'))}
for code in new:
    with Image.open(ROOT/'assets/img/Peças de PU/recortes-final'/f'{code} PU.png') as image:
        assert image.mode=='RGBA' and image.getchannel('A').getextrema()==(0,255),code
oem_count=0
photographs={}
for entry in entries:
    code=entry['code'];p=doc[entry['page']-1]
    x=(54 if entry['page']%2==0 else 14)+270*((entry['slot']-1)//5)
    y=94+142*((entry['slot']-1)%5)
    rect=fitz.Rect(x-1,y-1,x+258,y+136)
    text=p.get_text(clip=rect)
    assert code+' PU' in text,(code,text)
    if code in new:
        photo_rect=fitz.Rect(x,y+20,x+94,y+120)
        image_refs={im['xref'] for im in p.get_image_info(xrefs=True)
                    if fitz.Rect(im['bbox']).intersects(photo_rect) and im['width']>100}
        assert any(im[0] in image_refs and im[1]>0 for im in p.get_images(full=True)),(code,'alpha ausente no PDF')
        for field in ['name','specs','application','secondTitle','secondApplication']:
            for value in new[code].get(field,'').split(' | '):
                assert norm(value) in norm(text),(code,field,value,text)
        assert any(fitz.Rect(im['bbox']).intersects(fitz.Rect(x,y+20,x+94,y+120))
                   and im['width']>100 for im in p.get_image_info()),code
        if code=='7039':
            assert text.index('Volvo VM 260 / 270')<text.index('Bucha do suporte')<text.index('Volvo VM 330 Traçado')
            spans=[s for b in p.get_text('dict',clip=rect)['blocks'] for l in b.get('lines',[]) for s in l['spans']]
            assert all('Bold' in s['font'] for s in spans if 'Bucha' in s['text'])
    if data[code].get('originalCode'):
        assert data[code]['originalCode'] in text,(code,text)
        spans=[s for b in p.get_text('dict',clip=rect)['blocks'] for l in b.get('lines',[]) for s in l['spans'] if 'Cód. original:' in s['text']]
        assert len(spans)==1,(code,spans)
        span=spans[0]
        assert abs(span['size']-9)<.01 and span['color']==0 and 'Bold' in span['font']
        assert span['bbox'][3]<y+136
        oem_count+=1
    if code in ['0616','0616A']:
        photo_rect=fitz.Rect(x,y+20,x+94,y+120)
        photographs[code]={im['digest'].hex() for im in p.get_image_info(hashes=True)
                           if fitz.Rect(im['bbox']).intersects(photo_rect) and im['width']>100}
assert photographs['0616'] and photographs['0616']==photographs['0616A'],photographs
for p in doc:
    assert abs(p.rect.width-595.2)<.02 and abs(p.rect.height-841.92)<.02
    if p.number in [0,len(doc)-1]: continue
    for block in p.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                r=fitz.Rect(span['bbox'])
                assert r.x0>=-1 and r.y0>=-1 and r.x1<=p.rect.width+1 and r.y1<=p.rect.height+1,(p.number,span)
for row in manifest['textos']: assert row['body_bottom']<=121,row
for suffix in ['Clientes','Sangria-3mm']:
    variant=fitz.open(ROOT/f'output/pdf/Catalogo-PU-2026-Final-{suffix}.pdf')
    assert len(variant)==len(doc)
    assert len(variant.get_toc())==14
    if suffix=='Clientes':
        assert len(variant[1].get_links())==11
        for entry in entries: assert entry['code']+' PU' in variant[entry['page']-1].get_text(),entry
    else:
        for page in variant:
            assert abs(page.trimbox.width-595.2)<.02
            assert abs(page.trimbox.x0-3*72/25.4)<.02
report=dict(paginas=22,referencias=141,novas_fichas=15,ordem_conferida=True,
            recortes_transparentes=15,mascaras_transparencia_no_pdf=True,
            excluida_7036=True,foto_0616_identica_0616A=True,dois_titulos_7039=True,
            codigos_originais_9pt_preto_negrito=oem_count,links_indice=11,
            textos_dentro_das_paginas=True,medidas_aplicacoes_conferidas=True,
            versoes=['A4','Clientes','Sangria-3mm'],pendentes=[])
(OUT/'validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
