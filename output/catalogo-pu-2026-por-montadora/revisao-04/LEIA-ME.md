# Revisão 04 - prévia para conferência

Solicitação de 21/10/2026: ordem literal da direção, inclusão de peças ausentes, conferência da foto do 8016 e aumento da fonte do código original.

## Estado recuperado em 21/10/2026

A conferência do catálogo de 2025 foi concluída após a interrupção. Os dois relatórios desta pasta estavam preenchidos com bytes nulos e foram reconstruídos a partir do histórico, dos arquivos preservados e da inspeção visual das páginas. O PDF existente passou novamente pelo script `validar.py`.

## Realizado

- [Prévia em PDF](../../pdf/Catalogo-PU-2026-Revisao-04-PREVIA.pdf): 22 páginas, 142 posições, 126 fichas disponíveis e 16 posições sinalizadas como pendentes.
- Ordem da direção preservada em `ordem-diretoria.json`, inclusive 6057, 6056, 6058 e a linha 0600 depois da 9000.
- Códigos originais em 9 pontos, preto e negrito, presentes em 93 fichas. As transcrições adicionais de 16 fichas estão em `codigos-originais-fichas.json`.
- Até dez fichas por página, leitura pela coluna esquerda e depois pela direita, identidade visual, índice e marcadores preservados.
- 1046A, 1055 e 0611D não constam da nova lista e estão fora desta prévia. Continuam na revisão 03 e no cadastro do site.
- Site, PDFs anteriores e catálogo de amortecedor não foram alterados nesta retomada.

## Conferência do catálogo de 2025

Veja [o relatório com as páginas e referências verificadas](conferencia-catalogo-2025.md). O PDF fornecido é idêntico, por SHA-256, à fonte registrada anteriormente. Nenhuma das 16 referências pendentes nem a 8016 foi encontrada nesta cópia. Não houve ficha nova a incorporar.

## Pendências para concluir

Faltam ficha e foto identificadas como PU para: **1056, 2051, 2062B, 2065, 2066, 2068, 2081C, 2119, 6056, 7034, 7035, 7036, 7038, 7039, 8010 e 0613**.

A 7036 consta da sequência da direção, embora não estivesse na lista inicial de 15 peças faltantes.

A 8016 não consta da sequência solicitada nem do catálogo 2025 fornecido. Para corrigir a fotografia, ainda é necessário identificar a ficha/página mencionada e a foto correta. A troca permanece pendente.

A prévia contém espaços reservados e não está pronta para impressão final. Para prosseguir, é necessária outra versão do catálogo que contenha essas referências ou suas fichas e fotos identificadas.

## Reprodução e validação

Python com PyMuPDF 1.26.7, ReportLab e Pillow:

```sh
python output/catalogo-pu-2026-por-montadora/revisao-04/gerar.py
python output/catalogo-pu-2026-por-montadora/revisao-04/validar.py
```

`conferencia.json` registra as posições. `validacao.json` confere sequência, códigos originais, pendências, links e limites do texto. As imagens de revisão estão em `previas/`.
