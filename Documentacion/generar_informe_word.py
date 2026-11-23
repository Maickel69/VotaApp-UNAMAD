import os
import sys
import shutil
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
    r_fleft = p_fleft.add_run("VotaApp UNAMAD – Sistema Móvil Cloud de Encuestas y Votaciones")
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
    add_p(doc, "“DESARROLLO E IMPLEMENTACIÓN DE UNA APLICACIÓN MÓVIL NATIVA EN KOTLIN Y FIREBASE CLOUD PARA LA GESTIÓN DE ENCUESTAS, VOTACIONES Y CONTEO DE RESULTADOS”", space_before=1, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=12.5, font_color=RGBColor(0, 0, 0))
    add_p(doc, "(Sistema VotaApp UNAMAD - com.example.proyectofinal | Cloud Firestore & Auth)", space_before=0, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, font_size=10, font_color=RGBColor(0, 0, 0))

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
        ("    1.2. Descripción del Problema", "4"),
        ("    1.3. Objetivos (General y Específicos)", "5"),
        ("    1.4. Justificación (Técnica, Práctica, Académica y Social)", "6"),
        ("    1.5. Alcance y Limitaciones", "6"),
        ("    1.6. Usuarios Beneficiarios y Escuelas Profesionales UNAMAD", "7"),
        ("CAPÍTULO II. ANÁLISIS DE REQUERIMIENTOS", "7"),
        ("    2.1. Requerimientos Funcionales (RF01 - RF12)", "7"),
        ("    2.2. Requerimientos No Funcionales (RNF01 - RNF07)", "8"),
        ("    2.3. Diagrama de Casos de Uso del Sistema", "9"),
        ("    2.4. Especificación Detallada de Casos de Uso Principales (CU01 - CU03)", "10"),
        ("CAPÍTULO III. DISEÑO DE LA APLICACIÓN MÓVIL Y ARQUITECTURA CLOUD", "11"),
        ("    3.1. Arquitectura de la Aplicación en Tres Capas y Backend Cloud", "11"),
        ("    3.2. Diseño de Interfaces de Usuario (6 Activities y Modo Oscuro Obsidian MD3)", "12"),
        ("    3.3. Diagrama de Navegación y Flujo de Pantallas", "14"),
        ("    3.4. Diseño de Datos en Cloud Firestore, Reglas de Seguridad y SQLite Local", "15"),
        ("CAPÍTULO IV. DESARROLLO E IMPLEMENTACIÓN", "18"),
        ("    4.1. Herramientas, Tecnologías y Pipeline CI/CD con GitHub Actions", "18"),
        ("    4.2. Estructura Modular del Proyecto en Android Studio", "19"),
        ("    4.3. Implementación de Funcionalidades por Módulos y Código Fuente Real", "20"),
        ("    4.4. Seguridad en la Nube (firestore.rules) y Persistencia Híbrida", "25"),
        ("    4.5. Experiencia de Usuario, Modo Oscuro Obsidian MD3 y Edge-to-Edge", "26"),
        ("CAPÍTULO V. PRUEBAS Y RESULTADOS", "27"),
        ("    5.1. Matriz Exhaustiva de Pruebas Funcionales (CP01 - CP12)", "27"),
        ("    5.2. Evidencias de Ejecución y Validación en Emulador Android 16", "28"),
        ("    5.3. Dificultades Técnicas Identificadas y Soluciones de Ingeniería", "30"),
        ("    5.4. Evaluación de Cumplimiento y Resultados", "31"),
        ("CONCLUSIONES Y RECOMENDACIONES", "31"),
        ("REFERENCIAS BIBLIOGRÁFICAS", "32")
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
        ("Figura 2. Diagrama de Arquitectura Modular en Tres Capas y Backend Firebase Cloud", "12"),
        ("Figura 3. Prototipos de Pantallas: Acceso, Panel Principal Cloud, Creación y Preguntas", "13"),
        ("Figura 4. Prototipos de Pantallas: Registro de Votación y Resultados con DonutChartView", "14"),
        ("Figura 5. Diagrama de Estados y Navegación entre las 6 Activities del Sistema", "15"),
        ("Figura 6. Modelo de Datos Híbrido: Colecciones Cloud Firestore y Esquema Relacional SQLite", "16"),
        ("Figura 7. Estructura Oficial de Paquetes, Módulos Kotlin y Recursos en Android Studio", "19"),
        ("Figura 8. Capturas Reales en Emulador: Login OAuth, Panel Principal, Creación y Preguntas", "29"),
        ("Figura 9. Capturas Reales en Emulador: Votación Tonal y Resultados con DonutChartView", "30")
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
        ("Tabla 1. Especificación de Requerimientos Funcionales (RF01 - RF12)", "8"),
        ("Tabla 2. Especificación de Requerimientos No Funcionales (RNF01 - RNF07)", "9"),
        ("Tabla 3. Diccionario de Datos Cloud Firestore: Colección 'users/{uid}'", "16"),
        ("Tabla 4. Diccionario de Datos Cloud Firestore: Colección 'encuestas/{encuestaId}'", "17"),
        ("Tabla 5. Diccionario de Datos Cloud Firestore: Subcolección 'encuestas/{encuestaId}/votos/{voterUid}'", "17"),
        ("Tabla 6. Estructura de Respaldo Local SQLite (encuestas_unamad.db)", "18"),
        ("Tabla 7. Stack de Herramientas, Servicios Cloud y Pipeline CI/CD", "18"),
        ("Tabla 8. Matriz de Casos de Prueba Funcionales (CP01 - CP12)", "27"),
        ("Tabla 9. Matriz de Dificultades Técnicas y Soluciones de Ingeniería", "30"),
        ("Tabla 10. Matriz de Trazabilidad y Evaluación de Cumplimiento", "31")
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
    add_p(doc, "La evolución continua de las tecnologías móviles, la computación en la nube (Cloud Computing) y la masificación de los teléfonos inteligentes basados en el sistema operativo Android han transformado radicalmente la manera en que las instituciones académicas interactúan, recopilan opiniones y toman decisiones democráticas. Tal como señalan Pressman y Maxim (2021), la ingeniería de software aplicada a dispositivos móviles modernos exige arquitecturas distribuidas que combinen la agilidad del desarrollo nativo con la sincronización en tiempo real, la seguridad criptográfica de identidades y la experiencia de usuario adaptativa. En la Universidad Nacional Amazónica de Madre de Dios (UNAMAD), la participación activa de la comunidad estudiantil y docente de sus 12 Escuelas Profesionales en consultas académicas, evaluaciones de satisfacción de servicios y elecciones de delegados estudiantiles constituye un pilar esencial para la gobernanza universitaria y el aseguramiento de la calidad educativa, en concordancia con los estándares internacionales de sistemas de información (ISO/IEC, 2011).")
    add_p(doc, "A pesar de estos imperativos democráticos, tradicionalmente una proporción significativa de las consultas estudiantiles se ha ejecutado mediante cédulas impresas en papel o formularios genéricos sin validación de padrón electoral ni filtro por escuela profesional. Como advierte Sommerville (2019), los procesos sustentados en soportes físicos o herramientas no integradas al padrón institucional introducen cuellos de botella críticos: consumo de papel, lentitud en el escrutinio, errores de tabulación manual, imposibilidad de restringir automáticamente una votación a una escuela profesional específica o a una nómina de códigos de matrícula, y vulnerabilidad frente a sufragios duplicados.")
    add_p(doc, "Ante esta problemática, el presente proyecto final, desarrollado en la asignatura Desarrollo de Aplicaciones Móviles II (Semestre Académico 2026-II) de la Escuela Profesional de Ingeniería de Sistemas e Informática, presenta el diseño, desarrollo, despliegue en la nube y entrega continua del “Sistema Móvil de Encuestas y Votaciones (VotaApp UNAMAD)”. La solución consiste en una aplicación móvil nativa construida en Kotlin (JetBrains, 2024) sobre Android Studio, integrada con una arquitectura híbrida en la nube utilizando Firebase Authentication (Correo/Contraseña y Google Sign-In OAuth 2.0) y Cloud Firestore en el proyecto cloud votaapp-unamad-2026, junto con soporte de persistencia relacional local en SQLite (DatabaseHelper), siguiendo las directrices oficiales de arquitectura móvil (Google Developers, 2024).")
    add_p(doc, "El sistema VotaApp UNAMAD incorpora seis pantallas especializadas (LoginActivity, MainActivity, CrearEncuestaActivity, GestionarPreguntasActivity, RegistrarVotoActivity y ResultadosActivity) diseñadas bajo el sistema visual Material Design 3 con Modo Oscuro Obsidian predeterminado (values-night/colors.xml) y soporte Edge-to-Edge (UiInsetsHelper.kt). Entre sus innovaciones técnicas destacan: la restricción inteligente de encuestas hacia cualquiera de las 12 Escuelas Profesionales de la UNAMAD; la importación masiva de padrones de códigos estudiantiles desde archivos Excel (.csv), bloques de texto (.txt) o portapapeles mediante expresiones regulares en CatalogoUnamad; el blindaje de un voto único por cuenta autenticada (UID) gobernado por reglas declarativas de seguridad en firestore.rules; la visualización estadística en tiempo real mediante un gráfico circular animado personalizado en Canvas (DonutChartView) y barras horizontales animadas; la exportación inmediata del Acta Oficial de Resultados; y un pipeline de integración y despliegue continuo (CI/CD) con GitHub Actions (.github/workflows/android-release.yml) en el repositorio oficial https://github.com/Maickel69/VotaApp-UNAMAD.")
    add_p(doc, "El presente informe técnico documenta de forma exhaustiva cada fase del ciclo de vida de ingeniería de software: la descripción del problema y objetivos, el análisis de requerimientos funcionales y no funcionales, el modelado UML de casos de uso, la arquitectura en tres capas conectada a Firebase Cloud, los prototipos e interfaces de las seis Activities, el modelo de datos en Cloud Firestore y SQLite, los fragmentos reales de código fuente en Kotlin y reglas de seguridad, la matriz de pruebas funcionales verificadas en Android 16 (API 36), y las conclusiones técnicas del proyecto.")

    # =========================================================================
    # CAPÍTULO I. DESCRIPCIÓN DEL PROYECTO (100% Negro)
    # =========================================================================
    add_heading_1(doc, "CAPÍTULO I. DESCRIPCIÓN DEL PROYECTO")
    
    add_heading_2(doc, "1.1. Nombre del Proyecto")
    add_p(doc, "El proyecto se denomina oficialmente:")
    add_p(doc, "“Sistema Móvil de Encuestas y Votaciones en Tiempo Real (VotaApp UNAMAD)”", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11, font_color=RGBColor(0, 0, 0))
    add_p(doc, "Identificador de paquete Android: com.example.proyectofinal | Proyecto Firebase Cloud: votaapp-unamad-2026 | Repositorio Oficial CI/CD: https://github.com/Maickel69/VotaApp-UNAMAD. Esta plataforma móvil nativa permite gestionar procesos electorales estudiantiles, diagnósticos académicos y encuestas de satisfacción sincronizadas en tiempo real entre múltiples dispositivos Android de la comunidad universitaria.")

    add_heading_2(doc, "1.2. Descripción del Problema")
    add_p(doc, "En la Universidad Nacional Amazónica de Madre de Dios (UNAMAD), los procesos participativos de toma de decisiones y recolección de datos académicos se realizan constantemente en sus 12 carreras profesionales. Estos procesos incluyen elecciones de delegados de curso y representantes estudiantiles, diagnósticos de equipamiento de laboratorios, encuestas de tutoría y evaluación de servicios universitarios.")
    add_p(doc, "Sin embargo, la ejecución tradicional de estas consultas presenta cuatro limitaciones críticas:")
    add_p(doc, "1. Demora y errores en el escrutinio manual: El uso de ánforas y cédulas físicas demanda logística de impresión y conteo manual, generando retrasos y posibles inconsistencias aritméticas en el cálculo de porcentajes.")
    add_p(doc, "2. Ausencia de segmentación por Escuela Profesional y Padrón Electoral: Los formularios web convencionales no validan de forma nativa a qué carrera pertenece el estudiante ni permiten importar instantáneamente una lista de códigos de matrícula desde archivos Excel (.csv) o texto (.txt) para cerrar una votación únicamente a los alumnos matriculados en un curso o facultad.")
    add_p(doc, "3. Vulnerabilidad de sufragio duplicado y falta de trazabilidad: Sin una autenticación vinculada a un identificador único criptográfico (UID) y a un código universitario verificado sin duplicidad en la base de datos, existe el riesgo de que un mismo participante emita múltiples votos o suplante la identidad de otro compañero.")
    add_p(doc, "4. Carencia de visualización analítica instantánea y actas oficiales: Los organizadores requieren observar en tiempo real gráficos de distribución porcentual (gráficos de dona y barras comparativas) y compartir de inmediato un Acta Oficial de Resultados auditable por todos los participantes.")
    add_p(doc, "En respuesta a esta problemática, se diseñó e implementó VotaApp UNAMAD, combinando autenticación federada e institucional en Firebase Authentication, sincronización distribuida en Cloud Firestore protegida por reglas de seguridad del lado del servidor (firestore.rules), respaldo local SQLite y visualización gráfica nativa en Kotlin.")

    add_heading_2(doc, "1.3. Objetivos")
    add_heading_3(doc, "1.3.1. Objetivo General")
    add_p(doc, "Desarrollar e implementar una aplicación móvil nativa en Kotlin para Android integrada con Firebase Authentication y Cloud Firestore, que permita la gestión integral de encuestas segmentadas por escuela profesional y padrón de códigos estudiantiles, el registro seguro de votaciones con garantía de un voto único por UID y el análisis visual de resultados en tiempo real para la Universidad Nacional Amazónica de Madre de Dios.")
    
    add_heading_3(doc, "1.3.2. Objetivos Específicos")
    add_p(doc, "• OE1: Implementar un módulo de identidad y seguridad en LoginActivity mediante Firebase Authentication (Correo/Contraseña y Google Sign-In OAuth 2.0), recuperación de contraseña por correo y registro de perfil estudiantil con validación de código universitario único y pertenencia a una de las 12 Escuelas Profesionales de la UNAMAD.")
    add_p(doc, "• OE2: Diseñar y programar seis Activities nativas bajo el sistema Material Design 3 con Modo Oscuro Obsidian predeterminado (values-night/colors.xml) y soporte Edge-to-Edge (UiInsetsHelper.kt), integrando búsqueda en tiempo real, filtros por ChipGroup de categorías y tarjetas interactivas.")
    add_p(doc, "• OE3: Desarrollar la arquitectura de datos en la nube con FirebaseRepository.kt y reglas de seguridad declarativas (firestore.rules) sobre las colecciones users, encuestas y votos, incorporando filtrado por carrera e importación masiva de códigos estudiantiles desde archivos .txt / .csv o portapapeles.")
    add_p(doc, "• OE4: Construir un motor de escrutinio y visualización estadística en ResultadosActivity que integre un gráfico circular animado personalizado en Canvas (DonutChartView), barras horizontales animadas, padrón de auditoría de votantes y exportación del Acta Oficial de Resultados, automatizando la entrega del APK mediante GitHub Actions CI/CD.")

    add_heading_2(doc, "1.4. Justificación")
    add_p(doc, "• Justificación Técnica: El empleo de Kotlin 2.2.10 junto con el SDK nativo de Firebase BoM 34.7.0 (Firebase Auth, Cloud Firestore y Google Play Services Auth) permite sincronizar encuestas y sufragios en milisegundos entre todos los dispositivos conectados, mientras que las reglas firestore.rules garantizan en el servidor la inmutabilidad del voto y la restricción de un sufragio por UID (Google Developers, 2024; OWASP Foundation, 2024). Además, el flujo de integración continua con GitHub Actions compila, ejecuta pruebas unitarias y publica automáticamente el instalador APK ante cada actualización en la rama principal.")
    add_p(doc, "• Justificación Práctica: Docentes, comités electorales y delegados estudiantiles pueden crear una encuesta desde su celular, restringirla a una de las 12 carreras de la UNAMAD o pegar desde Excel la columna de códigos de matrícula habilitados, logrando que los estudiantes voten desde sus propios dispositivos con resultados consolidados al instante.")
    add_p(doc, "• Justificación Académica: El proyecto sintetiza competencias avanzadas de ingeniería de software móvil: diseño de vistas personalizadas en Canvas (DonutChartView), autenticación OAuth 2.0, modelado NoSQL documental en Cloud Firestore, persistencia relacional en SQLite, seguridad declarativa y DevOps móvil con GitHub Actions.")
    add_p(doc, "• Justificación Social y Ambiental: Elimina el uso de papel en elecciones de aula y encuestas universitarias, fomentando la transparencia electoral, la inclusión digital y la modernización tecnológica en la región Madre de Dios.")

    add_heading_2(doc, "1.5. Alcance y Limitaciones")
    add_p(doc, "Alcance del Sistema:")
    add_p(doc, "• Autenticación completa en la nube con Correo/Contraseña, inicio de sesión con un toque mediante Google Sign-In (OAuth 2.0), restablecimiento de contraseña por correo electrónico y alternancia de Modo Oscuro/Claro en tiempo real.")
    add_p(doc, "• Gestión del perfil del estudiante en la colección users/{uid}, garantizando que ningún código universitario pueda ser duplicado por otra cuenta y vinculando al alumno con una de las 12 Escuelas Profesionales de la UNAMAD.")
    add_p(doc, "• Creación, edición, filtrado multicriterio (texto, ChipGroup de categorías y estado Activa/Cerrada) y eliminación de encuestas en Cloud Firestore.")
    add_p(doc, "• Control de acceso electoral por encuesta: abierta a toda la UNAMAD, exclusiva para una Escuela Profesional específica o restringida a un padrón de códigos importado masivamente desde archivos .txt, .csv (Excel) o portapapeles.")
    add_p(doc, "• Configuración dinámica de preguntas de selección única (UNICA) y selección múltiple (MULTIPLE) con alternativas de respuesta embebidas y sincronizadas en Firestore.")
    add_p(doc, "• Emisión de voto con tarjetas tonales interactivas, preservación de selección ante rotación de pantalla y verificación criptográfica de voto único por UID en la subcolección encuestas/{encuestaId}/votos/{voterUid}.")
    add_p(doc, "• Escrutinio en tiempo real con gráfico de dona animado (DonutChartView), barras de progreso horizontales animadas, medalla a la opción ganadora, auditoría de participantes y generación compartible del Acta Oficial de Resultados.")
    add_p(doc, "Limitaciones:")
    add_p(doc, "• La sincronización multi-dispositivo en tiempo real requiere conectividad a internet (Wi-Fi o datos móviles) para comunicarse con los servidores de Google Cloud Firestore, disponiendo de DatabaseHelper (SQLite) como módulo de respaldo local.")

    add_heading_2(doc, "1.6. Usuarios Beneficiarios y Escuelas Profesionales UNAMAD")
    add_p(doc, "El sistema incluye soporte nativo en CatalogoUnamad para las 12 Escuelas Profesionales oficiales de la Universidad Nacional Amazónica de Madre de Dios:")
    add_p(doc, "1. Ingeniería de Sistemas e Informática (EPISI) | 2. Ingeniería Forestal y Medio Ambiente | 3. Ingeniería Agroindustrial | 4. Medicina Veterinaria y Zootecnia | 5. Enfermería | 6. Derecho y Ciencias Políticas | 7. Educación: Matemática y Computación | 8. Educación: Primaria e Informática | 9. Educación: Inicial y Especial | 10. Ecoturismo | 11. Administración y Negocios Internacionales | 12. Contabilidad y Finanzas.")

    # =========================================================================
    # CAPÍTULO II. ANÁLISIS DE REQUERIMIENTOS (Con Tablas y Figuras APA 7)
    # =========================================================================
    add_heading_1(doc, "CAPÍTULO II. ANÁLISIS DE REQUERIMIENTOS")
    
    add_heading_2(doc, "2.1. Requerimientos Funcionales")
    add_p(doc, "Los requerimientos funcionales especifican las capacidades operativas, reglas de validación y flujos transaccionales que el sistema VotaApp UNAMAD provee a sus usuarios autenticados. De acuerdo con Sommerville (2019), la trazabilidad entre requerimientos funcionales y módulos de código garantiza la completitud del software. En la Tabla 1 se detallan los 12 requerimientos funcionales implementados:")

    rf_headers = ["Código", "Requerimiento Funcional", "Descripción Operativa del Requerimiento", "Prioridad"]
    rf_data = [
        ["RF01", "Autenticación Firebase y Google OAuth 2.0", "El sistema debe permitir iniciar sesión y registrar usuarios mediante Correo/Contraseña y Google Sign-In OAuth 2.0, además de enviar correos de recuperación de contraseña.", "Crítica"],
        ["RF02", "Gestión de Perfil y 12 Carreras UNAMAD", "El sistema debe almacenar en users/{uid} el nombre, correo, Escuela Profesional (entre las 12 carreras UNAMAD) y código universitario, validando que el código no esté usado por otro UID.", "Alta"],
        ["RF03", "Dashboard Cloud, KPIs y Filtros Reactivos", "El sistema debe mostrar en MainActivity indicadores KPI con numerales tabulares, búsqueda instantánea por texto, ChipGroup por categoría y filtro por estado (Todas, Activas, Cerradas).", "Alta"],
        ["RF04", "Crear y Editar Encuesta en Firestore", "El sistema debe permitir crear y actualizar encuestas en encuestas/{encuestaId} definiendo título, descripción, categoría, estado activo y metadatos del creador.", "Alta"],
        ["RF05", "Filtro por Carrera e Importación de Padrón", "El sistema debe permitir restringir una encuesta a una de las 12 carreras UNAMAD y/o importar masivamente códigos estudiantiles autorizados desde archivos .txt/.csv (Excel) o portapapeles.", "Crítica"],
        ["RF06", "Eliminar Encuesta por Creador Autorizado", "El sistema debe permitir eliminar una encuesta y toda su subcolección de votos en cascada mediante WriteBatch únicamente cuando el usuario autenticado sea el creador.", "Alta"],
        ["RF07", "Gestionar Preguntas y Alternativas Cloud", "El sistema debe permitir agregar y eliminar preguntas dinámicas de Selección Única (UNICA) o Selección Múltiple (MULTIPLE) con un mínimo de 2 alternativas por pregunta.", "Alta"],
        ["RF08", "Verificación de Acceso Electoral al Votar", "Antes de permitir el sufragio, el sistema debe verificar con encuesta.verificarAcceso() si el votante pertenece a la Escuela Profesional requerida y si su código figura en el padrón autorizado.", "Crítica"],
        ["RF09", "Registro de Voto Único por UID con Tarjetas Tonales", "El sistema debe presentar tarjetas de votación interactivas y registrar el sufragio en encuestas/{encuestaId}/votos/{voterUid}, bloqueando cualquier intento de doble voto por cuenta.", "Crítica"],
        ["RF10", "Gráfico DonutChartView y Barras Animadas", "El sistema debe calcular en tiempo real los votos y porcentajes por alternativa, renderizando un gráfico circular animado en Canvas (DonutChartView), barras ProgressBar animadas y opción ganadora.", "Alta"],
        ["RF11", "Auditoría de Votantes y Reinicio de Conteo", "El sistema debe listar el padrón auditable de participantes con fecha/hora de sufragio y permitir al creador reiniciar el conteo de votos con confirmación modal.", "Media"],
        ["RF12", "Exportación de Acta Oficial de Resultados", "El sistema debe generar y compartir el Acta Oficial de Resultados formateada en texto plano hacia WhatsApp, correo o portapapeles mediante Intent.ACTION_SEND.", "Alta"]
    ]
    add_apa_table(doc, "1", "Especificación de Requerimientos Funcionales (RF01 - RF12)", [1.6, 3.8, 8.4, 1.7], rf_headers, rf_data, note_text="Elaboración propia basada en los módulos Cloud y móviles del sistema VotaApp UNAMAD (2026).")

    add_heading_2(doc, "2.2. Requerimientos No Funcionales")
    add_p(doc, "Los requerimientos no funcionales establecen los atributos de calidad, seguridad, diseño visual, rendimiento y automatización del ciclo de entrega conforme a la norma internacional ISO/IEC 25010 (ISO/IEC, 2011), presentados en la Tabla 2:")

    rnf_headers = ["Código", "Dimensión", "Criterio Técnico y Especificación de Calidad", "Métrica / Parámetro"]
    rnf_data = [
        ["RNF01", "Usabilidad y Modo Oscuro Obsidian MD3", "La interfaz debe implementar Material Design 3 con paleta Obsidian Midnight (#090E1A) por defecto, alternancia Día/Noche instantánea, diseño Edge-to-Edge y numerales tabulares.", "Contraste WCAG AAA / SUS > 90%"],
        ["RNF02", "Rendimiento y Sincronización Cloud", "Las consultas a Cloud Firestore, el filtrado local multicriterio y las animaciones a 60 fps de DonutChartView (650 ms) deben ejecutarse sin bloquear el hilo principal (UI Thread).", "Latencia < 300 ms | 60 FPS"],
        ["RNF03", "Seguridad Declarativa en Servidor", "El backend Cloud Firestore debe aplicar reglas firestore.rules que validen autenticación, propiedad de documentos (isOwner), esquemas de datos e inmutabilidad del voto por UID.", "100% rutas protegidas"],
        ["RNF04", "Compatibilidad Multi-Versión Android", "La aplicación debe ejecutarse de forma nativa desde Android 7.0 (API 24) hasta Android 16 (API 36), adaptando insets de barras del sistema y teclado virtual (IME).", "MinSdk: 24 | TargetSdk: 36"],
        ["RNF05", "Tolerancia y Persistencia Híbrida", "El sistema debe combinar la sincronización en la nube (FirebaseRepository) con el soporte de esquema relacional SQLite (DatabaseHelper) y preservación de estado ante rotación.", "Integridad ACID / Cloud"],
        ["RNF06", "Mantenibilidad y Modularidad Kotlin", "El código fuente debe estructurarse en componentes desacoplados con data classes inmutables, catálogo institucional (CatalogoUnamad) y extensiones reutilizables.", "11 archivos Kotlin limpios"],
        ["RNF07", "Automatización CI/CD (DevOps)", "Cada push a la rama main en GitHub debe disparar un flujo en GitHub Actions que ejecute pruebas unitarias, compile el APK y publique el release latest-apk automáticamente.", "Build & Release 100% automático"]
    ]
    add_apa_table(doc, "2", "Especificación de Requerimientos No Funcionales (RNF01 - RNF07)", [1.6, 3.3, 8.3, 2.3], rnf_headers, rnf_data, note_text="Elaboración propia basada en la norma técnica internacional ISO/IEC 25010 (2011).")

    add_heading_2(doc, "2.3. Diagrama de Casos de Uso del Sistema")
    add_p(doc, "El modelado de casos de uso representa las interacciones entre los actores universitarios y los procesos de VotaApp UNAMAD. Como exponen Pressman y Maxim (2021), la notación UML 2.5 permite visualizar las fronteras del sistema y la delegación de responsabilidades. Se distinguen dos roles operativos sobre la misma cuenta autenticada: el Organizador / Creador (docente, delegado o comité que crea la encuesta, define restricciones de carrera/padrón, gestiona preguntas y administra el escrutinio) y el Estudiante / Votante (miembro de cualquiera de las 12 Escuelas Profesionales que se autentica, configura su perfil académico, emite su voto único y consulta resultados). La Figura 1 muestra el diagrama de casos de uso del sistema.")

    fig1_path = os.path.join(diag_dir, "fig1_casos_uso.png")
    add_apa_figure(doc, "1", "Diagrama de Casos de Uso del Sistema VotaApp UNAMAD", fig1_path, note_text="Diagrama modelado conforme a la especificación UML 2.5 incluyendo autenticación Cloud, restricción por escuela/padrón y escrutinio (Elaboración propia, 2026).", width_cm=11.0)

    add_heading_2(doc, "2.4. Especificación Detallada de Casos de Uso Principales")
    add_p(doc, "A continuación se documentan los tres casos de uso críticos que gobiernan la seguridad de acceso, la restricción electoral y el escrutinio en la nube:")

    add_heading_3(doc, "CU01: Autenticar Usuario y Configurar Perfil Académico UNAMAD (Asociado a RF01, RF02)")
    add_p(doc, "• Actor: Estudiante / Docente UNAMAD.")
    add_p(doc, "• Precondiciones: El dispositivo cuenta con conexión a internet y servicios de Google Play activos.")
    add_p(doc, "• Flujo Principal:")
    add_p(doc, "  1. El usuario abre la aplicación; LoginActivity verifica si existe una sesión activa en FirebaseAuth.")
    add_p(doc, "  2. Si no hay sesión, se presenta la interfaz con soporte de Modo Oscuro Obsidian (btnTemaLogin), campos de correo y contraseña, botón de Google Sign-In OAuth 2.0 y la fila interactiva con las opciones 'Crear cuenta' junto a '¿Olvidaste tu contraseña?'.")
    add_p(doc, "  3. Al pulsar 'Crear cuenta', se despliega con transición animada el formulario de registro que solicita Nombre Completo, Código Universitario y Escuela Profesional (Spinner con las 12 carreras de la UNAMAD).")
    add_p(doc, "  4. FirebaseRepository.guardarPerfilUsuario() verifica en la colección users que el código universitario no esté registrado por otro UID y almacena el documento users/{uid} en Cloud Firestore.")
    add_p(doc, "  5. El sistema redirige automáticamente a MainActivity mostrando el saludo personalizado con nombre y código.")
    add_p(doc, "• Flujos Alternos:")
    add_p(doc, "  - 2a. Recuperación de contraseña: Al pulsar '¿Olvidaste tu contraseña?', se abre un cuadro de diálogo que invoca auth.sendPasswordResetEmail(correo) enviando el enlace oficial de restablecimiento.")
    add_p(doc, "  - 4a. Código universitario duplicado: Si otro estudiante ya registró ese código de matrícula, el sistema rechaza la asignación y muestra un mensaje de alerta protegiendo la unicidad del padrón.")

    add_heading_3(doc, "CU02: Crear Encuesta con Filtro de Escuela Profesional e Importación Masiva de Códigos (Asociado a RF04, RF05)")
    add_p(doc, "• Actor: Organizador / Creador.")
    add_p(doc, "• Flujo Principal:")
    add_p(doc, "  1. Desde MainActivity, el organizador pulsa '+ Crear Nueva Encuesta' para abrir CrearEncuestaActivity.")
    add_p(doc, "  2. Ingresa el título (mínimo 5 caracteres), descripción y selecciona la categoría (Académica, Satisfacción, Votación Estudiantil o General).")
    add_p(doc, "  3. En la sección de Control de Acceso Electoral, selecciona en spCarreraRestringida si la encuesta está abierta a 'Todas las carreras' o restringida exclusivamente a una de las 12 Escuelas Profesionales.")
    add_p(doc, "  4. Opcionalmente, pulsa 'Importar .txt / .csv' (selector de archivos nativo) o 'Pegar de Excel' (lectura directa del portapapeles). El motor CatalogoUnamad.extraerCodigosDesdeTexto() extrae y normaliza automáticamente todos los códigos de matrícula válidos, actualizando el contador en tiempo real.")
    add_p(doc, "  5. Al pulsar 'Guardar y Configurar Preguntas', el documento se crea en Cloud Firestore y navega a GestionarPreguntasActivity.")

    add_heading_3(doc, "CU03: Emitir Voto Único Verificado y Auditar Resultados con DonutChartView (Asociado a RF08 - RF12)")
    add_p(doc, "• Actor: Estudiante / Votante.")
    add_p(doc, "• Flujo Principal:")
    add_p(doc, "  1. El votante selecciona una encuesta activa; el sistema evalúa encuesta.verificarAcceso(perfilActual, uid).")
    add_p(doc, "  2. En RegistrarVotoActivity, el sistema consulta FirebaseRepository.yaVotoUsuario(idEncuesta, uid). Si no ha votado, renderiza tarjetas tonales interactivas para cada pregunta (RadioGroup para selección única y CheckBoxes para selección múltiple).")
    add_p(doc, "  3. Al confirmar el sufragio, se escribe el documento encuestas/{idEncuesta}/votos/{uid} en Cloud Firestore, donde las reglas firestore.rules garantizan que el ID del documento coincida exactamente con request.auth.uid.")
    add_p(doc, "  4. El sistema redirige a ResultadosActivity, donde se calcula la distribución estadística en tiempo real, dibujando el gráfico circular animado DonutChartView, las barras horizontales animadas, la opción ganadora, la lista de auditoría y el botón para compartir el Acta Oficial de Resultados.")

    # =========================================================================
    # CAPÍTULO III. DISEÑO DE LA APLICACIÓN MÓVIL Y ARQUITECTURA CLOUD
    # =========================================================================
    add_heading_1(doc, "CAPÍTULO III. DISEÑO DE LA APLICACIÓN MÓVIL Y ARQUITECTURA CLOUD")
    
    add_heading_2(doc, "3.1. Arquitectura de la Aplicación en Tres Capas y Backend Cloud")
    add_p(doc, "La arquitectura de VotaApp UNAMAD sigue un diseño modular en tres capas desacopladas (Presentación, Dominio/Lógica de Negocio y Persistencia Cloud/Local), alineado con las recomendaciones oficiales de Google Developers (2024) y Phillips et al. (2021):")
    add_p(doc, "1. Capa de Presentación y Componentes UI (Presentation Layer): Integrada por las 6 Activities del sistema (LoginActivity, MainActivity, CrearEncuestaActivity, GestionarPreguntasActivity, RegistrarVotoActivity y ResultadosActivity), el componente gráfico personalizado DonutChartView (basado en Android Canvas y ValueAnimator), el gestor de tema e insets UiInsetsHelper.kt y los layouts XML con soporte nativo para Modo Oscuro Obsidian MD3 (values-night/colors.xml).")
    add_p(doc, "2. Capa de Dominio y Modelos (Domain Layer): Conformada por Models.kt, que encapsula las estructuras de datos (UsuarioPerfil, Encuesta, Pregunta, Alternativa, ParticipanteRegistro, AlternativaEstadistica, PreguntaEstadistica) junto con el objeto singleton CatalogoUnamad, responsable del catálogo oficial de las 12 carreras profesionales, el extractor regex de códigos desde archivos Excel/.csv/.txt y el algoritmo de validación electoral verificarAcceso().")
    add_p(doc, "3. Capa de Datos y Servicios Cloud (Data & Persistence Layer): Orquestada por el repositorio singleton FirebaseRepository.kt, que centraliza las operaciones asíncronas con Firebase Authentication y Cloud Firestore (proyecto votaapp-unamad-2026), respaldada por las reglas de seguridad firestore.rules en el servidor y el gestor relacional local DatabaseHelper.kt (SQLiteOpenHelper sobre encuestas_unamad.db) para persistencia estructurada.")

    fig2_path = os.path.join(diag_dir, "fig2_arquitectura.png")
    add_apa_figure(doc, "2", "Diagrama de Arquitectura Modular en Tres Capas y Backend Firebase Cloud", fig2_path, note_text="Arquitectura en tres capas integrando las 6 Activities, DonutChartView, CatalogoUnamad, FirebaseRepository y Cloud Firestore (Elaboración propia, 2026).", width_cm=11.0)

    add_heading_2(doc, "3.2. Diseño de Interfaces de Usuario (6 Activities y Modo Oscuro Obsidian MD3)")
    add_p(doc, "El sistema de diseño de VotaApp UNAMAD implementa Material Design 3 con un tema predeterminado Modo Oscuro Obsidian (Obsidian Midnight #090E1A y superficies elevadas #121B2E) que reduce la fatiga visual y maximiza el contraste de los indicadores estadísticos, permitiendo conmutar al Modo Claro en cualquier momento. En las Figuras 3 y 4 se presentan los prototipos y flujos visuales de las 6 pantallas del sistema:")
    add_p(doc, "• Pantalla 1 (LoginActivity): Cabecera institucional UNAMAD con botón superior de cambio de tema (Modo Claro / Modo Oscuro), tarjeta elevada con campos TextInputLayout para correo y contraseña, fila horizontal simétrica que ubica el enlace 'Crear cuenta' al costado izquierdo de '¿Olvidaste tu contraseña?', sección colapsable de registro con selector Spinner de las 12 Escuelas Profesionales y código universitario, y botón oficial de Google Sign-In OAuth 2.0.")
    add_p(doc, "• Pantalla 2 (MainActivity): Centro de mando en la nube con SwipeRefreshLayout, barra superior con saludo personalizado ('Hola, Nombre • Código'), botones de edición de perfil ('Cuenta'), cambio de tema y cierre de sesión. Incluye tarjeta de 3 KPIs en tiempo real con numerales tabulares (fontFeatureSettings=\"tnum\"), buscador instantáneo etBuscarEncuesta, ChipGroup horizontal de categorías (cgCategorias), filtro segmentado (Todas, Activas, Cerradas) y listado de tarjetas item_encuesta con insignias de estado y restricción de carrera/padrón.")
    add_p(doc, "• Pantalla 3 (CrearEncuestaActivity): Formulario de alta y edición de encuestas con selector de categoría, tarjeta especial de Restricción de Acceso Electoral con Spinner de las 12 Escuelas Profesionales (spCarreraRestringida), botones de importación masiva de códigos ('Importar .txt / .csv' y 'Pegar de Excel'), contador dinámico de alumnos habilitados (tvContadorCodigos) y MaterialSwitch de estado activo.")
    add_p(doc, "• Pantalla 4 (GestionarPreguntasActivity): Constructor dinámico de preguntas de Selección Única (UNICA) o Selección Múltiple (MULTIPLE) con 2 a 4 alternativas y sincronización directa del arreglo de preguntas en Cloud Firestore.")

    fig3_path = os.path.join(diag_dir, "fig3_prototipos_ui.png")
    add_apa_figure(doc, "3", "Prototipos de Pantallas: Acceso, Panel Principal Cloud, Creación y Preguntas", fig3_path, note_text="Diseño de interfaces de usuario bajo lineamientos Material Design 3 (Elaboración propia, 2026).", width_cm=11.0)

    add_p(doc, "• Pantalla 5 (RegistrarVotoActivity): Cédula de votación digital de alta legibilidad. Precarga automáticamente el nombre y código universitario verificado del estudiante autenticado, valida su elegibilidad según carrera y padrón, y construye tarjetas de opción tonales interactivas (surface_option_selected y border_option_selected) que cambian de relieve y color al ser seleccionadas.")
    add_p(doc, "• Pantalla 6 (ResultadosActivity): Panel analítico de escrutinio en tiempo real. Por cada pregunta renderiza un gráfico circular animado DonutChartView con leyenda lateral y total de votos centrado, seguido de barras horizontales ProgressBar animadas, insignia dorada en la alternativa ganadora ('Ganadora • ...'), padrón auditable de votantes con marca de tiempo, botón de reinicio de conteo (exclusivo para el creador) y botón 'Compartir Acta Oficial de Resultados'.")

    fig4_path = os.path.join(diag_dir, "fig4_prototipos_votacion_resultados.png")
    add_apa_figure(doc, "4", "Prototipos de Pantallas: Registro de Votación y Resultados con DonutChartView", fig4_path, note_text="Interfaces móviles de votación tonal y escrutinio estadístico en tiempo real (Elaboración propia, 2026).", width_cm=10.8)

    add_heading_2(doc, "3.3. Diagrama de Navegación y Flujo de Pantallas")
    add_p(doc, "La navegación entre las 6 Activities se coordina mediante Intents explícitos que transportan el identificador documental EXTRA_ID_ENCUESTA. LoginActivity actúa como guardián de autenticación (Auth Gate): si Firebase.auth.currentUser está activo, redirige de inmediato a MainActivity. Desde MainActivity se bifurca el flujo hacia la creación/edición (CrearEncuestaActivity -> GestionarPreguntasActivity), la emisión del sufragio verificado (RegistrarVotoActivity) y la visualización o exportación del escrutinio (ResultadosActivity), como se ilustra en la Figura 5:")

    fig5_path = os.path.join(diag_dir, "fig5_navegacion.png")
    add_apa_figure(doc, "5", "Diagrama de Estados y Navegación entre las 6 Activities del Sistema", fig5_path, note_text="Flujo de navegación e intercambio de Intents entre las 6 pantallas de VotaApp UNAMAD (Elaboración propia, 2026).", width_cm=10.5)

    add_heading_2(doc, "3.4. Diseño de Datos en Cloud Firestore, Reglas de Seguridad y SQLite Local")
    add_p(doc, "El sistema implementa un modelo de datos híbrido orientado a documentos en la nube mediante Google Cloud Firestore (proyecto votaapp-unamad-2026) complementado por un esquema relacional en Tercera Forma Normal (3FN) en SQLite (Elmasri y Navathe, 2017; Hipp, 2024). En Cloud Firestore, la estructura se organiza en dos colecciones raíz (users y encuestas) y una subcolección jerárquica de sufragios (encuestas/{encuestaId}/votos/{voterUid}). El diseño asigna como ID del documento de voto el propio UID criptográfico del votante autenticado, lo cual garantiza matemáticamente a nivel de motor de base de datos y de reglas de seguridad que un estudiante solo pueda registrar un documento de voto por encuesta.")

    fig6_path = os.path.join(diag_dir, "fig6_base_datos_er.png")
    add_apa_figure(doc, "6", "Modelo de Datos Híbrido: Colecciones Cloud Firestore y Esquema Relacional SQLite", fig6_path, note_text="Estructura documental en Cloud Firestore y esquema relacional 3FN de respaldo en SQLite (Elaboración propia, 2026).", width_cm=10.5)

    add_p(doc, "A continuación se detallan los diccionarios de datos de las colecciones en Cloud Firestore y del esquema relacional local en formato APA 7 (Tablas 3 a 6):")

    # Tabla 3: Colección users
    t_usr_headers = ["Campo / Atributo", "Tipo Firestore", "Restricción / Regla", "Descripción Funcional"]
    t_usr_data = [
        ["uid (Document ID)", "String", "PK == request.auth.uid (Inmutable)", "Identificador único de Firebase Authentication del usuario."],
        ["nombre", "String", "Requerido (2 a 120 caracteres)", "Nombre completo del estudiante o docente universitario."],
        ["codigoUniversitario", "String", "Único en colección (0 a 30 chars)", "Código institucional de matrícula UNAMAD verificado sin duplicidad."],
        ["carrera", "String", "Catálogo 12 Escuelas UNAMAD", "Escuela Profesional oficial a la que pertenece el estudiante."],
        ["email", "String", "Formato Email válido (<= 254 chars)", "Correo electrónico institucional o personal vinculado a la cuenta."],
        ["fechaRegistro", "Number (Long)", "Timestamp >= 0 (Inmutable)", "Marca de tiempo epoch en milisegundos del alta inicial."]
    ]
    add_apa_table(doc, "3", "Diccionario de Datos Cloud Firestore: Colección 'users/{uid}'", [3.0, 2.3, 3.8, 6.4], t_usr_headers, t_usr_data, note_text="Elaboración propia a partir del modelo UsuarioPerfil en Models.kt y firestore.rules (2026).")

    # Tabla 4: Colección encuestas
    t_enc_headers = ["Campo / Atributo", "Tipo Firestore", "Restricción / Regla", "Descripción Funcional"]
    t_enc_data = [
        ["id (Document ID)", "String", "Auto-ID Firestore", "Identificador único global del documento de encuesta en la nube."],
        ["titulo", "String", "Requerido (5 a 160 caracteres)", "Título oficial de la encuesta o proceso electoral estudiantil."],
        ["descripcion", "String", "Requerido (1 a 1000 caracteres)", "Objetivo, instrucciones o contexto detallado de la consulta."],
        ["categoria", "String", "Enum (Académica, Satisfacción, Votación, General)", "Clasificación temática para filtrado rápido mediante ChipGroup."],
        ["activa", "Boolean", "true = Abierta | false = Cerrada", "Estado operativo que habilita o bloquea la recepción de votos."],
        ["fechaCreacion", "String", "Formato yyyy-MM-dd HH:mm (Inmutable)", "Estampa de tiempo de publicación original de la encuesta."],
        ["creadorUid", "String", "== request.auth.uid (Inmutable)", "UID del autor con privilegios exclusivos de edición y borrado."],
        ["creadorNombre", "String", "Requerido (1 a 120 caracteres)", "Nombre visible del docente o delegado organizador."],
        ["carreraRestringida", "String", "'TODAS' o 1 de las 12 Escuelas", "Filtro automático que restringe la votación a una carrera UNAMAD."],
        ["codigosPermitidos", "String", "Lista CSV/TXT o vacío (Abierta)", "Padrón de códigos universitarios autorizados importados de Excel/TXT."],
        ["preguntas", "Array<Map>", "Lista de 0 a 50 preguntas", "Arreglo estructurado con objetos Pregunta (id, texto, tipo, alternativas)."]
    ]
    add_apa_table(doc, "4", "Diccionario de Datos Cloud Firestore: Colección 'encuestas/{encuestaId}'", [3.0, 2.3, 3.8, 6.4], t_enc_headers, t_enc_data, note_text="Elaboración propia a partir del esquema documental de FirebaseRepository.kt (2026).")

    # Tabla 5: Subcolección votos
    t_vot_headers = ["Campo / Atributo", "Tipo Firestore", "Restricción / Regla", "Descripción Funcional"]
    t_vot_data = [
        ["voterUid (Doc ID)", "String", "PK == request.auth.uid (1 voto/UID)", "ID del documento idéntico al UID del votante; impide votos duplicados."],
        ["uid", "String", "Requerido (== voterUid)", "UID autenticado del estudiante que emite el sufragio."],
        ["participante", "String", "Requerido (2 a 120 caracteres)", "Etiqueta auditable del votante ('Nombre Completo - Código')."],
        ["fechaVoto", "String", "Formato yyyy-MM-dd HH:mm", "Fecha y hora exacta de emisión del sufragio en la nube."],
        ["respuestas", "Map<String, List>", "Máximo 50 entradas (Inmutable)", "Mapa que asocia cada idPregunta con la lista de idAlternativa elegidas."]
    ]
    add_apa_table(doc, "5", "Diccionario de Datos Cloud Firestore: Subcolección 'encuestas/{encuestaId}/votos/{voterUid}'", [3.0, 2.3, 3.8, 6.4], t_vot_headers, t_vot_data, note_text="Elaboración propia a partir de la subcolección de sufragios protegida por firestore.rules (2026).")

    # Tabla 6: Esquema SQLite de Respaldo Local
    t_sql_headers = ["Tabla SQLite Local", "Clave Primaria (PK)", "Claves Foráneas (FK) y Cascada", "Rol en el Módulo de Persistencia Local"]
    t_sql_data = [
        ["encuestas", "id_encuesta (INTEGER AUTOINCREMENT)", "Ninguna (Tabla Padre)", "Almacena metadatos locales de encuestas con estado activa (0/1)."],
        ["preguntas", "id_pregunta (INTEGER AUTOINCREMENT)", "id_encuesta -> encuestas ON DELETE CASCADE", "Registra enunciados asociados a una encuesta (UNICA / MULTIPLE)."],
        ["alternativas", "id_alternativa (INTEGER AUTOINCREMENT)", "id_pregunta -> preguntas ON DELETE CASCADE", "Guarda opciones de respuesta y contador local de votos."],
        ["respuestas", "id_respuesta (INTEGER AUTOINCREMENT)", "id_encuesta, id_pregunta, id_alternativa CASCADE", "Bitácora local de auditoría de sufragios con control yaVotoParticipante."]
    ]
    add_apa_table(doc, "6", "Estructura de Respaldo Local SQLite (encuestas_unamad.db)", [2.6, 3.2, 4.3, 5.4], t_sql_headers, t_sql_data, note_text="Elaboración propia basada en el esquema DDL de DatabaseHelper.kt (2026).")

    # =========================================================================
    # CAPÍTULO IV. DESARROLLO E IMPLEMENTACIÓN
    # =========================================================================
    add_heading_1(doc, "CAPÍTULO IV. DESARROLLO E IMPLEMENTACIÓN")
    
    add_heading_2(doc, "4.1. Herramientas, Tecnologías y Pipeline CI/CD con GitHub Actions")
    add_p(doc, "Para la construcción, sincronización en la nube y despliegue automatizado del sistema se empleó un stack tecnológico de última generación conforme a las especificaciones de Google Developers (2024) y Smyth (2023), detallado en la Tabla 7:")

    tech_headers = ["Herramienta / Tecnología", "Versión", "Rol en el Proyecto", "Justificación Técnica"]
    tech_data = [
        ["Kotlin", "2.2.10", "Lenguaje oficial de desarrollo", "Tipado estático con null-safety, lambdas, data classes y extensión de vistas."],
        ["Android Studio & SDK", "Ladybug | API 36 (Min 24)", "IDE y plataforma objetivo", "Soporte nativo desde Android 7.0 hasta Android 16 con Edge-to-Edge."],
        ["Firebase Authentication", "BoM 34.7.0", "Gestión de identidad en la nube", "Autenticación Email/Password, Google Sign-In OAuth 2.0 y reset de clave."],
        ["Cloud Firestore", "BoM 34.7.0 (votaapp-unamad-2026)", "Base de datos NoSQL Cloud", "Sincronización multi-dispositivo en tiempo real y reglas firestore.rules."],
        ["Material Components MD3", "1.10.0 + SwipeRefresh 1.1.0", "Sistema de diseño UI/UX", "Modo Oscuro Obsidian, ChipGroup, MaterialSwitch, TextInputLayout, Cards."],
        ["Kotlin Canvas & Animator", "Nativo Android Graphics", "Motor gráfico DonutChartView", "Renderizado vectorial antialiasing a 60 fps con DecelerateInterpolator."],
        ["SQLiteOpenHelper", "Nativo Android (encuestas_unamad.db)", "Persistencia relacional local", "Transacciones ACID locales con PRAGMA foreign_keys = ON y cascadas."],
        ["Gradle & GitHub Actions", "Gradle 9.6.0 / AGP 9.5.0", "Build y CI/CD Auto-Release", "Compilación en Ubuntu con JDK 17 Temurin y publicación de APK en Releases."]
    ]
    add_apa_table(doc, "7", "Stack de Herramientas, Servicios Cloud y Pipeline CI/CD", [2.8, 2.4, 3.4, 6.9], tech_headers, tech_data, note_text="Elaboración propia basada en libs.versions.toml, google-services.json y .github/workflows/android-release.yml (2026).")

    add_heading_2(doc, "4.2. Estructura Modular del Proyecto en Android Studio")
    add_p(doc, "El proyecto se estructura en 11 archivos Kotlin dentro del paquete com.example.proyectofinal, acompañados por sus recursos XML de diseño diurno/nocturno (res/layout, res/drawable, res/values y res/values-night), la configuración de Firebase (app/google-services.json), las reglas de seguridad (firestore.rules) y el flujo de integración continua (.github/workflows/android-release.yml). La Figura 7 ilustra la arquitectura de directorios del proyecto:")

    fig7_path = os.path.join(diag_dir, "fig7_estructura_proyecto.png")
    add_apa_figure(doc, "7", "Estructura Oficial de Paquetes, Módulos Kotlin y Recursos en Android Studio", fig7_path, note_text="Organización de los 11 archivos Kotlin, layouts XML, recursos Night Mode y pipeline CI/CD (Elaboración propia, 2026).", width_cm=10.8)

    add_heading_2(doc, "4.3. Implementación de Funcionalidades por Módulos y Código Fuente Real")
    add_p(doc, "A continuación se exponen los fragmentos clave del código fuente real en Kotlin compilado en app/src/main/java/com/example/proyectofinal/, demostrando la implementación técnica de las nuevas capacidades de VotaApp UNAMAD:")

    # 4.3.1 Models.kt y CatalogoUnamad
    add_heading_3(doc, "4.3.1. Modelos Cloud, Catálogo de 12 Carreras e Importador de Códigos (Models.kt)")
    add_p(doc, "En Models.kt se definen las entidades sincronizadas con Cloud Firestore y el objeto CatalogoUnamad, que lista las 12 Escuelas Profesionales de la UNAMAD, extrae códigos de matrícula mediante expresiones regulares desde archivos Excel (.csv) o texto (.txt) y verifica el acceso electoral del estudiante:")
    code_models = """package com.example.proyectofinal

data class UsuarioPerfil(
    val uid: String = "", val nombre: String = "", val codigoUniversitario: String = "",
    val carrera: String = "", val email: String = "", val fechaRegistro: Long = 0L
)

object CatalogoUnamad {
    val CARRERAS_UNAMAD = listOf(
        "Ingeniería de Sistemas e Informática", "Ingeniería Forestal y Medio Ambiente",
        "Ingeniería Agroindustrial", "Medicina Veterinaria y Zootecnia", "Enfermería",
        "Derecho y Ciencias Políticas", "Educación: Matemática y Computación",
        "Educación: Primaria e Informática", "Educación: Inicial y Especial",
        "Ecoturismo", "Administración y Negocios Internacionales", "Contabilidad y Finanzas"
    )
    val OPCIONES_FILTRO_CARRERA = listOf("Todas las carreras (Abierta)") + CARRERAS_UNAMAD

    fun extraerCodigosDesdeTexto(textoBruto: String): List<String> {
        if (textoBruto.isBlank()) return emptyList()
        val regexCodigo = Regex("\\\\b\\\\d{4,14}[A-Za-z0-9-]*\\\\b")
        val encontrados = regexCodigo.findAll(textoBruto)
            .map { it.value.trim().uppercase() }.distinct().toList()
        if (encontrados.isNotEmpty()) return encontrados
        return textoBruto.split(',', ';', '\\n', '\\r', '\\t', ' ')
            .map { it.trim().uppercase() }.filter { it.length >= 3 }.distinct()
    }
}

data class Encuesta(
    val id: String = "", val titulo: String = "", val descripcion: String = "",
    val categoria: String = "General", val activa: Boolean = true, val fechaCreacion: String = "",
    val creadorUid: String = "", val creadorNombre: String = "",
    val carreraRestringida: String = "TODAS", val codigosPermitidos: String = "",
    val preguntas: List<Pregunta> = emptyList(), var totalPreguntas: Int = 0, var totalVotos: Int = 0
) {
    fun verificarAcceso(perfil: UsuarioPerfil?, uidActual: String?): Pair<Boolean, String> {
        if (!uidActual.isNullOrBlank() && uidActual == creadorUid) return true to "Creador de la encuesta"
        val tieneCarrera = carreraRestringida.isNotBlank() && carreraRestringida != "TODAS"
        val cods = CatalogoUnamad.extraerCodigosDesdeTexto(codigosPermitidos)
        if (!tieneCarrera && cods.isEmpty()) return true to "Acceso abierto"
        val miCodigo = perfil?.codigoUniversitario?.trim()?.uppercase() ?: ""
        val miCarrera = perfil?.carrera?.trim() ?: ""
        if (tieneCarrera && !miCarrera.equals(carreraRestringida, ignoreCase = true)) {
            return false to "Esta encuesta es exclusiva para estudiantes de $carreraRestringida."
        }
        if (cods.isNotEmpty() && !cods.any { token -> miCodigo == token || (token.length in 4..6 && miCodigo.startsWith(token)) }) {
            return false to "Tu código ($miCodigo) no figura en el padrón autorizado (${cods.size} habilitados)."
        }
        return true to "Autorizado"
    }
}"""
    add_code_block(doc, code_models)

    # 4.3.2 FirebaseRepository.kt
    add_heading_3(doc, "4.3.2. Repositorio en la Nube y Voto Único por UID (FirebaseRepository.kt)")
    add_p(doc, "El objeto singleton FirebaseRepository administra las colecciones users, encuestas y la subcolección votos en Cloud Firestore, verificando que ningún código universitario se duplique entre distintos UIDs y registrando el voto único bajo la llave encuestas/{encuestaId}/votos/{uid}:")
    code_repo = """object FirebaseRepository {
    private val db get() = Firebase.firestore
    private val auth get() = Firebase.auth
    private const val COL_USERS = "users"
    private const val COL_ENCUESTAS = "encuestas"
    private const val SUB_VOTOS = "votos"

    fun yaVotoUsuario(encuestaId: String, uid: String, onResult: (Boolean) -> Unit) {
        db.collection(COL_ENCUESTAS).document(encuestaId)
            .collection(SUB_VOTOS).document(uid).get()
            .addOnSuccessListener { doc -> onResult(doc.exists()) }
            .addOnFailureListener { onResult(false) }
    }

    fun registrarVoto(
        encuestaId: String,
        participante: String,
        respuestasPorPregunta: Map<String, List<String>>,
        onComplete: (Boolean, String?) -> Unit
    ) {
        val uid = auth.currentUser?.uid ?: return onComplete(false, "Sesión no iniciada.")
        val fechaVoto = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault()).format(Date())
        val votoRef = db.collection(COL_ENCUESTAS).document(encuestaId)
            .collection(SUB_VOTOS).document(uid)

        val data = hashMapOf(
            "uid" to uid,
            "participante" to participante.trim(),
            "fechaVoto" to fechaVoto,
            "respuestas" to respuestasPorPregunta
        )
        votoRef.set(data)
            .addOnSuccessListener { onComplete(true, null) }
            .addOnFailureListener { e -> onComplete(false, e.localizedMessage) }
    }
}"""
    add_code_block(doc, code_repo)

    # 4.3.3 LoginActivity.kt
    add_heading_3(doc, "4.3.3. Autenticación Firebase, Google Sign-In OAuth 2.0 y Recuperación (LoginActivity.kt)")
    add_p(doc, "LoginActivity integra inicio de sesión con Correo/Contraseña, federación OAuth 2.0 con GoogleAuthProvider, restablecimiento de contraseña por correo y registro con selección de Escuela Profesional UNAMAD:")
    code_login = """private fun autenticarConGoogleEnFirebase(idToken: String, nombreCuenta: String, emailCuenta: String) {
    val credential = GoogleAuthProvider.getCredential(idToken, null)
    auth.signInWithCredential(credential)
        .addOnSuccessListener { res ->
            val uid = res.user?.uid ?: ""
            FirebaseRepository.obtenerPerfilUsuario(uid) { perfilExistente ->
                if (perfilExistente == null) {
                    FirebaseRepository.guardarPerfilUsuario(uid, nombreCuenta, "", emailCuenta, "") { _, _ -> irAMain() }
                } else {
                    irAMain()
                }
            }
        }
        .addOnFailureListener { e ->
            mostrarCargando(false)
            Toast.makeText(this, "Error con Google Auth: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
        }
}

private fun mostrarDialogoRecuperarPassword() {
    val inputEmail = EditText(this).apply {
        hint = "ejemplo@unamad.edu.pe"
        setText(etAuthEmail.text.toString().trim())
    }
    MaterialAlertDialogBuilder(this)
        .setTitle("Recuperar Contraseña")
        .setMessage("Ingresa tu correo registrado y te enviaremos un enlace para restablecer tu contraseña.")
        .setView(inputEmail)
        .setPositiveButton("Enviar Enlace") { _, _ ->
            val correo = inputEmail.text.toString().trim()
            if (correo.isNotEmpty()) auth.sendPasswordResetEmail(correo)
        }
        .setNegativeButton("Cancelar", null)
        .show()
}"""
    add_code_block(doc, code_login)

    # 4.3.4 CrearEncuestaActivity.kt
    add_heading_3(doc, "4.3.4. Filtro de 12 Escuelas e Importación de Padrón Excel/TXT (CrearEncuestaActivity.kt)")
    add_p(doc, "CrearEncuestaActivity permite importar archivos .txt o .csv directamente desde el almacenamiento del dispositivo o pegar bloques copiados desde hojas de cálculo de Microsoft Excel:")
    code_crear = """private val selectorArchivoCodigos = registerForActivityResult(
    ActivityResultContracts.GetContent()
) { uri: Uri? ->
    if (uri != null) importarCodigosDesdeUri(uri)
}

private fun importarCodigosDesdeUri(uri: Uri) {
    val contenido = contentResolver.openInputStream(uri)?.bufferedReader()?.use { it.readText() } ?: ""
    val extraidos = CatalogoUnamad.extraerCodigosDesdeTexto(contenido)
    if (extraidos.isNotEmpty()) {
        val existentes = CatalogoUnamad.extraerCodigosDesdeTexto(etCodigosPermitidos.text.toString())
        val combinados = (existentes + extraidos).distinct()
        etCodigosPermitidos.setText(combinados.joinToString(", "))
        Toast.makeText(this, "Se importaron ${extraidos.size} códigos (${combinados.size} en total).", Toast.LENGTH_SHORT).show()
    }
}"""
    add_code_block(doc, code_crear)

    # 4.3.5 DonutChartView.kt y ResultadosActivity.kt
    add_heading_3(doc, "4.3.5. Gráfico Circular Animado en Canvas y Acta Oficial (DonutChartView.kt y ResultadosActivity.kt)")
    add_p(doc, "DonutChartView extiende de View y dibuja mediante Canvas arcos proporcionales animados con ValueAnimator (650 ms) y leyenda lateral, mientras que ResultadosActivity permite exportar el Acta Oficial de Resultados:")
    code_donut = """class DonutChartView @JvmOverloads constructor(context: Context, attrs: AttributeSet? = null) : View(context, attrs) {
    data class Slice(val label: String, val value: Float, val color: Int)
    private var slices: List<Slice> = emptyList()
    private var totalVotos: Int = 0
    private var animProgress: Float = 1f

    fun setData(alternatives: List<AlternativaEstadistica>, total: Int) {
        totalVotos = total
        slices = alternatives.mapIndexed { idx, alt ->
            Slice(
                label = "${alt.texto.take(22)} (${String.format("%.0f", alt.porcentaje)}%)",
                value = alt.votos.toFloat(),
                color = if (alt.esGanadora) Color.parseColor("#D97706") else PALETTE[idx % PALETTE.size]
            )
        }
        ValueAnimator.ofFloat(0f, 1f).apply {
            duration = 650
            interpolator = DecelerateInterpolator()
            addUpdateListener { animProgress = it.animatedValue as Float; invalidate() }
            start()
        }
    }
}"""
    add_code_block(doc, code_donut)

    add_heading_2(doc, "4.4. Seguridad en la Nube (firestore.rules) y Pipeline CI/CD (GitHub Actions)")
    add_p(doc, "Para blindar la integridad electoral en el servidor de Google Cloud, se codificaron reglas declarativas en firestore.rules siguiendo el principio de mínimo privilegio (OWASP Foundation, 2024). La colección users/{uid} restringe la lectura y escritura exclusivamente al propietario del UID para proteger datos personales (PII). En encuestas/{encuestaId}/votos/{voterUid}, la regla allow create exige que isOwner(voterUid) sea verdadero, que la encuesta esté activa (isEncuestaActiva(encuestaId)) y prohíbe cualquier modificación posterior (allow update: if false):")
    code_rules = """match /encuestas/{encuestaId} {
  allow read: if isAuthenticated();
  allow create: if isAuthenticated() && isValidEncuesta(request.resource.data)
                && request.resource.data.creadorUid == request.auth.uid;
  allow update, delete: if isAuthenticated() && resource.data.creadorUid == request.auth.uid;

  match /votos/{voterUid} {
    allow read: if isAuthenticated();
    allow create: if isOwner(voterUid) && isValidVoto(request.resource.data, voterUid)
                  && isEncuestaActiva(encuestaId);
    allow update: if false;
    allow delete: if isAuthenticated() && isEncuestaCreator(encuestaId);
  }
}"""
    add_code_block(doc, code_rules)

    add_p(doc, "Asimismo, se implementó el flujo de Integración y Entrega Continua (CI/CD) en .github/workflows/android-release.yml dentro del repositorio oficial https://github.com/Maickel69/VotaApp-UNAMAD. Ante cada confirmación de código en la rama main, GitHub Actions aprovisiona un contenedor Ubuntu con JDK 17 (Eclipse Temurin) y Gradle 9.6.0, ejecuta las pruebas unitarias (./gradlew testDebugUnitTest), compila el paquete instalador (./gradlew assembleDebug) y actualiza automáticamente el release público etiquetado como latest-apk con el binario VotaApp-UNAMAD.apk.")

    add_heading_2(doc, "4.5. Experiencia de Usuario, Modo Oscuro Obsidian MD3 y Edge-to-Edge")
    add_p(doc, "• Modo Oscuro Obsidian MD3 (values-night/colors.xml): Define una jerarquía cromática de alto contraste con fondo principal Obsidian Midnight (#090E1A), tarjetas elevadas (#121B2E), contenedores tonales (#0D1526 y #1A2640), acento primario azul eléctrico (#3B82F6), insignias esmeralda para encuestas activas (#34D399) y resaltado ámbar para alternativas ganadoras (#FBBF24).")
    add_p(doc, "• Gestión Edge-to-Edge e Insets (UiInsetsHelper.kt): La función de extensión configurarEdgeToEdgeConHeader() aplica el modo oscuro por defecto mediante AppCompatDelegate.setDefaultNightMode(), configura íconos claros en la barra de estado y consume dinámicamente los insets de WindowInsetsCompat.Type.systemBars(), displayCutout() e ime() (teclado virtual) para evitar cualquier solapamiento en Android 16 (API 36).")

    # =========================================================================
    # CAPÍTULO V. PRUEBAS Y RESULTADOS
    # =========================================================================
    add_heading_1(doc, "CAPÍTULO V. PRUEBAS Y RESULTADOS")
    
    add_heading_2(doc, "5.1. Matriz Exhaustiva de Pruebas Funcionales")
    add_p(doc, "Se diseñó y ejecutó una matriz de 12 casos de prueba funcionales de caja negra (CP01 a CP12) cubriendo la totalidad de los requerimientos funcionales (RF01 a RF12). Conforme a Pressman y Maxim (2021), cada caso validó las precondiciones, pasos de ejecución y postcondiciones tanto en el cliente Android como en la consola de Firebase Cloud Firestore, alcanzando un 100% de aprobación en la Tabla 8:")

    cp_headers = ["ID", "RF", "Caso de Prueba", "Pasos de Ejecución", "Resultado Esperado", "Resultado Obtenido", "Estado"]
    cp_data = [
        ["CP01", "RF01", "Login Email/Password y Google OAuth 2.0", "Iniciar sesión con credenciales válidas o cuenta de Google.", "Autenticación exitosa en Firebase Auth y paso a MainActivity.", "Sesión iniciada con token OAuth 2.0 y UID activo.", "APROBADO"],
        ["CP02", "RF01", "Recuperación de contraseña por correo", "Pulsar '¿Olvidaste tu contraseña?' e ingresar correo institucional.", "Firebase envía correo de restablecimiento de clave.", "Alerta de confirmación y recepción de enlace oficial.", "APROBADO"],
        ["CP03", "RF02", "Validación de código universitario único", "Intentar registrar en 'Cuenta' un código asignado a otro UID.", "Firestore detecta colisión y rechaza el código duplicado.", "Mensaje: 'El código ya está registrado por otro estudiante'.", "APROBADO"],
        ["CP04", "RF03", "Búsqueda y filtrado por ChipGroup y estado", "Escribir texto en buscador y alternar chips de categoría y estado.", "La lista filtra en tiempo real sin recargar la pantalla.", "Filtrado multicriterio instantáneo y KPIs con tnum.", "APROBADO"],
        ["CP05", "RF04", "Creación de encuesta en Cloud Firestore", "Completar título, descripción, categoría y pulsar Guardar.", "Documento creado en colección encuestas/{encuestaId}.", "Persistencia inmediata en la nube y listado en panel.", "APROBADO"],
        ["CP06", "RF05", "Filtro por las 12 Escuelas Profesionales", "Restringir encuesta a 'Ingeniería de Sistemas e Informática'.", "Estudiantes de otras carreras ven bloqueado el acceso al voto.", "verificarAcceso() bloquea carreras distintas con aviso claro.", "APROBADO"],
        ["CP07", "RF05", "Importación masiva de códigos (.csv / Excel)", "Pulsar 'Importar .txt/.csv' o 'Pegar de Excel' con 45 códigos.", "Extractor regex detecta los 45 códigos y actualiza contador.", "Se importan y normalizan los códigos sin duplicados.", "APROBADO"],
        ["CP08", "RF07", "Gestión de preguntas UNICA y MULTIPLE", "Agregar preguntas con 3 alternativas en GestionarPreguntasActivity.", "Arreglo preguntas actualizado en el documento de Firestore.", "Sincronización exitosa y validación de mínimo 2 opciones.", "APROBADO"],
        ["CP09", "RF09", "Control de voto único por UID en Firestore", "Emitir voto en RegistrarVotoActivity e intentar votar de nuevo.", "El sistema detecta el documento votos/{uid} y bloquea el reenvío.", "Modo solo lectura activado y regla isOwner en servidor.", "APROBADO"],
        ["CP10", "RF10", "Renderizado de DonutChartView y ganador", "Abrir ResultadosActivity tras registrar sufragios en la nube.", "Gráfico de dona animado (650 ms), barras y medalla ganadora.", "Cálculo porcentual exacto y animación fluida a 60 fps.", "APROBADO"],
        ["CP11", "RF11", "Auditoría de votantes y reinicio de conteo", "Verificar lista de votantes y pulsar 'Reiniciar Conteo de Votos'.", "Solo el creador puede vaciar la subcolección votos con WriteBatch.", "Padrón auditable visible y reinicio a 0 votos confirmado.", "APROBADO"],
        ["CP12", "RF12", "Exportación de Acta Oficial de Resultados", "Pulsar 'Compartir Acta Oficial de Resultados' en ResultadosActivity.", "Se despliega el selector nativo de Android con el acta formateada.", "Acta enviada correctamente por WhatsApp y correo.", "APROBADO"]
    ]
    add_apa_table(doc, "8", "Matriz de Casos de Prueba Funcionales (CP01 - CP12)", [1.0, 1.0, 2.5, 3.1, 2.8, 2.8, 2.3], cp_headers, cp_data, note_text="Elaboración propia basada en las pruebas ejecutadas en emulador Android 16 (API 36) conectado a Firebase Cloud (2026).")

    add_heading_2(doc, "5.2. Evidencias de Ejecución y Validación en Emulador Android 16")
    add_p(doc, "Las pruebas integrales se ejecutaron sobre el emulador Android Medium_Phone_2 (Android 16 / API 36) verificando las seis Activities en Modo Oscuro Obsidian MD3 y Modo Claro:")
    add_p(doc, "• Flujo de Autenticación, Dashboard Cloud y Configuración (Figura 8): Evidencia la pantalla LoginActivity con inicio de sesión Email/Google OAuth 2.0 y enlace 'Crear cuenta' junto a '¿Olvidaste tu contraseña?', el panel principal MainActivity con tarjetas KPI tabulares, ChipGroup de categorías y búsqueda en tiempo real, así como CrearEncuestaActivity (con selector de las 12 carreras UNAMAD e importación de padrón) y GestionarPreguntasActivity.")

    ev1_path = os.path.join(cap_dir, "evidencia_1_gestion.png")
    add_apa_figure(doc, "8", "Capturas Reales en Emulador: Login OAuth, Panel Principal, Creación y Preguntas", ev1_path, note_text="Ejecución real de los módulos de acceso, panel Cloud, creación con filtro de carrera/padrón y gestión de preguntas (Elaboración propia, 2026).", width_cm=13.5)

    add_p(doc, "• Flujo de Votación Tonal y Escrutinio con DonutChartView (Figura 9): Evidencia la cédula interactiva en RegistrarVotoActivity con verificación automática del estudiante autenticado y la pantalla ResultadosActivity renderizando el gráfico circular animado DonutChartView, las barras horizontales de progreso, la distinción de la alternativa ganadora, el registro auditable de participantes y la acción para compartir el Acta Oficial de Resultados.")

    ev2_path = os.path.join(cap_dir, "evidencia_2_resultados.png")
    add_apa_figure(doc, "9", "Capturas Reales en Emulador: Votación Tonal y Resultados con DonutChartView", ev2_path, note_text="Ejecución real de RegistrarVotoActivity y ResultadosActivity con gráfico de dona en Canvas y barras de progreso (Elaboración propia, 2026).", width_cm=10.5)

    add_heading_2(doc, "5.3. Dificultades Técnicas Identificadas y Soluciones de Ingeniería")
    add_p(doc, "Durante el desarrollo e integración en la nube se resolvieron seis desafíos técnicos de ingeniería detallados en la Tabla 9:")

    dif_headers = ["N°", "Desafío Técnico Identificado", "Impacto Inicial en la App", "Solución de Ingeniería Aplicada en Kotlin / Cloud"]
    dif_data = [
        ["1", "Control de voto único en entornos multi-dispositivo en la nube", "Un usuario podía intentar votar desde dos teléfonos simultáneamente.", "Se diseñó la subcolección encuestas/{id}/votos/{voterUid} donde el ID del documento es el UID de Firebase Auth, validado en firestore.rules con isOwner(voterUid)."],
        ["2", "Extracción de códigos desde hojas de Excel con columnas mixtas", "Al copiar celdas de Excel venían nombres, tabulaciones y encabezados junto a los códigos.", "Se programó CatalogoUnamad.extraerCodigosDesdeTexto() con la expresión regular \\b\\d{4,14}[A-Za-z0-9-]*\\b que filtra y deduplica solo las matrículas."],
        ["3", "Colisión de códigos universitarios entre cuentas distintas", "Dos cuentas de correo diferentes podían escribir el mismo código estudiantil.", "En FirebaseRepository.guardarPerfilUsuario() se agregó una consulta previa whereEqualTo('codigoUniversitario', cod) que impide asignar un código ya ocupado por otro UID."],
        ["4", "Superposición de barra de estado y teclado en Android 16 (API 36)", "El modo Edge-to-Edge recortaba cabeceras o cubría inputs inferiores al abrir el teclado.", "Se implementó configurarEdgeToEdgeConHeader() en UiInsetsHelper.kt combinando WindowInsetsCompat.Type.systemBars(), displayCutout() e ime()."],
        ["5", "Pérdida de opciones marcadas al girar la pantalla durante el voto", "La recreación de la Activity limpiaba los RadioButtons y CheckBoxes dinámicos.", "Se implementó onSaveInstanceState() en RegistrarVotoActivity guardando los tags de las alternativas seleccionadas en KEY_SELECCIONES."],
        ["6", "Compilación manual repetitiva del instalador APK para distribución", "Generar y subir el APK manualmente tras cada mejora retrasaba las pruebas.", "Se configuró el pipeline CI/CD en .github/workflows/android-release.yml con GitHub Actions que compila con Gradle 9.6 y publica el release latest-apk automáticamente."]
    ]
    add_apa_table(doc, "9", "Matriz de Dificultades Técnicas y Soluciones de Ingeniería", [0.8, 3.6, 4.1, 7.0], dif_headers, dif_data, note_text="Elaboración propia con base en las soluciones arquitectónicas implementadas en VotaApp UNAMAD (2026).")

    add_heading_2(doc, "5.4. Evaluación de Cumplimiento y Resultados")
    add_p(doc, "La Tabla 10 sintetiza la matriz de trazabilidad que contrasta los objetivos específicos planteados al inicio del proyecto frente a los módulos entregados y validados según el estándar ISO/IEC 25010 (ISO/IEC, 2011):")

    eval_headers = ["Objetivo Específico", "Requerimientos Vinculados", "Resultado de Ingeniería Logrado", "Cumplimiento"]
    eval_data = [
        ["OE1: Autenticación Firebase, OAuth 2.0 y Perfil UNAMAD", "RF01, RF02, RNF03", "LoginActivity con Email/Password, Google Sign-In, reset de clave y perfil con las 12 carreras.", "100% CUMPLIDO"],
        ["OE2: 6 Activities en Modo Oscuro Obsidian MD3", "RF03, RNF01, RNF04", "6 pantallas responsivas con Modo Oscuro Obsidian, búsqueda, ChipGroup y Edge-to-Edge.", "100% CUMPLIDO"],
        ["OE3: Backend Cloud Firestore, Padrón y Reglas", "RF04 - RF09, RNF03, RNF05", "FirebaseRepository, firestore.rules, filtro por carrera, importador Excel/CSV y 1 voto/UID.", "100% CUMPLIDO"],
        ["OE4: Escrutinio con DonutChartView, Acta y CI/CD", "RF10 - RF12, RNF02, RNF07", "Gráfico DonutChartView en Canvas, barras animadas, Acta Oficial y GitHub Actions auto-release.", "100% CUMPLIDO"]
    ]
    add_apa_table(doc, "10", "Matriz de Trazabilidad y Evaluación de Cumplimiento", [3.6, 3.0, 6.2, 2.7], eval_headers, eval_data, note_text="Elaboración propia basada en la verificación final del sistema VotaApp UNAMAD (2026).")

    # =========================================================================
    # CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    add_heading_1(doc, "CONCLUSIONES Y RECOMENDACIONES")
    
    add_heading_2(doc, "Conclusiones")
    add_p(doc, "1. Se desarrolló, implementó y desplegó satisfactoriamente la aplicación móvil nativa 'VotaApp UNAMAD' en lenguaje Kotlin integrada con Google Firebase (Authentication y Cloud Firestore), dotando a las 12 Escuelas Profesionales de la Universidad Nacional Amazónica de Madre de Dios de una plataforma en tiempo real para la gestión transparente de encuestas académicas y elecciones estudiantiles.")
    add_p(doc, "2. La arquitectura de seguridad e identidad basada en LoginActivity (Correo/Contraseña y Google Sign-In OAuth 2.0), combinada con la validación de código universitario único en users/{uid} y la subcolección encuestas/{encuestaId}/votos/{voterUid} resguardada por firestore.rules, erradicó por completo el riesgo de votos duplicados y garantizó el principio democrático de un voto único por estudiante autenticado.")
    add_p(doc, "3. La incorporación del motor de segmentación electoral en CrearEncuestaActivity y CatalogoUnamad permitió restringir votaciones de manera automática a cualquiera de las 12 carreras profesionales de la UNAMAD o importar en segundos padrones de matrícula desde archivos Excel (.csv), texto (.txt) o portapapeles, adaptándose con precisión a la realidad operativa de las aulas universitarias.")
    add_p(doc, "4. El diseño visual bajo Material Design 3 con Modo Oscuro Obsidian predeterminado, junto con el gráfico circular animado DonutChartView en Canvas, las barras de progreso horizontales animadas, la exportación del Acta Oficial de Resultados y la automatización de entregas APK mediante GitHub Actions CI/CD, consolidaron un producto de software de calidad industrial alineado con la norma ISO/IEC 25010.")

    add_heading_2(doc, "Recomendaciones")
    add_p(doc, "1. Notificaciones Push con Firebase Cloud Messaging (FCM): Se recomienda integrar el servicio FCM para enviar alertas automáticas a los teléfonos de los estudiantes de una Escuela Profesional cuando se publique una nueva elección o falten pocos minutos para el cierre del padrón.")
    add_p(doc, "2. Verificación Biométrica Local (BiometricPrompt): Para elecciones de alta sensibilidad institucional, se sugiere añadir un paso adicional de confirmación mediante huella dactilar o reconocimiento facial nativo de Android antes de ejecutar FirebaseRepository.registrarVoto().")
    add_p(doc, "3. Firma Digital Criptográfica de Actas en PDF: Se aconseja extender la funcionalidad de exportación del Acta Oficial de Resultados para generar documentos PDF con código QR de verificación vinculable directamente a la URL de auditoría del documento en Cloud Firestore.")
    add_p(doc, "4. Panel Web Administrativo Complementario: Aprovechando que el backend ya opera en tiempo real sobre el proyecto Cloud Firestore votaapp-unamad-2026, se recomienda proyectar un dashboard web en Firebase Hosting para proyectar el escrutinio en vivo en los auditorios universitarios.")

    # =========================================================================
    # REFERENCIAS BIBLIOGRÁFICAS (Normas APA 7ma Edición, Arial, 100% Negro)
    # =========================================================================
    add_heading_1(doc, "REFERENCIAS BIBLIOGRÁFICAS")
    
    referencias_apa7 = [
        ("Deitel, P., & Deitel, H. (2020). ", "Android how to program with an introduction to Java and Kotlin", " (4th ed.). Pearson Education."),
        ("Elmasri, R., & Navathe, S. B. (2017). ", "Fundamentos de sistemas de bases de datos", " (7ª ed.). Pearson Educación."),
        ("Google Developers. (2024). ", "Guía de arquitectura de aplicaciones Android y documentación oficial de Firebase Cloud Firestore", ". Android Developers Documentation. https://developer.android.com/topic/architecture"),
        ("Hipp, D. R. (2024). ", "SQLite documentation and architecture specifications", ". SQLite Consortium. https://www.sqlite.org/docs.html"),
        ("ISO/IEC. (2011). ", "Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models", " (ISO/IEC Standard No. 25010:2011). International Organization for Standardization. https://www.iso.org/standard/35733.html"),
        ("Jemerov, D., & Isakova, S. (2022). ", "Kotlin in action", " (2nd ed.). Manning Publications."),
        ("JetBrains. (2024). ", "Kotlin programming language reference", ". JetBrains Documentation. https://kotlinlang.org/docs/home.html"),
        ("OWASP Foundation. (2024). ", "OWASP Mobile Application Security Verification Standard (MASVS) and serverless security rules guide", ". OWASP. https://mas.owasp.org/"),
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

    # Copia sincronizada en Informe_WordCraft_VotaApp_UNAMAD.docx
    wordcraft_copy = os.path.join(os.path.dirname(docx_path), "Informe_WordCraft_VotaApp_UNAMAD.docx")
    shutil.copy2(docx_path, wordcraft_copy)
    print(f"Copia WordCraft generada exitosamente en: {wordcraft_copy}")

if __name__ == "__main__":
    out_docx = r"C:\Users\HP\AndroidStudioProjects\ProyectoFinal\Documentacion\Informe_Tecnico_Encuestas_Votaciones_UNAMAD.docx"
    crear_informe_completo(out_docx)
