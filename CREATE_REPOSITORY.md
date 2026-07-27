# Publicar este manual num novo repositório GitHub

## 1. Criar o repositório vazio

No GitHub, seleccione **New repository** e utilize:

- **Repository name:** `qgis-plugin-development-manual`
- **Visibility:** Public
- não adicione README, `.gitignore` ou licença durante a criação, porque estes ficheiros já existem no pacote.

## 2. Publicar com Git

Abra um terminal dentro da pasta extraída e execute:

```bash
git init
git add .
git commit -m "Publish QGIS plugin development manual"
git branch -M main
git remote add origin https://github.com/Jubilio/qgis-plugin-development-manual.git
git push -u origin main
```

## 3. Configurar a página do repositório

Descrição sugerida:

```text
Manual em português para desenvolvimento de plugins QGIS com Python, do básico ao avançado, com exemplos reais e projectos práticos.
```

Tópicos sugeridos:

```text
qgis pyqgis python plugin-development qt6 gis tutorial portuguese
```

## 4. Criar a primeira release

Crie a tag `v1.0.0` e anexe o ficheiro PDF como activo da release. Título sugerido:

```text
Desenvolvimento de Plugins QGIS com Python - v1.0.0
```
