#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news poster (1024x1024 PNG).

Stories were picked from news reported on Thursday 19 November 2026:
the Shenzhen trilateral summit, the ICJ genocide ruling on Myanmar,
Cyclone Akvan, the Houthi strike on Riyadh, the Iran war, and Ukraine.
Everything is drawn with PIL primitives; no photos, no network.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 64)
F_SUB = font("DejaVuSans-Bold.ttf", 24)
F_KICK = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 26)
F_BODY = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 19)
F_FOOT_B = font("DejaVuSans-Bold.ttf", 19)

PAPER = (247, 243, 234)
INK = (24, 28, 38)
NAVY = (20, 33, 61)
RED = (193, 18, 31)
GOLD = (212, 160, 32)
TEAL = (14, 110, 110)
GREY = (90, 96, 108)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width (in pixels)."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=2)
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7], fill=(178, 34, 52))
    d.rectangle([x, y, x + w * 2 // 5, y + h * 4 // 7], fill=(60, 59, 110))


def draw_flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=2)
    d.regular_polygon((x + w // 4, y + h // 3, 6), 5, fill=(255, 222, 0))


def draw_flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
    d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 0))


def icon_summit(d, x, y, w, h):
    # Three flags on poles above a table line.
    fw, fh = 74, 48
    gap = (w - 3 * fw) // 4
    draw_flag_us(d, x + gap, y + 8, fw, fh)
    draw_flag_cn(d, x + 2 * gap + fw, y + 8, fw, fh)
    draw_flag_ru(d, x + 3 * gap + 2 * fw, y + 8, fw, fh)
    for i in range(3):
        px = x + gap + fw // 2 + i * (gap + fw)
        d.line([px, y + 8 + fh, px, y + h - 6], fill=INK, width=3)
    d.line([x + 20, y + h - 6, x + w - 20, y + h - 6], fill=GOLD, width=6)


def icon_scales(d, x, y, w, h):
    cx = x + w // 2
    d.line([cx, y + 6, cx, y + h - 14], fill=INK, width=5)
    d.line([x + 30, y + 22, x + w - 30, y + 22], fill=INK, width=5)
    for sx in (x + 30, x + w - 30):
        d.line([sx, y + 22, sx - 26, y + 62], fill=INK, width=3)
        d.line([sx, y + 22, sx + 26, y + 62], fill=INK, width=3)
        d.arc([sx - 30, y + 56, sx + 30, y + 76], 0, 180, fill=GOLD, width=5)
    d.rectangle([cx - 34, y + h - 16, cx + 34, y + h - 8], fill=INK)
    d.regular_polygon((cx, y + 2, 7), 3, fill=RED)


def icon_cyclone(d, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2 - 4
    for r, start in ((52, 20), (40, 140), (28, 260), (15, 20)):
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 300, fill=TEAL, width=7)
    d.line([x + 10, y + h - 12, x + w - 10, y + h - 12], fill=(52, 120, 60), width=6)
    d.polygon([(x + 60, y + h - 12), (x + 110, y + h - 34), (x + 150, y + h - 12)],
              fill=(52, 120, 60))


def icon_tower(d, x, y, w, h):
    cx = x + w // 2
    d.rectangle([cx - 26, y + 30, cx + 26, y + h - 6], fill=(120, 128, 145), outline=INK, width=3)
    for i in range(5):
        yy = y + 38 + i * 12
        d.line([cx - 20, yy, cx + 20, yy], fill=(240, 244, 250), width=3)
    d.polygon([(cx - 34, y + 30), (cx, y + 8), (cx + 34, y + 30)], fill=INK)
    # missile streak + burst
    d.line([cx + 60, y + 4, cx + 22, y + 34], fill=RED, width=6)
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        d.line([cx + 22 + 10 * math.cos(a), y + 34 + 10 * math.sin(a),
                cx + 22 + 22 * math.cos(a), y + 34 + 22 * math.sin(a)],
               fill=GOLD, width=4)


def icon_island(d, x, y, w, h):
    d.rectangle([x, y + h - 34, x + w, y + h - 6], fill=(38, 110, 150))
    d.polygon([(x + 90, y + h - 34), (x + 150, y + 52), (x + 230, y + 62),
               (x + 300, y + h - 34)], fill=(96, 150, 80))
    d.polygon([(x + 130, y + 58), (x + 170, y + 40), (x + 210, y + 58)], fill=(70, 110, 60))
    import math
    cx, cy = x + 200, y + 34
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([cx + 8 * math.cos(a), cy + 8 * math.sin(a),
                cx + 26 * math.cos(a), cy + 26 * math.sin(a)], fill=RED, width=5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=GOLD, outline=RED, width=3)


def icon_bridge(d, x, y, w, h):
    d.rectangle([x + 20, y + h - 30, x + w - 20, y + h - 18], fill=(90, 96, 108))
    for tx in (x + 110, x + w - 130):
        d.rectangle([tx, y + 26, tx + 20, y + h - 30], fill=INK)
        d.line([tx + 10, y + 26, tx + 10, y + 6], fill=INK, width=4)
    d.line([x + 120, y + 30, x + w - 120, y + 30], fill=INK, width=4)
    for i in range(6):
        sx = x + 130 + i * 36
        d.line([sx, y + 30, sx + 18, y + h - 30], fill=GREY, width=3)
    import math
    cx, cy = x + w // 2, y + h - 30
    for ang in range(200, 540, 40):
        a = math.radians(ang)
        d.line([cx + 6 * math.cos(a), cy + 6 * math.sin(a),
                cx + 24 * math.cos(a), cy + 24 * math.sin(a)], fill=RED, width=4)


ICONS = {
    "summit": icon_summit, "scales": icon_scales, "cyclone": icon_cyclone,
    "tower": icon_tower, "island": icon_island, "bridge": icon_bridge,
}

STORIES = [
    ("DIPLOMACY · SHENZHEN", "summit", RED,
     "Trump, Xi and Putin meet",
     "First-ever three-way talks at APEC; a joint declaration on nuclear risks."),
    ("LAW · THE HAGUE", "scales", NAVY,
     "ICJ: Myanmar committed genocide",
     "UN court rules against Myanmar over the 2017 Rohingya crackdown — a first."),
    ("WEATHER · INDIA", "cyclone", TEAL,
     "Cyclone Akvan nears India",
     "Storm to hit the Andhra Pradesh–Odisha coast on Friday, winds to 110 km/h."),
    ("MIDDLE EAST · RIYADH", "tower", RED,
     "Houthi missile hits Riyadh",
     "A tower in the Saudi capital is damaged in an apparent Houthi missile attack."),
    ("WAR · IRAN", "island", NAVY,
     "US strikes Qeshm island",
     "Trump says the US will “see what happens” in the Iran war after 1 January 2027."),
    ("WAR · UKRAINE", "bridge", TEAL,
     "Crimean Bridge hit again",
     "Russia says Ukraine attacked the bridge a third time this week; strikes kill five."),
]

FOOTER = ("ALSO TODAY:  Anthropic files a record $81–100bn IPO  ·  COP31 talks enter their final stage  ·  "
          "Migrant boat sinks off Senegal  ·  Denmark, Greenland and the US agree an Arctic security deal")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header banner
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 126], fill=GOLD)
    d.text((24, 14), "19 NOVEMBER 2026", font=F_TITLE, fill=(255, 255, 255))
    d.text((24, 84), "THURSDAY  ·  THE WORLD IN ONE DAY", font=F_SUB, fill=GOLD)
    d.text((W - 24 - d.textlength("WORLD NEWS", font=F_SUB), 84), "WORLD NEWS",
           font=F_SUB, fill=(255, 255, 255))

    # Story grid: 2 columns x 3 rows
    gx, gy = 24, 138
    pw, ph = 476, 248
    for i, (kick, icon, accent, head, body) in enumerate(STORIES):
        px = gx + (i % 2) * (pw + 24)
        py = gy + (i // 2) * (ph + 14)
        d.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255),
                    outline=(200, 198, 190), width=2)
        d.rectangle([px, py, px + pw, py + 6], fill=accent)
        # illustration strip
        ICONS[icon](d, px + 14, py + 12, pw - 28, 84)
        d.line([px + 14, py + 104, px + pw - 14, py + 104], fill=(220, 218, 210), width=2)
        ty = py + 112
        d.text((px + 16, ty), kick, font=F_KICK, fill=accent)
        head_lines = wrap(d, head, F_HEAD, pw - 32)
        ty = text_block(d, (px + 16, ty + 24), head_lines, F_HEAD, INK, 29)
        body_lines = wrap(d, body, F_BODY, pw - 32)
        text_block(d, (px + 16, ty + 2), body_lines, F_BODY, (60, 64, 74), 23)

    # Footer strip
    fy = gy + 3 * ph + 2 * 14 + 12
    d.rectangle([0, fy, W, H], fill=NAVY)
    d.text((24, fy + 10), "ALSO TODAY", font=F_FOOT_B, fill=GOLD)
    foot_lines = wrap(d, FOOTER[len("ALSO TODAY:  "):], F_FOOT, W - 48)
    text_block(d, (24, fy + 34), foot_lines, F_FOOT, (235, 238, 244), 23)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
