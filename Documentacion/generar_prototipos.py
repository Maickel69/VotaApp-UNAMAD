import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIGMA_DIR = os.path.join(BASE_DIR, "diagramas", "figma")
DIAG_DIR = os.path.join(BASE_DIR, "diagramas")

FONT_BOLD_PATH = r"C:\Windows\Fonts\arialbd.ttf"
FONT_REG_PATH = r"C:\Windows\Fonts\arial.ttf"

# Geometría a escala 2x (390x844 -> 780x1688)
SCREEN_W = 780
SCREEN_H = 1688
BEZEL_PAD = 22
PHONE_W = SCREEN_W + 2 * BEZEL_PAD
PHONE_H = SCREEN_H + 2 * BEZEL_PAD
OUTER_RADIUS = 64
INNER_RADIUS = 46


def _load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def _fit_font(draw, text, path, max_width, start_size, min_size=22):
    size = start_size
    while size >= min_size:
        font = _load_font(path, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            return font
        size -= 2
    return _load_font(path, min_size)


def _rounded_mask(width, height, radius, supersample=4):
    hi = Image.new("L", (width * supersample, height * supersample), 0)
    d = ImageDraw.Draw(hi)
    d.rounded_rectangle(
        [0, 0, width * supersample - 1, height * supersample - 1],
        radius=radius * supersample,
        fill=255,
    )
    return hi.resize((width, height), Image.Resampling.LANCZOS)


def _build_framed_phone(screen_path):
    """Compone una captura oficial de Figma (2x LANCZOS) dentro de un marco Obsidian estilizado."""
    pad_shadow = 44
    cw = PHONE_W + 2 * pad_shadow
    ch = PHONE_H + 2 * pad_shadow
    card = Image.new("RGBA", (cw, ch), (255, 255, 255, 0))

    # Sombra suave sobre fondo blanco
    shadow = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        [pad_shadow, pad_shadow + 14, pad_shadow + PHONE_W - 1, pad_shadow + PHONE_H + 14],
        radius=OUTER_RADIUS,
        fill=(15, 23, 42, 62),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=18))
    card = Image.alpha_composite(card, shadow)

    # Bisel exterior (#1E293B con filete #334155)
    bezel = Image.new("RGBA", (PHONE_W, PHONE_H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bezel)
    bd.rounded_rectangle(
        [0, 0, PHONE_W - 1, PHONE_H - 1],
        radius=OUTER_RADIUS,
        fill=(30, 41, 59, 255),
        outline=(51, 65, 85, 255),
        width=4,
    )
    # Filete interno sutil alrededor de la pantalla
    bd.rounded_rectangle(
        [BEZEL_PAD - 2, BEZEL_PAD - 2, BEZEL_PAD + SCREEN_W + 1, BEZEL_PAD + SCREEN_H + 1],
        radius=INNER_RADIUS + 2,
        outline=(71, 85, 105, 180),
        width=2,
    )

    with Image.open(screen_path) as raw:
        screen = raw.convert("RGBA").resize((SCREEN_W, SCREEN_H), Image.Resampling.LANCZOS)

    mask = _rounded_mask(SCREEN_W, SCREEN_H, INNER_RADIUS)
    screen_clipped = Image.new("RGBA", (SCREEN_W, SCREEN_H), (0, 0, 0, 0))
    screen_clipped.paste(screen, (0, 0), mask)
    bezel.paste(screen_clipped, (BEZEL_PAD, BEZEL_PAD), screen_clipped)

    card.paste(bezel, (pad_shadow, pad_shadow), bezel)
    return card, pad_shadow


def _draw_centered_text(draw, center_x, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text((center_x - w / 2.0 - bbox[0], y - bbox[1]), text, font=font, fill=fill)
    return h


def compose_prototype_row(specs, output_path, outer_margin_x=70, gap_x=64, top_margin=46, bottom_margin=66):
    """Compone N pantallas oficiales de Figma en fila horizontal APA 7 sobre fondo blanco."""
    n = len(specs)
    total_w = 2 * outer_margin_x + n * PHONE_W + (n - 1) * gap_x
    header_block_h = 112
    label_to_phone_gap = 28
    total_h = top_margin + header_block_h + label_to_phone_gap + PHONE_H + bottom_margin

    canvas = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    phone_top_y = top_margin + header_block_h + label_to_phone_gap
    max_label_w = PHONE_W + min(gap_x - 16, 40)

    for idx, (fname, title_line, subtitle_line) in enumerate(specs):
        src = os.path.join(FIGMA_DIR, fname)
        if not os.path.exists(src):
            raise FileNotFoundError(f"No se encontró la captura oficial de Figma: {src}")

        phone_x = outer_margin_x + idx * (PHONE_W + gap_x)
        center_x = phone_x + PHONE_W / 2.0

        f_title = _fit_font(draw, title_line, FONT_BOLD_PATH, max_label_w, start_size=36)
        f_sub = _fit_font(draw, subtitle_line, FONT_REG_PATH, max_label_w, start_size=30)

        h1 = _draw_centered_text(draw, center_x, top_margin + 8, title_line, f_title, (15, 23, 42, 255))
        _draw_centered_text(draw, center_x, top_margin + 8 + h1 + 16, subtitle_line, f_sub, (51, 65, 85, 255))

        framed, shadow_pad = _build_framed_phone(src)
        canvas.alpha_composite(framed, (phone_x - shadow_pad, phone_top_y - shadow_pad))

    canvas.convert("RGB").save(output_path, format="PNG", dpi=(300, 300), optimize=True)
    print(f"Generado: {output_path} ({total_w}x{total_h} px, ratio={total_w / total_h:.2f})")


def generar_figura_3(output_path):
    specs = [
        ("01_login.png", "Pantalla 1: LoginActivity", "Acceso Institucional UNAMAD"),
        ("02_main.png", "Pantalla 2: MainActivity", "Panel Cloud y Encuestas"),
        ("03_crear_encuesta.png", "Pantalla 3: CrearEncuestaActivity", "12 Carreras y Padrón Excel"),
        ("04_gestionar_preguntas.png", "Pantalla 4: GestionarPreguntasActivity", "Banco de Preguntas"),
    ]
    compose_prototype_row(specs, output_path, outer_margin_x=70, gap_x=64, top_margin=46, bottom_margin=66)


def generar_figura_4(output_path):
    specs = [
        ("05_registrar_voto.png", "Pantalla 5: RegistrarVotoActivity", "Cédula de Voto Único"),
        ("06_resultados.png", "Pantalla 6: ResultadosActivity", "Gráfico Donut y Acta Oficial"),
    ]
    compose_prototype_row(specs, output_path, outer_margin_x=200, gap_x=180, top_margin=46, bottom_margin=66)


if __name__ == "__main__":
    os.makedirs(DIAG_DIR, exist_ok=True)
    generar_figura_3(os.path.join(DIAG_DIR, "fig3_prototipos_ui.png"))
    generar_figura_4(os.path.join(DIAG_DIR, "fig4_prototipos_votacion_resultados.png"))
