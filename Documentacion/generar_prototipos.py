import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_phone_frame(ax, x0, y0, width, height, title="Pantalla", status_title="VotaApp UNAMAD"):
    # Outer phone shadow / border
    phone_bg = patches.FancyBboxPatch((x0, y0), width, height, boxstyle="round,pad=0.02,rounding_size=0.08",
                                     facecolor="#1A252F", edgecolor="#2C3E50", linewidth=3, zorder=1)
    ax.add_patch(phone_bg)
    
    # Inner screen
    screen_margin = 0.04
    sx = x0 + screen_margin
    sy = y0 + screen_margin
    sw = width - 2 * screen_margin
    sh = height - 2 * screen_margin
    screen = patches.FancyBboxPatch((sx, sy), sw, sh, boxstyle="round,pad=0.01,rounding_size=0.04",
                                   facecolor="#F4F6F7", edgecolor="#BDC3C7", linewidth=1.5, zorder=2)
    ax.add_patch(screen)
    
    # Speaker / camera notch
    cam = patches.Circle((x0 + width/2, y0 + height - 0.025), 0.012, facecolor="#000000", zorder=10)
    ax.add_patch(cam)
    
    # Status bar (Android)
    ax.text(sx + 0.03, sy + sh - 0.035, "10:30 AM", fontsize=7, fontweight='bold', color="#7F8C8D", zorder=5)
    ax.text(sx + sw - 0.12, sy + sh - 0.035, "4G  100%", fontsize=6.5, fontweight='bold', color="#7F8C8D", zorder=5)
    
    # App Bar (Header)
    appbar = patches.Rectangle((sx, sy + sh - 0.12), sw, 0.075, facecolor="#1A5276", edgecolor="none", zorder=3)
    ax.add_patch(appbar)
    ax.text(sx + 0.04, sy + sh - 0.08, status_title, fontsize=8.5, fontweight='bold', color="#FFFFFF", zorder=5)
    
    # Bottom Navigation bar (Android pill)
    nav_pill = patches.FancyBboxPatch((x0 + width/2 - 0.1, sy + 0.015), 0.2, 0.012, boxstyle="round,pad=0.005",
                                     facecolor="#BDC3C7", edgecolor="none", zorder=5)
    ax.add_patch(nav_pill)
    
    return sx, sy, sw, sh - 0.12

# ==========================================================
# FIGURA 3: PROTOTIPOS DE PANTALLAS (1, 2, 3)
# ==========================================================
def generar_figura_3(output_path):
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 3.8)
    ax.set_ylim(0, 2.5)
    ax.axis('off')
    
    fig.patch.set_facecolor('#FFFFFF')

    # PHONE 1: MainActivity
    sx, sy, sw, sh = draw_phone_frame(ax, 0.15, 0.1, 1.0, 2.25, status_title="VotaApp UNAMAD")
    ax.text(0.65, 2.4, "Prototipo 1: Panel Principal (MainActivity)", fontsize=9.5, fontweight='bold', ha='center', color='#1A5276')
    
    # Metric cards row
    cw = (sw - 0.08) / 3
    for i, (kpi, val, col) in enumerate([("Total", "6", "#2980B9"), ("Activas", "4", "#27AE60"), ("Votos", "78", "#8E44AD")]):
        card = patches.FancyBboxPatch((sx + 0.02 + i*(cw+0.02), sy + sh - 0.13), cw, 0.11,
                                      boxstyle="round,pad=0.01,rounding_size=0.02", facecolor="#FFFFFF", edgecolor=col, linewidth=1.5, zorder=4)
        ax.add_patch(card)
        ax.text(sx + 0.02 + i*(cw+0.02) + cw/2, sy + sh - 0.06, val, fontsize=10, fontweight='bold', ha='center', color=col, zorder=5)
        ax.text(sx + 0.02 + i*(cw+0.02) + cw/2, sy + sh - 0.105, kpi, fontsize=6.5, ha='center', color="#566573", zorder=5)
        
    # Filter Tabs
    tabs_bg = patches.Rectangle((sx + 0.02, sy + sh - 0.20), sw - 0.04, 0.055, facecolor="#EAECEE", zorder=4)
    ax.add_patch(tabs_bg)
    ax.text(sx + 0.08, sy + sh - 0.175, "Todas (6)", fontsize=7, color="#566573", zorder=5)
    tab_act = patches.Rectangle((sx + sw/3 - 0.02, sy + sh - 0.20), sw/3 + 0.04, 0.055, facecolor="#1A5276", zorder=5)
    ax.add_patch(tab_act)
    ax.text(sx + sw/2, sy + sh - 0.175, "Activas (4)", fontsize=7, fontweight='bold', color="#FFFFFF", ha='center', zorder=6)
    ax.text(sx + sw - 0.10, sy + sh - 0.175, "Cerradas (2)", fontsize=7, color="#566573", zorder=5)
    
    # Survey Card 1
    c1 = patches.FancyBboxPatch((sx + 0.03, sy + sh - 0.58), sw - 0.06, 0.35,
                                boxstyle="round,pad=0.01,rounding_size=0.03", facecolor="#FFFFFF", edgecolor="#D5D8DC", linewidth=1.2, zorder=4)
    ax.add_patch(c1)
    tag1 = patches.FancyBboxPatch((sx + sw - 0.28, sy + sh - 0.28), 0.22, 0.035, boxstyle="round,pad=0.005", facecolor="#D4EFDF", edgecolor="none", zorder=5)
    ax.add_patch(tag1)
    ax.text(sx + sw - 0.17, sy + sh - 0.265, "[ACTIVA]", fontsize=6, fontweight='bold', color="#1E8449", ha='center', zorder=6)
    ax.text(sx + 0.06, sy + sh - 0.27, "Elección de Delegado 2026-II", fontsize=7.5, fontweight='bold', color="#1A5276", zorder=5)
    ax.text(sx + 0.06, sy + sh - 0.32, "Cat: Estudiantil | 2 preguntas", fontsize=6.5, color="#7F8C8D", zorder=5)
    ax.text(sx + 0.06, sy + sh - 0.38, "Votación oficial de delegados para la\nasignatura Móviles II UNAMAD.", fontsize=6.2, color="#2C3E50", zorder=5)
    
    # Action buttons in card 1
    btn_votar = patches.FancyBboxPatch((sx + 0.06, sy + sh - 0.54), 0.24, 0.05, boxstyle="round,pad=0.005", facecolor="#27AE60", edgecolor="none", zorder=5)
    ax.add_patch(btn_votar)
    ax.text(sx + 0.18, sy + sh - 0.515, "Votar", fontsize=6.5, fontweight='bold', color="#FFFFFF", ha='center', zorder=6)
    
    btn_res = patches.FancyBboxPatch((sx + 0.33, sy + sh - 0.54), 0.24, 0.05, boxstyle="round,pad=0.005", facecolor="#2980B9", edgecolor="none", zorder=5)
    ax.add_patch(btn_res)
    ax.text(sx + 0.45, sy + sh - 0.515, "Conteo", fontsize=6.5, fontweight='bold', color="#FFFFFF", ha='center', zorder=6)

    btn_edit = patches.FancyBboxPatch((sx + 0.60, sy + sh - 0.54), 0.13, 0.05, boxstyle="round,pad=0.005", facecolor="#F39C12", edgecolor="none", zorder=5)
    ax.add_patch(btn_edit)
    ax.text(sx + 0.665, sy + sh - 0.515, "Edit", fontsize=6, fontweight='bold', color="#FFFFFF", ha='center', zorder=6)

    btn_del = patches.FancyBboxPatch((sx + 0.75, sy + sh - 0.54), 0.13, 0.05, boxstyle="round,pad=0.005", facecolor="#C0392B", edgecolor="none", zorder=5)
    ax.add_patch(btn_del)
    ax.text(sx + 0.815, sy + sh - 0.515, "Del", fontsize=6, fontweight='bold', color="#FFFFFF", ha='center', zorder=6)

    # Survey Card 2
    c2 = patches.FancyBboxPatch((sx + 0.03, sy + sh - 0.96), sw - 0.06, 0.35,
                                boxstyle="round,pad=0.01,rounding_size=0.03", facecolor="#FFFFFF", edgecolor="#D5D8DC", linewidth=1.2, zorder=4)
    ax.add_patch(c2)
    tag2 = patches.FancyBboxPatch((sx + sw - 0.28, sy + sh - 0.66), 0.22, 0.035, boxstyle="round,pad=0.005", facecolor="#D4EFDF", edgecolor="none", zorder=5)
    ax.add_patch(tag2)
    ax.text(sx + sw - 0.17, sy + sh - 0.645, "[ACTIVA]", fontsize=6, fontweight='bold', color="#1E8449", ha='center', zorder=6)
    ax.text(sx + 0.06, sy + sh - 0.65, "Evaluación Docente 2026-II", fontsize=7.5, fontweight='bold', color="#1A5276", zorder=5)
    ax.text(sx + 0.06, sy + sh - 0.70, "Cat: Académica | 3 preguntas", fontsize=6.5, color="#7F8C8D", zorder=5)
    ax.text(sx + 0.06, sy + sh - 0.76, "Percepción estudiantil sobre el avance\nsilábico y metodología de clase.", fontsize=6.2, color="#2C3E50", zorder=5)
    
    # Action buttons in card 2
    btn2_v = patches.FancyBboxPatch((sx + 0.06, sy + sh - 0.92), 0.24, 0.05, boxstyle="round,pad=0.005", facecolor="#27AE60", edgecolor="none", zorder=5)
    ax.add_patch(btn2_v)
    ax.text(sx + 0.18, sy + sh - 0.895, "Votar", fontsize=6.5, fontweight='bold', color="#FFFFFF", ha='center', zorder=6)
    btn2_r = patches.FancyBboxPatch((sx + 0.33, sy + sh - 0.92), 0.24, 0.05, boxstyle="round,pad=0.005", facecolor="#2980B9", edgecolor="none", zorder=5)
    ax.add_patch(btn2_r)
    ax.text(sx + 0.45, sy + sh - 0.895, "Conteo", fontsize=6.5, fontweight='bold', color="#FFFFFF", ha='center', zorder=6)

    # FAB Button "+"
    fab = patches.Circle((sx + sw - 0.12, sy + 0.10), 0.08, facecolor="#E67E22", edgecolor="#FFFFFF", linewidth=2, zorder=10)
    ax.add_patch(fab)
    ax.text(sx + sw - 0.12, sy + 0.08, "+", fontsize=16, fontweight='bold', color="#FFFFFF", ha='center', zorder=11)

    # ==========================================================
    # PHONE 2: CrearEncuestaActivity
    # ==========================================================
    sx, sy, sw, sh = draw_phone_frame(ax, 1.4, 0.1, 1.0, 2.25, status_title="<- Nueva Encuesta")
    ax.text(1.9, 2.4, "Prototipo 2: Formulario de Creación (CrearEncuestaActivity)", fontsize=9.5, fontweight='bold', ha='center', color='#1A5276')
    
    # Form Container
    form_box = patches.FancyBboxPatch((sx + 0.03, sy + 0.08), sw - 0.06, sh - 0.12,
                                      boxstyle="round,pad=0.01,rounding_size=0.03", facecolor="#FFFFFF", edgecolor="#D5D8DC", linewidth=1.2, zorder=4)
    ax.add_patch(form_box)
    
    # Input 1: Title
    ax.text(sx + 0.06, sy + sh - 0.08, "Título de la Encuesta (*)", fontsize=7, fontweight='bold', color="#1A5276", zorder=5)
    in1 = patches.Rectangle((sx + 0.06, sy + sh - 0.17), sw - 0.12, 0.075, facecolor="#F8F9F9", edgecolor="#BDC3C7", linewidth=1, zorder=5)
    ax.add_patch(in1)
    ax.text(sx + 0.08, sy + sh - 0.13, "Diagnóstico de Infraestructura Cómputo", fontsize=6.5, color="#2C3E50", zorder=6)
    
    # Input 2: Description
    ax.text(sx + 0.06, sy + sh - 0.22, "Descripción / Objetivo (*)", fontsize=7, fontweight='bold', color="#1A5276", zorder=5)
    in2 = patches.Rectangle((sx + 0.06, sy + sh - 0.39), sw - 0.12, 0.15, facecolor="#F8F9F9", edgecolor="#BDC3C7", linewidth=1, zorder=5)
    ax.add_patch(in2)
    ax.text(sx + 0.08, sy + sh - 0.27, "Recopilación de necesidades sobre\nconectividad, equipos y software\npara laboratorios de la UNAMAD.", fontsize=6.2, color="#2C3E50", zorder=6)
    
    # Input 3: Category Spinner
    ax.text(sx + 0.06, sy + sh - 0.44, "Categoría (*)", fontsize=7, fontweight='bold', color="#1A5276", zorder=5)
    sp = patches.Rectangle((sx + 0.06, sy + sh - 0.53), sw - 0.12, 0.075, facecolor="#F8F9F9", edgecolor="#BDC3C7", linewidth=1, zorder=5)
    ax.add_patch(sp)
    ax.text(sx + 0.08, sy + sh - 0.49, "Infraestructura y Tecnología", fontsize=6.8, color="#2C3E50", zorder=6)
    ax.text(sx + sw - 0.12, sy + sh - 0.49, "v", fontsize=7, fontweight='bold', color="#7F8C8D", zorder=6)

    # Switch Activa
    sw_bg = patches.FancyBboxPatch((sx + 0.06, sy + sh - 0.67), sw - 0.12, 0.09,
                                   boxstyle="round,pad=0.005", facecolor="#EAF2F8", edgecolor="none", zorder=5)
    ax.add_patch(sw_bg)
    ax.text(sx + 0.09, sy + sh - 0.63, "Estado: Activa para Votaciones", fontsize=6.8, fontweight='bold', color="#1A5276", zorder=6)
    # switch toggle
    sw_pill = patches.FancyBboxPatch((sx + sw - 0.18, sy + sh - 0.65), 0.09, 0.045, boxstyle="round,pad=0.002", facecolor="#2ECC71", zorder=6)
    ax.add_patch(sw_pill)
    sw_circ = patches.Circle((sx + sw - 0.11, sy + sh - 0.627), 0.018, facecolor="#FFFFFF", zorder=7)
    ax.add_patch(sw_circ)

    # Save button
    btn_save = patches.FancyBboxPatch((sx + 0.06, sy + sh - 0.83), sw - 0.12, 0.085,
                                      boxstyle="round,pad=0.01", facecolor="#1A5276", edgecolor="none", zorder=6)
    ax.add_patch(btn_save)
    ax.text(sx + sw/2, sy + sh - 0.785, "Guardar Encuesta", fontsize=8, fontweight='bold', color="#FFFFFF", ha='center', zorder=7)

    # Manage Questions Shortcut
    btn_q = patches.FancyBboxPatch((sx + 0.06, sy + sh - 0.95), sw - 0.12, 0.075,
                                   boxstyle="round,pad=0.01", facecolor="#EBF5FB", edgecolor="#2980B9", linewidth=1.2, zorder=6)
    ax.add_patch(btn_q)
    ax.text(sx + sw/2, sy + sh - 0.91, "Configurar Preguntas Asociadas", fontsize=7.2, fontweight='bold', color="#2980B9", ha='center', zorder=7)

    # ==========================================================
    # PHONE 3: GestionarPreguntasActivity
    # ==========================================================
    sx, sy, sw, sh = draw_phone_frame(ax, 2.65, 0.1, 1.0, 2.25, status_title="<- Gestionar Preguntas")
    ax.text(3.15, 2.4, "Prototipo 3: Preguntas y Alternativas (GestionarPreguntasActivity)", fontsize=9.5, fontweight='bold', ha='center', color='#1A5276')
    
    # Subheader encuesta
    subhdr = patches.Rectangle((sx + 0.03, sy + sh - 0.07), sw - 0.06, 0.055, facecolor="#D4E6F1", edgecolor="none", zorder=4)
    ax.add_patch(subhdr)
    ax.text(sx + 0.06, sy + sh - 0.045, "Encuesta: Elección Delegado 2026-II", fontsize=6.8, fontweight='bold', color="#1A5276", zorder=5)
    
    # Form card
    qbox = patches.FancyBboxPatch((sx + 0.03, sy + 0.08), sw - 0.06, sh - 0.17,
                                  boxstyle="round,pad=0.01,rounding_size=0.03", facecolor="#FFFFFF", edgecolor="#D5D8DC", linewidth=1.2, zorder=4)
    ax.add_patch(qbox)
    
    ax.text(sx + 0.06, sy + sh - 0.11, "Texto de la Pregunta (*)", fontsize=7, fontweight='bold', color="#1A5276", zorder=5)
    qinput = patches.Rectangle((sx + 0.06, sy + sh - 0.21), sw - 0.12, 0.08, facecolor="#F8F9F9", edgecolor="#BDC3C7", linewidth=1, zorder=5)
    ax.add_patch(qinput)
    ax.text(sx + 0.08, sy + sh - 0.165, "¿Qué candidato apoya como delegado?", fontsize=6.5, color="#2C3E50", zorder=6)
    
    # RadioGroup Tipo Pregunta
    ax.text(sx + 0.06, sy + sh - 0.25, "Tipo de Selección (*)", fontsize=7, fontweight='bold', color="#1A5276", zorder=5)
    r1 = patches.Circle((sx + 0.08, sy + sh - 0.29), 0.016, facecolor="#2980B9", edgecolor="#1A5276", linewidth=1.5, zorder=6)
    ax.add_patch(r1)
    ax.text(sx + 0.12, sy + sh - 0.297, "Selección Única", fontsize=6.5, fontweight='bold', color="#2C3E50", zorder=6)
    
    r2 = patches.Circle((sx + 0.52, sy + sh - 0.29), 0.016, facecolor="#FFFFFF", edgecolor="#7F8C8D", linewidth=1.5, zorder=6)
    ax.add_patch(r2)
    ax.text(sx + 0.56, sy + sh - 0.297, "Múltiple", fontsize=6.5, color="#7F8C8D", zorder=6)

    # Alternativas list
    ax.text(sx + 0.06, sy + sh - 0.35, "Alternativas (Mínimo 2 requeridas):", fontsize=7, fontweight='bold', color="#1A5276", zorder=5)
    
    for idx, (txt_alt) in enumerate(["Carlos Mendoza Ruiz (Lista 1)", "Ana Lucía Quispe (Lista 2)", "Voto en Blanco"]):
        y_alt = sy + sh - 0.43 - idx * 0.075
        alt_rect = patches.Rectangle((sx + 0.06, y_alt), sw - 0.19, 0.06, facecolor="#F4F6F7", edgecolor="#BDC3C7", linewidth=1, zorder=5)
        ax.add_patch(alt_rect)
        ax.text(sx + 0.08, y_alt + 0.018, f"{idx+1}. {txt_alt}", fontsize=6.2, color="#2C3E50", zorder=6)
        # delete btn
        d_btn = patches.FancyBboxPatch((sx + sw - 0.11, y_alt), 0.05, 0.06, boxstyle="round,pad=0.002", facecolor="#FDEDEC", edgecolor="#E74C3C", linewidth=1, zorder=5)
        ax.add_patch(d_btn)
        ax.text(sx + sw - 0.085, y_alt + 0.018, "X", fontsize=6.5, fontweight='bold', color="#C0392B", ha='center', zorder=6)

    # Button Agregar Alternativa
    btn_add_alt = patches.FancyBboxPatch((sx + 0.06, sy + sh - 0.68), sw - 0.12, 0.065,
                                        boxstyle="round,pad=0.005", facecolor="#EAF2F8", edgecolor="#2980B9", linewidth=1.2, linestyle='--', zorder=5)
    ax.add_patch(btn_add_alt)
    ax.text(sx + sw/2, sy + sh - 0.645, "+ Añadir Alternativa de Respuesta", fontsize=6.8, fontweight='bold', color="#2980B9", ha='center', zorder=6)

    # Button Guardar Pregunta
    btn_save_q = patches.FancyBboxPatch((sx + 0.06, sy + sh - 0.82), sw - 0.12, 0.085,
                                       boxstyle="round,pad=0.01", facecolor="#27AE60", edgecolor="none", zorder=6)
    ax.add_patch(btn_save_q)
    ax.text(sx + sw/2, sy + sh - 0.775, "Guardar Pregunta y Opciones", fontsize=7.5, fontweight='bold', color="#FFFFFF", ha='center', zorder=7)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figura 3 guardada con éxito:", output_path)

# ==========================================================
# FIGURA 4: PROTOTIPOS DE PANTALLAS (4, 5)
# ==========================================================
def generar_figura_4(output_path):
    fig, ax = plt.subplots(figsize=(13, 9), dpi=300)
    ax.set_xlim(0, 2.7)
    ax.set_ylim(0, 2.5)
    ax.axis('off')
    
    fig.patch.set_facecolor('#FFFFFF')

    # PHONE 4: RegistrarVotoActivity
    sx, sy, sw, sh = draw_phone_frame(ax, 0.2, 0.1, 1.05, 2.25, status_title="<- Registrar Mi Voto")
    ax.text(0.72, 2.4, "Prototipo 4: Votación Móvil (RegistrarVotoActivity)", fontsize=9.5, fontweight='bold', ha='center', color='#1A5276')
    
    # Encabezado informativo
    ihdr = patches.FancyBboxPatch((sx + 0.03, sy + sh - 0.12), sw - 0.06, 0.10,
                                  boxstyle="round,pad=0.005", facecolor="#D4E6F1", edgecolor="#2980B9", linewidth=1.2, zorder=4)
    ax.add_patch(ihdr)
    ax.text(sx + 0.05, sy + sh - 0.05, "Elección de Delegado 2026-II", fontsize=7.5, fontweight='bold', color="#1A5276", zorder=5)
    ax.text(sx + 0.05, sy + sh - 0.095, "Por favor ingrese su código/nombre y responda.", fontsize=6.2, color="#2C3E50", zorder=5)

    # Input Participante
    ax.text(sx + 0.05, sy + sh - 0.16, "Código o Nombre del Votante (*):", fontsize=7, fontweight='bold', color="#1A5276", zorder=5)
    inp_part = patches.Rectangle((sx + 0.05, sy + sh - 0.24), sw - 0.10, 0.065, facecolor="#FFFFFF", edgecolor="#2980B9", linewidth=1.3, zorder=5)
    ax.add_patch(inp_part)
    ax.text(sx + 0.08, sy + sh - 0.205, "202201045 - Juan Diego Pérez", fontsize=6.8, color="#2C3E50", zorder=6)

    # Question 1 Container (RadioGroup)
    q1_box = patches.FancyBboxPatch((sx + 0.03, sy + sh - 0.60), sw - 0.06, 0.33,
                                   boxstyle="round,pad=0.01", facecolor="#FFFFFF", edgecolor="#D5D8DC", linewidth=1.2, zorder=4)
    ax.add_patch(q1_box)
    ax.text(sx + 0.05, sy + sh - 0.29, "1. ¿Quién debe ser el Delegado? (Única)", fontsize=7, fontweight='bold', color="#1A5276", zorder=5)
    
    # Radio options
    alts1 = [
        ("(*) Carlos Mendoza Ruiz (Lista 1)", True),
        ("( ) Ana Lucía Quispe (Lista 2)", False),
        ("( ) Voto en Blanco", False)
    ]
    for idx, (txt, sel) in enumerate(alts1):
        y_opt = sy + sh - 0.36 - idx * 0.07
        bg_col = "#EBF5FB" if sel else "#F8F9F9"
        bd_col = "#2980B9" if sel else "#EAEDED"
        opt_box = patches.Rectangle((sx + 0.05, y_opt), sw - 0.10, 0.055, facecolor=bg_col, edgecolor=bd_col, linewidth=1, zorder=5)
        ax.add_patch(opt_box)
        txt_col = "#1B4F72" if sel else "#566573"
        ax.text(sx + 0.08, y_opt + 0.018, txt, fontsize=6.5, fontweight='bold' if sel else 'normal', color=txt_col, zorder=6)

    # Question 2 Container (CheckBoxes)
    q2_box = patches.FancyBboxPatch((sx + 0.03, sy + sh - 0.93), sw - 0.06, 0.30,
                                   boxstyle="round,pad=0.01", facecolor="#FFFFFF", edgecolor="#D5D8DC", linewidth=1.2, zorder=4)
    ax.add_patch(q2_box)
    ax.text(sx + 0.05, sy + sh - 0.64, "2. ¿Comisiones de interés? (Múltiple)", fontsize=7, fontweight='bold', color="#1A5276", zorder=5)
    
    alts2 = [
        ("[X] Comisión de Horarios y Aulas", True),
        ("[X] Comisión de Proyectos y Ferias", True),
        ("[ ] Comisión de Actividades Deportivas", False)
    ]
    for idx, (txt, sel) in enumerate(alts2):
        y_opt = sy + sh - 0.71 - idx * 0.065
        bg_col = "#E8F8F5" if sel else "#F8F9F9"
        bd_col = "#27AE60" if sel else "#EAEDED"
        opt_box = patches.Rectangle((sx + 0.05, y_opt), sw - 0.10, 0.055, facecolor=bg_col, edgecolor=bd_col, linewidth=1, zorder=5)
        ax.add_patch(opt_box)
        txt_col = "#1E8449" if sel else "#566573"
        ax.text(sx + 0.08, y_opt + 0.018, txt, fontsize=6.5, fontweight='bold' if sel else 'normal', color=txt_col, zorder=6)

    # Submit button
    btn_sub = patches.FancyBboxPatch((sx + 0.05, sy + 0.05), sw - 0.10, 0.085,
                                    boxstyle="round,pad=0.01", facecolor="#27AE60", edgecolor="none", zorder=6)
    ax.add_patch(btn_sub)
    ax.text(sx + sw/2, sy + 0.09, "Confirmar y Emitir Mi Voto", fontsize=8, fontweight='bold', color="#FFFFFF", ha='center', zorder=7)

    # ==========================================================
    # PHONE 5: ResultadosActivity
    # ==========================================================
    sx, sy, sw, sh = draw_phone_frame(ax, 1.45, 0.1, 1.05, 2.25, status_title="<- Resultados Oficiales")
    ax.text(1.97, 2.4, "Prototipo 5: Conteo y Estadísticas (ResultadosActivity)", fontsize=9.5, fontweight='bold', ha='center', color='#1A5276')
    
    # Encabezado de encuesta
    rhdr = patches.FancyBboxPatch((sx + 0.03, sy + sh - 0.15), sw - 0.06, 0.13,
                                  boxstyle="round,pad=0.01", facecolor="#1A5276", edgecolor="none", zorder=4)
    ax.add_patch(rhdr)
    ax.text(sx + 0.06, sy + sh - 0.06, "Elección de Delegado 2026-II", fontsize=8, fontweight='bold', color="#FFFFFF", zorder=5)
    ax.text(sx + 0.06, sy + sh - 0.10, "Total Votos Emitidos: 42 participantes", fontsize=6.8, color="#D4E6F1", zorder=5)
    ax.text(sx + 0.06, sy + sh - 0.13, "Estado: Cerrado / Conteo definitivo", fontsize=6.2, color="#A9DFBF", zorder=5)

    # Winner Banner
    wbox = patches.FancyBboxPatch((sx + 0.03, sy + sh - 0.25), sw - 0.06, 0.085,
                                  boxstyle="round,pad=0.005", facecolor="#FEF9E7", edgecolor="#F39C12", linewidth=1.5, zorder=5)
    ax.add_patch(wbox)
    ax.text(sx + 0.06, sy + sh - 0.20, "OPCIÓN GANADORA:", fontsize=6.8, fontweight='bold', color="#B9770E", zorder=6)
    ax.text(sx + 0.06, sy + sh - 0.235, "Carlos Mendoza Ruiz (26 votos - 61.9%)", fontsize=7.2, fontweight='bold', color="#1A5276", zorder=6)

    # Question Breakdown Container
    qres = patches.FancyBboxPatch((sx + 0.03, sy + sh - 0.72), sw - 0.06, 0.44,
                                  boxstyle="round,pad=0.01", facecolor="#FFFFFF", edgecolor="#D5D8DC", linewidth=1.2, zorder=4)
    ax.add_patch(qres)
    ax.text(sx + 0.05, sy + sh - 0.285, "1. ¿Quién debe ser el Delegado?", fontsize=7, fontweight='bold', color="#1A5276", zorder=5)
    
    # Progress bars and counts
    opciones = [
        ("Carlos Mendoza", 26, 61.9, "#2980B9"),
        ("Ana Lucía Quispe", 14, 33.3, "#27AE60"),
        ("Voto en Blanco", 2, 4.8, "#95A5A6")
    ]
    for idx, (nombre, votos, pct, col) in enumerate(opciones):
        y_bar = sy + sh - 0.34 - idx * 0.115
        ax.text(sx + 0.05, y_bar, f"{nombre} ({votos} votos)", fontsize=6.5, fontweight='bold', color="#2C3E50", zorder=5)
        ax.text(sx + sw - 0.16, y_bar, f"{pct:.1f}%", fontsize=6.5, fontweight='bold', color=col, zorder=5)
        
        # Background bar
        b_bg = patches.Rectangle((sx + 0.05, y_bar - 0.035), sw - 0.10, 0.022, facecolor="#EAEDED", edgecolor="none", zorder=5)
        ax.add_patch(b_bg)
        # Fill bar
        fill_w = (sw - 0.10) * (pct / 100.0)
        b_fill = patches.Rectangle((sx + 0.05, y_bar - 0.035), fill_w, 0.022, facecolor=col, edgecolor="none", zorder=6)
        ax.add_patch(b_fill)

    # Participantes Audit List
    part_box = patches.FancyBboxPatch((sx + 0.03, sy + sh - 0.90), sw - 0.06, 0.16,
                                     boxstyle="round,pad=0.005", facecolor="#F8F9F9", edgecolor="#BDC3C7", linewidth=1, zorder=4)
    ax.add_patch(part_box)
    ax.text(sx + 0.05, sy + sh - 0.76, "Registro de Auditoría de Votantes (Últimos):", fontsize=6.5, fontweight='bold', color="#1A5276", zorder=5)
    ax.text(sx + 0.05, sy + sh - 0.81, "* 202201045 - Juan Diego Pérez (10:45 AM)", fontsize=6, color="#566573", zorder=5)
    ax.text(sx + 0.05, sy + sh - 0.85, "* 202102011 - María Claudia Rojas (10:48 AM)", fontsize=6, color="#566573", zorder=5)
    ax.text(sx + 0.05, sy + sh - 0.89, "* 202303099 - Edwin S. Morales (10:52 AM)", fontsize=6, color="#566573", zorder=5)

    # Reset votes button
    btn_rst = patches.FancyBboxPatch((sx + 0.05, sy + 0.05), sw - 0.10, 0.07,
                                     boxstyle="round,pad=0.01", facecolor="#FDEDEC", edgecolor="#C0392B", linewidth=1.2, zorder=6)
    ax.add_patch(btn_rst)
    ax.text(sx + sw/2, sy + 0.085, "Reiniciar Conteo de Votos (Admin)", fontsize=7, fontweight='bold', color="#C0392B", ha='center', zorder=7)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figura 4 guardada con éxito:", output_path)

if __name__ == "__main__":
    generar_figura_3(r"C:\Users\HP\AndroidStudioProjects\ProyectoFinal\Documentacion\diagramas\fig3_prototipos_ui.png")
    generar_figura_4(r"C:\Users\HP\AndroidStudioProjects\ProyectoFinal\Documentacion\diagramas\fig4_prototipos_votacion_resultados.png")
