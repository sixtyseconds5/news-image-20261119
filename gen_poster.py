#!/usr/bin/env python3
"""Draw "The World in One Day" -- Thursday, 19 November 2026.

A single-page newspaper front page, 1024x1024, drawn entirely with
Pillow primitives.  Every picture on the page is a flat illustration
built from rectangles, ellipses, polygons and arcs -- no photos and
no downloaded art.

The page is data driven: the stories live in STORIES below and one
generic card painter lays them out, so adding a story is just adding
a dict.  The lead story gets its own larger treatment up top.

Run:  python3 gen_poster.py        # writes entry.png next to this file
"""

from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE = 1024
MARGIN = 16
GUTTER = 12

PAPER = (247, 241, 227)
INK = (24, 24, 24)
NAVY = (15, 35, 64)
NAVY_DARK = (11, 27, 50)
RED = (176, 30, 40)
GOLD = (217, 164, 65)
SLATE = (68, 78, 92)
RULE = (120, 110, 95)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def pick_font(size: int, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont:
    """Return a DejaVu font at the requested size and weight."""
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def split_lines(canvas: ImageDraw.ImageDraw, text: str,
                font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        current = ""
        for word in paragraph.split():
            trial = word if not current else current + " " + word
            if canvas.textlength(trial, font=font) <= max_width or not current:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def put_text(canvas: ImageDraw.ImageDraw, x: int, y: int, text: str,
             font: ImageFont.FreeTypeFont, fill, max_width: int,
             leading: int | None = None) -> int:
    """Draw wrapped text starting at (x, y); return the y below it."""
    if leading is None:
        leading = font.size + 6
    for line in split_lines(canvas, text, font, max_width):
        canvas.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories

LEAD = {
    "kicker": "ASIA  ·  APEC",
    "headline": "Trump, Xi and Putin meet in Shenzhen",
    "deck": (
        "First-ever trilateral of the three leaders, on the APEC "
        "sidelines in Shenzhen on 19 Nov; Iran and nuclear arms cuts "
        "on the table, Ukraine off it per US officials."
    ),
}

STORIES = [
    {
        "kind": "gta",
        "kicker": "CULTURE",
        "headline": "GTA VI is out at last",
        "deck": "Launches 19 Nov on PS5/Xbox at midnight local; "
                "99 Metascore; 8 Game Awards nominations.",
    },
    {
        "kind": "kuwait",
        "kicker": "MIDDLE EAST",
        "headline": "Iran fires on US base in Kuwait",
        "deck": "Overnight 18 Nov, Iran hit US sites at Ali Al Salem "
                "Air Base; drones intercepted; no US personnel hurt.",
    },
    {
        "kind": "speaker",
        "kicker": "UNITED STATES",
        "headline": "Jeffries nominated for Speaker",
        "deck": "House Democrats picked Hakeem Jeffries 251\u201311 on "
                "18 Nov; first Black Speaker if elected; House votes "
                "3 January.",
    },
    {
        "kind": "eu",
        "kicker": "EUROPE",
        "headline": "EU proposes \u20ac45bn loan for Ukraine",
        "deck": "Proposed 18 Nov: \u20ac25bn military, \u20ac20bn budget; "
                "repaid only after Russia pays reparations.",
    },
    {
        "kind": "voyager",
        "kicker": "SCIENCE",
        "headline": "Voyager 1, a light-day away",
        "deck": "Crossed one light-day (16.1bn miles) at 05:16 EST on "
                "18 Nov; NASA confirms at noon EST on 19 Nov.",
    },
    {
        "kind": "cyclone",
        "kicker": "WEATHER",
        "headline": "Cyclone Akvan bears down on India",
        "deck": "Severe storm, landfall due noon Fri 20 Nov between "
                "Narsapur and Puri; red alerts, schools shut.",
    },
]

ALSO_TODAY = (
    "Pew (18 Nov report): Islam to pass Christianity as the largest faith "
    "by 2035  \u00b7  Modi meets the Prince and Princess of Wales  \u00b7  "
    "Fed minutes point to more rate rises  \u00b7  Canada's Carney "
    "recalibrates China ties."
)


# ------------------------------------------------------- lead illustration

def paint_shenzhen(canvas: ImageDraw.ImageDraw, x: int, y: int,
                   w: int, h: int) -> None:
    """Shenzhen skyline at dusk, with three small flags below it."""
    canvas.rectangle([x, y, x + w, y + h], fill=(178, 205, 226))
    # low sun, top right
    canvas.ellipse([x + w - 78, y + 18, x + w - 18, y + 78], fill=(240, 178, 48))
    # towers: (offset, width, height)
    towers = [(0, 52, 150), (56, 44, 110), (104, 46, 170), (154, 38, 95),
              (196, 50, 185), (250, 44, 120), (298, 48, 165), (350, 46, 105),
              (400, 52, 145)]
    for off, tw, th in towers:
        top = y + h - 58 - th
        canvas.rectangle([x + off, top, x + off + tw, y + h - 58],
                         fill=NAVY_DARK)
        # a few lit windows, fixed pattern so output is deterministic
        for row in range(3, th // 16):
            for col in range(2):
                wx = x + off + 8 + col * 18
                wy = top + row * 16
                if (row * 7 + col * 3 + off) % 4 == 0:
                    canvas.rectangle([wx, wy, wx + 6, wy + 8],
                                     fill=(240, 200, 90))
    # tall central spire
    canvas.polygon([(x + 196, y + h - 58 - 185), (x + 206, y + 12),
                    (x + 216, y + h - 58 - 185)], fill=NAVY_DARK)
    # ground strip with the three flags
    canvas.rectangle([x, y + h - 58, x + w, y + h], fill=(238, 232, 214))
    flag_y = y + h - 48
    flag_h = 30
    thirds = w // 3
    # United States: stripes + blue canton
    fx = x + 8
    for i in range(7):
        colour = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        canvas.rectangle([fx, flag_y + i * 4, fx + thirds - 16,
                          flag_y + i * 4 + 4], fill=colour)
    canvas.rectangle([fx, flag_y, fx + 52, flag_y + 16], fill=(30, 58, 110))
    # China: red field, one large star + small stars as dots
    fx = x + thirds + 8
    canvas.rectangle([fx, flag_y, fx + thirds - 16, flag_y + flag_h],
                     fill=(222, 41, 16))
    canvas.ellipse([fx + 10, flag_y + 7, fx + 24, flag_y + 21],
                   fill=(255, 222, 0))
    for sx, sy in [(38, 6), (48, 12), (48, 22), (38, 26)]:
        canvas.ellipse([fx + sx, flag_y + sy, fx + sx + 5, flag_y + sy + 5],
                       fill=(255, 222, 0))
    # Russia: white / blue / red horizontal bands
    fx = x + 2 * thirds + 8
    for i, colour in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        canvas.rectangle([fx, flag_y + i * 10, fx + thirds - 16,
                          flag_y + (i + 1) * 10], fill=colour)
    # thin gold rule under the flags
    canvas.rectangle([x, y + h - 8, x + w, y + h - 2], fill=GOLD)


# ------------------------------------------------------- grid illustrations

def paint_gta(canvas: ImageDraw.ImageDraw, x: int, y: int,
              w: int, h: int) -> None:
    """Vice City dusk: pink-orange sky, dark towers, a big gold VI."""
    canvas.rectangle([x, y, x + w, y + h], fill=(232, 110, 120))
    canvas.rectangle([x, y + h - 34, x + w, y + h], fill=(24, 32, 54))
    canvas.ellipse([x + w - 62, y + 8, x + w - 18, y + 52], fill=(250, 190, 80))
    for bx, bw, bh in [(0, 58, 40), (64, 40, 50), (110, 66, 34),
                        (182, 46, 46), (234, 56, 32), (292, 30, 42)]:
        canvas.rectangle([x + bx, y + h - 34 - bh, x + bx + bw, y + h - 34],
                         fill=(28, 22, 48))
    # lit windows on the tallest block
    for r in range(3):
        for c in range(3):
            canvas.rectangle([x + 70 + c * 11, y + h - 34 - 48 + r * 13,
                              x + 76 + c * 11, y + h - 34 - 42 + r * 13],
                             fill=(64, 220, 200))
    big = pick_font(46, bold=True, serif=True)
    canvas.text((x + w // 2 - 8, y + h - 52), "VI", font=big, fill=GOLD)


def paint_kuwait(canvas: ImageDraw.ImageDraw, x: int, y: int,
                 w: int, h: int) -> None:
    """Night over the base: radar arcs, runway lights, a drone."""
    canvas.rectangle([x, y, x + w, y + h], fill=(16, 24, 44))
    for sx, sy in [(30, 14), (90, 26), (150, 10), (210, 30), (270, 16),
                    (60, 48), (180, 52), (250, 46)]:
        canvas.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                       fill=(255, 255, 255))
    # radar arcs, top left
    for r in range(18, 66, 16):
        canvas.arc([x + 18, y + 6, x + 18 + 2 * r, y + 6 + 2 * r],
                   start=270, end=360, fill=(240, 200, 90), width=3)
    canvas.ellipse([x + 118, y + 52, x + 138, y + 72], fill=(240, 170, 60))
    # hangar + runway, anchored to the bottom of the frame
    canvas.rectangle([x + 190, y + h - 26, x + 258, y + h - 2],
                     fill=(70, 80, 100))
    canvas.rectangle([x + 14, y + h - 12, x + w - 14, y + h],
                     fill=(40, 48, 66))
    for i in range(7):
        canvas.rectangle([x + 24 + i * 42, y + h - 8, x + 40 + i * 42,
                          y + h - 4], fill=(240, 200, 90))
    # small drone silhouette, centre right
    canvas.polygon([(x + 236, y + 30), (x + 268, y + 30), (x + 252, y + 40)],
                   fill=(200, 205, 215))
    canvas.rectangle([x + 228, y + 28, x + 276, y + 32], fill=(200, 205, 215))


def paint_speaker(canvas: ImageDraw.ImageDraw, x: int, y: int,
                  w: int, h: int) -> None:
    """The Capitol: white dome and wings on a pale sky, green lawn."""
    canvas.rectangle([x, y, x + w, y + h], fill=(196, 216, 232))
    canvas.ellipse([x + w - 56, y + 10, x + w - 16, y + 50], fill=(240, 178, 48))
    # dome
    canvas.pieslice([x + 118, y + 6, x + 202, y + 62], start=180, end=360,
                    fill=(255, 255, 255))
    canvas.rectangle([x + 150, y + 2, x + 170, y + 14], fill=(255, 255, 255))
    canvas.rectangle([x + 158, y - 2, x + 162, y + 4], fill=GOLD)
    # wings
    canvas.rectangle([x + 22, y + 52, x + 118, y + 78], fill=(255, 255, 255))
    canvas.rectangle([x + 202, y + 52, x + 298, y + 78], fill=(255, 255, 255))
    for wx in range(34, 112, 18):
        canvas.rectangle([x + wx, y + 58, x + wx + 9, y + 70],
                         fill=(178, 205, 226))
    for wx in range(214, 292, 18):
        canvas.rectangle([x + wx, y + 58, x + wx + 9, y + 70],
                         fill=(178, 205, 226))
    # lawn + a small podium at the right, inside the frame
    canvas.rectangle([x, y + 78, x + w, y + h], fill=(110, 168, 96))
    canvas.rectangle([x + 258, y + 58, x + 306, y + 66], fill=(120, 72, 32))
    canvas.rectangle([x + 278, y + 66, x + 286, y + h], fill=(120, 72, 32))


def paint_eu(canvas: ImageDraw.ImageDraw, x: int, y: int,
             w: int, h: int) -> None:
    """EU blue field, a ring of twelve gold stars, and the euro figure."""
    canvas.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    # small star ring in the upper half only, clear of the figure below
    cx, cy = x + w // 2, y + 26
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        sx = cx + int(22 * math.cos(angle))
        sy = cy + int(22 * math.sin(angle))
        canvas.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 204, 0))
    amount = pick_font(28, bold=True)
    label = "\u20ac45bn"
    tw = canvas.textlength(label, font=amount)
    canvas.text((x + (w - tw) / 2, y + h - 30), label, font=amount,
                fill=(255, 255, 255))


def paint_voyager(canvas: ImageDraw.ImageDraw, x: int, y: int,
                  w: int, h: int) -> None:
    """Deep space: stars, the probe's dish, and a gold sun at left."""
    canvas.rectangle([x, y, x + w, y + h], fill=(8, 10, 18))
    for sx, sy in [(24, 12), (70, 30), (120, 10), (180, 26), (240, 14),
                    (300, 34), (50, 56), (150, 48), (260, 58), (200, 8)]:
        canvas.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                       fill=(255, 255, 255))
    # gold sun, kept inside this card's own bounds
    canvas.ellipse([x + 2, y + h // 2 - 16, x + 34, y + h // 2 + 16],
                   fill=(240, 190, 60))
    # signal dashes from the sun to the probe
    for i in range(6):
        dx = x + 44 + i * 17
        canvas.rectangle([dx, y + h // 2 - 1, dx + 10, y + h // 2 + 1],
                         fill=(240, 200, 90))
    # probe body + dish
    canvas.rectangle([x + 168, y + h // 2 - 8, x + 206, y + h // 2 + 8],
                     fill=(180, 186, 196))
    canvas.pieslice([x + 206, y + h // 2 - 26, x + 252, y + h // 2 + 26],
                    start=270, end=90, fill=(240, 200, 90))
    canvas.line([x + 206, y + h // 2, x + 168, y + h // 2],
                fill=(220, 220, 220), width=2)
    tag = pick_font(13, bold=True)
    canvas.text((x + 128, y + h - 24), "1 LIGHT-DAY", font=tag,
                fill=(240, 200, 90))


def paint_cyclone(canvas: ImageDraw.ImageDraw, x: int, y: int,
                  w: int, h: int) -> None:
    """A spiral storm over a blue sea and a green coastline."""
    canvas.rectangle([x, y, x + w, y + h], fill=(168, 198, 226))
    canvas.rectangle([x, y + h - 30, x + w, y + h], fill=(28, 84, 150))
    # green headland, bottom left
    canvas.polygon([(x, y + h), (x, y + h - 26), (x + 120, y + h - 18),
                    (x + 150, y + h)], fill=(110, 168, 96))
    # spiral: concentric arcs shrinking toward the centre, inside frame
    cx, cy = x + w - 78, y + 42
    for r, start in [(40, 20), (30, 110), (20, 200), (12, 290)]:
        canvas.arc([cx - r, cy - r, cx + r, cy + r], start=start,
                   end=start + 260, fill=(255, 255, 255), width=5)
    canvas.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    # rain streaks under the spiral, inside the frame
    for i in range(5):
        rx = x + 170 + i * 26
        canvas.line([rx, y + 66, rx - 6, y + 80], fill=(255, 255, 255),
                    width=2)


PAINTERS = {
    "gta": paint_gta,
    "kuwait": paint_kuwait,
    "speaker": paint_speaker,
    "eu": paint_eu,
    "voyager": paint_voyager,
    "cyclone": paint_cyclone,
}


# ------------------------------------------------------------------- page

def draw_masthead(canvas: ImageDraw.ImageDraw) -> None:
    canvas.rectangle([0, 0, PAGE, 118], fill=NAVY)
    title = pick_font(58, bold=True, serif=True)
    text = "THE WORLD IN ONE DAY"
    tw = canvas.textlength(text, font=title)
    canvas.text(((PAGE - tw) / 2, 14), text, font=title, fill=(255, 255, 255))
    canvas.line([MARGIN, 92, PAGE - MARGIN, 92], fill=GOLD, width=2)
    date_font = pick_font(22, bold=True)
    date_text = "THURSDAY  \u00b7  19 NOVEMBER 2026"
    tw = canvas.textlength(date_text, font=date_font)
    canvas.text(((PAGE - tw) / 2, 96), date_text, font=date_font, fill=GOLD)


def draw_lead(canvas: ImageDraw.ImageDraw) -> None:
    top = 132
    pic_w, pic_h = 470, 252
    paint_shenzhen(canvas, MARGIN, top, pic_w, pic_h)
    tx = MARGIN + pic_w + 22
    tw = PAGE - MARGIN - tx
    y = top + 2
    y = put_text(canvas, tx, y, LEAD["kicker"], pick_font(19, bold=True),
                 RED, tw, leading=24)
    y += 4
    y = put_text(canvas, tx, y, LEAD["headline"],
                 pick_font(34, bold=True, serif=True), INK, tw, leading=40)
    y += 6
    put_text(canvas, tx, y, LEAD["deck"], pick_font(19), SLATE, tw,
             leading=26)
    canvas.line([MARGIN, 404, PAGE - MARGIN, 404], fill=RULE, width=1)


def draw_card(canvas: ImageDraw.ImageDraw, story: dict,
              x: int, y: int, w: int) -> None:
    # Shorter picture + tighter type so a 3-line deck ends well clear
    # of the next row's picture (the first render overflowed here).
    pic_h = 84
    PAINTERS[story["kind"]](canvas, x, y, w, pic_h)
    ty = y + pic_h + 8
    ty = put_text(canvas, x, ty, story["kicker"], pick_font(15, bold=True),
                  RED, w, leading=18)
    ty += 2
    ty = put_text(canvas, x, ty, story["headline"],
                  pick_font(21, bold=True, serif=True), INK, w, leading=25)
    ty += 3
    put_text(canvas, x, ty, story["deck"], pick_font(15), SLATE, w,
             leading=19)


def draw_also_today(canvas: ImageDraw.ImageDraw) -> None:
    top = 916
    canvas.line([MARGIN, top, PAGE - MARGIN, top], fill=RULE, width=1)
    label_font = pick_font(17, bold=True)
    body_font = pick_font(17)
    label = "ALSO TODAY  "
    lw = canvas.textlength(label, font=label_font)
    canvas.text((MARGIN, top + 12), label, font=label_font, fill=RED)
    put_text(canvas, MARGIN + int(lw), top + 12, ALSO_TODAY, body_font,
             INK, PAGE - 2 * MARGIN - int(lw), leading=23)


def build_poster() -> Image.Image:
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    canvas = ImageDraw.Draw(page)
    draw_masthead(canvas)
    draw_lead(canvas)
    card_w = (PAGE - 2 * MARGIN - 2 * GUTTER) // 3
    for row in range(2):
        for col in range(3):
            story = STORIES[row * 3 + col]
            x = MARGIN + col * (card_w + GUTTER)
            y = 414 + row * 238
            draw_card(canvas, story, x, y, card_w)
    draw_also_today(canvas)
    return page


def main() -> None:
    poster = build_poster()
    poster.save(OUT_PATH, format="PNG", optimize=True)
    print(f"wrote {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes)")


if __name__ == "__main__":
    main()
