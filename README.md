# Catálogo digital Borrachas Rocha

Site estático para consulta de peças e aplicações. Não exige build: `index.html` é o ponto de entrada.

## Publicação

O site é publicado pelo GitHub Pages a partir da branch `main`, pasta `/ (root)`, com domínio personalizado `borrachasrocha.com.br`. O arquivo `CNAME` na raiz registra esse domínio no código. Cada atualização enviada para `main` gera uma nova publicação.

O Cloudflare gerencia o DNS; a hospedagem e o deploy ficam no GitHub Pages. No Cloudflare, configure quatro registros `A` para `@` com os IPs oficiais do GitHub Pages (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`) e um `CNAME` de `www` para `agenciamarketingfigueroa.github.io`. Deixe os registros como **DNS only** durante a validação do domínio e do certificado HTTPS no GitHub. Remova os antigos registros de hospedagem da Nuvemshop em `@` e `www` no momento da migração, preservando quaisquer registros de e-mail e outros serviços.

No GitHub, em *Settings > Pages*, selecione *Deploy from a branch*, `main` e `/ (root)`; depois salve `borrachasrocha.com.br` em *Custom domain* e habilite *Enforce HTTPS* após a validação. No Registro.br, troque os servidores DNS pelos dois nomes exatos fornecidos pelo Cloudflare somente após revisar a zona importada.

## Conteúdo do catálogo

- A linha de borracha é pesquisável por código, nome, montadora e aplicação extraída do catálogo.
- A linha de PU traz as referências, aplicações e fotos individuais do catálogo. As imagens ficam em `assets/img/Peças de PU` e seguem o código da peça (por exemplo, `1026 PU.png`).
- Os cards mantêm uma área quadrada com `object-fit: contain`; as fotos originais não são recortadas nem esticadas.

Para acrescentar ou corrigir uma aplicação de PU, edite a lista `PU_PRODUCTS` em `catalog.js`.

## Pedido pelo WhatsApp

O carrinho funciona sem backend. Peças, quantidades e dados de entrega ficam salvos no `localStorage` do navegador até o cliente usar **Limpar pedido**. A finalização abre o WhatsApp com uma mensagem pronta; o cliente precisa confirmar o envio.

O pedido do cliente abre o WhatsApp de destino `+55 31 99616-5270`, configurado em `WHATSAPP_NUMBER` no arquivo `order.js`. Quando uma peça contém opções de medida identificadas no catálogo, o carrinho mostra uma quantidade independente para cada opção.

## Pedido interno para Expedição

Acesse pelo ícone de entrada no topo do site ou diretamente por `https://borrachasrocha.com.br/interno.html` após a publicação. A senha temporária de teste é `1234`; altere `TEST_PASSWORD` em `interno.js` quando quiser trocar esse código. O acesso fica lembrado somente na aba atual até clicar em **Sair**. Após entrar, escolha **Expedição** para abrir a ferramenta de pedidos, **Catálogo para impressão** para baixar o PDF original em alta qualidade, ou **Catálogo para cliente** para baixar a versão comprimida. A página usa o mesmo catálogo do site. O vendedor informa cliente, prazo e transportadora, busca por código, peça, montadora, aplicação ou descrição, adiciona quantidades e pode preencher o valor unitário de cada medida. Os valores são opcionais. O rascunho fica salvo apenas no `localStorage` do navegador; o resumo também pode ser copiado.

O botão de download na capa pública usa `output/pdf/Catalogo-PU-2026-Clientes.pdf` (5,6 MB). O botão de impressão da área interna usa `output/catalogo-pu-2026-por-montadora/revisao-02/Catalogo-PU-2026-Por-Montadora-A4.pdf` (95,4 MB). A versão para clientes foi gerada em 200 dpi a partir do mesmo catálogo de 28 páginas.

O pedido interno abre o WhatsApp da Expedição `+55 31 3357-1785`, configurado em `WHATSAPP_NUMBER` no arquivo `interno.js`. Para cadastrar preços padrão no futuro, preencha `CATALOG_PRICES_CENTS` no mesmo arquivo, usando o código da peça e o preço em centavos (por exemplo, `'BR-5015': 2590`). O vendedor ainda pode alterar o preço no pedido.

A senha temporária é conferida no JavaScript público: ela funciona como uma tela de entrada para testes, mas não protege os dados nem impede acesso por quem inspeciona o código. O GitHub Pages publica `interno.html` como página pública; `noindex` apenas pede aos buscadores que não a indexem. Antes de usar dados internos sensíveis, será necessário adicionar autenticação em uma hospedagem ou serviço que a suporte. Também não há fila central de pedidos: o envio só é concluído quando o vendedor confirma a mensagem no WhatsApp.

As 33 fotos novas de PU tratadas para a revisão 02 do PDF são usadas também no site. Os arquivos em `assets/img/Peças de PU/recortes/` preservam a transparência e foram aparados pelas bordas visíveis, com 4% de margem e até 900 pixels no maior lado. O script `scripts/prepare-site-cutouts.ps1` refaz esses arquivos a partir de `output/catalogo-pu-2026-por-montadora/revisao-02/recortes/`; a lista de códigos está em `SITE_CUTOUT_CODES` no `catalog.js`. As demais fotos seguem o cadastro original.

## Logos das linhas atendidas

Os botões usam os arquivos em `assets/img/montadoras/`, mapeados em `BRAND_LOGOS` no `catalog.js`. Treze logos vieram dos arquivos já usados no catálogo de PU por montadora. Os demais vieram da [logotipia oficial da Agrale](https://www.agrale.com.br/pt/logotipia), do [download oficial da Kia](https://worldwide.kia.com/en/brand/our-brand/brand-elements/brand-logo-story) e dos registros de [Fiat](https://commons.wikimedia.org/wiki/File:FIAT_logo_(2020).svg) e [Hyundai](https://commons.wikimedia.org/wiki/File:Hyundai_Motor_Company_logo.svg) no Wikimedia Commons. “Linha leve”, “Rodoviária” e “Truck” são categorias, não montadoras, e permanecem em texto.
