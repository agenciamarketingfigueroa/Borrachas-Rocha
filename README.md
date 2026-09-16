# Catálogo digital Borrachas Rocha

Site estático para consulta de peças e aplicações. Não exige build: `index.html` é o ponto de entrada.

## Publicação

Funciona nas duas opções abaixo:

- **Cloudflare Pages conectado ao GitHub:** crie o projeto apontando para este repositório, selecione `main` e deixe o campo de comando de build vazio. O diretório de publicação é a raiz do repositório (`/`).
- **GitHub Pages:** em *Settings > Pages*, selecione *Deploy from a branch*, a branch `main` e a pasta `/ (root)`.

## Conteúdo do catálogo

- A linha de borracha é pesquisável por código, nome, montadora e aplicação extraída do catálogo.
- A linha de PU traz as referências, aplicações e fotos individuais do catálogo. As imagens ficam em `assets/img/Peças de PU` e seguem o código da peça (por exemplo, `1026 PU.png`).
- Os cards mantêm uma área quadrada com `object-fit: contain`; as fotos originais não são recortadas nem esticadas.

Para acrescentar ou corrigir uma aplicação de PU, edite a lista `PU_PRODUCTS` em `catalog.js`.

## Pedido pelo WhatsApp

O carrinho funciona sem backend. Peças, quantidades e dados de entrega ficam salvos no `localStorage` do navegador até o cliente usar **Limpar pedido**. A finalização abre o WhatsApp com uma mensagem pronta; o cliente precisa confirmar o envio.

O número de destino está em `WHATSAPP_NUMBER` no arquivo `order.js`. Quando uma peça contém opções de medida identificadas no catálogo, o carrinho mostra uma quantidade independente para cada opção.
