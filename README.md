# Catálogo digital Borrachas Rocha

Site estático para consulta de peças e aplicações. Não exige build: `index.html` é o ponto de entrada.

## Publicação

Funciona nas duas opções abaixo:

- **Cloudflare Pages conectado ao GitHub:** crie o projeto apontando para este repositório, selecione `main` e deixe o campo de comando de build vazio. O diretório de publicação é a raiz do repositório (`/`).
- **GitHub Pages:** em *Settings > Pages*, selecione *Deploy from a branch*, a branch `main` e a pasta `/ (root)`.

## Conteúdo do catálogo

- A linha de borracha é pesquisável por código, nome, montadora e aplicação extraída do catálogo.
- A linha de PU traz as referências e aplicações do catálogo de 2024. A imagem em `assets/img/pecas-pu-placeholder.png` é temporária e pode ser trocada por fotos individuais a qualquer momento.
- Os cards mantêm uma área quadrada com `object-fit: contain`; as fotos originais não são recortadas nem esticadas.

Para acrescentar ou corrigir uma aplicação de PU, edite a lista `PU_PRODUCTS` em `catalog.js`.
