from pathlib import Path
from collections import Counter
import json,re
import fitz
from PIL import Image,ImageChops

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
items=json.loads((OUT/'produtos.json').read_text(encoding='utf-8'))
oems=json.loads((OUT/'codigos-originais.json').read_text(encoding='utf-8'))
by_code={i['code']:i for i in items}
approved=fitz.open(OUT.parent/'revisao-02/Catalogo-PU-2026-Por-Montadora-A4.pdf')
def render(p):
    pix=p.get_pixmap();return Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
report={}
for kind,name,count,pages in [('geral','Catalogo-PU-2026',129,21),('amortecedor','Catalogo-Buchas-do-Amortecedor-2026',14,4)]:
    manifest=json.loads((OUT/(kind+'-conferencia.json')).read_text(encoding='utf-8'))['referencias']
    codes={m['code'] for m in manifest}
    assert len(codes)==len(manifest)==count
    assert codes=={i['code'] for i in items if i['catalog']==kind}
    counts=Counter(m['page'] for m in manifest)
    assert max(counts.values())<=10
    for p in counts:
        entries=[m for m in manifest if m['page']==p]
        assert [m['slot'] for m in entries]==list(range(1,len(entries)+1))
        assert len({m['section'] for m in entries})==1
    for suffix in ['A4','Clientes','Sangria-3mm']:
        file=OUT/(name+'-'+suffix+'.pdf');doc=fitz.open(file)
        assert len(doc)==pages
        for m in manifest:
            text=doc[m['page']-1].get_text()
            assert m['code'] in text,(file.name,m)
            if m['code'] in oems: assert oems[m['code']] in text,(file.name,m,oems[m['code']])
        assert len(doc.get_toc())==(14 if kind=='geral' else 3)
        for p in doc:
            if suffix=='Sangria-3mm':
                assert abs(p.trimbox.width-595.2)<.02
                assert abs(p.trimbox.x0-3*72/25.4)<.02
            else: assert abs(p.rect.width-595.2)<.02 and abs(p.rect.height-841.92)<.02
        all_text='\n'.join(p.get_text() for p in doc)
        assert 'IMPLEMENTOS E COMPONENTES' not in all_text
        for brand in ['FORD','MERCEDES','VOLKSWAGEN']: assert 'TAMBÉM SE APLICA A '+brand not in all_text
        if suffix=='A4':
            assert ImageChops.difference(render(doc[-1]),render(approved[-1])).getbbox() is None
            if kind=='geral': assert ImageChops.difference(render(doc[0]),render(approved[0])).getbbox() is None
        if kind=='geral' and suffix!='Sangria-3mm':
            assert len(doc[1].get_links())==11
            assert all(2<=link['page']<=19 for link in doc[1].get_links())
        report[file.name]=dict(paginas=len(doc),referencias=count,bytes=file.stat().st_size,codigos_originais_verificados=sum(c in oems for c in codes))
    for section in set(m['section'] for m in manifest):
        group=[m for m in manifest if m['section']==section]
        if section!='Trucks e Carretas':
            expected=sorted([m['code'] for m in group],key=lambda c:(c.startswith('0'),c))
            assert [m['code'] for m in group]==expected
    report[kind]=dict(contagem_por_pagina=dict(counts),cinco_fichas_por_coluna=True)
assert {i['code'] for i in items if i['catalog']=='amortecedor'}=={c+' PU' for c in '3058 3079 3056 5021 5022 5023 5029 9028 0912 0912A 0828 0828A 0828C 0836'.split()}
report['pendencias_pu']=['1056','2051','2081C','2119','8010']
report['imagens_novas']=8
report['total_pu_site']=143
report['codigos_originais_dos_anexos']=len(oems)
(OUT/'validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
