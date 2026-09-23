# Catálogo PU 2026 — por montadora

**Revisão visual mais recente:** [revisao-02/LEIA-ME.md](revisao-02/LEIA-ME.md), com fundo removido das 33 fotos novas e escala visual padronizada. Os PDFs desta pasta são a primeira versão, preservada para comparação. A descrição abaixo documenta essa primeira entrega.

## Arquivos para revisão e impressão

- `Catalogo-PU-2026-Por-Montadora-A4.pdf`: 28 páginas, índice clicável e marcadores por marca, em ordem de leitura.
- `Catalogo-PU-2026-Por-Montadora-Sangria-3mm.pdf`: mesmas páginas, com 3 mm de sangria e área de corte definida; sem imposição.
- `visao-geral.jpg`: visão de todas as páginas.
- `previa-*.png`: páginas ampliadas para revisão.

135 fichas: 102 do catálogo de 2025 e 33 novas do `catalog.js` local. As variantes descritas dentro das fichas antigas foram preservadas. A referência **1013A PU não foi incluída**, por solicitação do usuário, até o fornecimento da fotografia.

## Organização e decisões confirmadas

Montadoras em ordem alfabética; em seguida, fabricantes de implementos e componentes. Cada marca começa em uma nova página. As peças seguem a ordem do código, da esquerda para a direita e de cima para baixo. As aplicações compartilhadas têm remissões nas seções pertinentes; o índice também aponta as aplicações DAF presentes nas fichas Scania/Volvo.

- 0836 PU: Mitsubishi Pajero TR4 / Pajero IO, como no PDF original.
- 6054 PU: mantida na seção Scania, com a aplicação DAF e todas as medidas do original, conforme confirmação do usuário.
- 1046A PU: HBZ, conforme confirmação do usuário.
- 0912A PU: corrigida a segunda etiqueta 0912 do original, correspondente ao diâmetro externo 41,5 mm, conforme o cadastro e a revisão anterior.
- Títulos de 5021, 5022 e 5023 PU: restaurado o texto completo “Bucha inferior do amortecedor dianteiro”, que já estava truncado no original; fotos, medidas e aplicações mantidas.
- Aplicações da 0633 PU: recomposta a mesma lista de modelos dentro da ficha, pois o texto original encostava na faixa azul.

A capa e a contracapa são as artes originais. Apenas o ano da capa foi alterado. As faixas laterais do novo miolo trazem 2026; o original ainda tinha 2024 nessas faixas. O conteúdo técnico das fichas antigas foi reaproveitado diretamente dos pixels do PDF a aproximadamente 300 dpi, evitando transcrição de medidas. As novas fichas usam os dados e as fotografias do projeto, sem gerar imagens de peças.

Logotipos reutilizados do PDF, com exceção da [JOST, obtida no site oficial](https://service-and-parts.jost-world.com/en/imprint.html). O SVG oficial contém somente geometria de imagem; a declaração DTD foi removida. O arquivo foi convertido localmente em PNG. “Rodoviária” usa identificação textual, conforme o cadastro; não foi inventado um emblema.

## Produção gráfica

Formato de corte: 209,97 × 297,01 mm, igual ao original e aproximadamente A4. A versão com sangria estende as bordas sem aumentar o conteúdo. As 28 páginas são múltiplo de quatro. RGB preservado; não se trata de PDF/X nem de conversão para CMYK. O perfil de cor e a imposição podem ser definidos pela gráfica. A resolução das fotos novas depende dos arquivos fornecidos no projeto.

## Fontes e manutenção

`produtos.json` contém as fichas e a atribuição de marcas. `conferencia.json` relaciona código e página. `fontes.json` registra fontes, decisões e hashes. `validacao.json` registra os controles executados.

`gerar.py` reconstrói os PDFs a partir de `produtos.json`, `fichas/`, `logos/`, fotos locais e PDF original. Dependências: PyMuPDF, Pillow, ReportLab; fontes Arial do macOS. Execute `python gerar.py` e `python validar.py`. `preparar.py` documenta a extração inicial das fichas; não precisa ser executado para regenerar o catálogo com os recortes fornecidos. O caminho do original está em `fontes.json`.

Para acrescentar uma peça, adicionar foto e registro a `produtos.json`, e executar `gerar.py`. O gerador reordena e pagina as marcas automaticamente; o total de páginas de uma nova edição deve ser ajustado e validado para o acabamento escolhido. A conferência atual exige os 135 códigos e as 28 páginas desta entrega.
