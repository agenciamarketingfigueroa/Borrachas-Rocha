# Catálogo PU 2026 - edição final de 21/10/2026

22 páginas, 141 referências, 15 novas fichas completas e nenhuma posição pendente.

Arquivos finais em `output/pdf/`:

- `Catalogo-PU-2026-Final-Clientes.pdf`: compartilhamento, índice clicável e texto pesquisável.
- `Catalogo-PU-2026-Final-A4.pdf`: impressão A4, texto novo vetorial e fotografias em alta resolução.
- `Catalogo-PU-2026-Final-Sangria-3mm.pdf`: gráfica, sangria de 3 mm e TrimBox A4.

## Alterações

- Incluídas 1056, 2051, 2062B, 2065, 2066, 2068, 2081C, 2119, 6056, 7034, 7035, 7038, 7039, 8010 e 0613, com os dados enviados na conversa.
- BR 7036 PU retirada por confirmação expressa do usuário. A ordem da revisão 04 foi preservada para todas as demais referências, inclusive 6057, 6056, 6058 e as famílias iniciadas por zero depois da linha 9000.
- BR 0616 PU usa exatamente a mesma imagem da BR 0616A PU: `revisao-02/recortes/0616A PU.png`. Seus próprios dados, incluindo comprimento de 70 mm e código original 93808935, permanecem preservados.
- BR 7039 PU apresenta os dois títulos e suas respectivas aplicações na mesma ficha, na sequência solicitada.
- BR 2051 PU reúne B (28 mm), C (32 mm) e D (36 mm).
- BR 6056 PU inclui o código original 2280638. Não foram acrescentados modelos de veículo não informados.
- Os cabeçalhos das linhas 6000 e 7000 também identificam as aplicações DAF e Scania que compartilham essas seções.
- Os 94 códigos originais ficam em 9 pt, preto e negrito, conforme a revisão 04.
- Capa, contracapa, paleta, tipografia, molduras e até dez fichas por página preservados.

## Fontes e fotografias

`novas-fichas.json` transcreve as 15 fichas enviadas pelo usuário. `produtos.json` consolida esta edição. As medidas foram apenas padronizadas quanto a espaço antes de `mm` e pontuação; nomes e aplicações seguem o conteúdo fornecido. A BR 2081C não recebeu um nome técnico presumido, pois o usuário informou somente medidas e aplicação.

As 15 fotografias novas vêm dos JPG identificados por código em `assets/img/Peças de PU/`. Seus arquivos originais foram preservados, incluindo cor, forma, fundo e detalhes. O PDF respeita a orientação EXIF da câmera e enquadra as peças sem as deformar. Nenhuma imagem de produto foi gerada ou substituída por uma peça semelhante, exceto a reutilização da 0616A solicitada expressamente para a 0616.

O catálogo separado de amortecedor e as versões anteriores permanecem arquivados. Não houve publicação remota ou atualização do cadastro do site nesta entrega. A antiga anotação sobre a foto 8016 não gerou alteração adicional: a correção agora identificada pelo usuário foi aplicada à 0616.

## Validação e reprodução

`conferencia.json` registra páginas, posições, fonte mínima e alterações; `validacao.json` registra a conferência automática. São verificados a ordem completa, medidas e aplicações das novas fichas, os dois títulos da 7039, a identidade da imagem incorporada para 0616/0616A, códigos originais, links, limites de texto e sangria. A revisão visual está em `previas/`.

Requer Python, Pillow, ReportLab e PyMuPDF 1.26.7. No ambiente desta tarefa, PyMuPDF está em `tmp/pdf-final-deps`; o script também pode usar uma instalação normal dessa dependência.

```sh
python output/catalogo-pu-2026-por-montadora/final-2026/preparar.py
python output/catalogo-pu-2026-por-montadora/final-2026/gerar.py
python output/catalogo-pu-2026-por-montadora/final-2026/validar.py
```

A versão de gráfica mantém RGB e sangria de 3 mm, como o projeto anterior; não é uma conversão CMYK ou certificação PDF/X.
