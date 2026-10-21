"""Consolida as 15 fichas enviadas em 21/10/2026, preservando as fotos originais."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageOps

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
rows = [
    ['2062B','Mercedes-Benz','Bucha Silenciosa do Feixe de Molas Dianteiro da Parte Traseira','Comprimento: 95,0 mm | Diâmetro Externo: 60,0 mm | Diâmetro Interno: 18,0 mm','MB Atego','BR 2062 B PU.JPG'],
    ['2081C','Mercedes-Benz','','Aplicável em Olhais com Diâmetro: 65,0 mm | Diâmetro Interno (Furo): 20,0 mm','MB Atego','BR 2081 C PU .JPG'],
    ['2119','Mercedes-Benz','Bucha da barra estabilizadora dianteira','Diâmetro Interno: 38,0 mm','MB Actros / Axor','BR 2119 PU.JPG'],
    ['8010','Truck','Bucha tensor Guerra / Fahchinni','Diâmetro Externo: 71 mm','','BR 8010 PU.JPG'],
    ['2066','Mercedes-Benz','Bucha da ponta estabilizadora dianteira e traseira','Comprimento: 40 mm | Diâmetro: 36 mm | Diâmetro do Furo: 16 mm','MB Atego / Acello 1016','BR 2066 PU.JPG'],
    ['0613','Iveco','Bucha do feixe de mola dianteiro','Comprimento: 84 mm | Diâmetro: 60 mm | Diâmetro Interno: 20,2 mm','Iveco Tector','BR 0613 PU.JPG'],
    ['2068','Mercedes-Benz','Bucha da ponta do estabilizador dianteiro e traseiro','Diâmetro Interno: 12,5 mm','MB Accelo','BR 2068 PU.JPG'],
    ['2051','Mercedes-Benz','Bucha da Barra estabilizadora dianteira e traseira','2051 B Diâmetro Interno: 28 mm | 2051 C Diâmetro Interno: 32 mm | 2051 D Diâmetro Interno: 36 mm','MB Atego / MB Accelo','BR 2051 PU.JPG'],
    ['7034','Scania','Batente da mola dianteira','Lado Direito','Scania','BR 7034 PU.JPG'],
    ['1056','Volkswagen','Bucha da ponta da Barra Estabilizadora Dianteira','Comprimento: 43 mm | Diâmetro Externo: 48 mm | Diâmetro Interno: 18 mm','VW 11.180 / 9.170 / Delivery','BR 1056 PU.JPG'],
    ['2065','Mercedes-Benz','Bucha da ponta estabilizadora dianteira superior','Comprimento: 42 mm | Diâmetro Externo: 44 mm | Diâmetro do Furo: 22 mm','MB Atego','BR 2065 PU.JPG'],
    ['7038','DAF','Bucha da ponta estabilizadora dianteira DAF','Comprimento: 46 mm | Diâmetro Externo: 44 mm | Diâmetro do Furo: 16 mm','','BR 7038 PU.JPG'],
    ['6056','Scania','Bucha da Ponta da Barra Estabilizadora Dianteira','Comprimento: 46 mm | Diâmetro Externo: 48 mm | Interno do Furo: 16 mm','','BR 6056 PU.JPG'],
    ['7039','Volvo','Bucha da Mola Dianteira','Aplicável em olhal de 50mm','Volvo VM 260 / 270','BR 7039 PU .JPG'],
    ['7035','Scania','Batente da mola dianteira','Lado esquerdo','Scania','BR 7035 PU.JPG'],
]
items=[]
for code,brand,name,specs,application,photo in rows:
    assert (ROOT/'assets/img/Peças de PU'/photo).is_file(), photo
    item=dict(code=code+' PU',brand=brand,name=name,specs=specs,application=application,
              image=photo,original=False,new=True,catalog='geral',source='Mensagem do usuário, 21/10/2026')
    if code=='6056': item['originalCode']='2280638'
    if code=='7039':
        item['secondTitle']='Bucha do suporte da Mola Dianteira'
        item['secondApplication']='Volvo VM 330 Traçado'
    items.append(item)
(OUT/'novas-fichas.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
# Folha de contato exclusivamente para inspeção das fotografias, sem alterar originais.
sheet=Image.new('RGB',(1500,1800),'white')
draw=ImageDraw.Draw(sheet)
for n,item in enumerate(items):
    with Image.open(ROOT/'assets/img/Peças de PU'/item['image']) as src:
        im=ImageOps.exif_transpose(src).convert('RGB')
        im.thumbnail((280,530))
        x,y=(n%5)*300,(n//5)*600
        sheet.paste(im,(x+(300-im.width)//2,y+30))
        draw.text((x+10,y+10),item['code'],fill='black')
sheet.save(OUT/'fotos-conferencia.jpg',quality=90)
print('15 fichas e fotos conferíveis preparadas.')
