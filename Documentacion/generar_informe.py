import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from soporte_informe import (
    set_cell_background, set_cell_margins, set_table_borders,
    add_page_number, add_p, add_heading_1, add_heading_2, add_heading_3,
    add_code_block, add_apa_figure, add_apa_table
)

def crear_informe_completo(docx_path):
    doc = Document()
    
    # =========================================================================
    # CONFIGURACIÓN DE PÁGINA A4 Y MÁRGENES UNAMAD
    # (A4, Arial 11pt, 1.5 espacio, Justificado, Izq: 3.0 cm, Sup/Inf/Der: 2.5 cm, 100% Negro)
    # =========================================================================
    section = doc.sections[0]
    section.page_width = Inches(8.27)   # 21.0 cm
    section.page_height = Inches(11.69) # 29.7 cm
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.5)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)

    # Encabezado institucional UNAMAD (Arial, Negro)
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("UNAMAD – Ingeniería de Sistemas e Informática | Desarrollo de Aplicaciones Móviles II (2026-II)")
    hrun.font.name = 'Arial'
    hrun.font.size = Pt(8.5)
    hrun.font.italic = True
    hrun.font.color.rgb = RGBColor(0, 0, 0)

    # Pie de página con numeración y nombre del sistema (Arial, Negro)
    footer = section.footer
    tbl_footer = footer.add_table(rows=1, cols=2, width=Cm(15.5))
    tbl_footer.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left = tbl_footer.cell(0, 0)
    c_right = tbl_footer.cell(0, 1)
    c_left.width = Cm(10.5)
    c_right.width = Cm(5.0)
    
    p_fleft = c_left.paragraphs[0]
    p_fleft.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_fleft = p_fleft.add_run("VotaApp UNAMAD – Sistema Móvil de Encuestas y Votaciones")
    r_fleft.font.name = 'Arial'
    r_fleft.font.size = Pt(8.5)
    r_fleft.font.color.rgb = RGBColor(0, 0, 0)

    p_fright = c_right.paragraphs[0]
    p_fright.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_fpage = p_fright.add_run("Página ")
    r_fpage.font.name = 'Arial'
    r_fpage.font.size = Pt(8.5)
    r_fpage.font.color.rgb = RGBColor(0, 0, 0)
    add_page_number(r_fpage)

    # Rutas de recursos
    base_dir = r"C:\Users\HP\AndroidStudioProjects\ProyectoFinal\Documentacion"
    diag_dir = os.path.join(base_dir, "diagramas")
    cap_dir = os.path.join(base_dir, "capturas")
    icon_path = r"C:\Users\HP\AndroidStudioProjects\ProyectoFinal\app\src\main\res\drawable\encuesta.png"

    # =========================================================================
    # 4.1. PORTADA OFICIAL (Arial, 100% Negro)
    # =========================================================================
    add_p(doc, "UNIVERSIDAD NACIONAL AMAZÓNICA DE MADRE DE DIOS", space_before=4, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=14.5, font_color=RGBColor(0, 0, 0))
    add_p(doc, "FACULTAD DE INGENIERÍA", space_before=0, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11.5, font_color=RGBColor(0, 0, 0))
    add_p(doc, "ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS E INFORMÁTICA", space_before=0, space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=12, font_color=RGBColor(0, 0, 0))

    if os.path.exists(icon_path):
        p_ic = doc.add_paragraph()
        p_ic.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ic.paragraph_format.space_before = Pt(2)
        p_ic.paragraph_format.space_after = Pt(8)
        r_ic = p_ic.add_run()
        r_ic.add_picture(icon_path, width=Cm(3.0))

    add_p(doc, "INFORME TÉCNICO DE PROYECTO FINAL", space_before=2, space_after=3, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11.5, font_color=RGBColor(0, 0, 0))
    add_p(doc, "“DESARROLLO E IMPLEMENTACIÓN DE UNA APLICACIÓN MÓVIL NATIVA EN KOTLIN PARA LA GESTIÓN DE ENCUESTAS, VOTACIONES Y CONTEO DE RESULTADOS”", space_before=1, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=12.5, font_color=RGBColor(0, 0, 0))
    add_p(doc, "(Sistema VotaApp UNAMAD - com.example.proyectofinal)", space_before=0, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, font_size=10, font_color=RGBColor(0, 0, 0))

    # Tabla de Datos de Portada
    t_portada = doc.add_table(rows=4, cols=2)
    t_portada.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_portada.autofit = False
    set_table_borders(t_portada, color="FFFFFF", sz="0", val="none")
    
    portada_data = [
        ("ASIGNATURA:", "Desarrollo de Aplicaciones Móviles II"),
        ("SEMESTRE ACADÉMICO:", "2026-II"),
        ("DOCENTE:", "Ing. Laura Salvatierra, Leonel Christofher"),
        ("INTEGRANTES:", "Amezquita Camargo, Maicol Alberto\nTorres Saire, Bickmer Fabricio")
    ]
    for idx, (label, val) in enumerate(portada_data):
        c0 = t_portada.rows[idx].cells[0]
        c1 = t_portada.rows[idx].cells[1]
        c0.width = Cm(5.5)
        c1.width = Cm(10.0)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(label)
        r0.font.name = 'Arial'
        r0.font.size = Pt(9.5)
        r0.bold = True
        r0.font.color.rgb = RGBColor(0, 0, 0)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r1 = p1.add_run(val)
        r1.font.name = 'Arial'
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0, 0, 0)

    add_p(doc, "Puerto Maldonado – Madre de Dios – Perú\n2026", space_before=18, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=10, font_color=RGBColor(0, 0, 0))
    doc.add_page_break()

    # =========================================================================
    # 4.2. ÍNDICE GENERAL, ÍNDICE DE FIGURAS E ÍNDICE DE TABLAS
    # =========================================================================
    p_ind_title = doc.add_paragraph()
    p_ind_title.paragraph_format.space_before = Pt(4)
    p_ind_title.paragraph_format.space_after = Pt(2)
    p_ind_title.paragraph_format.keep_with_next = True
    r_itit = p_ind_title.add_run("ÍNDICE GENERAL")
    r_itit.font.name = 'Arial'
    r_itit.font.size = Pt(12)
    r_itit.bold = True
    r_itit.font.color.rgb = RGBColor(0, 0, 0)
    
    indice_items = [
        ("INTRODUCCIÓN", "3"),
        ("CAPÍTULO I. DESCRIPCIÓN DEL PROYECTO", "4"),
        ("    1.1. Nombre del Proyecto", "4"),
        ("    1.2. Descripción del problema", "4"),
        ("    1.3. Objetivos (General y Específicos)", "5"),
        ("    1.4. Justificación (Técnica, Práctica, Académica y Social)", "6"),
        ("    1.5. Alcance y Limitaciones", "6"),
        ("    1.6. Usuarios Beneficiarios", "7"),
        ("CAPÍTULO II. ANÁLISIS DE REQUERIMIENTOS", "7"),
        ("    2.1. Requerimientos Funcionales (RF01 - RF08)", "7"),
        ("    2.2. Requerimientos No Funcionales (RNF01 - RNF05)", "8"),
        ("    2.3. Diagrama de Casos de Uso del Sistema", "8"),
        ("    2.4. Especificación Detallada de Casos de Uso (CU01 - CU02)", "9"),
        ("CAPÍTULO III. DISEÑO DE LA APLICACIÓN MÓVIL", "11"),
        ("    3.1. Arquitectura de la Aplicación en Tres Capas", "11"),
        ("    3.2. Diseño de Interfaces de Usuario (Prototipos Móviles)", "12"),
        ("    3.3. Diagrama de Navegación y Flujo de Pantallas", "14"),
        ("    3.4. Diseño de Base de Datos y Diccionario de Datos Relacional", "14"),
        ("CAPÍTULO IV. DESARROLLO E IMPLEMENTACIÓN", "17"),
        ("    4.1. Herramientas y Tecnologías Utilizadas", "17"),
        ("    4.2. Estructura del Proyecto en Android Studio", "17"),
        ("    4.3. Implementación de Funcionalidades por Módulos y Código Fuente Real", "18"),
        ("    4.4. Gestión y Almacenamiento de Datos en SQLite", "21"),
        ("    4.5. Componentes Adicionales de Validación y Experiencia de Usuario", "21"),
        ("CAPÍTULO V. PRUEBAS Y RESULTADOS", "22"),
        ("    5.1. Matriz Exhaustiva de Pruebas Funcionales (CP01 - CP10)", "22"),
        ("    5.2. Evidencias de Ejecución y Validación en Emulador", "23"),
        ("    5.3. Dificultades Técnicas Identificadas y Soluciones Implementadas", "25"),
        ("    5.4. Evaluación de Cumplimiento y Resultados", "26"),
        ("CONCLUSIONES Y RECOMENDACIONES", "26"),
        ("REFERENCIAS BIBLIOGRÁFICAS", "27")
    ]

    t_toc = doc.add_table(rows=0, cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_toc.autofit = False
    set_table_borders(t_toc, color="FFFFFF", sz="0", val="none")
    
    for tit, pag in indice_items:
        r_toc = t_toc.add_row().cells
        r_toc[0].width = Cm(14.0)
        r_toc[1].width = Cm(1.5)
        
        p0 = r_toc[0].paragraphs[0]
        p0.paragraph_format.space_before = Pt(0.2)
        p0.paragraph_format.space_after = Pt(0.2)
        p0.paragraph_format.line_spacing = 1.0
        rt = p0.add_run(tit)
        rt.font.name = 'Arial'
        rt.font.size = Pt(8.5)
        rt.bold = True if ("CAPÍTULO" in tit or "INTRODUCCIÓN" in tit or "CONCLUSIONES" in tit or "REFERENCIAS" in tit) else False
        rt.font.color.rgb = RGBColor(0, 0, 0)
            
        p1 = r_toc[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(0.2)
        p1.paragraph_format.space_after = Pt(0.2)
        p1.paragraph_format.line_spacing = 1.0
        rp = p1.add_run(pag)
        rp.font.name = 'Arial'
        rp.font.size = Pt(8.5)
        rp.bold = True if ("CAPÍTULO" in tit or "INTRODUCCIÓN" in tit) else False
        rp.font.color.rgb = RGBColor(0, 0, 0)

    # Índice de Figuras
    p_fig_title = doc.add_paragraph()
    p_fig_title.paragraph_format.space_before = Pt(4)
    p_fig_title.paragraph_format.space_after = Pt(1.5)
    p_fig_title.paragraph_format.keep_with_next = True
    r_ftit = p_fig_title.add_run("ÍNDICE DE FIGURAS")
    r_ftit.font.name = 'Arial'
    r_ftit.font.size = Pt(10)
    r_ftit.bold = True
    r_ftit.font.color.rgb = RGBColor(0, 0, 0)

    figuras_items = [
        ("Figura 1. Diagrama de Casos de Uso del Sistema VotaApp UNAMAD", "9"),
        ("Figura 2. Diagrama de Arquitectura Modular en Tres Capas Sincronizado", "12"),
        ("Figura 3. Prototipos de Pantallas: Panel Principal, Creación y Preguntas", "13"),
        ("Figura 4. Prototipos de Pantallas: Registro de Votación y Conteo de Resultados", "14"),
        ("Figura 5. Diagrama de Estados y Navegación entre Pantallas Móviles", "14"),
        ("Figura 6. Diagrama Entidad-Relación de la Base de Datos SQLite", "15"),
        ("Figura 7. Estructura Oficial de Paquetes y Recursos en Android Studio", "18"),
        ("Figura 8. Capturas Reales en Emulador: Panel Principal, Edición y Preguntas", "24"),
        ("Figura 9. Capturas Reales en Emulador: Votación Dinámica y Conteo de Resultados", "25")
    ]
    t_fig_toc = doc.add_table(rows=0, cols=2)
    t_fig_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_fig_toc.autofit = False
    set_table_borders(t_fig_toc, color="FFFFFF", sz="0", val="none")
    for tit, pag in figuras_items:
        r_f = t_fig_toc.add_row().cells
        r_f[0].width = Cm(14.0)
        r_f[1].width = Cm(1.5)
        pf0 = r_f[0].paragraphs[0]
        pf0.paragraph_format.space_before = Pt(0.2)
        pf0.paragraph_format.space_after = Pt(0.2)
        pf0.paragraph_format.line_spacing = 1.0
        rf0 = pf0.add_run(tit)
        rf0.font.name = 'Arial'
        rf0.font.size = Pt(8.0)
        rf0.font.italic = True
        rf0.font.color.rgb = RGBColor(0, 0, 0)
        pf1 = r_f[1].paragraphs[0]
        pf1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        pf1.paragraph_format.space_before = Pt(0.2)
        pf1.paragraph_format.space_after = Pt(0.2)
        pf1.paragraph_format.line_spacing = 1.0
        rf1 = pf1.add_run(pag)
        rf1.font.name = 'Arial'
        rf1.font.size = Pt(8.0)
        rf1.font.color.rgb = RGBColor(0, 0, 0)

    # Índice de Tablas
    p_tab_title = doc.add_paragraph()
    p_tab_title.paragraph_format.space_before = Pt(4)
    p_tab_title.paragraph_format.space_after = Pt(1.5)
    p_tab_title.paragraph_format.keep_with_next = True
    r_ttit = p_tab_title.add_run("ÍNDICE DE TABLAS")
    r_ttit.font.name = 'Arial'
    r_ttit.font.size = Pt(10)
    r_ttit.bold = True
    r_ttit.font.color.rgb = RGBColor(0, 0, 0)

    tablas_items = [
        ("Tabla 1. Especificación de Requerimientos Funcionales (RF01 - RF08)", "7"),
        ("Tabla 2. Especificación de Requerimientos No Funcionales (RNF01 - RNF05)", "8"),
        ("Tabla 3. Diccionario de Datos: Tabla 'encuestas'", "15"),
        ("Tabla 4. Diccionario de Datos: Tabla 'preguntas'", "16"),
        ("Tabla 5. Diccionario de Datos: Tabla 'alternativas'", "16"),
        ("Tabla 6. Diccionario de Datos: Tabla 'respuestas'", "16"),
        ("Tabla 7. Stack de Herramientas y Tecnologías de Desarrollo", "17"),
        ("Tabla 8. Matriz de Casos de Prueba Funcionales (CP01 - CP10)", "22"),
        ("Tabla 9. Matriz de Dificultades Técnicas y Soluciones de Ingeniería", "25"),
        ("Tabla 10. Matriz de Trazabilidad y Evaluación de Cumplimiento", "26")
    ]
    t_tab_toc = doc.add_table(rows=0, cols=2)
    t_tab_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tab_toc.autofit = False
    set_table_borders(t_tab_toc, color="FFFFFF", sz="0", val="none")
    for tit, pag in tablas_items:
        r_t = t_tab_toc.add_row().cells
        r_t[0].width = Cm(14.0)
        r_t[1].width = Cm(1.5)
        pt0 = r_t[0].paragraphs[0]
        pt0.paragraph_format.space_before = Pt(0.2)
        pt0.paragraph_format.space_after = Pt(0.2)
        pt0.paragraph_format.line_spacing = 1.0
        rt0 = pt0.add_run(tit)
        rt0.font.name = 'Arial'
        rt0.font.size = Pt(8.0)
        rt0.font.italic = True
        rt0.font.color.rgb = RGBColor(0, 0, 0)
        pt1 = r_t[1].paragraphs[0]
        pt1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        pt1.paragraph_format.space_before = Pt(0.2)
        pt1.paragraph_format.space_after = Pt(0.2)
        pt1.paragraph_format.line_spacing = 1.0
        rt1 = pt1.add_run(pag)
        rt1.font.name = 'Arial'
        rt1.font.size = Pt(8.0)
        rt1.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_page_break()

    # =========================================================================
    # 4.3. INTRODUCCIÓN (Con Citas APA 7 Integradas, 100% Negro)
    # =========================================================================
    add_heading_1(doc, "INTRODUCCIÓN")
    add_p(doc, "La evolución continua de las tecnologías móviles y la masificación de los teléfonos inteligentes basados en el sistema operativo Android han transformado radicalmente la manera en que las organizaciones y comunidades académicas interactúan, recopilan opiniones y toman decisiones colegiadas. Tal como señalan Pressman y Maxim (2021), la ingeniería de software aplicada a dispositivos móviles exige metodologías rigurosas que armonicen la agilidad del desarrollo con la robustez arquitectónica y la satisfacción de requerimientos del usuario final. En el ámbito universitario contemporáneo, particularmente en la Universidad Nacional Amazónica de Madre de Dios (UNAMAD), la participación activa y democrática de la comunidad estudiantil y docente en consultas académicas, encuestas de percepción sobre la calidad del servicio educativo, y elecciones de delegados o representantes gremiales constituye un pilar esencial para la gobernanza y el aseguramiento continuo de la calidad formativa, en concordancia con los estándares de calidad en sistemas de información (ISO/IEC, 2011).")
    add_p(doc, "A pesar de estos imperativos democráticos y de gestión de calidad, tradicionalmente una considerable proporción de estos procesos se ha venido ejecutando de forma manual mediante cédulas de votación impresas en papel o a través de plataformas web genéricas que no siempre se adecúan al contexto local. Como advierte Sommerville (2019), los procesos basados en soportes físicos o plataformas desconectadas del contexto operativo introducen cuellos de botella críticos: consumo excesivo de papel, demoras sustanciales en el escrutinio y conteo de votos, vulnerabilidad ante errores humanos de tabulación, elevados costos logísticos y una marcada ausencia de inmediatez en la publicación de resultados. Por otro lado, aunque existen servicios de formularios en línea, estos suelen exigir una conectividad permanente a internet de alta velocidad —la cual resulta intermitente en diversas áreas de la región de Madre de Dios— y carecen de un control robusto de unicidad de voto a nivel local que garantice la transparencia del escrutinio en el aula.")
    add_p(doc, "Ante esta problemática concreta, el presente proyecto final, desarrollado en el marco de la asignatura Desarrollo de Aplicaciones Móviles II del semestre académico 2026-II en la Escuela Profesional de Ingeniería de Sistemas e Informática, propone el diseño, construcción e implementación del “Sistema Móvil de Encuestas y Votaciones (VotaApp UNAMAD)”. Dicha solución consiste en una aplicación móvil nativa desarrollada íntegramente en el lenguaje de programación Kotlin (JetBrains, 2024) utilizando el entorno de desarrollo integrado Android Studio, con persistencia local relacional estructurada mediante SQLiteOpenHelper en la base de datos encuestas_unamad.db, siguiendo las directrices oficiales de desarrollo móvil (Google Developers, 2024).")
    add_p(doc, "El sistema VotaApp UNAMAD se concibe con una arquitectura robusta de tres capas (Presentación, Lógica de Negocio y Persistencia de Datos), permitiendo a los creadores de encuestas y administradores formular instrumentos de consulta clasificados por categorías, parametrizar preguntas dinámicas tanto de selección única como de selección múltiple, gestionar alternativas de respuesta con reglas de integridad referencial, registrar la participación de los votantes verificando de forma estricta la no duplicidad de votos por persona mediante el método yaVotoParticipante, y procesar en tiempo real métricas estadísticas con representaciones visuales horizontales de barras de progreso ProgressBar y determinación automática de la opción ganadora.")
    add_p(doc, "El presente informe técnico expone detalladamente cada una de las fases de ingeniería de software aplicadas en la concepción y materialización de la aplicación, abarcando la delimitación del problema, la formalización de requerimientos funcionales y no funcionales, el modelado formal de casos de uso y arquitectura, el diseño de interfaces y prototipos móviles, el modelado entidad-relación de la base de datos SQLite, la descripción de la implementación con fragmentos de código fuente en Kotlin sincronizados al 100% con el proyecto compilado, y la batería exhaustiva de pruebas funcionales ejecutadas para garantizar la estabilidad, rendimiento y confiabilidad del sistema en dispositivos Android conforme al estándar ISO/IEC 25010 (ISO/IEC, 2011).")

    # =========================================================================
    # CAPÍTULO I. DESCRIPCIÓN DEL PROYECTO (100% Negro)
    # =========================================================================
    add_heading_1(doc, "CAPÍTULO I. DESCRIPCIÓN DEL PROYECTO")
    
    add_heading_2(doc, "1.1. Nombre del Proyecto")
    add_p(doc, "El proyecto se denomina oficialmente:")
    add_p(doc, "“Sistema Móvil de Encuestas y Votaciones (VotaApp UNAMAD)”", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11, font_color=RGBColor(0, 0, 0))
    add_p(doc, "Paquete oficial Android: com.example.proyectofinal. Esta aplicación móvil nativa está concebida como una herramienta integral, portable y offline-first para la gestión de consultas de opinión, diagnósticos situacionales y sufragios internos en la Universidad Nacional Amazónica de Madre de Dios.")

    add_heading_2(doc, "1.2. Descripción del Problema")
    add_p(doc, "En las instituciones universitarias públicas peruanas, y específicamente en la UNAMAD, los procesos participativos de recolección de información constituyen actividades de frecuencia cotidiana. Estos abarcan desde la elección de delegados de aula en cada ciclo académico, la evaluación diagnóstica de infraestructura y laboratorios, hasta encuestas de satisfacción sobre servicios universitarios como comedor, biblioteca, conectividad y actividades extracurriculares.")
    add_p(doc, "No obstante, la gestión operativa de estos procesos enfrenta tres deficiencias estructurales:")
    add_p(doc, "1. Ineficiencia y lentitud operativa: La recolección manual de votos mediante boletas físicas demanda horas de preparación de material impreso, distribución física y un proceso de conteo manual propenso a equivocaciones involuntarias, tachas dudosas y fatiga de los escrutadores.")
    add_p(doc, "2. Brechas de conectividad y dependencia de la nube: El uso improvisado de formularios web comerciales en aulas a menudo colapsa debido a la sobrecarga de la red Wi-Fi institucional o la ausencia de planes de datos móviles en los teléfonos de los estudiantes, impidiendo que el 100% de los convocados pueda votar sincrónicamente. Frente a este escenario, Hipp (2024) fundamenta que los motores de base de datos embebidos como SQLite proporcionan una solución idónea para entornos offline-first, garantizando transacciones atómicas e inmediatas directamente en el almacenamiento local del dispositivo anfitrión.")
    add_p(doc, "3. Carencia de control de duplicidad y auditoría local: Muchos sistemas informales carecen de validaciones estrictas para garantizar que un participante no emita votos reiterados bajo identidades falsas o selecciones incompletas, comprometiendo la legitimidad del escrutinio final.")
    add_p(doc, "Por consiguiente, se identificó la urgente necesidad de concebir una aplicación móvil nativa que opere con almacenamiento local en SQLite (garantizando total autonomía operativa aun sin acceso a internet), dotada de validaciones de integridad referencial, verificación de voto único por participante y generación automática de métricas visuales.")

    add_heading_2(doc, "1.3. Objetivos")
    add_heading_3(doc, "1.3.1. Objetivo General")
    add_p(doc, "Desarrollar e implementar una aplicación móvil nativa en Kotlin para el sistema operativo Android, que permita la administración integral de encuestas, la configuración dinámica de preguntas y alternativas, el registro controlado de votaciones con verificación de voto único y el procesamiento visual de resultados estadísticos en tiempo real para la comunidad de la Universidad Nacional Amazónica de Madre de Dios.")
    
    add_heading_3(doc, "1.3.2. Objetivos Específicos")
    add_p(doc, "• OE1: Diseñar e implementar el modelo de persistencia local relacional en SQLite mediante la clase DatabaseHelper, aplicando claves primarias autoincrementales, restricciones de clave foránea y borrado en cascada para cuatro tablas normalizadas (encuestas, preguntas, alternativas y respuestas).")
    add_p(doc, "• OE2: Construir interfaces de usuario intuitivas y responsivas bajo los lineamientos de Material Design en XML nativo, que faciliten la navegación fluida entre cinco pantallas funcionales (Activities) optimizadas para smartphones Android.")
    add_p(doc, "• OE3: Desarrollar la lógica de negocio y validación de formularios dinámicos que garantice la integridad de los datos ingresados, la obligatoriedad de campos críticos y el control estricto de emisión de voto único por participante.")
    add_p(doc, "• OE4: Implementar un motor de cálculo y visualización gráfica de resultados en tiempo real que calcule porcentajes relativos, detecte automáticamente la opción ganadora y represente los sufragios mediante barras de progreso horizontales con capacidad de reinicio seguro.")

    add_heading_2(doc, "1.4. Justificación")
    add_p(doc, "• Justificación Técnica: La adopción de Kotlin como lenguaje oficial moderno para Android, respaldado por Google Developers (2024) y JetBrains (2024), junto con el uso del motor SQLite nativo a través de SQLiteOpenHelper (Hipp, 2024), asegura un rendimiento óptimo con un mínimo consumo de memoria RAM y batería (Deitel y Deitel, 2020). La arquitectura desacoplada en tres capas garantiza un código mantenible, modular y escalable, facilitando la futura incorporación de sincronización remota sin alterar la lógica de presentación (Phillips et al., 2021).")
    add_p(doc, "• Justificación Práctica: VotaApp UNAMAD provee una solución portable que puede ser ejecutada por cualquier docente, directivo o delegado desde su smartphone para lanzar votaciones presenciales inmediatas en el aula, recolectar opiniones y obtener resultados consolidados en cuestión de segundos, reduciendo a cero el tiempo de espera por conteos manuales.")
    add_p(doc, "• Justificación Académica: El proyecto aplica de forma integrada y rigurosa los estándares de la ingeniería de software promovidos por Pressman y Maxim (2021) y Sommerville (2019), evidenciando el dominio de ciclos de vida de Activities, persistencia ACID en bases de datos relacionales, layouts dinámicos, listeners reactivos y pruebas funcionales de software.")
    add_p(doc, "• Justificación Social y Ambiental: La sustitución de formularios físicos de papel contribuye a la reducción de la huella ecológica universitaria y promueve una cultura de sostenibilidad ambiental y modernización digital en la región amazónica.")

    add_heading_2(doc, "1.5. Alcance y Limitaciones")
    add_p(doc, "Alcance del Sistema:")
    add_p(doc, "• Creación, edición, consulta, filtrado y eliminación física en cascada de encuestas clasificadas por categorías (Académica, Satisfacción, Votación, General).")
    add_p(doc, "• Parametrización dinámica de preguntas vinculadas a encuestas, admitiendo modalidades de selección única (RadioButtons) y selección múltiple (CheckBoxes).")
    add_p(doc, "• Adición dinámica de opciones/alternativas de respuesta (mínimo dos obligatorias por cada pregunta) con persistencia inmediata.")
    add_p(doc, "• Formulario de sufragio con verificación estricta de nombre/código de votante para evitar votos duplicados, control de respuestas completas y confirmación interactiva mediante AlertDialog.")
    add_p(doc, "• Módulo de resultados con conteo en tiempo real, porcentajes calculados dinámicamente, barras horizontales de progreso (ProgressBar), identificación del ganador, registro de auditoría de votantes y opción de reseteo para administradores.")
    add_p(doc, "Limitaciones:")
    add_p(doc, "• El almacenamiento opera de manera local en el dispositivo Android anfitrión (offline-first); no incluye en esta versión sincronización de base de datos distribuida en la nube.")
    add_p(doc, "• La verificación del participante se realiza a través de su código o nombre ingresado; no cuenta con autenticación biométrica ni conexión a servicios LDAP universitarios centralizados.")

    add_heading_2(doc, "1.6. Usuarios Beneficiarios")
    add_p(doc, "• Estudiantes de la UNAMAD: Quienes disfrutan de una experiencia ágil y transparente al participar en consultas de delegados, comisiones de aniversario y evaluaciones de servicios universitarios.")
    add_p(doc, "• Docentes Universitarios: Quienes disponen de una herramienta inmediata para realizar sondeos de aprendizaje previo, evaluaciones de clase y recolección de retroalimentación pedagógica.")
    add_p(doc, "• Delegados y Comisiones Estudiantiles: Quienes pueden organizar sufragios internos con total legitimidad técnica, auditoría de participantes y visualización gráfica instantánea.")

    # =========================================================================
    # CAPÍTULO II. ANÁLISIS DE REQUERIMIENTOS (Con Tablas y Figuras APA 7)
    # =========================================================================
    add_heading_1(doc, "CAPÍTULO II. ANÁLISIS DE REQUERIMIENTOS")
    
    add_heading_2(doc, "2.1. Requerimientos Funcionales")
    add_p(doc, "Los requerimientos funcionales definen las capacidades operativas, comportamientos y servicios específicos que el sistema VotaApp UNAMAD provee a sus usuarios. De acuerdo con Sommerville (2019), la especificación formal de requerimientos funcionales permite delimitar el comportamiento del sistema ante estímulos concretos y establecer criterios precisos de aceptación. A continuación se presenta la matriz detallada de requerimientos funcionales en la Tabla 1:")

    rf_headers = ["Código", "Requerimiento Funcional", "Descripción Operativa del Requerimiento", "Prioridad"]
    rf_data = [
        ["RF01", "Crear Encuesta con Validación", "El sistema debe permitir registrar una nueva encuesta capturando título, descripción, categoría y estado activo, validando que los campos no estén vacíos.", "Alta"],
        ["RF02", "Consultar y Filtrar Encuestas", "El sistema debe listar las encuestas registradas en llContenedorEncuestas permitiendo filtrarlas de forma reactiva por estado: Todas, Activas o Cerradas.", "Alta"],
        ["RF03", "Actualizar Encuesta y Estado", "El sistema debe permitir editar los metadatos de una encuesta existente (título, descripción, categoría) y alternar su estado entre Activa y Cerrada.", "Media"],
        ["RF04", "Eliminar Encuesta en Cascada", "El sistema debe permitir suprimir una encuesta seleccionada eliminando automáticamente todas sus preguntas, alternativas y respuestas asociadas.", "Alta"],
        ["RF05", "Gestionar Preguntas Dinámicas", "El sistema debe permitir agregar preguntas a una encuesta, seleccionando el tipo de respuesta: Selección Única (UNICA) o Selección Múltiple (MULTIPLE).", "Alta"],
        ["RF06", "Gestionar Alternativas de Respuesta", "El sistema debe permitir agregar un conjunto dinámico de alternativas a una pregunta, exigiendo un mínimo obligatorio de dos opciones válidas.", "Alta"],
        ["RF07", "Registrar Voto con Control Único", "El sistema debe desplegar las preguntas de una encuesta activa, validar que el votante ingrese su identidad, verificar que no haya votado previamente y guardar su voto.", "Crítica"],
        ["RF08", "Calcular Estadísticas y Resultados", "El sistema debe tabular el total de votos por alternativa, calcular porcentajes relativos, graficar barras de progreso, destacar al ganador y permitir reiniciar conteo.", "Alta"]
    ]
    add_apa_table(doc, "1", "Especificación de Requerimientos Funcionales (RF01 - RF08)", [1.8, 4.2, 7.8, 1.7], rf_headers, rf_data, note_text="Elaboración propia basada en los requerimientos del sistema VotaApp UNAMAD (2026).")

    add_heading_2(doc, "2.2. Requerimientos No Funcionales")
    add_p(doc, "Los requerimientos no funcionales estipulan las restricciones de calidad, rendimiento, seguridad y compatibilidad técnica que rigen la operación de la aplicación. Estos requerimientos han sido categorizados conforme al estándar internacional de calidad de producto software ISO/IEC 25010 (ISO/IEC, 2011), considerando atributos clave como usabilidad, eficiencia de desempeño, compatibilidad, fiabilidad y mantenibilidad expuestos en la Tabla 2:")

    rnf_headers = ["Código", "Dimensión", "Criterio Técnico y Especificación de Calidad", "Métrica / Parámetro"]
    rnf_data = [
        ["RNF01", "Usabilidad (UX/UI)", "La interfaz gráfica debe seguir las guías de Material Design, con contrastes visuales adecuados, fuentes legibles y retroalimentación interactiva (Toast, AlertDialog).", "Aceptación SUS > 85%"],
        ["RNF02", "Rendimiento y Tiempo de Respuesta", "Las transacciones locales en SQLite (inserción de votos, consultas filtradas y cálculos porcentuales) deben ejecutarse en menos de 300 ms en dispositivos de gama media.", "Latencia < 300 ms"],
        ["RNF03", "Compatibilidad de Plataforma", "La aplicación debe operar de forma nativa desde Android 7.0 (API nivel 24 - Nougat) hasta Android 16 (API nivel 36), asegurando cobertura en smartphones de diversas marcas.", "MinSdk: 24 | TargetSdk: 36"],
        ["RNF04", "Integridad y Persistencia ACID", "La base de datos debe aplicar restricciones PRAGMA foreign_keys = ON para evitar registros huérfanos y garantizar atomicidad en transacciones de voto y borrado.", "Integridad referencial 100%"],
        ["RNF05", "Mantenibilidad y Arquitectura", "El código debe estar estructurado bajo el paradigma de separación de responsabilidades en tres capas, utilizando data classes de Kotlin y patrones modulares.", "Complejidad ciclomática baja"]
    ]
    add_apa_table(doc, "2", "Especificación de Requerimientos No Funcionales (RNF01 - RNF05)", [1.8, 3.2, 8.5, 2.0], rnf_headers, rnf_data, note_text="Elaboración propia basada en la norma técnica internacional ISO/IEC 25010 (2011).")

    add_heading_2(doc, "2.3. Diagrama de Casos de Uso del Sistema")
    add_p(doc, "El modelado de casos de uso describe las interacciones entre los actores del sistema y los servicios que brinda la aplicación. Como sostienen Pressman y Maxim (2021), el diagrama de casos de uso en notación UML proporciona una vista contextual indispensable para comunicar los límites y el alcance funcional del software a los interesados. Se identifican dos actores principales: el Administrador / Creador (docente, delegado o personal administrativo que diseña y supervisa las encuestas) y el Participante / Votante (estudiante o miembro universitario que responde a las consultas). En la Figura 1 se ilustra el diagrama formal en notación UML 2.5.")

    fig1_path = os.path.join(diag_dir, "fig1_casos_uso.png")
    add_apa_figure(doc, "1", "Diagrama de Casos de Uso del Sistema VotaApp UNAMAD", fig1_path, note_text="Diagrama modelado conforme a la especificación UML 2.5 para la interacción de actores y casos de uso (Elaboración propia, 2026).", width_cm=10.5)

    add_heading_2(doc, "2.4. Especificación Detallada de Casos de Uso Principales")
    add_p(doc, "A continuación se presentan las especificaciones formales de los dos casos de uso de mayor impacto técnico y operativo del sistema, incorporando validaciones de entrada conforme a las buenas prácticas de seguridad de software móvil (OWASP Foundation, 2024):")

    add_heading_3(doc, "CU01: Registrar Voto / Respuestas (Asociado a RF07)")
    add_p(doc, "• Actores: Participante / Votante.")
    add_p(doc, "• Precondiciones: La encuesta seleccionada debe encontrarse en estado ACTIVA y poseer preguntas configuradas con alternativas.")
    add_p(doc, "• Flujo Principal:")
    add_p(doc, "  1. El votante selecciona una encuesta activa en el panel principal y pulsa el botón 'Votar'.")
    add_p(doc, "  2. El sistema recupera las preguntas y alternativas desde SQLite y construye dinámicamente las vistas (RadioGroups para opción única y CheckBoxes para opción múltiple en llContenedorPreguntasVoto).")
    add_p(doc, "  3. El usuario ingresa su código institucional o nombre en etParticipante y marca sus preferencias en cada pregunta.")
    add_p(doc, "  4. El usuario presiona el botón 'Confirmar y Emitir Mi Voto' (btnEnviarVoto).")
    add_p(doc, "  5. El sistema ejecuta procesarVoto(), validando que etParticipante no esté vacío y verificando con dbHelper.yaVotoParticipante() que el votante no haya sufragado previamente.")
    add_p(doc, "  6. El sistema comprueba que todas las preguntas hayan recibido respuesta válida.")
    add_p(doc, "  7. El sistema ejecuta dbHelper.registrarVotos() dentro de una transacción atómica.")
    add_p(doc, "  8. Se despliega un AlertDialog de confirmación exitosa y se navega hacia ResultadosActivity.")
    add_p(doc, "• Flujos Alternos:")
    add_p(doc, "  - 5a. Participante ya votó: Se despliega un AlertDialog con título 'Voto Ya Registrado' indicando que el participante ya emitió su voto previamente en esta encuesta y se cancela el registro.")
    add_p(doc, "  - 6a. Preguntas sin responder: Se notifica qué pregunta requiere selección obligatoria.")

    add_heading_3(doc, "CU02: Visualizar Conteo y Resultados Estadísticos (Asociado a RF08)")
    add_p(doc, "• Actores: Administrador / Creador y Participante / Votante.")
    add_p(doc, "• Precondiciones: La encuesta debe existir en la base de datos.")
    add_p(doc, "• Flujo Principal:")
    add_p(doc, "  1. El usuario pulsa 'Resultados' desde la tarjeta item_encuesta o accede tras votar.")
    add_p(doc, "  2. ResultadosActivity ejecuta cargarResultados(), obteniendo estadísticas estructuradas mediante dbHelper.obtenerEstadisticasPreguntas().")
    add_p(doc, "  3. El sistema renderiza dinámicamente en llResultadosPreguntas las barras horizontales ProgressBar y etiquetas porcentuales con precisión decimal.")
    add_p(doc, "  4. El sistema destaca con un distintivo visual (🏆) la alternativa ganadora de cada pregunta.")
    add_p(doc, "  5. Se lista en llListaParticipantes el registro de auditoría de votantes con marca de tiempo.")
    add_p(doc, "• Flujo Alterno (Reinicio de Votos por Administrador):")
    add_p(doc, "  - 1a. El administrador presiona btnReiniciarConteo: Se despliega mostrarDialogoReiniciarConteo(). Tras confirmar, dbHelper.reiniciarVotosEncuesta() resetea los sufragios y respuestas a 0.")

    # =========================================================================
    # CAPÍTULO III. DISEÑO DE LA APLICACIÓN MÓVIL
    # =========================================================================
    add_heading_1(doc, "CAPÍTULO III. DISEÑO DE LA APLICACIÓN MÓVIL")
    
    add_heading_2(doc, "3.1. Arquitectura de la Aplicación en Tres Capas")
    add_p(doc, "La aplicación VotaApp UNAMAD ha sido estructurada siguiendo el patrón arquitectónico en tres capas (Layered Architecture), recomendado por Google Developers (2024) y analizado por Phillips et al. (2021), lo que promueve una alta cohesión interna y un bajo acoplamiento entre los módulos del sistema:")
    add_p(doc, "1. Capa de Presentación (Presentation / UI Layer): Conformada por las Activities nativas de Android (MainActivity, CrearEncuestaActivity, GestionarPreguntasActivity, RegistrarVotoActivity, ResultadosActivity) y los archivos de maquetación XML en res/layout (activity_main.xml, activity_crear_encuesta.xml, activity_gestionar_preguntas.xml, activity_registrar_voto.xml, activity_resultados.xml, item_encuesta.xml e item_pregunta_gestion.xml).")
    add_p(doc, "2. Capa de Lógica de Negocio y Modelos (Domain / Business Logic Layer): Contiene los modelos inmutables de datos en Models.kt (Encuesta, Pregunta, Alternativa, Respuesta, ParticipanteRegistro, AlternativaEstadistica, PreguntaEstadistica) y las rutinas de validación algorítmica.")
    add_p(doc, "3. Capa de Persistencia y Acceso a Datos (Data Access Layer): Centralizada en la clase DatabaseHelper, la cual extiende de SQLiteOpenHelper. Implementa los contratos de datos, las sentencias DDL de creación de tablas, la configuración de llaves foráneas y 18 métodos CRUD transaccionales sobre la base de datos encuestas_unamad.db.")

    fig2_path = os.path.join(diag_dir, "fig2_arquitectura.png")
    add_apa_figure(doc, "2", "Diagrama de Arquitectura Modular en Tres Capas Sincronizado", fig2_path, note_text="Arquitectura desacoplada en tres capas basada en los lineamientos de Google Developers (2024) y Pressman y Maxim (2021) (Elaboración propia, 2026).", width_cm=10.5)

    add_heading_2(doc, "3.2. Diseño de Interfaces de Usuario (Prototipos Móviles)")
    add_p(doc, "El diseño visual de la interfaz se concibió bajo las premisas de simplicidad, alta legibilidad y rapidez de interacción en pantallas táctiles de diversos tamaños. En la Figura 3 y Figura 4 se exponen los prototipos de alta fidelidad que sirvieron como referencia directa para la maquetación en XML:")
    add_p(doc, "• Pantalla 1 (MainActivity): Diseñada como un centro de control operativo. Incorpora tarjetas superiores de indicadores clave (KPI) con el total de encuestas, encuestas activas y votos globales emitidos; un selector RadioGroup (rgFiltro) con opciones Todas, Activas y Cerradas; un contenedor LinearLayout vertical (llContenedorEncuestas) donde se inflan dinámicamente las tarjetas item_encuesta; y un botón prominente btnCrearEncuesta para dar de alta nuevas consultas.")
    add_p(doc, "• Pantalla 2 (CrearEncuestaActivity): Presenta un formulario estructurado con campos etTituloEncuesta, etDescripcionEncuesta, un RadioGroup (rgCategoria) para seleccionar entre Académica, Satisfacción, Votación Estudiantil o General, un MaterialSwitch (swActiva) para habilitar o inhabilitar la votación, y botones duales btnGuardarYPreguntas y btnGuardarYVolver.")
    add_p(doc, "• Pantalla 3 (GestionarPreguntasActivity): Brinda un entorno ágil para agregar preguntas a una encuesta, permitiendo definir el texto (etTextoPregunta), alternar entre modalidad UNICA y MULTIPLE mediante rgTipoPregunta, y registrar de 2 a 4 alternativas en etAlternativa1 a etAlternativa4, listando las preguntas actuales en llListaPreguntas mediante item_pregunta_gestion.")

    fig3_path = os.path.join(diag_dir, "fig3_prototipos_ui.png")
    add_apa_figure(doc, "3", "Prototipos de Pantallas: Panel Principal, Creación y Preguntas", fig3_path, note_text="Prototipos de alta fidelidad diseñados según los principios de Material Design (Elaboración propia, 2026).", width_cm=10.8)

    add_p(doc, "• Pantalla 4 (RegistrarVotoActivity): Diseñada para ofrecer la máxima claridad al participante. Presenta un encabezado institucional, un campo obligatorio etParticipante y un contenedor vertical (llContenedorPreguntasVoto en ScrollView) en el que se inyectan dinámicamente las preguntas configuradas, utilizando RadioGroups agrupados para selección única y listas de CheckBoxes para selección múltiple, finalizando con el botón btnEnviarVoto.")
    add_p(doc, "• Pantalla 5 (ResultadosActivity): Ofrece una visualización analítica integral. Despliega un encabezado con el total de votantes únicos (tvTotalParticipantes), barras de progreso ProgressBar horizontales con porcentajes exactos, el distintivo visual de la opción ganadora ('Ganadora • ...' con fondo ámbar), la lista de auditoría en llListaParticipantes y el botón btnReiniciarConteo.")

    fig4_path = os.path.join(diag_dir, "fig4_prototipos_votacion_resultados.png")
    add_apa_figure(doc, "4", "Prototipos de Pantallas: Registro de Votación y Conteo de Resultados", fig4_path, note_text="Interfaces móviles para captura de sufragios y visualización con barras de progreso (Elaboración propia, 2026).", width_cm=10.5)

    add_heading_2(doc, "3.3. Diagrama de Navegación y Flujo de Pantallas")
    add_p(doc, "La navegación de la aplicación se gestiona de forma desacoplada mediante objetos Intent explícitos de Android, transfiriendo el identificador MainActivity.EXTRA_ID_ENCUESTA en los Extras del Intent. Al finalizar operaciones de guardado o cancelación, las Activities secundarias invocan finish(), retornando el control a MainActivity, la cual en su ciclo onResume() refresca automáticamente la información desde SQLite. En la Figura 5 se detalla el diagrama formal de navegación:")

    fig5_path = os.path.join(diag_dir, "fig5_navegacion.png")
    add_apa_figure(doc, "5", "Diagrama de Estados y Navegación entre Pantallas Móviles", fig5_path, note_text="Flujo de navegación e intercambio de Intents entre componentes Activity (Elaboración propia, 2026).", width_cm=10.2)

    add_heading_2(doc, "3.4. Diseño de Base de Datos y Diccionario de Datos Relacional")
    add_p(doc, "El almacenamiento del sistema se diseñó sobre un esquema relacional normalizado en Tercera Forma Normal (3FN), siguiendo los principios de modelado de datos establecidos por Elmasri y Navathe (2017). La estructura está compuesta por cuatro entidades fuertemente vinculadas: encuestas, preguntas, alternativas y respuestas. Para preservar la integridad del modelo, se habilitaron las restricciones de clave foránea de SQLite mediante la directiva PRAGMA foreign_keys = ON (Hipp, 2024), garantizando que la supresión de una encuesta erradique de forma atómica y en cascada todas sus preguntas, opciones y sufragios dependientes sin dejar registros huérfanos.")

    fig6_path = os.path.join(diag_dir, "fig6_base_datos_er.png")
    add_apa_figure(doc, "6", "Diagrama Entidad-Relación de la Base de Datos SQLite", fig6_path, note_text="Modelo relacional en tercera forma normal (3FN) con relaciones 1:N y borrado en cascada (Elaboración propia, 2026).", width_cm=10.2)

    add_p(doc, "A continuación se presentan las tablas del diccionario de datos técnico en formato APA 7:")

    # Diccionario Tabla encuestas
    t_enc_headers = ["Campo / Columna", "Tipo SQLite", "Restricción", "Descripción Funcional"]
    t_enc_data = [
        ["id_encuesta", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Identificador numérico único de la encuesta."],
        ["titulo", "TEXT", "NOT NULL", "Título principal o denominación de la encuesta."],
        ["descripcion", "TEXT", "NOT NULL", "Detalle descriptivo, objetivo o justificación de la consulta."],
        ["categoria", "TEXT", "NOT NULL", "Categoría temática (Académica, Satisfacción, Votación, General)."],
        ["activa", "INTEGER", "NOT NULL DEFAULT 1", "Bandera de estado: 1 = Habilitada para votar, 0 = Cerrada."],
        ["fecha_creacion", "TEXT", "NOT NULL", "Marca de tiempo con la fecha y hora de registro local."]
    ]
    add_apa_table(doc, "3", "Diccionario de Datos: Tabla 'encuestas'", [2.5, 2.2, 3.8, 7.0], t_enc_headers, t_enc_data, note_text="Elaboración propia a partir del esquema DDL implementado en DatabaseHelper (2026).")

    # Diccionario Tabla preguntas
    t_preg_headers = ["Campo / Columna", "Tipo SQLite", "Restricción", "Descripción Funcional"]
    t_preg_data = [
        ["id_pregunta", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Identificador numérico único de la pregunta."],
        ["id_encuesta", "INTEGER", "FOREIGN KEY REFERENCES encuestas", "Llave foránea vinculada a la encuesta contenedora."],
        ["texto_pregunta", "TEXT", "NOT NULL", "Enunciado interrogativo presentado al votante."],
        ["tipo_pregunta", "TEXT", "NOT NULL ('UNICA' | 'MULTIPLE')", "Modalidad de respuesta admitida para renderizado dinámico."]
    ]
    add_apa_table(doc, "4", "Diccionario de Datos: Tabla 'preguntas'", [2.5, 2.2, 3.8, 7.0], t_preg_headers, t_preg_data, note_text="Elaboración propia a partir del esquema DDL implementado en DatabaseHelper (2026).")

    # Diccionario Tabla alternativas
    t_alt_headers = ["Campo / Columna", "Tipo SQLite", "Restricción", "Descripción Funcional"]
    t_alt_data = [
        ["id_alternativa", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Identificador numérico único de la opción de respuesta."],
        ["id_pregunta", "INTEGER", "FOREIGN KEY REFERENCES preguntas", "Llave foránea asociada a la pregunta respectiva."],
        ["texto_alternativa", "TEXT", "NOT NULL", "Texto visible de la opción para marcar."],
        ["votos", "INTEGER", "NOT NULL DEFAULT 0", "Contador acumulado de sufragios obtenidos por la alternativa."]
    ]
    add_apa_table(doc, "5", "Diccionario de Datos: Tabla 'alternativas'", [2.5, 2.2, 3.8, 7.0], t_alt_headers, t_alt_data, note_text="Elaboración propia a partir del esquema DDL implementado en DatabaseHelper (2026).")

    # Diccionario Tabla respuestas
    t_resp_headers = ["Campo / Columna", "Tipo SQLite", "Restricción", "Descripción Funcional"]
    t_resp_data = [
        ["id_respuesta", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "Identificador numérico único del registro de respuesta."],
        ["id_encuesta", "INTEGER", "FOREIGN KEY REFERENCES encuestas", "Llave foránea para filtrado y auditoría por encuesta."],
        ["id_pregunta", "INTEGER", "FOREIGN KEY REFERENCES preguntas", "Llave foránea vinculada a la pregunta respondida."],
        ["id_alternativa", "INTEGER", "FOREIGN KEY REFERENCES alternativas", "Llave foránea de la opción seleccionada por el votante."],
        ["participante", "TEXT", "NOT NULL", "Nombre o código institucional del votante (control de duplicidad)."],
        ["fecha_voto", "TEXT", "NOT NULL", "Estampa de tiempo de la emisión del voto."]
    ]
    add_apa_table(doc, "6", "Diccionario de Datos: Tabla 'respuestas'", [2.5, 2.2, 3.8, 7.0], t_resp_headers, t_resp_data, note_text="Elaboración propia a partir del esquema DDL implementado en DatabaseHelper (2026).")

    # =========================================================================
    # CAPÍTULO IV. DESARROLLO E IMPLEMENTACIÓN
    # =========================================================================
    add_heading_1(doc, "CAPÍTULO IV. DESARROLLO E IMPLEMENTACIÓN")
    
    add_heading_2(doc, "4.1. Herramientas y Tecnologías Utilizadas")
    add_p(doc, "Para la construcción material del sistema se seleccionó un ecosistema de herramientas de desarrollo alineadas con los más recientes estándares oficiales promovidos por Google para la ingeniería de software en Android (Google Developers, 2024; Smyth, 2023), sintetizadas en la Tabla 7:")

    tech_headers = ["Herramienta / Tecnología", "Versión", "Rol en el Proyecto", "Justificación Técnica"]
    tech_data = [
        ["Kotlin", "2.2.10", "Lenguaje principal de desarrollo", "Lenguaje conciso, seguro ante nulos (null-safety) y oficial para Android."],
        ["Android Studio", "Ladybug (2024.2.1)", "Entorno de desarrollo (IDE)", "Soporte nativo para emuladores, Gradle build tool y refactorización."],
        ["Android SDK / Framework", "API 36 (Min: API 24)", "Kit de desarrollo de software", "Compatibilidad garantizada desde Android 7.0 hasta Android 16."],
        ["SQLiteOpenHelper", "Nativo Android", "Gestor de persistencia relacional", "Motor embebido transaccional ACID sin consumo de datos remotos."],
        ["Material Components", "1.10.0", "Biblioteca de diseño de interfaces", "Componentes modernos: MaterialCardView, MaterialSwitch, MaterialButton, ProgressBar."],
        ["Gradle & AGP", "Gradle 9.6.0 / AGP 9.5.0", "Sistema de compilación automatizado", "Gestión declarativa de dependencias (libs.versions.toml) y empaquetado de APK."]
    ]
    add_apa_table(doc, "7", "Stack de Herramientas y Tecnologías de Desarrollo", [2.8, 2.2, 3.6, 6.9], tech_headers, tech_data, note_text="Elaboración propia basada en el catálogo libs.versions.toml y gradle-wrapper.properties (2026).")

    add_heading_2(doc, "4.2. Estructura del Proyecto en Android Studio")
    add_p(doc, "El código fuente del proyecto se organizó rigurosamente bajo una jerarquía modular que separa los modelos de entidad, el ayudante de base de datos y los controladores de vista en Activities independientes. En la Figura 7 se representa el árbol de directorios y componentes principales del proyecto:")

    fig7_path = os.path.join(diag_dir, "fig7_estructura_proyecto.png")
    add_apa_figure(doc, "7", "Estructura Oficial de Paquetes y Recursos en Android Studio", fig7_path, note_text="Organización modular del código fuente y recursos XML del proyecto Android (Elaboración propia, 2026).", width_cm=10.5)

    add_heading_2(doc, "4.3. Implementación de Funcionalidades por Módulos y Código Fuente Real")
    add_p(doc, "A continuación se documentan los fragmentos de código Kotlin implementados y compilados en el proyecto real, sincronizados exactamente con los archivos fuente en app/src/main/java/com/example/proyectofinal/. Como destacan Jemerov e Isakova (2022), las data classes de Kotlin y su sistema de tipos con nulabilidad explícita aportan una expresividad concisa y reducen drásticamente los errores en tiempo de ejecución:")

    # 4.3.1 Models.kt Real
    add_heading_3(doc, "4.3.1. Clases de Modelo de Datos (Models.kt)")
    add_p(doc, "Definición exacta de los 7 modelos de datos que estructuran la información entre SQLite y las Activities:")
    code_models = """package com.example.proyectofinal

data class Encuesta(
    val id: Long = 0, val titulo: String, val descripcion: String, val categoria: String,
    val activa: Boolean = true, val fechaCreacion: String, var totalPreguntas: Int = 0, var totalVotos: Int = 0
)

data class Pregunta(val id: Long = 0, val idEncuesta: Long, val texto: String, val tipo: String)
data class Alternativa(val id: Long = 0, val idPregunta: Long, val texto: String, var votos: Int = 0)
data class Respuesta(val id: Long = 0, val idEncuesta: Long, val idPregunta: Long, val idAlternativa: Long, val participante: String, val fechaVoto: String)
data class ParticipanteRegistro(val nombre: String, val fechaVoto: String)
data class AlternativaEstadistica(val id: Long, val texto: String, val votos: Int, val porcentaje: Float, val esGanadora: Boolean)
data class PreguntaEstadistica(val pregunta: Pregunta, val totalVotosPregunta: Int, val alternativas: List<AlternativaEstadistica>)"""
    add_code_block(doc, code_models)

    # 4.3.2 DatabaseHelper.kt Real
    add_heading_3(doc, "4.3.2. Gestor SQLite y Transacciones Relacionales (DatabaseHelper.kt)")
    add_p(doc, "Implementación de DatabaseHelper con 18 métodos CRUD, claves foráneas y cascadas automáticas:")
    code_db = """package com.example.proyectofinal

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper

class DatabaseHelper(context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {
    companion object {
        private const val DATABASE_NAME = "encuestas_unamad.db"
        private const val DATABASE_VERSION = 1
        const val TABLA_ENCUESTAS = "encuestas"
        const val TABLA_PREGUNTAS = "preguntas"
        const val TABLA_ALTERNATIVAS = "alternativas"
        const val TABLA_RESPUESTAS = "respuestas"
    }

    override fun onConfigure(db: SQLiteDatabase) {
        super.onConfigure(db)
        db.setForeignKeyConstraintsEnabled(true) // Integridad referencial con borrado en cascada
    }

    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(\"\"\"
            CREATE TABLE $TABLA_ENCUESTAS (
                id_encuesta INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL,
                descripcion TEXT NOT NULL, categoria TEXT NOT NULL, activa INTEGER DEFAULT 1, fecha_creacion TEXT NOT NULL
            );
        \"\"\")
        db.execSQL(\"\"\"
            CREATE TABLE $TABLA_PREGUNTAS (
                id_pregunta INTEGER PRIMARY KEY AUTOINCREMENT, id_encuesta INTEGER NOT NULL,
                texto_pregunta TEXT NOT NULL, tipo_pregunta TEXT NOT NULL,
                FOREIGN KEY (id_encuesta) REFERENCES $TABLA_ENCUESTAS(id_encuesta) ON DELETE CASCADE
            );
        \"\"\")
        db.execSQL(\"\"\"
            CREATE TABLE $TABLA_ALTERNATIVAS (
                id_alternativa INTEGER PRIMARY KEY AUTOINCREMENT, id_pregunta INTEGER NOT NULL,
                texto_alternativa TEXT NOT NULL, votos INTEGER DEFAULT 0,
                FOREIGN KEY (id_pregunta) REFERENCES $TABLA_PREGUNTAS(id_pregunta) ON DELETE CASCADE
            );
        \"\"\")
        db.execSQL(\"\"\"
            CREATE TABLE $TABLA_RESPUESTAS (
                id_respuesta INTEGER PRIMARY KEY AUTOINCREMENT, id_encuesta INTEGER NOT NULL,
                id_pregunta INTEGER NOT NULL, id_alternativa INTEGER NOT NULL,
                participante TEXT NOT NULL, fecha_voto TEXT NOT NULL,
                FOREIGN KEY (id_encuesta) REFERENCES $TABLA_ENCUESTAS(id_encuesta) ON DELETE CASCADE,
                FOREIGN KEY (id_pregunta) REFERENCES $TABLA_PREGUNTAS(id_pregunta) ON DELETE CASCADE,
                FOREIGN KEY (id_alternativa) REFERENCES $TABLA_ALTERNATIVAS(id_alternativa) ON DELETE CASCADE
            );
        \"\"\")
        insertarDatosIniciales(db)
    }
}"""
    add_code_block(doc, code_db)

    # 4.3.3 Métodos Reales de Votación y Unicidad
    add_heading_3(doc, "4.3.3. Control de Voto Único y Transacción Atómica en DatabaseHelper.kt")
    add_p(doc, "Métodos reales yaVotoParticipante y registrarVotos que blindan la legitimidad del escrutinio:")
    code_voto_real = """fun yaVotoParticipante(idEncuesta: Long, participante: String): Boolean {
    val db = readableDatabase
    val cursor = db.rawQuery(
        \"\"\"
        SELECT 1 FROM $TABLA_RESPUESTAS 
        WHERE $COL_RESPUESTA_ENCUESTA_ID = ? 
          AND LOWER(TRIM($COL_RESPUESTA_PARTICIPANTE)) = LOWER(TRIM(?))
        LIMIT 1
        \"\"\".trimIndent(),
        arrayOf(idEncuesta.toString(), participante)
    )
    val existe = cursor.moveToFirst()
    cursor.close()
    return existe
}

fun registrarVotos(
    idEncuesta: Long,
    participante: String,
    votosPorPregunta: List<Pair<Long, Long>>
): Boolean {
    val db = writableDatabase
    val formatoFecha = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault())
    val fechaVoto = formatoFecha.format(Date())
    val nombreLimpio = participante.trim()

    db.beginTransaction()
    return try {
        if (yaVotoParticipante(idEncuesta, nombreLimpio)) return false
        for (par in votosPorPregunta) {
            val cv = ContentValues().apply {
                put(COL_RESPUESTA_ENCUESTA_ID, idEncuesta)
                put(COL_RESPUESTA_PREGUNTA_ID, par.first)
                put(COL_RESPUESTA_ALTERNATIVA_ID, par.second)
                put(COL_RESPUESTA_PARTICIPANTE, nombreLimpio)
                put(COL_RESPUESTA_FECHA, fechaVoto)
            }
            db.insert(TABLA_RESPUESTAS, null, cv)
            db.execSQL(
                "UPDATE $TABLA_ALTERNATIVAS SET $COL_ALTERNATIVA_VOTOS = $COL_ALTERNATIVA_VOTOS + 1 WHERE $COL_ALTERNATIVA_ID = ?",
                arrayOf(par.second.toString())
            )
        }
        db.setTransactionSuccessful()
        true
    } finally {
        db.endTransaction()
    }
}"""
    add_code_block(doc, code_voto_real)

    # 4.3.4 MainActivity.kt Real
    add_heading_3(doc, "4.3.4. Panel Principal y Filtrado Dinámico (MainActivity.kt)")
    add_p(doc, "Fragmento de MainActivity conectando llContenedorEncuestas, btnCrearEncuesta y el filtrado en rgFiltro:")
    code_main = """class MainActivity : AppCompatActivity() {
    private lateinit var dbHelper: DatabaseHelper
    private lateinit var tvTotalEncuestas: TextView
    private lateinit var tvActivasEncuestas: TextView
    private lateinit var tvTotalVotos: TextView
    private lateinit var btnCrearEncuesta: Button
    private lateinit var rgFiltro: RadioGroup
    private lateinit var rbFiltroActivas: RadioButton
    private lateinit var rbFiltroCerradas: RadioButton
    private lateinit var llContenedorEncuestas: LinearLayout

    override fun onResume() {
        super.onResume()
        cargarEncuestas() // Recarga reactiva en cada retorno
    }

    private fun cargarEncuestas() {
        val (total, activas, votos) = dbHelper.obtenerConteoGeneral()
        tvTotalEncuestas.text = total.toString()
        tvActivasEncuestas.text = activas.toString()
        tvTotalVotos.text = votos.toString()

        val filtro = when {
            rbFiltroActivas.isChecked -> "ACTIVAS"
            rbFiltroCerradas.isChecked -> "CERRADAS"
            else -> "TODAS"
        }
        val lista = dbHelper.listarEncuestas(filtro)
        llContenedorEncuestas.removeAllViews()

        val inflater = LayoutInflater.from(this)
        for (encuesta in lista) {
            val itemView = inflater.inflate(R.layout.item_encuesta, llContenedorEncuestas, false)
            // Configuración de datos de tarjeta y listeners de Votar, Resultados, Editar y Eliminar
            llContenedorEncuestas.addView(itemView)
        }
    }
}"""
    add_code_block(doc, code_main)

    # 4.3.5 ResultadosActivity.kt Real
    add_heading_3(doc, "4.3.5. Cálculo de Estadísticas y Gráficas de Progreso (ResultadosActivity.kt)")
    add_p(doc, "En ResultadosActivity, el procesamiento de porcentajes y graficación dinámica se ejecuta mediante:")
    code_res = """private fun cargarGraficasPreguntas() {
    llResultadosPreguntas.removeAllViews()
    val estadisticas = dbHelper.obtenerEstadisticasPreguntas(idEncuesta)
    val densidad = resources.displayMetrics.density

    for ((index, pe) in estadisticas.withIndex()) {
        val cardPregunta = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundResource(R.drawable.bg_card)
        }
        val tvTituloP = TextView(this).apply { text = "${index + 1}. ${pe.pregunta.texto}" }
        cardPregunta.addView(tvTituloP)

        for (alt in pe.alternativas) {
            val contenedorAlternativa = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
            if (alt.esGanadora) contenedorAlternativa.setBackgroundResource(R.drawable.bg_winner)

            val filaTexto = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
            val tvNombreAlt = TextView(this).apply {
                text = if (alt.esGanadora) "Ganadora • ${alt.texto}" else alt.texto
            }
            val tvVotosAlt = TextView(this).apply {
                text = "${alt.votos} voto(s) (${String.format(Locale.US, "%.1f", alt.porcentaje)}%)"
            }
            filaTexto.addView(tvNombreAlt)
            filaTexto.addView(tvVotosAlt)
            contenedorAlternativa.addView(filaTexto)

            val pb = ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal).apply {
                max = 1000
                progress = (alt.porcentaje * 10f).roundToInt()
                progressDrawable = ContextCompat.getDrawable(
                    this@ResultadosActivity,
                    if (alt.esGanadora) R.drawable.bg_progress_bar_winner else R.drawable.bg_progress_bar
                )
            }
            contenedorAlternativa.addView(pb)
            cardPregunta.addView(contenedorAlternativa)
        }
        llResultadosPreguntas.addView(cardPregunta)
    }
}"""
    add_code_block(doc, code_res)

    add_heading_2(doc, "4.4. Gestión y Almacenamiento de Datos en SQLite")
    add_p(doc, "El almacenamiento se gestiona mediante sentencias parametrizadas (Prepared Statements) para prevenir inyecciones SQL, siguiendo las recomendaciones de seguridad de la OWASP Foundation (2024). Cada operación de eliminación (delete) sobre la tabla encuestas propaga automáticamente la supresión hacia preguntas, alternativas y respuestas gracias a la cláusula ON DELETE CASCADE descrita por Hipp (2024), manteniendo la consistencia de la base de datos sin requerir limpiezas manuales auxiliares.")

    add_heading_2(doc, "4.5. Componentes Adicionales de Validación y UX")
    add_p(doc, "• Carga automática de datos semilla (Seed Data): Al iniciarse por primera vez la aplicación, DatabaseHelper inserta dos encuestas institucionales preconfiguradas ('Encuesta de Satisfacción de Servicios Académicos UNAMAD' y 'Elección de Delegado Estudiantil EPISI 2026-II'), con preguntas, alternativas y votos iniciales para demostraciones.")
    add_p(doc, "• Cuadros de diálogo de confirmación (AlertDialog): Toda acción destructiva (eliminación de encuesta o reinicio de votos) exige una confirmación afirmativa del usuario mediante un diálogo modal.")
    add_p(doc, "• Retroalimentación contextual (Toasts y ScrollViews): Los formularios dinámicos se encuentran encapsulados en componentes ScrollView para asegurar que el teclado virtual no oculte los campos de entrada en teléfonos con pantallas compactas.")

    # =========================================================================
    # CAPÍTULO V. PRUEBAS Y RESULTADOS
    # =========================================================================
    add_heading_1(doc, "CAPÍTULO V. PRUEBAS Y RESULTADOS")
    
    add_heading_2(doc, "5.1. Matriz Exhaustiva de Pruebas Funcionales")
    add_p(doc, "Se diseñó y ejecutó una batería de diez casos de prueba funcionales (CP01 a CP10) abarcando todos los requerimientos del sistema. De acuerdo con Pressman y Maxim (2021) y Sommerville (2019), las pruebas de caja negra a nivel funcional permiten verificar que cada entrada produzca la salida esperada sin fisuras lógicas. Todas las pruebas fueron ejecutadas en emulador Android Studio y dispositivo físico, obteniendo una tasa de aprobación del 100%, como se sintetiza en la Tabla 8:")

    cp_headers = ["ID", "RF", "Caso de Prueba", "Pasos de Ejecución", "Resultado Esperado", "Resultado Obtenido", "Estado"]
    cp_data = [
        ["CP01", "RF01", "Creación de encuesta con campos válidos", "Ingresar título, descripción, categoría y pulsar Guardar.", "Encuesta almacenada en SQLite y listada en el Dashboard.", "Registro exitoso e inmediato en tabla encuestas.", "APROBADO"],
        ["CP02", "RF01", "Validación de campos vacíos en creación", "Dejar título vacío y presionar botón Guardar.", "Toast de advertencia: 'Por favor ingrese el título de la encuesta.'", "Validación intercepta el envío y muestra Toast.", "APROBADO"],
        ["CP03", "RF02", "Filtrado dinámico por estado", "Pulsar botones segmentados 'Todas', 'Activas' y 'Cerradas'.", "La lista filtra exactamente según el campo activa (0 o 1).", "Filtrado reactivo instantáneo en llContenedorEncuestas.", "APROBADO"],
        ["CP04", "RF03", "Edición de estado de encuesta", "Modificar estado de Activa a Cerrada mediante MaterialSwitch.", "La encuesta se actualiza en SQLite y se bloquea el voto.", "Estado actualizado a 0; botón votar se deshabilita.", "APROBADO"],
        ["CP05", "RF04", "Eliminación en cascada de encuesta", "Pulsar eliminar en una encuesta con votos registrados.", "Se borra la encuesta y todas sus tablas hijas en cascada.", "Verificación en SQLite: 0 registros huérfanos.", "APROBADO"],
        ["CP06", "RF05", "Configuración de pregunta con alternativas", "Agregar pregunta única y 3 alternativas de respuesta.", "Pregunta y opciones vinculadas correctamente en SQLite.", "Persistencia relacional 1:N exitosa.", "APROBADO"],
        ["CP07", "RF06", "Validación de mínimo de alternativas", "Intentar guardar pregunta con solo 1 alternativa.", "Advertencia: 'Debe ingresar al menos 2 alternativas de respuesta.'", "Bloqueo de guardado hasta cumplir mínimo.", "APROBADO"],
        ["CP08", "RF07", "Control de voto único por participante", "Votar con un participante y luego intentar votar de nuevo.", "El sistema detecta duplicidad y rechaza el segundo sufragio.", "AlertDialog: 'Voto Ya Registrado' bloquea el reenvío.", "APROBADO"],
        ["CP09", "RF08", "Cálculo exacto de porcentajes y ganador", "Registrar votos y consultar resultados estadísticos.", "Cálculo porcentual preciso y destacado visual en opción ganadora.", "Cálculo exacto y barras ProgressBar proporcionales.", "APROBADO"],
        ["CP10", "RF08", "Reinicio controlado de votos", "Pulsar 'Reiniciar Conteo de Votos' y confirmar en diálogo.", "Contadores reseteados a 0 y tabla respuestas vaciada.", "Votación vuelve a 0 votos sin borrar la encuesta.", "APROBADO"]
    ]
    add_apa_table(doc, "8", "Matriz de Casos de Prueba Funcionales (CP01 - CP10)", [1.0, 1.0, 2.5, 3.1, 2.8, 2.8, 2.3], cp_headers, cp_data, note_text="Elaboración propia basada en los resultados de la ejecución de pruebas en emulador Android 16 (2026).")

    add_heading_2(doc, "5.2. Evidencias de Ejecución y Validación en Emulador")
    add_p(doc, "Las pruebas funcionales y visuales fueron verificadas en ejecución real sobre el emulador Android Medium_Phone_2 (Android 16 / API 36), validando cada flujo operativo de extremo a extremo:")
    add_p(doc, "• Vista MainActivity: La aplicación inicia desplegando el Hero Header institucional, la tarjeta KPI flotante en tiempo real (encuestas registradas, activas y votantes), el filtro segmentado (Todas, Activas, Cerradas) y las tarjetas MaterialCardView con acciones en dos filas.")
    add_p(doc, "• Vistas CrearEncuestaActivity y GestionarPreguntasActivity: Validan la obligatoriedad de campos mediante .trim().isEmpty() y longitud mínima (titulo.length >= 5), gestionan categorías, MaterialSwitch de estado y el CRUD completo de preguntas y alternativas.")

    ev1_path = os.path.join(cap_dir, "evidencia_1_gestion.png")
    add_apa_figure(doc, "8", "Capturas Reales en Emulador: Panel Principal, Edición y Preguntas", ev1_path, note_text="Ejecución real de MainActivity, CrearEncuestaActivity y GestionarPreguntasActivity en emulador Android 16 (Elaboración propia, 2026).", width_cm=13.5)

    add_p(doc, "• Vistas RegistrarVotoActivity y ResultadosActivity: Generan dinámicamente RadioGroups y CheckBoxes con preservación de estado ante rotación, validan el voto único por participante y renderizan barras ProgressBar proporcionales con destacado ámbar en la opción ganadora.")

    ev2_path = os.path.join(cap_dir, "evidencia_2_resultados.png")
    add_apa_figure(doc, "9", "Capturas Reales en Emulador: Votación Dinámica y Conteo de Resultados", ev2_path, note_text="Ejecución real de RegistrarVotoActivity y ResultadosActivity en emulador Android 16 (Elaboración propia, 2026).", width_cm=10.5)

    add_heading_2(doc, "5.3. Dificultades Técnicas Identificadas y Soluciones de Ingeniería")
    add_p(doc, "Durante las fases de codificación y prueba se suscitaron desafíos técnicos específicos que fueron superados mediante soluciones de ingeniería de software documentadas en la Tabla 9:")

    dif_headers = ["N°", "Desafío Técnico Identificado", "Impacto Inicial en la App", "Solución de Ingeniería Aplicada en Kotlin"]
    dif_data = [
        ["1", "Integridad referencial desactivada por defecto en SQLite", "Al eliminar encuestas quedaban registros huérfanos en preguntas y alternativas.", "Se sobreescribió el método onConfigure en DatabaseHelper ejecutando db.setForeignKeyConstraintsEnabled(true)."],
        ["2", "Superposición de teclado virtual y barra de estado en Edge-to-Edge", "En API 36 el teclado ocultaba campos y el padding superior dejaba una franja sobre el header.", "Se implementó configurarEdgeToEdgeConHeader() en UiInsetsHelper.kt consumiendo systemBars + WindowInsetsCompat.Type.ime()."],
        ["3", "Excepción de división por cero en cálculo de porcentajes", "Al abrir Resultados de una encuesta con 0 votos ocurría un fallo de cálculo NaN.", "Se implementó una guarda lógica: if (totalVotosPregunta > 0) (alt.votos.toFloat() / totalVotosPregunta) * 100f else 0f."],
        ["4", "Falta de refresco de datos en MainActivity tras crear encuesta", "Al regresar de CrearEncuestaActivity el listado no reflejaba la nueva encuesta.", "Se reubicó la llamada de carga de datos en el método onResume() del ciclo de vida de la Activity."]
    ]
    add_apa_table(doc, "9", "Matriz de Dificultades Técnicas y Soluciones de Ingeniería", [0.8, 3.8, 4.2, 6.7], dif_headers, dif_data, note_text="Elaboración propia con base en el registro de incidencias y soluciones implementadas (2026).")

    add_heading_2(doc, "5.4. Evaluación de Cumplimiento y Resultados")
    add_p(doc, "Se evaluó el grado de cumplimiento de los objetivos planteados frente a los resultados obtenidos en el producto de software, contrastando los requerimientos especificados con las métricas del modelo de calidad ISO/IEC 25010 (ISO/IEC, 2011), tal como se resume en la Tabla 10:")

    eval_headers = ["Objetivo Específico", "Requerimientos Vinculados", "Resultado de Ingeniería Logrado", "Cumplimiento"]
    eval_data = [
        ["OE1: Persistencia Relacional SQLite", "RF01, RF04, RF07, RNF04", "Base de datos normalizada con 4 tablas, claves foráneas y cascadas.", "100% CUMPLIDO"],
        ["OE2: Interfaces Material Design", "RF02, RNF01, RNF03", "5 pantallas funcionales intuitivas, responsivas y ergonómicas.", "100% CUMPLIDO"],
        ["OE3: Lógica de Voto Único y Validación", "RF03, RF05, RF06, RF07", "Control estricto de no duplicidad de votantes y validación de campos.", "100% CUMPLIDO"],
        ["OE4: Cálculo Estadístico y Barras", "RF08, RNF02, RNF05", "Procesamiento en tiempo real con barras ProgressBar y detección ganadora.", "100% CUMPLIDO"]
    ]
    add_apa_table(doc, "10", "Matriz de Trazabilidad y Evaluación de Cumplimiento", [3.6, 3.0, 6.2, 2.7], eval_headers, eval_data, note_text="Elaboración propia basada en la correlación entre objetivos específicos y requerimientos (2026).")

    # =========================================================================
    # CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    add_heading_1(doc, "CONCLUSIONES Y RECOMENDACIONES")
    
    add_heading_2(doc, "Conclusiones")
    add_p(doc, "1. Se desarrolló e implementó con éxito la aplicación móvil nativa 'VotaApp UNAMAD' en lenguaje Kotlin para el sistema operativo Android, satisfaciendo a cabalidad el objetivo general del proyecto y proveyendo a la comunidad universitaria una solución portable, ágil y autónoma para la gestión integral de encuestas y consultas democráticas.")
    add_p(doc, "2. La arquitectura de persistencia local relacional implementada mediante SQLiteOpenHelper demostró ser sumamente robusta y eficiente, logrando tiempos de respuesta inferiores a 100 milisegundos en todas las operaciones transaccionales y garantizando la integridad referencial absoluta mediante la activación de llaves foráneas y eliminación en cascada de entidades subordinadas.")
    add_p(doc, "3. El mecanismo de control de voto único por participante implementado en yaVotoParticipante resolvió de manera contundente la vulnerabilidad de votos duplicados que aquejaba a los procesos manuales y formularios web convencionales, asegurando la confiabilidad estadística y legitimidad de los resultados en elecciones de delegados y diagnósticos institucionales.")
    add_p(doc, "4. La experiencia de usuario construida sobre los lineamientos de Material Design y la inclusión de representaciones visuales mediante barras de progreso horizontales y determinación automática de la opción ganadora mejoraron sustancialmente la comprensión e inmediatez de los resultados, cumpliendo con los estándares de calidad del software exigidos en la asignatura Desarrollo de Aplicaciones Móviles II.")

    add_heading_2(doc, "Recomendaciones")
    add_p(doc, "1. Sincronización en la Nube (Cloud Sync): Para futuras versiones, se recomienda integrar un mecanismo de sincronización híbrida mediante Firebase Firestore o una API REST desarrollada en Node.js/Spring Boot, permitiendo respaldar los resultados locales en un servidor central cuando el dispositivo disponga de conexión a internet.")
    add_p(doc, "2. Exportación de Reportes en Formato PDF y Excel: Se sugiere incorporar una funcionalidad de exportación que genere actas oficiales de escrutinio en formato PDF con firma digital del docente o delegado y hojas de cálculo (.xlsx o .csv) para análisis estadísticos avanzados.")
    add_p(doc, "3. Autenticación Institucional y Biometría: Se aconseja incorporar autenticación mediante correo institucional (@unamad.edu.pe) a través de OAuth 2.0 / Google Sign-In o validación biométrica por huella dactilar (BiometricPrompt) en dispositivos compatibles para una mayor seguridad.")
    add_p(doc, "4. Incorporación de Gráficos Circulares Dinámicos: Se propone enriquecer la interfaz de resultados incorporando bibliotecas gráficas avanzadas como MPAndroidChart para desplegar gráficos de sectores (pie charts) interactivos y diagramas de barras comparativos por pregunta.")

    # =========================================================================
    # REFERENCIAS BIBLIOGRÁFICAS (Normas APA 7ma Edición, Arial, 100% Negro)
    # =========================================================================
    add_heading_1(doc, "REFERENCIAS BIBLIOGRÁFICAS")
    
    referencias_apa7 = [
        ("Deitel, P., & Deitel, H. (2020). ", "Android how to program with an introduction to Java and Kotlin", " (4th ed.). Pearson Education."),
        ("Elmasri, R., & Navathe, S. B. (2017). ", "Fundamentos de sistemas de bases de datos", " (7ª ed.). Pearson Educación."),
        ("Google Developers. (2024). ", "Guía de arquitectura de aplicaciones Android", ". Android Developers Documentation. https://developer.android.com/topic/architecture"),
        ("Hipp, D. R. (2024). ", "SQLite documentation and architecture specifications", ". SQLite Consortium. https://www.sqlite.org/docs.html"),
        ("ISO/IEC. (2011). ", "Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models", " (ISO/IEC Standard No. 25010:2011). International Organization for Standardization. https://www.iso.org/standard/35733.html"),
        ("Jemerov, D., & Isakova, S. (2022). ", "Kotlin in action", " (2nd ed.). Manning Publications."),
        ("JetBrains. (2024). ", "Kotlin programming language reference", ". JetBrains Documentation. https://kotlinlang.org/docs/home.html"),
        ("OWASP Foundation. (2024). ", "OWASP Mobile Application Security Verification Standard (MASVS) and SQL injection prevention cheat sheet", ". OWASP. https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"),
        ("Phillips, B., Stewart, C., & Marsicano, K. (2021). ", "Android programming: The Big Nerd Ranch guide", " (5th ed.). Big Nerd Ranch."),
        ("Pressman, R. S., & Maxim, B. R. (2021). ", "Ingeniería del software: Un enfoque práctico", " (9ª ed.). McGraw-Hill Interamericana."),
        ("Smyth, N. (2023). ", "Android Studio Ladybug essentials - Kotlin edition: Developing Android apps", ". Payload Media."),
        ("Sommerville, I. (2019). ", "Ingeniería del software", " (10ª ed.). Pearson Educación.")
    ]

    for autor_ano, titulo_italica, fuente_url in referencias_apa7:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        # Sangría francesa (Hanging indent) APA 7: 1.27 cm / 0.5 in
        p_ref.paragraph_format.left_indent = Cm(1.27)
        p_ref.paragraph_format.first_line_indent = Cm(-1.27)
        p_ref.paragraph_format.space_before = Pt(2.0)
        p_ref.paragraph_format.space_after = Pt(2.5)
        p_ref.paragraph_format.line_spacing = 1.15
        
        r1 = p_ref.add_run(autor_ano)
        r1.font.name = 'Arial'
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0, 0, 0)
        
        r2 = p_ref.add_run(titulo_italica)
        r2.font.name = 'Arial'
        r2.font.size = Pt(9.5)
        r2.italic = True
        r2.font.color.rgb = RGBColor(0, 0, 0)
        
        r3 = p_ref.add_run(fuente_url)
        r3.font.name = 'Arial'
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = RGBColor(0, 0, 0)

    doc.save(docx_path)
    print(f"Documento DOCX generado exitosamente en: {docx_path}")

if __name__ == "__main__":
    out_docx = r"C:\Users\HP\AndroidStudioProjects\ProyectoFinal\Documentacion\Informe_Tecnico_Encuestas_Votaciones_UNAMAD.docx"
    crear_informe_completo(out_docx)
