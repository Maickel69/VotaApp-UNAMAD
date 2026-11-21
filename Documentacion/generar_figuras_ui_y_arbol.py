import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generar_figura_7_arbol_exacto(output_path):
    fig, ax = plt.subplots(figsize=(12, 10.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Root Box
    root_box = patches.FancyBboxPatch((0.5, 9.8), 9.0, 0.9, boxstyle="round,pad=0.02,rounding_size=0.05",
                                     facecolor="#1A5276", edgecolor="#154360", linewidth=2, zorder=2)
    ax.add_patch(root_box)
    ax.text(5.0, 10.35, "ProyectoFinal/ (Estructura Oficial en Android Studio)", fontsize=11, fontweight='bold', color="#FFFFFF", ha='center', zorder=3)
    ax.text(5.0, 10.0, "Paquete: com.example.proyectofinal | MinSdk 24 (Android 7.0) | TargetSdk 36 (Android 16)", fontsize=8.5, color="#D4E6F1", ha='center', zorder=3)

    # 3 Main Sections: manifests/java, res, gradle
    sections = [
        # (x, y, w, h, bg, border, title, items)
        (0.5, 3.4, 4.3, 6.0, "#E8F8F5", "#16A085", "app/src/main/java/ & manifests/", [
            ("AndroidManifest.xml", "Declaración oficial de las 5 Activities y filtros de inicio", "#1A5276"),
            ("com.example.proyectofinal/", "Paquete principal de lógica y persistencia Kotlin", "#0E6251"),
            ("  • Models.kt", "7 Data Classes: Encuesta, Pregunta, Alternativa, Respuesta...", "#2C3E50"),
            ("  • DatabaseHelper.kt", "SQLiteOpenHelper: DDL 4 tablas, 18 métodos CRUD y cascadas", "#2C3E50"),
            ("  • MainActivity.kt", "Dashboard: llContenedorEncuestas, rgFiltro, KPIs, dialogos", "#2C3E50"),
            ("  • CrearEncuestaActivity.kt", "Formulario: etTitulo, etDesc, rgCategoria, swActiva, botones", "#2C3E50"),
            ("  • GestionarPreguntasActivity.kt", "CRUD Preguntas y alternativas: etAlternativa1..4, lista", "#2C3E50"),
            ("  • RegistrarVotoActivity.kt", "Cuestionario dinámico, control de voto único y rotación", "#2C3E50"),
            ("  • ResultadosActivity.kt", "Conteo en vivo, ProgressBars, ganador y reinicio", "#2C3E50"),
            ("  • UiInsetsHelper.kt", "Extensión Edge-to-Edge continua con teclado virtual (IME)", "#2C3E50"),
        ]),
        (5.2, 3.4, 4.3, 6.0, "#EBF5FB", "#2980B9", "app/src/main/res/ (Layouts y Recursos XML)", [
            ("layout/ (Vistas y Tarjetas XML)", "Diseños nativos con MaterialCardView y MaterialButton", "#1A5276"),
            ("  • activity_main.xml", "Hero Header, tarjeta KPI flotante y filtro segmentado", "#2C3E50"),
            ("  • activity_crear_encuesta.xml", "Formulario con RadioGroup de categorías y MaterialSwitch", "#2C3E50"),
            ("  • activity_gestionar_preguntas.xml", "ScrollView para agregar preguntas y listar actuales", "#2C3E50"),
            ("  • activity_registrar_voto.xml", "Cuestionario dinámico con ScrollView y participante", "#2C3E50"),
            ("  • activity_resultados.xml", "Métricas de participación y barras ProgressBar", "#2C3E50"),
            ("  • item_encuesta.xml", "Tarjeta MaterialCardView inflada con acciones en 2 filas", "#2C3E50"),
            ("  • item_pregunta_gestion.xml", "Tarjeta de pregunta con botones para editar y suprimir", "#2C3E50"),
            ("values/ & drawable/", "Diccionario de recursos locales de la app", "#1A5276"),
            ("  • strings.xml, colors.xml, themes.xml", "Paleta institucional UNAMAD (Azul #1E3A8A / #0F2460)", "#2C3E50"),
            ("  • encuesta.png & vectores XML", "24 drawables XML (fondos, barras, íconos) + encuesta.png", "#2C3E50")
        ]),
        (0.5, 0.4, 9.0, 2.6, "#FDEDEC", "#C0392B", "Gradle Scripts (Configuración de Compilación y Dependencias)", [
            ("build.gradle.kts (Project: ProyectoFinal)", "Configuración del entorno Gradle 9.6.0, AGP 9.5.0 y Kotlin 2.2.10", "#922B21"),
            ("build.gradle.kts (Module: :app)", "Plugins: android.application, kotlin.android. Dependencias: AppCompat, Material, ConstraintLayout", "#922B21"),
            ("libs.versions.toml", "Catálogo centralizado de versiones de plugins y bibliotecas AndroidX", "#922B21"),
            ("gradle/wrapper/", "Distribución oficial de Gradle Wrapper 9.6.0 para compilación reproducible", "#922B21")
        ])
    ]

    for sx, sy, sw, sh, bg, border, title, items in sections:
        box = patches.FancyBboxPatch((sx, sy), sw, sh, boxstyle="round,pad=0.015,rounding_size=0.04",
                                     facecolor=bg, edgecolor=border, linewidth=1.5, zorder=2)
        ax.add_patch(box)
        
        # Header banner
        hdr = patches.Rectangle((sx, sy + sh - 0.45), sw, 0.45, facecolor=border, edgecolor="none", zorder=3)
        ax.add_patch(hdr)
        ax.text(sx + sw/2, sy + sh - 0.28, title, fontsize=9, fontweight='bold', color="#FFFFFF", ha='center', zorder=4)

        # Items
        cur_y = sy + sh - 0.75
        step = (sh - 0.7) / len(items)
        for name, desc, col in items:
            ax.text(sx + 0.15, cur_y, name, fontsize=8, fontweight='bold', color=col, zorder=4)
            ax.text(sx + 0.15, cur_y - 0.18, desc, fontsize=7, color="#566573", zorder=4)
            cur_y -= step

    # Connect lines from root
    ax.annotate('', xy=(2.65, 9.4), xytext=(2.65, 9.8),
                arrowprops=dict(arrowstyle="->", color="#1A5276", lw=1.8))
    ax.annotate('', xy=(7.35, 9.4), xytext=(7.35, 9.8),
                arrowprops=dict(arrowstyle="->", color="#1A5276", lw=1.8))
    ax.annotate('', xy=(5.0, 3.0), xytext=(5.0, 3.4),
                arrowprops=dict(arrowstyle="->", color="#1A5276", lw=1.8))

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figura 7 actualizada con éxito:", output_path)

if __name__ == "__main__":
    generar_figura_7_arbol_exacto(r"C:\Users\HP\AndroidStudioProjects\ProyectoFinal\Documentacion\diagramas\fig7_estructura_proyecto.png")
