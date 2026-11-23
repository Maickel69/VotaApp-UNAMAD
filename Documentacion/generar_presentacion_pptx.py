import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# =============================================================================
# PALETA DARK MODE OBSIDIAN & UNAMAD INSTITUTIONAL BLUE
# =============================================================================
BG_OBSIDIAN = RGBColor(9, 14, 26)        # #090E1A - Fondo principal Obsidian
SURFACE_CARD = RGBColor(18, 27, 46)      # #121B2E - Superficie de tarjetas
SURFACE_ELEVATED = RGBColor(24, 36, 61)  # #18243D - Superficie secundaria / badge
UNAMAD_BLUE = RGBColor(30, 58, 138)      # #1E3A8A - Azul Institucional UNAMAD
ACCENT_BLUE = RGBColor(59, 130, 246)     # #3B82F6 - Azul Eléctrico Principal
EMERALD = RGBColor(52, 211, 153)         # #34D399 - Verde Esmeralda (Verificado / Cloud)
TEXT_WHITE = RGBColor(248, 250, 252)     # #F8FAFC - Texto primario blanco nieve
TEXT_SILVER = RGBColor(203, 213, 225)    # #CBD5E1 - Texto secundario claro
TEXT_MUTED = RGBColor(148, 163, 184)     # #94A3B8 - Texto atenuado / subtítulos
AMBER_GOLD = RGBColor(245, 158, 11)      # #F59E0B - Ámbar (Ganadora / Estadísticas)
CORAL_RED = RGBColor(248, 113, 113)      # #F87171 - Coral (Problemática / Alertas)
BORDER_SUBTLE = RGBColor(36, 52, 84)     # #243454 - Borde sutil de tarjetas


def set_slide_bg(slide, color=BG_OBSIDIAN):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, badge_text, title_text, subtitle_text, slide_num, total_slides=11):
    # Barra superior Obsidian elevada
    top_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.12)
    )
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = SURFACE_CARD
    top_bar.line.fill.background()

    # Banda lateral izquierda azul eléctrico
    left_stripe = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.12), Inches(1.12)
    )
    left_stripe.fill.solid()
    left_stripe.fill.fore_color.rgb = ACCENT_BLUE
    left_stripe.line.fill.background()

    # Línea inferior de acento institucional
    bottom_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.12), Inches(13.333), Inches(0.035)
    )
    bottom_line.fill.solid()
    bottom_line.fill.fore_color.rgb = UNAMAD_BLUE
    bottom_line.line.fill.background()

    # Badge de sección arriba a la derecha
    badge = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.25), Inches(0.18), Inches(2.55), Inches(0.34)
    )
    badge.fill.solid()
    badge.fill.fore_color.rgb = UNAMAD_BLUE
    badge.line.color.rgb = ACCENT_BLUE
    badge.line.width = Pt(1)
    badge.adjustments[0] = 0.45

    b_tf = badge.text_frame
    b_tf.word_wrap = False
    b_p = b_tf.paragraphs[0]
    b_p.alignment = PP_ALIGN.CENTER
    b_r = b_p.add_run()
    b_r.text = badge_text.upper()
    b_r.font.name = "Segoe UI"
    b_r.font.size = Pt(9.5)
    b_r.font.bold = True
    b_r.font.color.rgb = TEXT_WHITE

    # Título y subtítulo de la diapositiva
    tb = slide.shapes.add_textbox(Inches(0.45), Inches(0.10), Inches(9.65), Inches(0.96))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_top = Inches(0.04)

    p1 = tf.paragraphs[0]
    p1.space_after = Pt(2)
    r1 = p1.add_run()
    r1.text = title_text
    r1.font.name = "Segoe UI"
    r1.font.size = Pt(21)
    r1.font.bold = True
    r1.font.color.rgb = TEXT_WHITE

    p2 = tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = subtitle_text
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(11)
    r2.font.color.rgb = TEXT_MUTED

    # Pie de página institucional
    footer_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(7.08), Inches(12.23), Inches(0.015)
    )
    footer_line.fill.solid()
    footer_line.fill.fore_color.rgb = BORDER_SUBTLE
    footer_line.line.fill.background()

    ft_left = slide.shapes.add_textbox(Inches(0.55), Inches(7.12), Inches(8.5), Inches(0.30))
    ft_ltf = ft_left.text_frame
    ft_lp = ft_ltf.paragraphs[0]
    ft_lr = ft_lp.add_run()
    ft_lr.text = "UNAMAD · EPISI · Desarrollo de Aplicaciones Móviles II (2026-II) · VotaApp UNAMAD Cloud"
    ft_lr.font.name = "Segoe UI"
    ft_lr.font.size = Pt(9.5)
    ft_lr.font.color.rgb = TEXT_MUTED

    ft_right = slide.shapes.add_textbox(Inches(9.2), Inches(7.12), Inches(3.58), Inches(0.30))
    ft_rtf = ft_right.text_frame
    ft_rp = ft_rtf.paragraphs[0]
    ft_rp.alignment = PP_ALIGN.RIGHT
    ft_rr = ft_rp.add_run()
    ft_rr.text = f"Diapositiva {slide_num} de {total_slides}"
    ft_rr.font.name = "Segoe UI"
    ft_rr.font.size = Pt(9.5)
    ft_rr.font.bold = True
    ft_rr.font.color.rgb = ACCENT_BLUE


def add_card_base(slide, left, top, width, height, accent_color=ACCENT_BLUE, bg_color=SURFACE_CARD, border_color=BORDER_SUBTLE):
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.1)
    card.adjustments[0] = 0.03

    # Barra de acento superior izquierda dentro de la tarjeta
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(left), Inches(top + 0.16), Inches(0.08), Inches(0.38)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent_color
    bar.line.fill.background()
    return card


def add_card(
    slide,
    left,
    top,
    width,
    height,
    title,
    items,
    accent_color=ACCENT_BLUE,
    title_size=14.5,
    body_size=11.5,
    space_after=5,
    bg_color=SURFACE_CARD,
    border_color=BORDER_SUBTLE
):
    """
    Crea una tarjeta estilizada Dark Mode Obsidian.
    `items` puede ser una lista de strings o tuplas `(prefijo_negrita, texto_normal)`.
    """
    add_card_base(slide, left, top, width, height, accent_color, bg_color, border_color)

    tb = slide.shapes.add_textbox(
        Inches(left + 0.20), Inches(top + 0.12), Inches(width - 0.34), Inches(height - 0.22)
    )
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)

    p_title = tf.paragraphs[0]
    p_title.space_after = Pt(7)
    rt = p_title.add_run()
    rt.text = title
    rt.font.name = "Segoe UI"
    rt.font.size = Pt(title_size)
    rt.font.bold = True
    rt.font.color.rgb = accent_color

    for item in items:
        p = tf.add_paragraph()
        p.space_after = Pt(space_after)
        if isinstance(item, tuple):
            lead, rest = item
            r_bullet = p.add_run()
            r_bullet.text = "▸ "
            r_bullet.font.name = "Segoe UI"
            r_bullet.font.size = Pt(body_size)
            r_bullet.font.bold = True
            r_bullet.font.color.rgb = accent_color

            r_lead = p.add_run()
            r_lead.text = lead + " "
            r_lead.font.name = "Segoe UI"
            r_lead.font.size = Pt(body_size)
            r_lead.font.bold = True
            r_lead.font.color.rgb = TEXT_WHITE

            r_rest = p.add_run()
            r_rest.text = rest
            r_rest.font.name = "Segoe UI"
            r_rest.font.size = Pt(body_size)
            r_rest.font.color.rgb = TEXT_SILVER
        else:
            r_bullet = p.add_run()
            r_bullet.text = "▸ "
            r_bullet.font.name = "Segoe UI"
            r_bullet.font.size = Pt(body_size)
            r_bullet.font.bold = True
            r_bullet.font.color.rgb = accent_color

            r = p.add_run()
            r.text = str(item)
            r.font.name = "Segoe UI"
            r.font.size = Pt(body_size)
            r.font.color.rgb = TEXT_SILVER


def add_picture_fit(slide, img_path, box_left, box_top, box_w, box_h, add_frame=False, frame_border=BORDER_SUBTLE):
    """
    Inserta una imagen centrada exactamente dentro del rectángulo (box_left, box_top, box_w, box_h)
    preservando su relación de aspecto real para evitar distorsión o solapamiento de texto.
    """
    if not os.path.exists(img_path):
        return
    with Image.open(img_path) as im:
        w_px, h_px = im.size
    aspect = float(w_px) / float(h_px)
    box_aspect = float(box_w) / float(box_h)

    if aspect > box_aspect:
        final_w = box_w
        final_h = box_w / aspect
    else:
        final_h = box_h
        final_w = box_h * aspect

    final_left = box_left + (box_w - final_w) / 2.0
    final_top = box_top + (box_h - final_h) / 2.0

    if add_frame:
        pad = 0.06
        frame = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(final_left - pad),
            Inches(final_top - pad),
            Inches(final_w + pad * 2),
            Inches(final_h + pad * 2)
        )
        frame.fill.solid()
        frame.fill.fore_color.rgb = BG_OBSIDIAN
        frame.line.color.rgb = frame_border
        frame.line.width = Pt(1.2)
        frame.adjustments[0] = 0.03

    slide.shapes.add_picture(
        img_path,
        Inches(final_left),
        Inches(final_top),
        width=Inches(final_w),
        height=Inches(final_h)
    )


def add_image_caption(slide, left, top, width, text, color=TEXT_MUTED):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(0.32))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.name = "Segoe UI"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = color


def build_presentation(out_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    base_dir = os.path.dirname(os.path.abspath(out_path))
    diag_dir = os.path.join(base_dir, "diagramas")
    cap_dir = os.path.join(base_dir, "capturas")
    icon_path = os.path.abspath(os.path.join(base_dir, "..", "app", "src", "main", "res", "drawable", "encuesta.png"))

    # =========================================================================
    # SLIDE 1: PORTADA INSTITUCIONAL UNAMAD
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    set_slide_bg(s1, BG_OBSIDIAN)

    # Franja vertical izquierda doble (Azul UNAMAD + Azul Eléctrico + Verde Esmeralda)
    b1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.22), Inches(7.5))
    b1.fill.solid()
    b1.fill.fore_color.rgb = UNAMAD_BLUE
    b1.line.fill.background()

    b2 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.22), Inches(0), Inches(0.07), Inches(7.5))
    b2.fill.solid()
    b2.fill.fore_color.rgb = ACCENT_BLUE
    b2.line.fill.background()

    # Panel decorativo derecho para albergar capturas reales
    showcase_panel = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.35), Inches(0.55), Inches(4.50), Inches(6.40)
    )
    showcase_panel.fill.solid()
    showcase_panel.fill.fore_color.rgb = SURFACE_CARD
    showcase_panel.line.color.rgb = UNAMAD_BLUE
    showcase_panel.line.width = Pt(1.5)
    showcase_panel.adjustments[0] = 0.03

    # Encabezado Universidad + Icono
    if os.path.exists(icon_path):
        s1.shapes.add_picture(icon_path, Inches(0.68), Inches(0.55), height=Inches(0.88))

    tb_uni = s1.shapes.add_textbox(Inches(1.72), Inches(0.52), Inches(6.40), Inches(0.98))
    tf_uni = tb_uni.text_frame
    tf_uni.word_wrap = True
    pu1 = tf_uni.paragraphs[0]
    pu1.space_after = Pt(2)
    ru1 = pu1.add_run()
    ru1.text = "UNIVERSIDAD NACIONAL AMAZÓNICA DE MADRE DE DIOS"
    ru1.font.name = "Segoe UI"
    ru1.font.size = Pt(14.5)
    ru1.font.bold = True
    ru1.font.color.rgb = TEXT_WHITE

    pu2 = tf_uni.add_paragraph()
    ru2 = pu2.add_run()
    ru2.text = "Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas e Informática"
    ru2.font.name = "Segoe UI"
    ru2.font.size = Pt(11)
    ru2.font.color.rgb = ACCENT_BLUE

    # Píldora de curso y stack
    pill_course = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.68), Inches(1.65), Inches(7.35), Inches(0.40)
    )
    pill_course.fill.solid()
    pill_course.fill.fore_color.rgb = SURFACE_ELEVATED
    pill_course.line.color.rgb = ACCENT_BLUE
    pill_course.line.width = Pt(1)
    pill_course.adjustments[0] = 0.45
    pc_tf = pill_course.text_frame
    pc_p = pc_tf.paragraphs[0]
    pc_p.alignment = PP_ALIGN.CENTER
    pc_r = pc_p.add_run()
    pc_r.text = "PROYECTO FINAL · DESARROLLO DE APLICACIONES MÓVILES II (2026-II) · KOTLIN & FIREBASE CLOUD"
    pc_r.font.name = "Segoe UI"
    pc_r.font.size = Pt(9.5)
    pc_r.font.bold = True
    pc_r.font.color.rgb = EMERALD

    # Título Principal del Proyecto
    tb_title = s1.shapes.add_textbox(Inches(0.68), Inches(2.20), Inches(7.40), Inches(2.35))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True

    pt1 = tf_title.paragraphs[0]
    pt1.space_after = Pt(8)
    rt1 = pt1.add_run()
    rt1.text = "VotaApp UNAMAD: Sistema Cloud de Encuestas y Votación Estudiantil en Tiempo Real"
    rt1.font.name = "Segoe UI"
    rt1.font.size = Pt(28)
    rt1.font.bold = True
    rt1.font.color.rgb = TEXT_WHITE

    pt2 = tf_title.add_paragraph()
    rt2 = pt2.add_run()
    rt2.text = (
        "Plataforma móvil nativa en Kotlin con Material Design 3, Modo Oscuro Obsidian, "
        "autenticación federada Google OAuth 2.0, padrón para las 12 carreras UNAMAD, "
        "gráficos Donut animados y despliegue continuo CI/CD con GitHub Actions."
    )
    rt2.font.name = "Segoe UI"
    rt2.font.size = Pt(12.5)
    rt2.font.color.rgb = TEXT_SILVER

    # Tarjeta de Créditos Académicos (Docente e Integrantes)
    cred_box = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.68), Inches(4.72), Inches(7.40), Inches(2.23)
    )
    cred_box.fill.solid()
    cred_box.fill.fore_color.rgb = SURFACE_CARD
    cred_box.line.color.rgb = ACCENT_BLUE
    cred_box.line.width = Pt(1.2)
    cred_box.adjustments[0] = 0.04

    cred_bar = s1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.68), Inches(4.92), Inches(0.09), Inches(1.80)
    )
    cred_bar.fill.solid()
    cred_bar.fill.fore_color.rgb = EMERALD
    cred_bar.line.fill.background()

    tbc = s1.shapes.add_textbox(Inches(0.92), Inches(4.84), Inches(7.00), Inches(2.00))
    tfc = tbc.text_frame
    tfc.word_wrap = True

    credits_data = [
        ("DOCENTE:", "Ing. Laura Salvatierra, Leonel Christofher", ACCENT_BLUE),
        ("INTEGRANTES:", "Amezquita Camargo, Maicol Alberto\nTorres Saire, Bickmer Fabricio", EMERALD),
        ("CLOUD & CI/CD:", "Firebase ID: votaapp-unamad-2026  |  Puerto Maldonado, Madre de Dios · 2026", TEXT_MUTED),
    ]
    for idx, (lbl, val, col) in enumerate(credits_data):
        p = tfc.paragraphs[0] if idx == 0 else tfc.add_paragraph()
        p.space_after = Pt(6)
        rl = p.add_run()
        rl.text = f"{lbl} "
        rl.font.name = "Segoe UI"
        rl.font.size = Pt(11.5)
        rl.font.bold = True
        rl.font.color.rgb = col

        rv = p.add_run()
        rv.text = val
        rv.font.name = "Segoe UI"
        rv.font.size = Pt(12)
        rv.font.bold = (idx < 2)
        rv.font.color.rgb = TEXT_WHITE if idx < 2 else TEXT_SILVER

    # Capturas reales en el panel derecho de la portada
    add_image_caption(s1, 8.45, 0.72, 4.30, "INTERFAZ REAL ANDROID · MODO OSCURO OBSIDIAN", EMERALD)
    add_picture_fit(
        s1, os.path.join(cap_dir, "cap0_login.png"),
        8.52, 1.12, 2.02, 5.20, add_frame=True, frame_border=ACCENT_BLUE
    )
    add_picture_fit(
        s1, os.path.join(cap_dir, "cap1_main.png"),
        10.68, 1.12, 2.02, 5.20, add_frame=True, frame_border=EMERALD
    )
    add_image_caption(s1, 8.50, 6.45, 2.05, "Login + Google OAuth", TEXT_SILVER)
    add_image_caption(s1, 10.66, 6.45, 2.05, "Dashboard Cloud Real-Time", TEXT_SILVER)

    # =========================================================================
    # SLIDE 2: PROBLEMÁTICA Y JUSTIFICACIÓN
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    set_slide_bg(s2)
    add_header(
        s2,
        "1. Contexto Institucional",
        "Problemática y Justificación del Sistema Cloud",
        "Limitaciones de encuestas manuales/locales frente al sufragio estudiantil verificado en la nube",
        2
    )

    add_card(
        s2, 0.55, 1.32, 3.92, 5.58,
        "Problemática: Encuestas Manuales y Locales",
        [
            ("Escrutinio en papel ineficiente:", "El conteo físico de boletas en aulas y asambleas genera demoras, errores de tabulación y costos operativos."),
            ("Limitación de bases locales aisladas:", "Un esquema puramente local (SQLite en 1 solo dispositivo) obliga a rotar un teléfono físico y no escala a votaciones remotas."),
            ("Riesgo de suplantación en formularios web:", "Los enlaces abiertos carecen de validación estricta del padrón por código universitario y Escuela Profesional."),
            ("Falta de auditoría inmediata:", "Demora en la emisión de actas oficiales y ausencia de trazabilidad criptográfica de cada voto emitido.")
        ],
        accent_color=CORAL_RED,
        body_size=11.0,
        space_after=6
    )

    add_card(
        s2, 4.68, 1.32, 3.92, 5.58,
        "Justificación: Sufragio Cloud Verificado",
        [
            ("Sincronización multi-dispositivo real-time:", "Cada estudiante sufraga desde su propio smartphone Android conectado a Cloud Firestore (votaapp-unamad-2026)."),
            ("Identidad institucional autenticada:", "Integración de Firebase Authentication + Google Sign-In OAuth 2.0 vinculando cada cuenta a un UID único."),
            ("Control de padrón por carrera y código:", "Segmentación nativa para las 12 carreras de la UNAMAD y listas cerradas importadas desde .TXT, .CSV o Excel."),
            ("Transparencia y escrutinio instantáneo:", "Garantía matemática de 1 voto por cuenta (votos/{uid}), gráfico Donut animado y exportación de Acta Oficial.")
        ],
        accent_color=EMERALD,
        body_size=11.0,
        space_after=6
    )

    add_card_base(s2, 8.81, 1.32, 3.97, 5.58, accent_color=ACCENT_BLUE)
    add_card(
        s2, 8.81, 1.32, 3.97, 1.75,
        "Actores y Casos de Uso (UML)",
        [
            ("Estudiante Votante:", "Autentica, filtra y emite voto único."),
            ("Organizador / Creador:", "Crea encuestas, carga padrón y audita.")
        ],
        accent_color=ACCENT_BLUE,
        title_size=13.5,
        body_size=10.5,
        space_after=3
    )
    add_picture_fit(
        s2, os.path.join(diag_dir, "fig1_casos_uso.png"),
        8.96, 3.15, 3.67, 3.35, add_frame=True, frame_border=UNAMAD_BLUE
    )
    add_image_caption(s2, 8.90, 6.55, 3.78, "Fig. 1: Diagrama UML de Casos de Uso del Sistema", TEXT_MUTED)

    # =========================================================================
    # SLIDE 3: OBJETIVOS Y ALCANCE DEL SISTEMA
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    set_slide_bg(s3)
    add_header(
        s3,
        "2. Objetivos & Alcance",
        "Objetivos Académicos y Alcance Funcional del Proyecto",
        "Definición de metas de ingeniería de software móvil y flujo integral de navegación en 6 pantallas",
        3
    )

    add_card(
        s3, 0.55, 1.32, 12.23, 1.28,
        "Objetivo General",
        [
            (
                "Desarrollar e implementar VotaApp UNAMAD:",
                "Una aplicación móvil nativa en Kotlin para Android con arquitectura en la nube (Firebase Auth + Cloud Firestore) que permita gestionar encuestas y votaciones estudiantiles en tiempo real, garantizando identidad verificada por Escuela Profesional, unicidad matemática del sufragio y escrutinio gráfico automatizado."
            )
        ],
        accent_color=ACCENT_BLUE,
        title_size=14.0,
        body_size=11.5,
        space_after=2
    )

    add_card(
        s3, 0.55, 2.76, 5.95, 4.14,
        "Objetivos Específicos (OE1 – OE4)",
        [
            ("OE1 · Autenticación y Seguridad Cloud:", "Implementar login con Correo/Contraseña, Google OAuth 2.0 y reglas firestore.rules con aislamiento por UID."),
            ("OE2 · Padrón Electoral y 12 Carreras UNAMAD:", "Validar acceso por Escuela Profesional y cargar padrones masivos de códigos mediante archivos .TXT, .CSV o Excel."),
            ("OE3 · Experiencia Material 3 & Modo Obsidian:", "Diseñar 6 Activities adaptativas con tema oscuro Obsidian (#090E1A), cifras tabulares (tnum) y DonutChartView nativo."),
            ("OE4 · Automatización DevOps CI/CD:", "Construir un pipeline en GitHub Actions que ejecute pruebas unitarias, compile el APK y actualice el release latest-apk.")
        ],
        accent_color=EMERALD,
        body_size=11.0,
        space_after=6
    )

    add_card_base(s3, 6.72, 2.76, 6.06, 4.14, accent_color=AMBER_GOLD)
    add_card(
        s3, 6.72, 2.76, 6.06, 1.45,
        "Alcance Funcional y Mapa de Navegación",
        [
            ("Cobertura End-to-End:", "6 pantallas nativas conectadas a FirebaseRepository (Login, Main Dashboard, Crear/Editar Encuesta, Gestionar Preguntas, Registrar Voto y Resultados + Acta).")
        ],
        accent_color=AMBER_GOLD,
        title_size=14.0,
        body_size=10.8,
        space_after=2
    )
    add_picture_fit(
        s3, os.path.join(diag_dir, "fig5_navegacion.png"),
        6.90, 4.25, 5.70, 2.30, add_frame=True, frame_border=UNAMAD_BLUE
    )
    add_image_caption(s3, 6.85, 6.58, 5.80, "Fig. 5: Flujo de Navegación entre Activities y Retorno Seguro", TEXT_MUTED)

    # =========================================================================
    # SLIDE 4: ARQUITECTURA CLOUD & STACK TECNOLÓGICO
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    set_slide_bg(s4)
    add_header(
        s4,
        "3. Arquitectura Cloud",
        "Arquitectura Cloud & Stack Tecnológico de Producción",
        "Kotlin 2.2.10 · Material Design 3 (1.12.0) · Firebase Auth + Google OAuth · Cloud Firestore · GitHub Actions",
        4
    )

    add_card(
        s4, 0.55, 1.32, 5.85, 5.58,
        "Stack Tecnológico Real del Proyecto",
        [
            ("Lenguaje & Compilador:", "Kotlin 2.2.10 (JVM Target 11) con tipado estático null-safe, corrutinas/callbacks tipados y data classes inmutables."),
            ("Android SDK & Build System:", "Gradle 9.1.0 · Android Gradle Plugin (AGP) 9.0.1 · minSdk 24 (Android 7.0) hasta compileSdk / targetSdk 36 (Android 16)."),
            ("UI & Material Design 3:", "Material Components 1.12.0, SwipeRefreshLayout 1.1.0, Edge-to-Edge (UiInsetsHelper.kt) y paleta Obsidian (#090E1A / #121B2E)."),
            ("Autenticación Federada:", "Firebase Auth (firebase-bom 34.7.0) + Google Play Services Auth (21.3.0) para OAuth 2.0 y recuperación de contraseña."),
            ("Base de Datos Real-Time:", "Cloud Firestore (proyecto votaapp-unamad-2026) con sincronización reactiva addSnapshotListener y transacciones ACID."),
            ("Integración Continua (CI/CD):", "GitHub Actions (.github/workflows/android-release.yml) con JDK 17 Temurin y despliegue automático en GitHub Releases.")
        ],
        accent_color=ACCENT_BLUE,
        body_size=10.8,
        space_after=5
    )

    add_card_base(s4, 6.60, 1.32, 6.18, 5.58, accent_color=EMERALD)
    tb_a = s4.shapes.add_textbox(Inches(6.82), Inches(1.42), Inches(5.80), Inches(0.42))
    tf_a = tb_a.text_frame
    pa = tf_a.paragraphs[0]
    ra = pa.add_run()
    ra.text = "Arquitectura Multicapa Orientada a Servicios Cloud (Firebase)"
    ra.font.name = "Segoe UI"
    ra.font.size = Pt(14)
    ra.font.bold = True
    ra.font.color.rgb = EMERALD

    add_picture_fit(
        s4, os.path.join(diag_dir, "fig2_arquitectura.png"),
        6.80, 1.90, 5.78, 4.60, add_frame=True, frame_border=UNAMAD_BLUE
    )
    add_image_caption(
        s4, 6.75, 6.56, 5.88,
        "Fig. 2: Capa de Presentación (Activities + Custom Views) ↔ FirebaseRepository ↔ Cloud Firestore",
        TEXT_MUTED
    )

    # =========================================================================
    # SLIDE 5: AUTENTICACIÓN PROFESIONAL & MODO OSCURO OBSIDIAN
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    set_slide_bg(s5)
    add_header(
        s5,
        "4. Identidad & UX Obsidian",
        "Autenticación Profesional & Modo Oscuro Obsidian",
        "LoginActivity · Google Sign-In OAuth 2.0 · Recuperación de Contraseña · Registro Integrado · Selector de Tema",
        5
    )

    add_card(
        s5, 0.55, 1.32, 4.75, 2.70,
        "Autenticación en LoginActivity.kt",
        [
            ("Acceso Dual:", "Inicio de sesión con Correo/Contraseña y botón oficial Google Sign-In (GoogleAuthProvider)."),
            ("Enlace 'Crear cuenta' integrado:", "Alternancia animada (TransitionManager) en la misma pantalla desplegando Nombre, Código Universitario y Carrera UNAMAD."),
            ("Recuperación de clave:", "Flujo sendPasswordResetEmail con diálogo de confirmación instantáneo.")
        ],
        accent_color=ACCENT_BLUE,
        title_size=13.5,
        body_size=10.5,
        space_after=4
    )

    add_card(
        s5, 0.55, 4.18, 4.75, 2.72,
        "Modo Oscuro Obsidian & Perfil Cloud",
        [
            ("Selector Oscuro / Claro en vivo:", "Botón superior conmuta AppCompatDelegate.MODE_NIGHT_YES / NO y persiste la preferencia en SharedPreferences."),
            ("Ergonomía Visual Obsidian:", "Superficies #090E1A y #121B2E con acentos #3B82F6 y #34D399 que maximizan legibilidad y ahorro energético OLED."),
            ("Autocompletado de Perfil:", "Si el usuario ingresa con Google por primera vez, MainActivity solicita completar su Carrera y Código Universitario.")
        ],
        accent_color=EMERALD,
        title_size=13.5,
        body_size=10.5,
        space_after=4
    )

    add_card_base(s5, 5.50, 1.32, 7.28, 5.58, accent_color=ACCENT_BLUE)
    tb_s5 = s5.shapes.add_textbox(Inches(5.72), Inches(1.42), Inches(6.90), Inches(0.40))
    p_s5 = tb_s5.text_frame.paragraphs[0]
    r_s5 = p_s5.add_run()
    r_s5.text = "Evidencia de Interfaz: LoginActivity y Prototipos de Alta Fidelidad"
    r_s5.font.name = "Segoe UI"
    r_s5.font.size = Pt(14)
    r_s5.font.bold = True
    r_s5.font.color.rgb = ACCENT_BLUE

    add_picture_fit(
        s5, os.path.join(cap_dir, "cap0_login.png"),
        5.72, 1.92, 2.15, 4.60, add_frame=True, frame_border=ACCENT_BLUE
    )
    add_image_caption(s5, 5.65, 6.58, 2.30, "Captura Real: LoginActivity", TEXT_SILVER)

    add_picture_fit(
        s5, os.path.join(diag_dir, "fig3_prototipos_ui.png"),
        8.12, 1.92, 4.42, 2.75, add_frame=True, frame_border=UNAMAD_BLUE
    )
    add_card(
        s5, 8.06, 4.85, 4.52, 1.85,
        "Sincronización en /users/{uid}",
        [
            ("Documento de Perfil:", "Almacena uid, nombre, codigoUniversitario, carrera, email y fechaRegistro."),
            ("Privacidad PII:", "Regla allow read, write: if isOwner(uid) protege los datos personales.")
        ],
        accent_color=AMBER_GOLD,
        title_size=12.5,
        body_size=10.0,
        space_after=3,
        bg_color=SURFACE_ELEVATED
    )

    # =========================================================================
    # SLIDE 6: CATÁLOGO DE 12 CARRERAS UNAMAD & IMPORTACIÓN MASIVA DE CÓDIGOS
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    set_slide_bg(s6)
    add_header(
        s6,
        "5. Padrón & 12 Carreras",
        "Catálogo de 12 Carreras UNAMAD & Importación Masiva",
        "CatalogoUnamad · Filtro por Escuela Profesional · Carga de Códigos (.TXT / .CSV / Excel) · Código Único por UID",
        6
    )

    add_card(
        s6, 0.55, 1.32, 4.55, 5.58,
        "Catálogo Oficial: 12 Carreras UNAMAD",
        [
            ("1. Ing. de Sistemas e Informática", "(EPISI)"),
            ("2. Ing. Forestal y Medio Ambiente", ""),
            ("3. Ingeniería Agroindustrial", ""),
            ("4. Medicina Veterinaria y Zootecnia", ""),
            ("5. Enfermería", "· 6. Derecho y Ciencias Políticas"),
            ("7. Educación: Matemática y Computación", ""),
            ("8. Educación: Primaria e Informática", ""),
            ("9. Educación: Inicial y Especial", ""),
            ("10. Ecoturismo", ""),
            ("11. Administración y Negocios Int.", ""),
            ("12. Contabilidad y Finanzas", ""),
            ("Modalidad de Encuesta:", "Abierta a toda la UNAMAD o restringida a una Escuela Profesional específica.")
        ],
        accent_color=ACCENT_BLUE,
        title_size=13.5,
        body_size=10.2,
        space_after=2.5
    )

    add_card(
        s6, 5.28, 1.32, 4.55, 5.58,
        "Importación Masiva (.TXT / .CSV / Excel)",
        [
            ("Carga de Archivos (.TXT / .CSV):", "CrearEncuestaActivity integra ActivityResultContracts.GetContent() para importar listas completas de matrícula."),
            ("Pegado Directo desde Excel:", "Botón 'Pegar' lee el portapapeles y extrae códigos automáticamente aunque incluyan columnas de nombres o tabulaciones."),
            ("Motor Regex en CatalogoUnamad:", "extraerCodigosDesdeTexto() aplica Regex('\\b\\d{4,14}[A-Za-z0-9-]*\\b'), normaliza a mayúsculas y elimina duplicados."),
            ("Código Estudiantil Único por UID:", "FirebaseRepository verifica antes de guardar que ningún otro usuario haya registrado el mismo codigoUniversitario."),
            ("Verificación Pre-Sufragio:", "encuesta.verificarAcceso() comprueba carrera y padrón antes de habilitar el formulario de votación.")
        ],
        accent_color=EMERALD,
        title_size=13.5,
        body_size=10.5,
        space_after=5
    )

    add_card_base(s6, 10.01, 1.32, 2.77, 5.58, accent_color=AMBER_GOLD)
    add_image_caption(s6, 10.06, 1.42, 2.67, "CrearEncuestaActivity", AMBER_GOLD)
    add_picture_fit(
        s6, os.path.join(cap_dir, "cap2_crear_encuesta.png"),
        10.22, 1.80, 2.35, 4.70, add_frame=True, frame_border=AMBER_GOLD
    )
    add_image_caption(s6, 10.06, 6.56, 2.67, "Filtro Carrera + Padrón CSV/TXT", TEXT_SILVER)

    # =========================================================================
    # SLIDE 7: PANEL PRINCIPAL CLOUD, BUSCADOR EN TIEMPO REAL Y FILTROS
    # =========================================================================
    s7 = prs.slides.add_slide(blank)
    set_slide_bg(s7)
    add_header(
        s7,
        "6. Dashboard Real-Time",
        "Panel Principal Cloud, Buscador en Tiempo Real y Filtros",
        "MainActivity · KPIs con Cifras Tabulares (tnum) · SwipeRefreshLayout · ChipGroup · Gestión de Preguntas",
        7
    )

    add_card(
        s7, 0.55, 1.32, 6.10, 5.58,
        "Arquitectura Reactiva del Panel Principal (MainActivity)",
        [
            ("Sincronización Cloud en Vivo:", "escucharEncuestasEnTiempoReal() suscribe un addSnapshotListener a la colección /encuestas para reflejar cambios al instante."),
            ("Tarjetas KPI con Cifras Tabulares (tnum):", "Contadores superiores (Total, Activas, Votos) utilizan fontFeatureSettings='tnum' para mantener ancho fijo por dígito sin vibración visual."),
            ("Buscador en Tiempo Real (TextWatcher):", "Filtra instantáneamente por título, descripción, categoría o carrera restringida mientras el estudiante escribe."),
            ("Filtros por Estado (ChipGroup) y SwipeRefresh:", "Chips interactivos (Todas / Activas / Cerradas) combinados con SwipeRefreshLayout para recarga manual fluida."),
            ("Insignias de Padrón y Control de Autor:", "Cada tarjeta muestra estado, carrera destino, cantidad de códigos habilitados y botones exclusivos para el creador (Editar, Preguntas, Cerrar, Eliminar).")
        ],
        accent_color=ACCENT_BLUE,
        title_size=14.0,
        body_size=10.8,
        space_after=5
    )

    add_card_base(s7, 6.85, 1.32, 5.93, 5.58, accent_color=EMERALD)
    tb_s7 = s7.shapes.add_textbox(Inches(7.05), Inches(1.42), Inches(5.55), Inches(0.40))
    p_s7 = tb_s7.text_frame.paragraphs[0]
    r_s7 = p_s7.add_run()
    r_s7.text = "Capturas Reales: Dashboard Cloud y Configuración de Preguntas"
    r_s7.font.name = "Segoe UI"
    r_s7.font.size = Pt(13.5)
    r_s7.font.bold = True
    r_s7.font.color.rgb = EMERALD

    add_picture_fit(
        s7, os.path.join(cap_dir, "cap1_main.png"),
        7.18, 1.90, 2.20, 4.60, add_frame=True, frame_border=ACCENT_BLUE
    )
    add_picture_fit(
        s7, os.path.join(cap_dir, "cap3_gestionar_preguntas.png"),
        10.12, 1.90, 2.20, 4.60, add_frame=True, frame_border=EMERALD
    )
    add_image_caption(s7, 7.05, 6.56, 2.46, "MainActivity (KPIs + Filtros)", TEXT_SILVER)
    add_image_caption(s7, 9.98, 6.56, 2.48, "GestionarPreguntasActivity", TEXT_SILVER)

    # =========================================================================
    # SLIDE 8: CÉDULA DE VOTACIÓN INTERACTIVA Y REGLAS DE SEGURIDAD
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    set_slide_bg(s8)
    add_header(
        s8,
        "7. Sufragio & Seguridad",
        "Cédula de Votación Interactiva y Reglas de Seguridad",
        "RegistrarVotoActivity · firestore.rules · Garantía Matemática de 1 Voto por Cuenta (encuestas/{id}/votos/{uid})",
        8
    )

    add_card(
        s8, 0.55, 1.32, 4.55, 5.58,
        "Cédula Interactiva (RegistrarVotoActivity)",
        [
            ("Identidad Bloqueada por Sesión:", "El votante se identifica automáticamente con su perfil autenticado (Nombre + Código Universitario verificado)."),
            ("Renderizado Dinámico:", "Construye RadioGroups para preguntas de Selección Única y CheckBoxes para Selección Múltiple."),
            ("Persistencia ante Rotación:", "onSaveInstanceState preserva las opciones marcadas al girar el dispositivo."),
            ("Transacción Atómica (runTransaction):", "Verifica en una sola operación ACID que el documento votos/{uid} no exista, que la encuesta siga activa e incrementa los contadores."),
            ("Confirmación Modal:", "Diálogo MaterialAlertDialogBuilder previene envíos accidentales.")
        ],
        accent_color=ACCENT_BLUE,
        title_size=13.5,
        body_size=10.5,
        space_after=4.5
    )

    add_card_base(s8, 5.28, 1.32, 4.55, 5.58, accent_color=EMERALD)
    add_card(
        s8, 5.28, 1.32, 4.55, 2.85,
        "Seguridad Server-Side (firestore.rules)",
        [
            ("Garantía 1 Voto = 1 UID:", "Ruta encuestas/{encuestaId}/votos/{voterUid} exige isOwner(voterUid) y data.uid == request.auth.uid."),
            ("Voto Inmutable:", "allow update: if false impide alterar un voto emitido; solo se permite create si isEncuestaActiva()."),
            ("Protección de Esquema:", "Valida longitudes, categorías permitidas e inmutabilidad de creadorUid.")
        ],
        accent_color=EMERALD,
        title_size=13.5,
        body_size=10.2,
        space_after=3
    )
    add_picture_fit(
        s8, os.path.join(diag_dir, "fig6_base_datos_er.png"),
        5.50, 4.24, 4.10, 2.32, add_frame=True, frame_border=UNAMAD_BLUE
    )
    add_image_caption(s8, 5.38, 6.60, 4.35, "Fig. 6: Estructura de Datos y Subcolección votos/{uid}", TEXT_MUTED)

    add_card_base(s8, 10.01, 1.32, 2.77, 5.58, accent_color=ACCENT_BLUE)
    add_image_caption(s8, 10.06, 1.42, 2.67, "RegistrarVotoActivity", ACCENT_BLUE)
    add_picture_fit(
        s8, os.path.join(cap_dir, "cap4_registrar_voto.png"),
        10.22, 1.80, 2.35, 4.70, add_frame=True, frame_border=ACCENT_BLUE
    )
    add_image_caption(s8, 10.06, 6.56, 2.67, "Cédula de Sufragio Verificada", TEXT_SILVER)

    # =========================================================================
    # SLIDE 9: ESCRUTINIO EN TIEMPO REAL, GRÁFICO DONUT ANIMADO Y ACTA OFICIAL
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    set_slide_bg(s9)
    add_header(
        s9,
        "8. Escrutinio & Analítica",
        "Escrutinio en Tiempo Real, Gráfico Donut y Acta Oficial",
        "ResultadosActivity · DonutChartView.kt en Canvas 2D · Barras Porcentuales · Exportación de Acta de Escrutinio",
        9
    )

    add_card(
        s9, 0.55, 1.32, 6.10, 5.58,
        "Visualización Estadística y Auditoría (ResultadosActivity)",
        [
            ("DonutChartView.kt (Custom View en Canvas):", "Componente gráfico vectorial propio con animación ValueAnimator (650 ms, DecelerateInterpolator), total de votos centrado y leyenda lateral automática."),
            ("Destacado Automático de Opción Ganadora:", "Algoritmo identifica el máximo de votos (> 0), asigna insignia ámbar ('Ganadora • #D97706') y anima ProgressBar con precisión decimal (%.1f%%)."),
            ("Padrón Auditable de Participantes:", "Lista en tiempo real de los estudiantes que emitieron sufragio (nombre verificado + timestamp de votación) desde la subcolección /votos."),
            ("Exportación de Acta Oficial de Escrutinio:", "Botón 'Compartir Acta' genera un resumen formal foliado y lo envía mediante Intent.ACTION_SEND (WhatsApp, Correo Institucional, Drive)."),
            ("Reinicio Seguro de Conteo:", "El organizador puede reiniciar los votos a cero mediante lote transaccional previa confirmación modal.")
        ],
        accent_color=AMBER_GOLD,
        title_size=14.0,
        body_size=10.7,
        space_after=5
    )

    add_card_base(s9, 6.85, 1.32, 5.93, 5.58, accent_color=ACCENT_BLUE)
    tb_s9 = s9.shapes.add_textbox(Inches(7.05), Inches(1.42), Inches(5.55), Inches(0.40))
    p_s9 = tb_s9.text_frame.paragraphs[0]
    r_s9 = p_s9.add_run()
    r_s9.text = "Capturas Reales: Barras Estadísticas y Gráfico Donut Animado"
    r_s9.font.name = "Segoe UI"
    r_s9.font.size = Pt(13.5)
    r_s9.font.bold = True
    r_s9.font.color.rgb = ACCENT_BLUE

    add_picture_fit(
        s9, os.path.join(cap_dir, "cap5_resultados.png"),
        7.18, 1.90, 2.20, 4.60, add_frame=True, frame_border=AMBER_GOLD
    )
    add_picture_fit(
        s9, os.path.join(cap_dir, "cap_resultados_donut.png"),
        10.12, 1.90, 2.20, 4.60, add_frame=True, frame_border=EMERALD
    )
    add_image_caption(s9, 7.05, 6.56, 2.46, "Escrutinio + Padrón Votantes", TEXT_SILVER)
    add_image_caption(s9, 9.98, 6.56, 2.48, "DonutChartView + Acta Oficial", TEXT_SILVER)

    # =========================================================================
    # SLIDE 10: DESPLIEGUE CONTINUO (CI/CD) CON GITHUB ACTIONS Y RELEASE APK
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    set_slide_bg(s10)
    add_header(
        s10,
        "9. DevOps & CI/CD",
        "Despliegue Continuo (CI/CD) con GitHub Actions y Release APK",
        "Compilación automatizada en la nube, ejecución de pruebas unitarias y publicación continua en GitHub Releases",
        10
    )

    add_card(
        s10, 0.55, 1.32, 6.25, 4.25,
        "Pipeline .github/workflows/android-release.yml",
        [
            ("Activación Automática:", "Se dispara en cada push o pull_request hacia la rama main y vía workflow_dispatch en runners ubuntu-latest."),
            ("Aprovisionamiento JDK 17 & Caché Gradle:", "Configura Eclipse Temurin JDK 17 (actions/setup-java@v4) y caché de dependencias con gradle/actions/setup-gradle@v4."),
            ("Verificación y Compilación Limpia:", "Ejecuta ./gradlew testDebugUnitTest seguido de ./gradlew assembleDebug generando el binario firmado VotaApp-UNAMAD.apk."),
            ("Artefacto y Release Automático (gh release):", "Publica el artefacto con retención de 30 días y actualiza automáticamente el release tag 'latest-apk' con --clobber.")
        ],
        accent_color=EMERALD,
        title_size=14.0,
        body_size=10.8,
        space_after=5
    )

    # Tarjeta destacada con URL oficial de Release
    url_card = s10.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(5.72), Inches(6.25), Inches(1.18)
    )
    url_card.fill.solid()
    url_card.fill.fore_color.rgb = SURFACE_ELEVATED
    url_card.line.color.rgb = ACCENT_BLUE
    url_card.line.width = Pt(1.4)
    url_card.adjustments[0] = 0.06

    tb_url = s10.shapes.add_textbox(Inches(0.75), Inches(5.80), Inches(5.90), Inches(1.00))
    tf_url = tb_url.text_frame
    tf_url.word_wrap = True
    pu_1 = tf_url.paragraphs[0]
    pu_1.space_after = Pt(3)
    ru_1 = pu_1.add_run()
    ru_1.text = "ENLACE OFICIAL DE DESCARGA DIRECTA DEL APK (GITHUB RELEASES):"
    ru_1.font.name = "Segoe UI"
    ru_1.font.size = Pt(10.5)
    ru_1.font.bold = True
    ru_1.font.color.rgb = EMERALD

    pu_2 = tf_url.add_paragraph()
    ru_2 = pu_2.add_run()
    ru_2.text = "https://github.com/Maickel69/VotaApp-UNAMAD/releases/tag/latest-apk"
    ru_2.font.name = "Consolas"
    ru_2.font.size = Pt(11.5)
    ru_2.font.bold = True
    ru_2.font.color.rgb = TEXT_WHITE

    add_card_base(s10, 7.00, 1.32, 5.78, 5.58, accent_color=ACCENT_BLUE)
    tb_s10 = s10.shapes.add_textbox(Inches(7.22), Inches(1.42), Inches(5.40), Inches(0.40))
    p_s10 = tb_s10.text_frame.paragraphs[0]
    r_s10 = p_s10.add_run()
    r_s10.text = "Estructura Modular del Proyecto Android & Pipeline CI/CD"
    r_s10.font.name = "Segoe UI"
    r_s10.font.size = Pt(13.5)
    r_s10.font.bold = True
    r_s10.font.color.rgb = ACCENT_BLUE

    add_picture_fit(
        s10, os.path.join(diag_dir, "fig7_estructura_proyecto.png"),
        7.20, 1.90, 5.38, 4.55, add_frame=True, frame_border=UNAMAD_BLUE
    )
    add_image_caption(
        s10, 7.10, 6.56, 5.58,
        "Fig. 7: Árbol de Paquetes Kotlin, Recursos XML, Reglas Firestore y Workflow CI/CD",
        TEXT_MUTED
    )

    # =========================================================================
    # SLIDE 11: CONCLUSIONES
    # =========================================================================
    s11 = prs.slides.add_slide(blank)
    set_slide_bg(s11)
    add_header(
        s11,
        "10. Conclusiones",
        "Conclusiones e Impacto Institucional en la UNAMAD",
        "Síntesis de los logros arquitectónicos, seguridad electoral, usabilidad Obsidian y despliegue continuo",
        11
    )

    add_card(
        s11, 0.55, 1.32, 5.95, 2.68,
        "1. Arquitectura Cloud Reactiva Multi-Dispositivo",
        [
            ("Sincronización en Tiempo Real:", "La integración de Cloud Firestore (votaapp-unamad-2026) permitió superar el aislamiento de bases locales, logrando que cada estudiante vote desde su propio dispositivo con actualización instantánea."),
            ("Escalabilidad Universitaria:", "El patrón repositorio en FirebaseRepository desacopla la lógica de datos y soporta concurrencia en procesos electorales de toda la UNAMAD.")
        ],
        accent_color=ACCENT_BLUE,
        title_size=14.0,
        body_size=11.0,
        space_after=5
    )

    add_card(
        s11, 6.83, 1.32, 5.95, 2.68,
        "2. Identidad Verificada y Padrón para las 12 Carreras",
        [
            ("Autenticación Robusta:", "Firebase Auth + Google Sign-In OAuth 2.0 garantizan que cada sesión corresponda a un estudiante real con perfil validado en /users/{uid}."),
            ("Cero Suplantación de Matrícula:", "El catálogo de las 12 Escuelas Profesionales (CatalogoUnamad), la unicidad de código por UID y la carga masiva (.TXT/.CSV/Excel) aseguran padrones auditables.")
        ],
        accent_color=EMERALD,
        title_size=14.0,
        body_size=11.0,
        space_after=5
    )

    add_card(
        s11, 0.55, 4.22, 5.95, 2.68,
        "3. Garantía Matemática de Voto Único y Escrutinio Gráfico",
        [
            ("Integridad Transaccional y Reglas:", "La estructura encuestas/{id}/votos/{uid} combinada con runTransaction y firestore.rules hace imposible emitir votos duplicados o alterar sufragios."),
            ("Transparencia Electoral:", "El componente nativo DonutChartView.kt, las barras porcentuales y la exportación de Actas Oficiales entregan resultados verificables al instante.")
        ],
        accent_color=AMBER_GOLD,
        title_size=14.0,
        body_size=11.0,
        space_after=5
    )

    add_card(
        s11, 6.83, 4.22, 5.95, 2.68,
        "4. Calidad Industrial: UX Obsidian & DevOps CI/CD",
        [
            ("Diseño Material 3 & Modo Obsidian:", "La paleta #090E1A / #121B2E, cifras tabulares (tnum) y soporte Edge-to-Edge ofrecen una experiencia visual moderna y accesible."),
            ("Entrega Continua Verificada:", "El pipeline de GitHub Actions automatiza las pruebas, compilación y publicación del APK en GitHub Releases (latest-apk), asegurando calidad de software.")
        ],
        accent_color=ACCENT_BLUE,
        title_size=14.0,
        body_size=11.0,
        space_after=5
    )

    prs.save(out_path)
    print(f"Presentación de {len(prs.slides)} diapositivas generada exitosamente en: {out_path}")


if __name__ == "__main__":
    output_pptx = r"c:\Users\HP\AndroidStudioProjects\ProyectoFinal\Documentacion\Presentacion_VotaApp_UNAMAD.pptx"
    build_presentation(output_pptx)
