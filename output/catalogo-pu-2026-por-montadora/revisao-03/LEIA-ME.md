# Revisão de 21/10/2026

Atualização baseada nos documentos `Update 21_10_26.pdf` e `Códigos Originais.pdf` fornecidos pelo usuário. A revisão 02 aprovada permanece na pasta vizinha.

## Catálogos

| Uso | Geral de PU | Buchas do amortecedor |
| --- | --- | --- |
| Compartilhar | [PDF leve](Catalogo-PU-2026-Clientes.pdf) | [PDF leve](Catalogo-Buchas-do-Amortecedor-2026-Clientes.pdf) |
| Impressão A4 | [PDF A4](Catalogo-PU-2026-A4.pdf) | [PDF A4](Catalogo-Buchas-do-Amortecedor-2026-A4.pdf) |
| Gráfica, sangria 3 mm | [PDF com sangria](Catalogo-PU-2026-Sangria-3mm.pdf) | [PDF com sangria](Catalogo-Buchas-do-Amortecedor-2026-Sangria-3mm.pdf) |

- Geral: 129 referências, 21 páginas. Amortecedor: 14 referências, 4 páginas.
- Preservadas as fontes Arial/Arial Rounded, cores, moldura lateral, etiquetas com logos e composição de foto e descrição. Capa geral e contracapas preservadas; na capa do amortecedor muda a identificação da linha.
- Até 10 peças por página: cinco na coluna esquerda, seguidas de cinco na direita. As páginas finais de cada seção conservam a sobra, sem omitir referências.
- Ordem das seções: Volkswagen, Mercedes-Benz, Ford, Toyota, Scania, Volvo, Trucks e Carretas, Chevrolet, Iveco, Mitsubishi e Nissan. As famílias iniciadas por zero ficam depois das iniciadas por nove.
- A seção Trucks e Carretas reúne 11 referências em duas páginas (10 + 1), com as marcas agrupadas. A 8027 não recebe uma marca presumida: o documento não informa fabricante.
- As 14 referências indicadas pela diretoria saíram do catálogo geral e aparecem apenas no catálogo de amortecedor, conforme resposta do usuário. Todas continuam disponíveis na busca do site.
- A 0836 foi incluída no catálogo de amortecedor por estar explicitamente na lista da reunião. Sua descrição e aplicação continuam sendo as da ficha aprovada: braço transversal traseiro, Pajero TR4 / IO. A 0636 é uma referência distinta, Iveco.
- Retiradas as notas “Também se aplica” de Ford, Mercedes-Benz e Volkswagen. A nota de Volvo permanece, com as páginas atualizadas.
- 79 referências recebem códigos originais dos anexos, com zeros, letras e referências múltiplas preservados. A busca pública e a busca interna aceitam esses códigos, inclusive sem pontuação.
- Medidas e aplicações complementares do anexo foram incorporadas, incluindo 7012C com furo de 44 mm e 0627 com furo de 33 mm.

## Peças ausentes e recuperação do site

O gerador anterior excluía expressamente a 1013A até a chegada de foto (`fontes.json` e `revisao-02/LEIA-ME.md`). Sua foto foi fornecida agora e a referência foi incluída. Também entraram 0819, 8027, 1012, 0605, 1034, 0636 e 0616.

O cadastro anterior do site possuía 78 referências de PU. Havia 58 referências presentes no PDF, mas ausentes desse cadastro. Elas foram recuperadas das fichas existentes, conferidas visualmente e adicionadas ao site. Com as sete referências que ainda não existiam no site e a atualização da 1013A, o site passa a 143 referências de PU. As imagens dessas 58 fichas foram extraídas do próprio catálogo.

Não foi localizada evidência suficiente para acrescentar estas cinco referências como PU:

| Referência | Situação encontrada |
| --- | --- |
| 1056 | Sem cadastro ou fotografia de PU nos arquivos disponíveis. |
| 2051 | Encontrada somente como BR-2051 na linha de borracha. |
| 2081C | Sem cadastro ou fotografia de PU nos arquivos disponíveis. A 2081B é outra referência. |
| 2119 | Sem cadastro ou fotografia de PU nos arquivos disponíveis. |
| 8010 | Encontrada somente como BR-8010 na linha de borracha. |

Não é possível afirmar por que essas cinco peças não entraram no catálogo anterior com base nos arquivos disponíveis. Não foram convertidas referências de borracha em PU por suposição. A foto `BR 0693 PU.JPG` também ficou sem utilização: não há ficha correspondente nem instrução de inclusão nos anexos.

## Imagens e reprodução

Os oito recortes novos estão em `assets/img/Peças de PU/recortes/`, na raiz do projeto, sob os códigos 0819, 1012, 0605, 1034, 0636, 0616, 1013A e 8027. Os originais foram preservados. Foi usada a ferramenta integrada `image_gen.imagegen` para remover o fundo, com instrução explícita de preservar peça, perspectiva, cor, furos, pinos e textura. O prompt e os caminhos estão em `edicao-imagens.json`. Por ser uma ferramenta generativa, o recorte não representa conservação literal de todos os pixels.

`produtos.json` guarda os dados consolidados; `codigos-originais.json` guarda as referências dos anexos; `geral-conferencia.json` e `amortecedor-conferencia.json` relacionam códigos e páginas. `fichas-transcricao.json` é a leitura auxiliar por OCR, não a fonte técnica final. `site-base.json` preserva o cadastro anterior para reproduzir a consolidação.

Para reconstruir, com Python, PyMuPDF 1.26.7, Pillow e ReportLab:

```sh
python scripts/prepare-catalog-2026-10-21.py
python output/catalogo-pu-2026-por-montadora/revisao-03/gerar.py
python output/catalogo-pu-2026-por-montadora/revisao-03/validar.py
node scripts/test-catalog-2026-10-21.cjs
```

As versões de gráfica mantêm RGB e sangria de 3 mm, como a base. Não houve conversão para CMYK nem certificação PDF/X. As mudanças do site estão no projeto local, sem publicação remota nesta tarefa.
