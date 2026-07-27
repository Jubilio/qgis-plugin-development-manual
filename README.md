# Desenvolvimento de Plugins QGIS com Python

Manual em português, do básico ao avançado, com estudos de caso de dois plugins reais:

- [GPX Batch Converter](https://github.com/Jubilio/gpx-batch-converter)
- [GeoClick Capture](https://github.com/Jubilio/qgis-latlon)

## Conteúdo do repositório

- `manual/Desenvolvimento_de_Plugins_QGIS_com_Python.pdf` - manual final em PDF;
- `manual/Desenvolvimento_de_Plugins_QGIS_com_Python.docx` - versão editável;
- `manual/manual.md` - fonte principal em Markdown;
- `examples/minimal_plugin` - estrutura mínima instalável de um plugin QGIS;
- `examples/quick_point_logger` - projecto pedagógico com captura de pontos;
- `snippets` - padrões reutilizáveis para Qt 5/6, tarefas, snapping e rede;
- `checklists` - listas de controlo para desenvolvimento, bugs e publicação;
- `assets/diagrams` - diagramas e fontes Graphviz;
- `.github/workflows/plugin-checks.yml` - exemplo de integração contínua;
- `CREATE_REPOSITORY.md` - passos para publicar este pacote num novo repositório GitHub.

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
python -m compileall -q examples snippets
```

Para executar os plugins, copie a pasta do exemplo para o directório de plugins do perfil QGIS e reinicie ou recarregue o plugin.

## Gerar o manual

Requisitos de documentação:

- Python 3 com `python-docx`;
- Pandoc;
- LibreOffice;
- Graphviz, apenas para regenerar os diagramas.

No Linux/macOS:

```bash
bash build_manual.sh
```

O processo cria o documento de referência, converte Markdown para DOCX e exporta o PDF com LibreOffice.

## Publicação no GitHub

Consulte [`CREATE_REPOSITORY.md`](CREATE_REPOSITORY.md). O nome recomendado é:

```text
qgis-plugin-development-manual
```

## Licenças

- documentação: Creative Commons Attribution 4.0 International - consulte `LICENSE-DOCS.md`;
- exemplos e código: MIT - consulte `LICENSE`.

## Autor

**Jubílio Filiano Mausse**
