import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=45, bottom=45, left=70, right=70):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_apa_table_borders(table, color="000000", sz_top="8", sz_bottom="8"):
    """
    Bordes estándar APA 7ma Edición en Negro Puro (000000):
    Únicamente borde horizontal superior y borde horizontal inferior de la tabla.
    Sin bordes verticales ni líneas horizontales internas entre filas de datos.
    """
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz_top}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz_bottom}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="none"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_page_number(run):
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def add_p(doc, text="", style='Normal', space_before=0, space_after=1.8, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, font_size=11, font_color=RGBColor(0, 0, 0)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Arial'
        run.font.size = Pt(font_size)
        run.font.color.rgb = font_color
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(13)
    run.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0) # 100% Negro APA 7
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(11.5)
    run.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0) # 100% Negro APA 7
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3.5)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(11)
    run.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0) # 100% Negro APA 7
    return p

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Cm(15.5)
    cell = tbl.cell(0, 0)
    cell.width = Cm(15.5)
    set_cell_background(cell, "FAFAFA")
    set_cell_margins(cell, top=45, bottom=45, left=90, right=90)
    
    # Borde sobrio en negro / gris neutro
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:left w:val="single" w:sz="18" w:space="0" w:color="000000"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(code_text.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(7.5)
    run.font.color.rgb = RGBColor(0, 0, 0) # 100% Negro
    
    # Space after code block
    add_p(doc, "", space_after=1)

def add_apa_figure(doc, figure_num, figure_title, img_path, note_text=None, width_cm=11.5):
    """
    Formato de Figuras en APA 7ma Edición (Arial, 100% Negro):
    1. Línea 1 en Negrita: 'Figura X' (sin punto)
    2. Línea 2 en Cursiva: 'Título descriptivo de la figura'
    3. Imagen centrada
    4. Línea debajo en formato: '*Nota.* Explicación descriptiva...'
    """
    # Línea 1: Figura X en Negrita
    p_num = doc.add_paragraph()
    p_num.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_num.paragraph_format.space_before = Pt(5)
    p_num.paragraph_format.space_after = Pt(0.5)
    p_num.paragraph_format.keep_with_next = True
    r_num = p_num.add_run(f"Figura {figure_num}")
    r_num.font.name = 'Arial'
    r_num.font.size = Pt(10)
    r_num.bold = True
    r_num.font.color.rgb = RGBColor(0, 0, 0)
    
    # Línea 2: Título en Cursiva
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2.5)
    p_title.paragraph_format.keep_with_next = True
    r_title = p_title.add_run(figure_title)
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(9.5)
    r_title.italic = True
    r_title.font.color.rgb = RGBColor(0, 0, 0)
    
    # Imagen centrada
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(1)
        p_img.paragraph_format.space_after = Pt(1)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Cm(width_cm))
    else:
        print(f"Advertencia: No se encontró la imagen {img_path}")
        
    # Nota de figura APA 7
    if note_text:
        p_note = doc.add_paragraph()
        p_note.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_note.paragraph_format.space_before = Pt(1.5)
        p_note.paragraph_format.space_after = Pt(5)
        p_note.paragraph_format.line_spacing = 1.05
        r_lbl = p_note.add_run("Nota. ")
        r_lbl.font.name = 'Arial'
        r_lbl.font.size = Pt(8.5)
        r_lbl.font.italic = True
        r_lbl.font.color.rgb = RGBColor(0, 0, 0)
        r_txt = p_note.add_run(note_text)
        r_txt.font.name = 'Arial'
        r_txt.font.size = Pt(8.5)
        r_txt.font.color.rgb = RGBColor(0, 0, 0)

def add_apa_table(doc, table_num, table_title, col_widths, headers, rows_data, note_text=None):
    """
    Formato de Tablas en APA 7ma Edición (Arial, 100% Negro):
    1. Línea 1 en Negrita: 'Tabla X' (sin punto)
    2. Línea 2 en Cursiva: 'Título descriptivo de la tabla'
    3. Bordes de tabla: Únicamente borde superior de tabla, inferior de encabezado e inferior de tabla en color negro (000000).
       Sin bordes verticales ni líneas horizontales internas entre filas.
    4. Encabezados: Fondo blanco/transparente, texto en Arial negrita negro.
    5. Celdas: Texto en Arial negro.
    6. Línea debajo en formato: '*Nota.* Explicación de la tabla...' en Arial negro.
    """
    # Línea 1: Tabla X en Negrita
    p_num = doc.add_paragraph()
    p_num.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_num.paragraph_format.space_before = Pt(5)
    p_num.paragraph_format.space_after = Pt(0.5)
    p_num.paragraph_format.keep_with_next = True
    r_num = p_num.add_run(f"Tabla {table_num}")
    r_num.font.name = 'Arial'
    r_num.font.size = Pt(10)
    r_num.bold = True
    r_num.font.color.rgb = RGBColor(0, 0, 0)
    
    # Línea 2: Título en Cursiva
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2.5)
    p_title.paragraph_format.keep_with_next = True
    r_title = p_title.add_run(table_title)
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(9.5)
    r_title.italic = True
    r_title.font.color.rgb = RGBColor(0, 0, 0)
    
    # Creación de tabla
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Aplicar bordes exteriores e internos conforme a APA 7 en Negro puro
    set_apa_table_borders(table, color="000000", sz_top="8", sz_bottom="8")
    
    # Encabezado (Fila 0)
    tr0 = table.rows[0]._tr.get_or_add_trPr()
    tr0.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    tr0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = Cm(col_widths[i])
        set_cell_margins(hdr_cells[i], top=40, bottom=40, left=50, right=50)
        set_cell_background(hdr_cells[i], "FFFFFF") # Fondo blanco sin relleno azul
        
        # Borde inferior del encabezado en Negro (Línea separadora APA 7)
        tcPr = hdr_cells[i]._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:tcBorders {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/></w:tcBorders>'))
        
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(title)
        r.font.name = 'Arial'
        r.font.size = Pt(9.0)
        r.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0) # 100% Negro
        
    # Filas de datos
    for r_idx, row in enumerate(rows_data):
        row_obj = table.add_row()
        tr = row_obj._tr.get_or_add_trPr()
        tr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        row_cells = row_obj.cells
        for c_idx, val in enumerate(row):
            row_cells[c_idx].width = Cm(col_widths[c_idx])
            set_cell_margins(row_cells[c_idx], top=30, bottom=30, left=50, right=50)
            set_cell_background(row_cells[c_idx], "FFFFFF")
            p = row_cells[c_idx].paragraphs[0]
            if len(str(val)) <= 8 or c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            r = p.add_run(str(val))
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(0, 0, 0) # 100% Negro
            
    # Nota APA 7 al pie de la tabla
    if note_text:
        p_note = doc.add_paragraph()
        p_note.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_note.paragraph_format.space_before = Pt(1.5)
        p_note.paragraph_format.space_after = Pt(5)
        p_note.paragraph_format.line_spacing = 1.05
        r_lbl = p_note.add_run("Nota. ")
        r_lbl.font.name = 'Arial'
        r_lbl.font.size = Pt(8.5)
        r_lbl.font.italic = True
        r_lbl.font.color.rgb = RGBColor(0, 0, 0)
        r_txt = p_note.add_run(note_text)
        r_txt.font.name = 'Arial'
        r_txt.font.size = Pt(8.5)
        r_txt.font.color.rgb = RGBColor(0, 0, 0)

# Compatibilidad con llamadas legacy
def add_image_figure(doc, img_path, caption_text, width_cm=11.2):
    add_apa_figure(doc, "1", caption_text, img_path, width_cm=width_cm)

def format_styled_table(table, col_widths, headers, rows_data):
    set_apa_table_borders(table, color="000000")
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = Cm(col_widths[i])
        set_cell_margins(hdr_cells[i], top=40, bottom=40, left=50, right=50)
        set_cell_background(hdr_cells[i], "FFFFFF")
        tcPr = hdr_cells[i]._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:tcBorders {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/></w:tcBorders>'))
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.font.name = 'Arial'
        r.font.size = Pt(9.0)
        r.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
    for r_idx, row in enumerate(rows_data):
        row_cells = table.add_row().cells
        for c_idx, val in enumerate(row):
            row_cells[c_idx].width = Cm(col_widths[c_idx])
            set_cell_margins(row_cells[c_idx], top=30, bottom=30, left=50, right=50)
            set_cell_background(row_cells[c_idx], "FFFFFF")
            p = row_cells[c_idx].paragraphs[0]
            r = p.add_run(str(val))
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(0, 0, 0)
