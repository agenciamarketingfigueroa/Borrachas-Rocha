"""Confere sequência, posições reservadas, códigos originais e limites de texto."""
from pathlib import Path
import json
import fitz

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
order=json.loads((OUT/'ordem-diretoria.json').read_text(encoding='utf-8'))
expected=[c for line in order for c in line['codes']]
manifest=json.loads((OUT/'conferencia.json').read_text(encoding='utf-8'))
entries=manifest['referencias']
assert [e['code'] for e in entries]==expected
assert len(expected)==len(set(expected))==142
assert len([e for e in entries if e['status']=='pendente'])==16
assert expected.index('6057')+1==expected.index('6056')
data={i['code'].split()[0]:i for i in json.loads((OUT.parent/'revisao-03/produtos.json').read_text(encoding='utf-8'))}
for code,oem in json.loads((OUT/'codigos-originais-fichas.json').read_text(encoding='utf-8')).items():
    data[code]['originalCode']=oem
doc=fitz.open(ROOT/'output/pdf/Catalogo-PU-2026-Revisao-04-PREVIA.pdf')
assert len(doc)==manifest['paginas']
assert len(doc[1].get_links())==11
assert len(doc.get_toc())==14
assert 'PRÉVIA DE CONFERÊNCIA' in doc[0].get_text()
oem_count=0
for e in entries:
    p=doc[e['page']-1]
    x=(54 if e['page']%2==0 else 14)+270*((e['slot']-1)//5)
    y=94+142*((e['slot']-1)%5)
    rect=fitz.Rect(x-1,y-1,x+258,y+136)
    text=p.get_text(clip=rect)
    assert e['code']+' PU' in text, e
    if e['status']=='pendente':
        assert 'FICHA PENDENTE' in text, e
    elif data[e['code']].get('originalCode'):
        assert data[e['code']]['originalCode'] in text, (e,text)
        spans=[s for b in p.get_text('dict',clip=rect)['blocks'] for l in b.get('lines',[]) for s in l['spans'] if 'Cód. original:' in s['text']]
        assert len(spans)==1,(e,spans)
        s=spans[0]
        assert abs(s['size']-9)<.01 and s['color']==0 and 'Bold' in s['font'],(e,s)
        assert s['bbox'][3] < y+136,(e,s)
        oem_count+=1
for p in doc:
    assert abs(p.rect.width-595.2)<.02 and abs(p.rect.height-841.92)<.02
    for b in p.get_text('dict')['blocks']:
        for line in b.get('lines',[]):
            for s in line['spans']:
                # Capas têm arte própria; verificar texto vetorial do miolo.
                if p.number in (0,len(doc)-1): continue
                r=fitz.Rect(s['bbox'])
                assert r.x0>=-1 and r.y0>=-1 and r.x1<=p.rect.width+1 and r.y1<=p.rect.height+1,(p.number,s)
report=dict(paginas=len(doc),posicoes=142,fichas_disponiveis=126,pendentes=manifest['pendentes'],
            ordem_exata=True,codigos_originais_9pt_preto_negrito=oem_count,
            links_indice=11,textos_dentro_das_paginas=True,status='Prévia; inclusão e foto 8016 ainda pendentes')
(OUT/'validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
