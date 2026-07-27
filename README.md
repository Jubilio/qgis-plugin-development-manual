# Desenvolvimento de Plugins QGIS com Python

[![Validar exemplos](https://github.com/Jubilio/qgis-plugin-development-manual/actions/workflows/plugin-checks.yml/badge.svg)](https://github.com/Jubilio/qgis-plugin-development-manual/actions/workflows/plugin-checks.yml)
[![Construir manual](https://github.com/Jubilio/qgis-plugin-development-manual/actions/workflows/build-release.yml/badge.svg)](https://github.com/Jubilio/qgis-plugin-development-manual/actions/workflows/build-release.yml)
[![Publicar livro Quarto](https://github.com/Jubilio/qgis-plugin-development-manual/actions/workflows/publish-quarto.yml/badge.svg)](https://github.com/Jubilio/qgis-plugin-development-manual/actions/workflows/publish-quarto.yml)

Manual em português, do básico ao avançado, com estudos de caso de dois plugins reais:

- [GPX Batch Converter](https://github.com/Jubilio/gpx-batch-converter)
- [GeoClick Capture](https://github.com/Jubilio/qgis-latlon)

**Autor:** Jubílio Filiano Maússe

## Ler online

A versão Quarto oferece pesquisa, navegação por capítulos, tema claro/escuro, links directos para secções e botões para copiar código.

[**Abrir o livro online**](https://jubilio.github.io/qgis-plugin-development-manual/)

## Downloads

A release mais recente disponibiliza:

- manual em PDF;
- versão editável em Word;
- pacote-fonte do repositório;
- hashes SHA-256 para verificação.

[Descarregar a versão mais recente](https://github.com/Jubilio/qgis-plugin-development-manual/releases/latest)

## Conteúdo do repositório

- `manual/manual.md` - fonte canónica do manual;
- `_quarto.yml` - configuração do livro web;
- `index.qmd` - página inicial do livro;
- `scripts/prepare_quarto.py` - geração automática dos capítulos Quarto;
- `examples/minimal_plugin` - estrutura mínima instalável de um plugin QGIS;
- `examples/quick_point_logger` - projecto pedagógico com captura de pontos;
- `snippets` - padrões reutilizáveis para Qt 5/6, tarefas, snapping e rede;
- `checklists` - listas de controlo para desenvolvimento, bugs e publicação;
- `assets/diagrams` - diagramas e respectivas fontes Graphviz;
- `.github/workflows/plugin-checks.yml` - validação de exemplos e estrutura;
- `.github/workflows/build-release.yml` - construção e publicação de PDF/Word;
- `.github/workflows/publish-quarto.yml` - publicação automática no GitHub Pages.

## Temas abordados

O manual cobre o ciclo completo de desenvolvimento:

1. planeamento e arquitectura;
2. estrutura mínima e `classFactory()`;
3. menus, barras de ferramentas, diálogos e painéis laterais;
4. camadas, geometrias, CRS e escrita de ficheiros;
5. tarefas em segundo plano, cancelamento, progresso e logs;
6. ferramentas de mapa, snapping e geocodificação reversa;
7. compatibilidade QGIS 3/4 e Qt 5/6;
8. segurança, testes, empacotamento e CI/CD;
9. releases e submissão ao repositório oficial do QGIS;
10. estudos de caso e construção do Quick Point Logger.

## Validar os exemplos

A compilação verifica a sintaxe sem precisar de iniciar o QGIS:

```bash
python -m compileall -q examples snippets scripts
```

Para executar os plugins, copie a pasta do exemplo para o directório de plugins do perfil QGIS e reinicie ou recarregue o plugin.

## Pré-visualizar o livro Quarto

Instale o [Quarto](https://quarto.org/docs/get-started/) e execute:

```bash
quarto preview
```

O comando `pre-render` gera automaticamente os capítulos em `chapters/` a partir de `manual/manual.md`. Os capítulos e a pasta `_book/` não são guardados no Git.

Para apenas gerar a versão web:

```bash
quarto render --to html
```

## Gerar PDF e Word

Requisitos:

- Python 3 com `python-docx`;
- Pandoc;
- LibreOffice;
- Graphviz.

No Linux ou macOS:

```bash
python -m pip install python-docx
bash build_manual.sh
```

O processo gera os diagramas, cria o documento de referência, converte Markdown para DOCX e exporta o PDF com LibreOffice.

## Licenças

- documentação: Creative Commons Attribution 4.0 International - consulte [`LICENSE-DOCS.md`](LICENSE-DOCS.md);
- exemplos e código: MIT - consulte [`LICENSE`](LICENSE).

## Autor

**Jubílio Filiano Maússe**
