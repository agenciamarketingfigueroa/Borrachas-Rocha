# Revisão 02 — fotografias e tamanho visual

Revisão do catálogo PU 2026 para nova avaliação dos responsáveis.

- 33 fotografias novas com fundo transparente, salvas em `recortes/`.
- Enquadramento calculado pela área visível da peça: caixa de até 91 × 104 pontos, com escala proporcional e centralização. As margens vazias do arquivo não reduzem mais o tamanho da peça na página.
- Mantidos 135 produtos, 28 páginas, ordem por marca, conteúdo técnico, capa 2026 e contracapa. A primeira versão continua na pasta superior.
- 1013A PU continua pendente de fotografia, conforme orientação do usuário.

## Entregas

`Catalogo-PU-2026-Por-Montadora-A4.pdf` é a versão para revisão, com índice clicável. `Catalogo-PU-2026-Por-Montadora-Sangria-3mm.pdf` inclui sangria e área de corte. O arquivo mantém RGB, sem conversão CMYK ou certificação PDF/X.

## Tratamento e reprodução

As fotos foram editadas individualmente com a ferramenta integrada `image_gen.imagegen`, usando as fotografias locais como referência. Os prompts pediram remoção do fundo e preservação de forma, perspectiva, cor, furos e conjuntos. O processamento é generativo, portanto não equivale a uma máscara que conserva literalmente cada pixel; especialmente a foto pequena da 0828C não ganha detalhe fotográfico comprovado pela ampliação. Os originais do cadastro foram preservados.

`edicao-imagens.json` registra fontes, arquivos resultantes e instruções de edição. O tamanho visual é aplicado pelo gerador do PDF, sem deformar os recortes. As fichas antigas continuam com suas fotos incorporadas no original.

Para reconstruir a revisão, executar na pasta superior:

```sh
python gerar.py --revisao-02
python validar.py --revisao-02
```

Dependências: PyMuPDF, Pillow, ReportLab e fontes Arial do macOS. `validacao.json` registra os controles do PDF e da transparência; `conferencia.json` relaciona as referências às páginas.

Esta revisão permanece sujeita à aprovação visual solicitada pelo usuário. Após aprovação, a organização por marca e a escala baseada na área visível podem ser mantidas nas próximas edições.
