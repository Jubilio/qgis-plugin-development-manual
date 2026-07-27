#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANUAL_DIR="$ROOT/manual"
DIAGRAM_DIR="$ROOT/assets/diagrams"

mkdir -p "$MANUAL_DIR"

for source in "$DIAGRAM_DIR"/*.dot; do
  dot -Tpng "$source" -o "${source%.dot}.png"
done

python "$ROOT/make_reference.py"

pandoc "$MANUAL_DIR/manual.md" \
  -o "$MANUAL_DIR/Desenvolvimento_de_Plugins_QGIS_com_Python.docx" \
  --reference-doc="$MANUAL_DIR/reference.docx" \
  --lua-filter="$MANUAL_DIR/pagebreak.lua" \
  --resource-path="$ROOT" \
  --metadata title="Desenvolvimento de Plugins QGIS com Python" \
  --metadata author="Jubílio Filiano Maússe"

libreoffice --headless --convert-to pdf \
  --outdir "$MANUAL_DIR" \
  "$MANUAL_DIR/Desenvolvimento_de_Plugins_QGIS_com_Python.docx"

echo "Manual criado em: $MANUAL_DIR"
