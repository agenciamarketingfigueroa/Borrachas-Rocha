# Catálogo PU — edição 2026

- `Catalogo-PU-2026-A4.pdf`: 16 páginas em ordem de leitura, tamanho do original (aproximadamente A4), sem sangria.
- `Catalogo-PU-2026-Grafica-Sangria-3mm.pdf`: as mesmas 16 páginas, com 3 mm de sangria e TrimBox definido. Sem imposição; adequado para a gráfica montar o caderno.
- `previa-pagina-*.png`: capa e páginas acrescentadas para conferência visual.

A capa é a arte original com o ano alterado para 2026. O conteúdo das 13 páginas fornecidas foi preservado; as tarjas laterais também foram atualizadas para 2026. Foram acrescentadas 34 referências do cadastro publicado em `https://borrachasrocha.com.br/catalog.js`, que coincidiu integralmente com o `catalog.js` local na consulta de 18/09/2026.

A referência **0836 PU permanece como bucha do braço transversal traseiro da Pajero TR4 / Pajero IO (2002 a 2015)**, conforme escolha expressa do cliente. Não foi incluída a aplicação conflitante para Iveco Mascarello.

O original repetia a etiqueta 0912 PU na peça com diâmetro externo de 41,5 mm. Essa segunda etiqueta foi corrigida para **0912A PU**, conforme o cadastro do site e a medida correspondente. As demais informações dessa peça foram preservadas.

A referência **1013A PU** está incluída com descrição, aplicação e medida, mas sem fotografia: não há foto no cadastro do site. Nenhuma foto de outra peça foi usada em seu lugar.

As imagens das páginas originais foram mantidas na resolução original, aproximadamente 300 dpi. As novas fotos usam os arquivos do site, sem recorte ou deformação. Fontes dos textos adicionados estão incorporadas. O espaço de cor RGB do material fornecido foi preservado; o arquivo não é uma conversão CMYK ou uma certificação PDF/X. A sangria foi criada por extensão das bordas, sem ampliar a área de corte.

`conferencia.json` registra as referências, fontes e decisões. `validacao.json` registra a verificação de páginas, códigos, fontes e preservação visual do original fora das áreas editadas.

Para regenerar, execute `gerar_catalogo.py` com Python, PyMuPDF, Pillow e ReportLab, passando o caminho do PDF original como primeiro argumento. O script utiliza as fontes Arial instaladas no macOS e as imagens do repositório. O site e os catálogos anteriores não foram alterados.
