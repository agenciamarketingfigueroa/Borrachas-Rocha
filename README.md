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

O número de destino está em `WHATSAPP_NUMBER` no arquivo `order.js`. Quando uma peça contém opções de medida identificadas no catálogo, o carrinho mostra uma quantidade independente para cada opção.
