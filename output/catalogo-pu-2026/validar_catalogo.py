"""Confere os PDFs gerados; argumento: caminho do PDF original."""
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw
import pymupdf as fitz
import json
import re
import sys

out = Path(__file__).resolve().parent
a = fitz.open(out / 'Catalogo-PU-2026-A4.pdf')
b = fitz.open(out / 'Catalogo-PU-2026-Grafica-Sangria-3mm.pdf')
source = fitz.open(sys.argv[1])
manifest = json.loads((out / 'conferencia.json').read_text())
assert len(a) == len(b) == 16
text = '\n'.join(a[i].get_text() for i in [12, 13, 14])
codes = re.findall(r'\b\d{4}[A-D]? PU\b', text)
assert len(codes) == len(set(codes)) == 34
assert set(codes) == {p['code'] for p in manifest['novos_produtos']}
assert all('2026' in a[i].get_text() for i in range(15))
assert 'Iveco ônibus Mascarello' not in text
assert '0912A PU' in a[11].get_text()

checks = []
for i in range(13):
    final_index = i if i < 12 else 15
    old = source[i].get_pixmap()
    current = a[final_index].get_pixmap()
    im1 = Image.frombytes('RGB', (old.width, old.height), old.samples)
    im2 = Image.frombytes('RGB', (current.width, current.height), current.samples)
    masks = []
    if i == 0:
        masks = [(40, 589, 293, 674)]
    elif i < 12:
        masks = [(12, 204, 36, 544) if i % 2 else (559, 204, 583, 544)]
    if i == 11:
        masks.append((86, 204, 139, 222))
    for im in [im1, im2]:
        draw = ImageDraw.Draw(im)
        for box in masks:
            draw.rectangle(box, fill='white')
    diff = ImageChops.difference(im1, im2).getbbox()
    assert diff is None, (i, diff)
    checks.append(dict(pagina_original=i+1, pagina_final=final_index+1,
                       conteudo_preservado=True))
for page in b:
    assert abs(page.trimbox.width - 595.2) < .01
    assert abs(page.trimbox.height - 841.92) < .01
    assert abs(page.trimbox.x0 - 3*72/25.4) < .01
fonts = {r[0] for page in a for r in page.get_fonts()}
assert all(a.extract_font(x)[3] for x in fonts)
summary = dict(paginas=16, novos_codigos_conferidos=34, fontes_incorporadas=len(fonts),
               preservacao_original=checks, sangria_mm=3,
               formato_corte_mm=[round(595.2*25.4/72, 2), round(841.92*25.4/72, 2)])
(out / 'validacao.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
contact = Image.new('RGB', (4*300, 4*445), '#dedede')
draw = ImageDraw.Draw(contact)
for i, page in enumerate(a):
    pix = page.get_pixmap(matrix=fitz.Matrix(.48, .48))
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    x, y = i % 4 * 300, i // 4 * 445
    contact.paste(im, (x+5, y+3))
    draw.text((x+10, y+415), f'{i+1:02}', fill='black')
contact.save(out / 'visao-geral.jpg')
print('OK: 16 páginas, 34 adições, fontes incorporadas e sangria de 3 mm.')
print('OK: 13 páginas originais preservadas fora das intervenções documentadas.')
