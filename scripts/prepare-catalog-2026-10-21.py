"""Consolida a revisão de 21/10/2026 sem alterar os arquivos da revisão aprovada."""
from pathlib import Path
import ast, json, re
import fitz

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'output/catalogo-pu-2026-por-montadora'
OUT = BASE / 'revisao-03'
OUT.mkdir(exist_ok=True)
source = (ROOT / 'catalog.js').read_text(encoding='utf-8')
rows = json.loads((OUT/'site-base.json').read_text(encoding='utf-8'))
site = {r[0]: dict(code=r[0],brand=r[1],name=r[2],application=r[3],specs=r[4] if len(r)>4 else '',image=r[5] if len(r)>5 else r[0]+'.png',material='PU') for r in rows}
items = json.loads((BASE / 'produtos.json').read_text(encoding='utf-8'))
ocr = json.loads((OUT / 'fichas-transcricao.json').read_text(encoding='utf-8'))

# Transcrição conferida visualmente nas fichas existentes; OCR só auxilia a leitura.
app_starts = r'^(VW|MB |Ônibus|Hilux|Scania|Volvo|DAF|S10|Iveco|L200|Frontier|Xterra|Pajero|Ranger)'
spec_starts = r'^(Comprimento|Diâm|Interno|A: |B: |C: |605\d[A-Z]?:|7012[A-Z]:|Aplicável|Entre|Código|Cód\.|Cod\.|Trava|IDiâm)'
fixes = {'SIO':'S10','16,bmm':'16,0mm','42 Omm':'42,0mm','45 Omm':'45,0mm','ADIicável':'Aplicável','96,0m':'96,0mm','em dante':'em diante','90\\/16':'90V16','90\\/18':'90V18','90./18':'90V18','Strallis':'Stralis','IDiâm.':'Diâm.'}
for item in items:
    code = item['code']
    if code in site:
        item.update({k:site[code][k] for k in ['name','application','specs']})
        continue
    lines = ocr[code.split()[0]]
    first = next(n for n,t in enumerate(lines) if ' PU' in t)
    lines = lines[first+1:]
    for a,b in fixes.items(): lines=[t.replace(a,b) for t in lines]
    lines=[t.replace('mmm','mm') for t in lines]
    ai = next((n for n,t in enumerate(lines) if re.match(app_starts,t)),len(lines))
    si = next((n for n,t in enumerate(lines[:ai]) if re.match(spec_starts,t)),ai)
    name=' '.join(lines[:si]); specs=[]
    for line in lines[si:ai]:
        if re.match(r'^(C[oó]d|A: 239)',line): continue
        specs.append(line)
    application=' '.join(lines[ai:])
    item.update(name=name,application=application,specs=' | '.join(specs))
    brand={'Mercedes-Benz':'Mercedes','Nissan':'Nissan Frontier','JOST':'Jost'}.get(item['brand'],item['brand'])
    # Exportação da área fotográfica da ficha do PDF; sem recriar o produto.
    photo_dir=ROOT/'assets/img/Peças de PU/fotos-catalogo'; photo_dir.mkdir(exist_ok=True)
    image_path=BASE/item['image']
    pix=fitz.Pixmap(str(image_path)); width,height=pix.width*.24,pix.height*.24
    photo_doc=fitz.open(); page=photo_doc.new_page(width=width,height=height)
    page.insert_image(page.rect,filename=str(image_path))
    page.get_pixmap(matrix=fitz.Matrix(3,3),clip=fitz.Rect(0,20,min(94,width*.39),height)).save(photo_dir/(code+'.png'))
    site[code]=dict(code=code,brand=brand,name=name,application=application,specs=item['specs'],image='fotos-catalogo/'+code+'.png',material='PU')

new_rows=[
 ['0819','Mitsubishi','Bucha da barra estabilizadora dianteira','Pajero TR4','Interno do furo: 23 mm','BR 0819 PU.JPG','MR455699'],
 ['8027','Truck','Bucha do 4º eixo do cavalo mecânico','','Comprimento: 122 mm | Diâmetro externo: 62 mm | Interno do furo: 24 mm','BR 8027 PU.JPG',''],
 ['1012','Volkswagen','Bucha da barra estabilizadora dianteira','VW 6.90 ao 8.160','Interno do furo: 26 mm','BR 1012 PU.JPG','TO6411041'],
 ['0605','Iveco','Bucha da ponta estabilizadora traseira','Iveco Daily 70C16 / 70C17','A: Interno do furo: 28 mm | B: Interno do furo: 34 mm','BR 0605 PU.JPG','8560291'],
 ['1034','Volkswagen','Bucha da barra estabilizadora dianteira','VW 17.230 / 24.280','Interno do furo: 38 mm','BR 1034 PU.JPG','2T2411041'],
 ['1013A','Volkswagen','Bucha da barra estabilizadora traseira','VW 6.90 ao 8.160','Interno do furo: 30 mm','BR 1013 A PU.JPG','600511413A'],
 ['0636','Iveco','Bucha da mola dianteira e traseira','Iveco 150E21 Ônibus','Comprimento: 80 mm | Diâmetro externo: 60 mm | Interno do furo: 16 mm','BR 0636 PU.JPG','500090937'],
 ['0616','Iveco','Bucha de mola e suporte traseiro','Iveco Daily; aplicar em mola com olhal de 60 mm de largura','Comprimento: 70 mm | Diâmetro externo: 40 mm | Interno do furo: 16 mm','BR 0616 PU.JPG','93808935'],
]
for code,brand,name,application,specs,image,oem in new_rows:
    code+=' PU'
    p=dict(code=code,brand=brand,name=name,application=application,specs=specs,image=image,material='PU',originalCode=oem)
    site[code]=p.copy(); items.append(dict(p,original=False,new=True))

# Códigos literais do anexo: zeros iniciais, letras e referências múltiplas preservados.
oem_text='''1008 T06411045
1010 600511421
1011 T21411045
1014 TAR411041
1020 TJG411171
1021 TJ6899397
1026 T20411171
1050 23B899397
1053 23B511473
1055 23B411719B
1061 23B411719B
1062 23B411719C
2008 3143260481
2010 A6883207173
2015 A3843207050
2039 A3193240750
2048 A6343260281
2048A A6343260281
2049 A3843237081
2054 A3843177051
2062 A9743200044
2063A A9703200344
2063B A9703200344
2063C A9703200344
2074A A9583200344
2074B A9583200344
2074C A9583200344
2078 A9793200544
2078A A6703200444
2078C A9793200544
2081B A9583200204
2120 A9603264781
2121 9603231885
5003 9038598001
5004 9038598002
5007 9038518007
5008 9038518046
5019 9038914004
6053 2031367 / 2470850
6054 1854592
6057 2773898
6058 36006117
7010 20553083
7012 20428160 / 20428167
7014 20498774
7019 20587455
7020 20542833
7033 21175831
7037 20881775
8001 20200039
8002 20200051
8003 20200052
8004 20200052
8011 208006277 / R71000018
8012 717000009
8013 341502-5 / 9583250150
8024 212008921
8023 6933165972
9022 973557492
9023 97946545
9024 52144770
9026 94773365
0610 8162306
0610A 8162306
0611 98469635
0611D 98469635
0614A 070641170
0614B 5949895134
0615 8127910
0616 93808935
0627 500350342
0805 MB584530
0806 MB584531'''
oems={line.split(' ',1)[0]+' PU':line.split(' ',1)[1] for line in oem_text.splitlines()}
oems.update({r[0]+' PU':r[-1] for r in new_rows if r[-1]})
updates={
 '2054':dict(specs='Diâmetro externo: 40 mm | Interno do furo: 22 mm'),
 '2078C':dict(specs='Comprimento: 86 mm | Diâmetro externo: 55 mm | Interno do furo: 18 mm'),
 '2120':dict(specs='Comprimento: 50 mm | Diâmetro do olhal: 75 mm | Interno do tubo: 35 mm'),
 '5003':dict(application='Toyota Bandeirante 1992 em diante',specs='Comprimento: 45 mm | Diâmetro externo: 35 mm | Interno do furo: 18 mm'),
 '5004':dict(application='Toyota Bandeirante 1992 em diante',specs='Comprimento: 45 mm | Diâmetro externo: 40 mm | Interno do furo: 18 mm'),
 '7012':dict(application='Volvo FH / Volvo VM traçado',specs='7012A: Diâm. interno: 34 mm | 7012B: Diâm. interno: 39 mm | 7012C: Diâm. interno: 44 mm'),
 '9020':dict(application='S10 até 2011',specs='Comprimento: 76 mm | Diâmetro externo: 40 mm | Interno do furo: 14 mm'),
 '9022':dict(specs='Comprimento: 36 mm | Diâmetro externo: 30 mm | Interno do furo: 18 mm'),
 '9023':dict(specs='Comprimento: 50 mm | Diâmetro externo: 30 mm | Interno do furo: 18 mm'),
 '0627':dict(specs='Altura: 32 mm | Diâmetro externo: 65 mm | Interno do furo: 33 mm'),
 '0836':dict(name='Bucha do braço transversal traseiro',application='Pajero TR4 / Pajero IO (2002 a 2015)',specs='A: Diâmetro interno: 12 mm | B: Diâmetro interno: 14 mm',brand='Mitsubishi'),
 '8011':dict(name='Bucha do tensor do truck',application='Randon 2000',specs='Comprimento: 63 mm | Diâmetro externo: 58,5 mm | Interno do furo: 24 mm'),
 '1026A':dict(specs='Comprimento: 88 mm | Diâmetro externo: 42 mm | Diâmetro interno: 16 mm'),
}
for code in ['0614','0614A','0614B','0615']:
    updates.setdefault(code,{})['application']='Iveco Vertice / 90V16 / 90V18 / Tector 11.190'
for item in items:
    code=item['code']; changes=updates.get(code.split()[0],{})
    item.update(changes); site[code].update(changes)
    site[code]['brand']={'Mercedes-Benz':'Mercedes','Nissan':'Nissan Frontier','JOST':'Jost'}.get(item['brand'],item['brand'])
    if code=='0836 PU': site[code]['image']='fotos-catalogo/0836 PU.png'
    if code in oems: item['originalCode']=oems[code];site[code]['originalCode']=oems[code]
    if changes: item['recompose']=True
    item['catalog']='amortecedor' if code.split()[0] in '3058 3079 3056 5021 5022 5023 5029 9028 0912 0912A 0828 0828A 0828C 0836'.split() else 'geral'
    site[code]['catalog']=item['catalog']
    if item['brand'] in ['HBZ','JOST','Randon','Rodoviária','Suspensys','Truck']: item['section']='Trucks e Carretas'
    else: item['section']=item['brand']
assert len(items)==len(site)==143
assert len({i['code'] for i in items})==143
assert all(c in site for c in oems)
(OUT/'produtos.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'codigos-originais.json').write_text(json.dumps(oems,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'site-produtos.json').write_text(json.dumps(list(site.values()),ensure_ascii=False,indent=2),encoding='utf-8')
payload='const PU_PRODUCTS = '+json.dumps(list(site.values()),ensure_ascii=False,indent=2)+';'
source=re.sub(r'const PU_PRODUCTS = \[.*?(?=\n\nconst state =)',lambda _:payload,source,count=1,flags=re.S)
(ROOT/'catalog.js').write_text(source,encoding='utf-8')
print('143 produtos consolidados;',len(oems),'referências com código original dos anexos.')
