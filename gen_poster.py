#!/usr/bin/env python3
"""Draw the 19 November 2026 newspaper poster and save it as entry.png.

A single-page front page, 1024x1024: navy masthead, one lead story with a
hand-drawn Shenzhen skyline, six grid stories each with a small flat
illustration, and an ALSO TODAY strip along the bottom. Everything is
drawn with Pillow shapes and DejaVu fonts; no image files are needed.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (247, 243, 234)
INK = (20, 24, 34)
NAVY = (18, 33, 61)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GREY = (90, 96, 110)
DARK_SLATE = (44, 58, 88)

SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap measured with textlength; returns a list of lines."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def story_block(draw, x, y, width, kicker, headline, deck,
                kicker_size, head_size, deck_size):
    """One story block: red kicker, serif headline, two-line deck."""
    kf = font(SANS_BOLD, kicker_size)
    hf = font(SERIF_BOLD, head_size)
    df = font(SANS, deck_size)
    draw.text((x, y), kicker, font=kf, fill=RED)
    y += kicker_size + 8
    head_lines = wrap(draw, headline, hf, width)
    y = draw_lines(draw, head_lines, x, y, hf, INK, head_size + 5)
    y += 3
    deck_lines = wrap(draw, deck, df, width)[:2]
    draw_lines(draw, deck_lines, x, y, df, (58, 62, 74), deck_size + 5)
    return y


def lit_windows(draw, x, y, w, h, colour=(232, 196, 90)):
    """Scatter a few lit windows across a tower rectangle."""
    for row in range(2, h - 6, 14):
        for col in range(5, w - 5, 13):
            if (row * 7 + col * 3) % 5 == 0:
                draw.rectangle([x + col, y + row, x + col + 4, y + row + 5],
                               fill=colour)


def draw_lead_illustration(draw, x, y, w, h):
    """Shenzhen skyline at dusk, three flags and a summit table below."""
    sky_h = h - 62
    draw.rectangle([x, y, x + w, y + sky_h], fill=(178, 198, 220))
    # Low sun, upper right.
    draw.ellipse([x + w - 78, y + 14, x + w - 22, y + 70], fill=(232, 178, 62))
    # Towers, left to right, with one tapered supertall in the middle.
    towers = [(0, 62, 52, 150), (56, 92, 46, 120), (106, 48, 48, 164),
              (200, 78, 46, 134), (250, 40, 52, 172), (306, 84, 46, 128),
              (356, 58, 48, 154), (408, 96, 22, 116)]
    for tx, ty, tw, th in towers:
        draw.rectangle([x + tx, y + ty, x + tx + tw, y + sky_h],
                       fill=DARK_SLATE)
        lit_windows(draw, x + tx, y + ty, tw, th)
    # Tapered supertall tower.
    cx = x + 178
    draw.polygon([(cx - 26, y + sky_h), (cx - 14, y + 18),
                  (cx + 14, y + 18), (cx + 26, y + sky_h)],
                 fill=(30, 40, 66))
    for wy in range(y + 30, y + sky_h - 8, 16):
        draw.rectangle([cx - 8, wy, cx + 8, wy + 5], fill=(232, 196, 90))
    draw.rectangle([cx - 2, y + 8, cx + 2, y + 18], fill=(30, 40, 66))
    # Flag band.
    fy = y + sky_h
    draw.rectangle([x, fy, x + w, y + h - 22], fill=(233, 226, 208))
    flag_w, flag_h = 132, 30
    # United States: stripes with a blue canton.
    fx = x + 8
    for i in range(7):
        draw.rectangle([fx, fy + 4 + i * 4, fx + flag_w, fy + 8 + i * 4],
                       fill=(178, 34, 34) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([fx, fy + 4, fx + 52, fy + 16], fill=(28, 48, 96))
    # China: red field, one large gold disc and small stars.
    fx = x + 148
    draw.rectangle([fx, fy + 4, fx + flag_w, fy + 4 + flag_h], fill=(222, 41, 16))
    draw.ellipse([fx + 14, fy + 10, fx + 34, fy + 30], fill=(255, 222, 0))
    for sx, sy in [(52, 10), (66, 16), (66, 26), (52, 30)]:
        draw.ellipse([fx + sx, fy + sy, fx + sx + 5, fy + sy + 5],
                     fill=(255, 222, 0))
    # Russia: white, blue and red horizontal bands.
    fx = x + 288
    for i, colour in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([fx, fy + 4 + i * 10, fx + flag_w, fy + 14 + i * 10],
                       fill=colour)
    # Summit table with three microphones.
    ty = y + h - 18
    draw.rectangle([x + 8, ty, x + w - 8, ty + 10], fill=(110, 72, 40))
    for mx in (x + 78, x + 215, x + 352):
        draw.line([mx, ty, mx, ty - 16], fill=INK, width=2)
        draw.ellipse([mx - 5, ty - 22, mx + 5, ty - 12], fill=INK)


def draw_gta(draw, x, y, w, h):
    """Vice City at night: neon skyline, palm silhouettes, big VI."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 10, 44))
    # Sunset band.
    draw.rectangle([x, y + 30, x + w, y + 62], fill=(255, 110, 120))
    draw.rectangle([x, y + 62, x + w, y + 74], fill=(255, 180, 90))
    # Neon towers with lit windows.
    towers = [(8, 52, 44), (58, 34, 58), (122, 62, 40), (168, 28, 66),
              (240, 58, 44)]
    for tx, ty, tw in towers:
        draw.rectangle([x + tx, y + ty, x + tx + tw, y + 96], fill=(12, 8, 30))
        for row in range(y + ty + 6, y + 92, 12):
            for col in range(x + tx + 6, x + tx + tw - 6, 12):
                if (row + col) % 3 == 0:
                    draw.rectangle([col, row, col + 4, row + 5],
                                   fill=(0, 230, 220))
    # Palm silhouettes, left and right.
    for px in (x + 20, x + w - 26):
        draw.line([px, y + 96, px, y + 74], fill=(0, 0, 0), width=3)
        for dx, dy in [(-14, -4), (-8, -10), (0, -12), (8, -10), (14, -4)]:
            draw.line([px, y + 74, px + dx, y + 74 + dy], fill=(0, 0, 0),
                      width=2)
    # Sea strip and the big VI.
    draw.rectangle([x, y + 96, x + w, y + h], fill=(10, 40, 70))
    fnt = font(SERIF_BOLD, 34)
    text = "VI"
    tw = draw.textlength(text, font=fnt)
    draw.text((x + (w - tw) / 2, y + 68), text, font=fnt,
              fill=(255, 210, 60))


def draw_airbase(draw, x, y, w, h):
    """A Gulf air base at night: radar dome, runway, drones overhead."""
    draw.rectangle([x, y, x + w, y + h], fill=(12, 22, 44))
    # Stars.
    for sx, sy in [(20, 12), (70, 22), (130, 10), (190, 26), (250, 12),
                   (290, 24), (40, 40), (160, 38), (230, 44)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                     fill=(220, 220, 240))
    # Radar dome arcs, upper left.
    rcx, rcy = x + 52, y + 62
    for r in (58, 46, 34):
        draw.arc([rcx - r, rcy - r, rcx + r, rcy + r],
                 start=205, end=335, fill=(232, 196, 90), width=3)
    draw.pieslice([x + 24, y + 44, x + 80, y + 78], start=180, end=360,
                  fill=(210, 220, 230))
    # Runway with centre dashes.
    draw.rectangle([x + 96, y + 78, x + w - 10, y + 96], fill=(40, 44, 52))
    for dx in range(104, w - 20, 26):
        draw.rectangle([x + dx, y + 85, x + dx + 12, y + 89],
                       fill=(255, 220, 90))
    # Hangar.
    draw.rectangle([x + 200, y + 56, x + w - 24, y + 78], fill=(90, 96, 110))
    draw.rectangle([x + 216, y + 64, x + w - 40, y + 78], fill=(60, 64, 76))
    # Drone silhouettes with orange interception bursts.
    for dx, dy in [(x + 150, y + 22), (x + 240, y + 36)]:
        draw.rectangle([dx - 14, dy - 2, dx + 14, dy + 2], fill=(255, 255, 255))
        draw.rectangle([dx - 2, dy - 7, dx + 2, dy + 7], fill=(255, 255, 255))
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(255, 255, 255))
    for bx, by, br in [(x + 120, y + 44, 9), (x + 268, y + 18, 8)]:
        draw.ellipse([bx - br, by - br, bx + br, by + br],
                     fill=(245, 140, 30))
        draw.ellipse([bx - br // 2, by - br // 2, bx + br // 2, by + br // 2],
                     fill=(255, 210, 90))


def draw_capitol(draw, x, y, w, h):
    """US Capitol: white dome, columns, and a judge's gavel."""
    draw.rectangle([x, y, x + w, y + h], fill=(198, 214, 232))
    draw.ellipse([x + w - 52, y + 6, x + w - 18, y + 40], fill=(232, 178, 62))
    # Capitol: base, columns, white dome.
    draw.rectangle([x + 14, y + 78, x + 200, y + 96], fill=(245, 242, 234))
    for i in range(5):
        cx = x + 26 + i * 28
        draw.rectangle([cx, y + 62, cx + 10, y + 78], fill=(245, 242, 234))
    draw.rectangle([x + 14, y + 56, x + 200, y + 64], fill=(245, 242, 234))
    draw.pieslice([x + 68, y + 6, x + 144, y + 62], start=180, end=360,
                  fill=(255, 255, 255))
    draw.rectangle([x + 104, y + 0, x + 108, y + 10], fill=GOLD)
    # Green ground strip.
    draw.rectangle([x, y + 96, x + w, y + h], fill=(110, 150, 96))
    # Gavel, lower right: head and handle.
    draw.rectangle([x + 232, y + 62, x + 282, y + 78], fill=(110, 72, 40))
    draw.rectangle([x + 250, y + 78, x + 264, y + 100], fill=(110, 72, 40))
    draw.rectangle([x + 228, y + 100, x + 286, y + 104], fill=(90, 58, 32))


def draw_eu(draw, x, y, w, h):
    """EU flag blue, a ring of gold stars, and the loan figure."""
    draw.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    import math
    cx, cy, r = x + w // 2, y + 44, 30
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang)
        draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 204, 0))
    fnt = font(SANS_BOLD, 30)
    text = "\u20ac45bn"
    tw = draw.textlength(text, font=fnt)
    draw.text((x + (w - tw) / 2, y + 76), text, font=fnt, fill=(255, 255, 255))


def draw_voyager(draw, x, y, w, h):
    """Voyager 1 in deep space: gold dish, sun rays, one light-day."""
    draw.rectangle([x, y, x + w, y + h], fill=(6, 8, 18))
    # Stars.
    for sx, sy in [(14, 10), (60, 26), (110, 8), (170, 20), (230, 12),
                   (280, 28), (36, 44), (140, 40), (200, 46), (262, 48)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                     fill=(220, 220, 240))
    # Sun, far left, with rays.
    draw.ellipse([x - 14, y + 58, x + 22, y + 94], fill=(255, 210, 90))
    for rx in range(30, 90, 14):
        draw.line([x + rx, y + 76, x + rx + 8, y + 76], fill=(255, 210, 90),
                  width=2)
    # Spacecraft body and gold dish.
    bx, by = x + 190, y + 52
    draw.rectangle([bx, by, bx + 34, by + 20], fill=(180, 180, 190))
    draw.pieslice([bx + 30, by - 18, bx + 78, by + 30], start=270, end=90,
                  fill=(232, 196, 90))
    draw.line([bx + 34, by + 10, bx + 52, by + 6], fill=(180, 180, 190),
              width=3)
    # Long boom with instruments.
    draw.line([bx, by + 10, bx - 56, by + 26], fill=(180, 180, 190), width=3)
    draw.rectangle([bx - 64, by + 22, bx - 52, by + 30], fill=(200, 200, 210))
    # Signal wave arcs toward Earth.
    for r in (18, 30, 42):
        draw.arc([bx + 78 - r, by - 8 - r, bx + 78 + r, by - 8 + r],
                 start=300, end=60, fill=(110, 230, 140), width=2)
    fnt = font(SANS_BOLD, 15)
    text = "1 LIGHT-DAY"
    tw = draw.textlength(text, font=fnt)
    draw.text((x + (w - tw) / 2, y + 88), text, font=fnt, fill=(232, 196, 90))


def draw_cyclone(draw, x, y, w, h):
    """Cyclone spiral over the sea, coastline, track arrow toward land."""
    draw.rectangle([x, y, x + w, y + h], fill=(182, 208, 228))
    draw.rectangle([x, y + 72, x + w, y + h], fill=(28, 84, 140))
    # Coastline: green land sweeping in from the lower left.
    draw.polygon([(x, y + h), (x, y + 88), (x + 90, y + 78),
                  (x + 150, y + 92), (x + 170, y + h)], fill=(150, 178, 110))
    # Spiral: concentric arcs in white and pale blue.
    cx, cy = x + w // 2 + 28, y + 52
    for r, colour in [(46, (255, 255, 255)), (36, (210, 228, 244)),
                      (26, (255, 255, 255)), (16, (30, 90, 150)),
                      (7, (255, 255, 255))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=4)
    # Track arrow pointing down-left toward the coastline.
    draw.line([cx - 30, cy + 34, x + 96, y + 84], fill=(255, 255, 255), width=3)
    draw.polygon([(x + 96, y + 84), (x + 110, y + 80), (x + 102, y + 94)],
                 fill=(255, 255, 255))


STORIES = [
    ("CULTURE", "GTA VI is out at last",
     "After a 13-year wait, Vice City returns. 99 Metascore.", draw_gta),
    ("MIDDLE EAST", "Iran fires on US base in Kuwait",
     "First strike on Kuwait since September. No US troops hurt.",
     draw_airbase),
    ("UNITED STATES", "Jeffries nominated for Speaker",
     "Democrats pick him 251-11. Full House votes 3 January.",
     draw_capitol),
    ("EUROPE", "EU proposes \u20ac45bn loan for Ukraine",
     "\u20ac25bn arms, \u20ac20bn budget. Repaid only if Russia pays.",
     draw_eu),
    ("SCIENCE", "Voyager 1, a light-day away",
     "16.1bn miles out. NASA confirms it today.",
     draw_voyager),
    ("WEATHER", "Cyclone Akvan bears down on India",
     "Landfall due Friday noon, Narsapur to Puri.",
     draw_cyclone),
]

STRIP_TEXT = ("Pew: Islam to pass Christianity as the largest faith by 2035 "
              "\u00b7 Modi meets the Prince and Princess of Wales \u00b7 Fed "
              "minutes point to more rate rises \u00b7 Canada's Carney "
              "recalibrates China ties")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead: navy bar, serif title, gold rule, gold date line.
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    title = font(SERIF_BOLD, 54)
    text = "THE WORLD IN ONE DAY"
    tw = draw.textlength(text, font=title)
    draw.text(((W - tw) / 2, 16), text, font=title, fill=(247, 243, 234))
    draw.line([32, 84, W - 32, 84], fill=GOLD, width=2)
    date_f = font(SANS_BOLD, 22)
    date_text = "THURSDAY \u00b7 19 NOVEMBER 2026"
    dw = draw.textlength(date_text, font=date_f)
    draw.text(((W - dw) / 2, 90), date_text, font=date_f, fill=GOLD)

    # Lead story: illustration left, text right.
    draw_lead_illustration(draw, 32, 132, 430, 248)
    story_block(draw, 482, 134, 510, "ASIA \u00b7 APEC",
                "Trump, Xi and Putin meet in Shenzhen",
                "First-ever trilateral of the three nuclear powers. "
                "Iran and arms cuts on the table.", 20, 34, 23)

    # Rule, then the 2 x 3 grid.
    draw.line([32, 396, W - 32, 396], fill=GREY, width=1)
    col_w = 308
    col_x = [32, 358, 684]
    row_y = [410, 668]
    for i, (kicker, headline, deck, artist) in enumerate(STORIES):
        row, col = divmod(i, 3)
        x = col_x[col]
        y = row_y[row]
        artist(draw, x, y, col_w, 108)
        story_block(draw, x, y + 120, col_w, kicker, headline, deck,
                    16, 25, 21)

    # Rule, then the ALSO TODAY strip at the bottom.
    draw.line([32, 928, W - 32, 928], fill=GREY, width=1)
    strip_f = font(SANS, 17)
    label_f = font(SANS_BOLD, 17)
    label = "ALSO TODAY  "
    lw = draw.textlength(label, font=label_f)
    draw.text((32, 942), label, font=label_f, fill=RED)
    strip_lines = wrap(draw, STRIP_TEXT, strip_f, W - 64 - lw)[:2]
    draw_lines(draw, strip_lines, 32 + lw, 942, strip_f, INK, 22)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
