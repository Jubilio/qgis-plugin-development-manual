#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANUAL_DIR="$ROOT/manual"

python "$ROOT/make_reference.py"

pandoc "$MANUAL_DIR/manual.md" \
  -o "$MANUAL_DIR/Desenvolvimento_de_Plugins_QGIS_com_Python.docx" \
  --reference-doc="$MANUAL_DIR/reference.docx" \
  --lua-filter="$MANUAL_DIR/pagebreak.lua" \
  --resource-path="$ROOT" \
  --metadata title="Desenvolvimento de Plugins QGIS com Python" \
  --metadata author="Jubílio Filiano Mausse"

libreoffice --headless --convert-to pdf \
  --outdir "$MANUAL_DIR" \
  "$MANUAL_DIR/Desenvolvimento_de_Plugins_QGIS_com_Python.docx"

echo "Manual criado em: $MANUAL_DIR"
