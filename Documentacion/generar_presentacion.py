import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Paleta Institucional UNAMAD
NAVY_DARK = RGBColor(15, 36, 96)     # #0F2460
NAVY = RGBColor(30, 58, 138)         # #1E3A8A
ACCENT = RGBColor(37, 99, 235)       # #2563EB
BG_SLATE = RGBColor(241, 245, 249)   # #F1F5F9
WHITE = RGBColor(255, 255, 255)
TEXT_DARK = RGBColor(15, 23, 42)     # #0F172A
TEXT_MUTED = RGBColor(71, 85, 105)   # #475569
BORDER = RGBColor(203, 213, 225)     # #CBD5E1
SUCCESS = RGBColor(4, 120, 87)       # #047857
WARNING = RGBColor(180, 83, 9)       # #B45309


def add_header(slide, title_text, subtitle_text, page_num):
    # Top navy bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY_DARK
    bar.line.fill.background()

    # Accent stripe
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = ACCENT
    stripe.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.18), Inches(11.0), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    r1 = p1.add_run()
    r1.text = title_text
    r1.font.name = "Arial"
    r1.font.size = Pt(24)
    r1.font.bold = True
    r1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = subtitle_text
    r2.font.name = "Arial"
    r2.font.size = Pt(12)
    r2.font.color.rgb = RGBColor(203, 213, 225)

    # Footer
    ft = slide.shapes.add_textbox(Inches(0.6), Inches(7.1), Inches(12.1), Inches(0.3))
    ftf = ft.text_frame
    fp = ftf.paragraphs[0]
    fp.alignment = PP_ALIGN.RIGHT
    fr = fp.add_run()
    fr.text = f"VotaApp UNAMAD · Desarrollo de Aplicaciones Móviles II (2026-II)   |   Diapositiva {page_num}"
    fr.font.name = "Arial"
    fr.font.size = Pt(10)
    fr.font.color.rgb = TEXT_MUTED


def add_card(slide, left, top, width, height, title, bullets, accent_color=ACCENT):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = BORDER
    card.line.width = Pt(1)
    card.adjustments[0] = 0.04

    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top + 0.15), Inches(0.08), Inches(0.42))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent_color
    bar.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(left + 0.22), Inches(top + 0.14), Inches(width - 0.38), Inches(height - 0.25))
    tf = tb.text_frame
    tf.word_wrap = True

    p_title = tf.paragraphs[0]
    p_title.space_after = Pt(8)
    rt = p_title.add_run()
    rt.text = title
    rt.font.name = "Arial"
    rt.font.size = Pt(15)
    rt.font.bold = True
    rt.font.color.rgb = NAVY

    for b in bullets:
        p = tf.add_paragraph()
        p.space_after = Pt(5)
        r = p.add_run()
        r.text = f"• {b}"
        r.font.name = "Arial"
        r.font.size = Pt(12.5)
        r.font.color.rgb = TEXT_DARK


def set_bg(slide, color=BG_SLATE):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def build_presentation(out_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    base_dir = r"C:\Users\HP\AndroidStudioProjects\ProyectoFinal\Documentacion"
    diag_dir = os.path.join(base_dir, "diagramas")
    cap_dir = os.path.join(base_dir, "capturas")
    icon_path = r"C:\Users\HP\AndroidStudioProjects\ProyectoFinal\app\src\main\res\drawable\encuesta.png"

    # =========================================================================
    # SLIDE 1: PORTADA
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    set_bg(s1, NAVY_DARK)

    accent_band = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.28), Inches(7.5))
    accent_band.fill.solid()
    accent_band.fill.fore_color.rgb = ACCENT
    accent_band.line.fill.background()

    if os.path.exists(icon_path):
        s1.shapes.add_picture(icon_path, Inches(0.9), Inches(0.7), height=Inches(1.1))

    tb1 = s1.shapes.add_textbox(Inches(2.2), Inches(0.7), Inches(10.3), Inches(1.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    r = p.add_run()
    r.text = "UNIVERSIDAD NACIONAL AMAZÓNICA DE MADRE DE DIOS"
    r.font.name = "Arial"
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    r2 = p2.add_run()
    r2.text = "Escuela Profesional de Ingeniería de Sistemas e Informática · Desarrollo de Aplicaciones Móviles II (2026-II)"
    r2.font.name = "Arial"
    r2.font.size = Pt(13)
    r2.font.color.rgb = RGBColor(191, 219, 254)

    tb_main = s1.shapes.add_textbox(Inches(0.9), Inches(2.25), Inches(11.5), Inches(2.4))
    tfm = tb_main.text_frame
    tfm.word_wrap = True
    pm1 = tfm.paragraphs[0]
    pm1.space_after = Pt(10)
    rm1 = pm1.add_run()
    rm1.text = "VotaApp UNAMAD"
    rm1.font.name = "Arial"
    rm1.font.size = Pt(40)
    rm1.font.bold = True
    rm1.font.color.rgb = WHITE

    pm2 = tfm.add_paragraph()
    rm2 = pm2.add_run()
    rm2.text = "Aplicación Móvil Nativa en Kotlin para la Gestión de Encuestas, Votaciones y Conteo de Resultados en Tiempo Real"
    rm2.font.name = "Arial"
    rm2.font.size = Pt(20)
    rm2.font.color.rgb = RGBColor(226, 232, 240)

    info_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(4.85), Inches(11.5), Inches(1.85))
    info_box.fill.solid()
    info_box.fill.fore_color.rgb = NAVY
    info_box.line.color.rgb = ACCENT
    info_box.line.width = Pt(1.2)
    info_box.adjustments[0] = 0.06

    tbi = s1.shapes.add_textbox(Inches(1.2), Inches(5.05), Inches(10.9), Inches(1.5))
    tfi = tbi.text_frame
    tfi.word_wrap = True
    for lbl, val in [
        ("Docente:", "Ing. Laura Salvatierra, Leonel Christofher"),
        ("Integrantes:", "Amezquita Camargo, Maicol Alberto  |  Torres Saire, Bickmer Fabricio"),
        ("Lugar y Año:", "Puerto Maldonado – Madre de Dios – Perú · 2026")
    ]:
        pi = tfi.add_paragraph() if len(tfi.paragraphs[0].text) > 0 else tfi.paragraphs[0]
        pi.space_after = Pt(6)
        rl = pi.add_run()
        rl.text = f"{lbl} "
        rl.font.name = "Arial"
        rl.font.size = Pt(14)
        rl.font.bold = True
        rl.font.color.rgb = RGBColor(147, 197, 253)
        rv = pi.add_run()
        rv.text = val
        rv.font.name = "Arial"
        rv.font.size = Pt(14)
        rv.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 2: PROBLEMA Y SOLUCIÓN
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    set_bg(s2)
    add_header(s2, "1. Problemática y Propuesta de Solución", "Bloque 1: Problema y Objetivos (3 min)", 2)

    add_card(s2, 0.6, 1.55, 5.9, 5.2, "Problemática Identificada en UNAMAD", [
        "Ineficiencia operativa: el conteo manual en boletas físicas genera demoras, costos de papel y errores humanos de tabulación.",
        "Brechas de conectividad: los formularios web fallan en aulas cuando la red Wi-Fi se satura o no hay datos móviles.",
        "Falta de control de duplicidad: ausencia de validación estricta que impida que un participante emita múltiples votos.",
        "Ausencia de métricas inmediatas: los resultados consolidados tardan horas en publicarse tras el sufragio."
    ], accent_color=RGBColor(220, 38, 38))

    add_card(s2, 6.8, 1.55, 5.9, 5.2, "Solución: VotaApp UNAMAD (Offline-First)", [
        "Aplicación móvil nativa en Kotlin (100% autónoma sin depender de internet en aula).",
        "Persistencia relacional local en SQLite (encuestas_unamad.db) con integridad referencial y transacciones ACID.",
        "Control estricto de voto único por encuesta mediante yaVotoParticipante() con normalización LOWER(TRIM()).",
        "Conteo instantáneo con porcentajes exactos, barras ProgressBar, opción ganadora y auditoría de votantes."
    ], accent_color=SUCCESS)

    # =========================================================================
    # SLIDE 3: OBJETIVOS Y ALCANCE
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    set_bg(s3)
    add_header(s3, "2. Objetivos y Alcance Funcional", "Bloque 1: Problema y Objetivos (3 min)", 3)

    add_card(s3, 0.6, 1.55, 12.1, 1.55, "Objetivo General", [
        "Desarrollar e implementar una aplicación móvil nativa en Kotlin para Android que permita administrar encuestas, configurar preguntas dinámicas, registrar votaciones con control de voto único y visualizar resultados estadísticos en tiempo real."
    ], accent_color=NAVY)

    add_card(s3, 0.6, 3.3, 5.9, 3.45, "Objetivos Específicos (OE1 – OE4)", [
        "OE1: Modelo relacional SQLite con 4 tablas, llaves foráneas y borrado en cascada.",
        "OE2: Interfaces Material Design 3 en 5 pantallas (Activities) intuitivas y responsivas.",
        "OE3: Validación de formularios y control estricto de no duplicidad de voto.",
        "OE4: Motor estadístico en tiempo real con porcentajes, barras y ganador."
    ], accent_color=ACCENT)

    add_card(s3, 6.8, 3.3, 5.9, 3.45, "Requerimientos Funcionales (RF01 – RF08)", [
        "RF01–RF04: CRUD completo de encuestas (crear, filtrar, editar, eliminar en cascada).",
        "RF05–RF06: Preguntas dinámicas (Selección Única / Múltiple) con mínimo 2 alternativas.",
        "RF07: Sufragio con identificación obligatoria y bloqueo de doble voto.",
        "RF08: Tabulación, porcentajes decimales, registro de auditoría y reinicio a 0."
    ], accent_color=SUCCESS)

    # =========================================================================
    # SLIDE 4: ARQUITECTURA Y STACK
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    set_bg(s4)
    add_header(s4, "3. Arquitectura en Tres Capas y Stack Tecnológico", "Bloque 2: Diseño y Tecnologías (3 min)", 4)

    add_card(s4, 0.6, 1.55, 5.3, 5.2, "Stack Real del Proyecto", [
        "Lenguaje: Kotlin 2.2.10 (null-safety, data classes).",
        "IDE & Build: Android Studio · Gradle 9.6.0 · AGP 9.5.0.",
        "SDK: Android 7.0 (API 24) a Android 16 (API 36).",
        "UI: Material Components 1.10.0 (MaterialCardView, MaterialSwitch, MaterialButton, Edge-to-Edge + IME).",
        "Persistencia: SQLiteOpenHelper nativo (18 métodos CRUD + 3 helpers internos)."
    ], accent_color=NAVY)

    fig2 = os.path.join(diag_dir, "fig2_arquitectura.png")
    if os.path.exists(fig2):
        s4.shapes.add_picture(fig2, Inches(6.15), Inches(1.55), width=Inches(6.55))

    # =========================================================================
    # SLIDE 5: BASE DE DATOS RELACIONAL
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    set_bg(s5)
    add_header(s5, "4. Diseño de Base de Datos Relacional (3FN)", "Bloque 2: Diseño y Tecnologías (3 min)", 5)

    fig6 = os.path.join(diag_dir, "fig6_base_datos_er.png")
    if os.path.exists(fig6):
        s5.shapes.add_picture(fig6, Inches(0.6), Inches(1.5), height=Inches(5.35))

    add_card(s5, 6.2, 1.55, 6.5, 5.2, "Integridad Referencial y Tablas (SQLite)", [
        "encuestas: id_encuesta (PK), titulo, descripcion, categoria, activa (0/1), fecha_creacion.",
        "preguntas: id_pregunta (PK), id_encuesta (FK CASCADE), texto_pregunta, tipo_pregunta ('UNICA'|'MULTIPLE').",
        "alternativas: id_alternativa (PK), id_pregunta (FK CASCADE), texto_alternativa, votos.",
        "respuestas: id_respuesta (PK), 3 FKs CASCADE, participante, fecha_voto.",
        "PRAGMA foreign_keys = ON habilitado en onConfigure() + transacciones atómicas."
    ], accent_color=ACCENT)

    # =========================================================================
    # SLIDE 6: EVIDENCIAS PARTE 1
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    set_bg(s6)
    add_header(s6, "5. Demostración Funcional: Gestión de Encuestas y Preguntas", "Bloque 3: Demostración Funcional (6 min)", 6)

    ev1 = os.path.join(cap_dir, "evidencia_1_gestion.png")
    if os.path.exists(ev1):
        s6.shapes.add_picture(ev1, Inches(0.75), Inches(1.5), width=Inches(11.8))

    # =========================================================================
    # SLIDE 7: EVIDENCIAS PARTE 2
    # =========================================================================
    s7 = prs.slides.add_slide(blank)
    set_bg(s7)
    add_header(s7, "6. Demostración Funcional: Votación y Resultados en Vivo", "Bloque 3: Demostración Funcional (6 min)", 7)

    ev2 = os.path.join(cap_dir, "evidencia_2_resultados.png")
    if os.path.exists(ev2):
        s7.shapes.add_picture(ev2, Inches(0.6), Inches(1.5), height=Inches(5.35))

    add_card(s7, 7.6, 1.55, 5.1, 5.2, "Aspectos Clave en Ejecución", [
        "Renderizado dinámico de RadioGroups (selección única) y CheckBoxes (múltiple).",
        "Preservación de respuestas seleccionadas al rotar la pantalla (onSaveInstanceState).",
        "Bloqueo automático de voto si la encuesta está Cerrada o el participante ya sufragó.",
        "Destacado ámbar ('Ganadora • ...') y barras ProgressBar con precisión decimal."
    ], accent_color=WARNING)

    # =========================================================================
    # SLIDE 8: LÓGICA CRÍTICA EN KOTLIN
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    set_bg(s8)
    add_header(s8, "7. Validaciones, Seguridad y Transacciones en Kotlin", "Bloque 3: Demostración y Defensa Técnica", 8)

    add_card(s8, 0.6, 1.55, 5.9, 5.2, "Control de Voto Único y Atomicidad", [
        "Consultas SQL parametrizadas (Prepared Statements) contra inyección SQL.",
        "yaVotoParticipante(): compara LOWER(TRIM(participante)) por encuesta con LIMIT 1.",
        "registrarVotos(): envuelve inserción en 'respuestas' + incremento en 'alternativas' dentro de beginTransaction() / setTransactionSuccessful().",
        "Eliminación en cascada y reinicio seguro a 0 con confirmación modal (AlertDialog)."
    ], accent_color=NAVY)

    add_card(s8, 6.8, 1.55, 5.9, 5.2, "Validaciones y Experiencia de Usuario", [
        "Encuesta: título obligatorio (>= 5 caracteres) y descripción obligatoria.",
        "Preguntas: enunciado obligatorio y mínimo 2 alternativas válidas.",
        "Votación: identificación (>= 3 caracteres) y todas las preguntas respondidas.",
        "Navegación segura: OnBackPressedCallback impide salir de GestionarPreguntas sin al menos 1 pregunta.",
        "Edge-to-Edge continuo con UiInsetsHelper.kt y soporte de teclado (IME)."
    ], accent_color=ACCENT)

    # =========================================================================
    # SLIDE 9: PRUEBAS Y CUMPLIMIENTO
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    set_bg(s9)
    add_header(s9, "8. Pruebas Funcionales y Matriz de Cumplimiento", "Verificación sobre Emulador Android 16 (API 36)", 9)

    add_card(s9, 0.6, 1.55, 5.9, 5.2, "Batería de Pruebas (CP01 – CP10: 100%)", [
        "CP01–CP02: Alta de encuestas y bloqueo de campos vacíos/cortos.",
        "CP03–CP04: Filtrado reactivo y bloqueo de voto al cerrar encuesta.",
        "CP05: Eliminación física en cascada verificada (0 registros huérfanos).",
        "CP06–CP07: Preguntas UNICA/MULTIPLE y mínimo de 2 alternativas.",
        "CP08–CP10: Bloqueo de voto duplicado, porcentajes exactos y reinicio a 0."
    ], accent_color=SUCCESS)

    add_card(s9, 6.8, 1.55, 5.9, 5.2, "Cumplimiento de Objetivos (ISO/IEC 25010)", [
        "OE1 (Persistencia SQLite): 100% CUMPLIDO (4 tablas normalizadas + cascadas).",
        "OE2 (Interfaces Material 3): 100% CUMPLIDO (5 pantallas + contraste WCAG AA).",
        "OE3 (Voto Único y Validación): 100% CUMPLIDO (control transaccional estricto).",
        "OE4 (Estadísticas en Vivo): 100% CUMPLIDO (cálculo porcentual + ProgressBar).",
        "Compilación y tests: assembleDebug y testDebugUnitTest exitosos."
    ], accent_color=NAVY)

    # =========================================================================
    # SLIDE 10: CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    set_bg(s10)
    add_header(s10, "9. Conclusiones y Trabajo Futuro", "Cierre y Preguntas del Docente (3 min)", 10)

    add_card(s10, 0.6, 1.55, 5.9, 5.2, "Conclusiones", [
        "Se implementó con éxito VotaApp UNAMAD en Kotlin nativo, resolviendo el problema de votaciones y encuestas presenciales sin internet.",
        "SQLiteOpenHelper con llaves foráneas y transacciones atómicas garantiza integridad referencial y respuesta inmediata.",
        "yaVotoParticipante() elimina el riesgo de votos duplicados en el aula.",
        "El diseño Material 3 con capturas verificadas ofrece alta usabilidad y claridad visual."
    ], accent_color=SUCCESS)

    add_card(s10, 6.8, 1.55, 5.9, 5.2, "Recomendaciones de Mejora", [
        "Sincronización híbrida en la nube mediante Firebase Firestore o API REST.",
        "Exportación de actas oficiales en PDF y hojas de cálculo (.csv / .xlsx).",
        "Autenticación institucional (@unamad.edu.pe) y biometría (BiometricPrompt).",
        "Gráficos estadísticos complementarios (sectores y barras comparativas con MPAndroidChart)."
    ], accent_color=ACCENT)

    prs.save(out_path)
    print("Presentación PPTX generada exitosamente:", out_path)


if __name__ == "__main__":
    build_presentation(r"C:\Users\HP\AndroidStudioProjects\ProyectoFinal\Documentacion\Presentacion_VotaApp_UNAMAD.pptx")
