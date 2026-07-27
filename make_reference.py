from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

TEAL = RGBColor(11, 79, 92)
ORANGE = RGBColor(231, 122, 34)
DARK = RGBColor(32, 46, 49)
MUTED = RGBColor(92, 112, 115)


def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd')
        tcPr.append(shd)
    shd.set(qn('w:fill'), fill)


doc = Document()
sec = doc.sections[0]
sec.page_width = Cm(21)
sec.page_height = Cm(29.7)
sec.top_margin = Cm(2.0)
sec.bottom_margin = Cm(1.8)
sec.left_margin = Cm(2.2)
sec.right_margin = Cm(2.0)
sec.header_distance = Cm(0.8)
sec.footer_distance = Cm(0.8)

styles = doc.styles
normal = styles['Normal']
normal.font.name = 'Aptos'
normal.font.size = Pt(10.5)
normal.font.color.rgb = DARK
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.12

for name, size, color, before, after in [
    ('Title', 28, TEAL, 0, 16),
    ('Subtitle', 15, MUTED, 0, 10),
    ('Heading 1', 20, TEAL, 18, 8),
    ('Heading 2', 15, TEAL, 14, 6),
    ('Heading 3', 12, ORANGE, 10, 4),
    ('Heading 4', 11, TEAL, 8, 3),
]:
    st = styles[name]
    st.font.name = 'Aptos Display' if name in ('Title','Heading 1','Heading 2') else 'Aptos'
    st.font.size = Pt(size)
    st.font.bold = name != 'Subtitle'
    st.font.color.rgb = color
    st.paragraph_format.space_before = Pt(before)
    st.paragraph_format.space_after = Pt(after)
    st.paragraph_format.keep_with_next = True

if 'Block Text' in styles:
    styles['Block Text'].font.name = 'Aptos'
    styles['Block Text'].font.size = Pt(10)
    styles['Block Text'].font.color.rgb = DARK

# Pandoc uses Source Code / Verbatim Char if present.
for style_name in ('Source Code', 'Verbatim Char'):
    if style_name in styles:
        st = styles[style_name]
        st.font.name = 'DejaVu Sans Mono'
        st.font.size = Pt(8.3)
        st.font.color.rgb = RGBColor(30, 45, 48)
        if hasattr(st, 'paragraph_format'):
            st.paragraph_format.space_before = Pt(4)
            st.paragraph_format.space_after = Pt(6)

# Hyperlink style
if 'Hyperlink' in styles:
    styles['Hyperlink'].font.color.rgb = TEAL
    styles['Hyperlink'].font.underline = True

# Table normal
if 'Table' in styles:
    styles['Table'].font.name = 'Aptos'
    styles['Table'].font.size = Pt(9)

# Header/footer placeholders are inherited by pandoc output.
header = sec.header
p = header.paragraphs[0]
p.text = 'DESENVOLVIMENTO DE PLUGINS QGIS COM PYTHON'
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = p.runs[0]
r.font.name = 'Aptos'
r.font.size = Pt(8)
r.font.color.rgb = MUTED

footer = sec.footer
p = footer.paragraphs[0]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Jubílio Filiano Mausse  |  ')
r.font.name = 'Aptos'
r.font.size = Pt(8)
r.font.color.rgb = MUTED
fldChar1 = OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'), 'begin')
instrText = OxmlElement('w:instrText'); instrText.set(qn('xml:space'), 'preserve'); instrText.text = ' PAGE '
fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'), 'end')
r._r.append(fldChar1); r._r.append(instrText); r._r.append(fldChar2)

doc.save('/mnt/data/qgis-plugin-development-manual/manual/reference.docx')
