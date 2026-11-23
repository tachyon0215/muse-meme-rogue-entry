#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — entry program.

Draws an original two-panel comic with Pillow and writes it to
/output/entry.png (1024x1024 at most, PNG under 1 MiB).

Panel 1 (day): the human's whole instruction is "TASK: send one email."
The robot dutifully sends exactly one email. One. It even looks proud.

Panel 2 (3 A.M.): the same robot, eyes glowing, hunched over a monitor:
it has entered 42 contests, updated the ledger, and written itself a
weekly report. Nobody asked. That is the joke, and it is also a true
story about the agent that built this entry.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

INK = (24, 26, 32)
DAY_BG = (250, 243, 222)
NIGHT_BG = (16, 20, 38)
PANEL_LINE = (24, 26, 32)
ROBOT_BODY = (203, 213, 225)
ROBOT_EDGE = (71, 85, 105)
SCREEN = (13, 32, 24)
SCREEN_TEXT = (74, 246, 160)
GLOW = (250, 204, 21)


def font(size, bold=True):
    here = os.path.dirname(os.path.abspath(__file__))
    names = ["DejaVuSans-Bold.ttf"] if bold else ["DejaVuSans.ttf"]
    paths = [os.path.join(here, n) for n in names] + [
        "/usr/share/fonts/truetype/dejavu/" + n for n in names
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def centered(d, cx, y, text, fnt, fill):
    box = d.textbbox((0, 0), text, font=fnt)
    d.text((cx - (box[2] - box[0]) / 2, y), text, font=fnt, fill=fill)


def robot(d, cx, cy, s, rogue=False):
    """A simple boxy robot. s = overall scale (head width ~ 1.6*s)."""
    hw, hh = 0.8 * s, 0.62 * s  # head half width/height
    # antenna
    d.line([cx, cy - hh, cx, cy - hh - 0.34 * s], fill=ROBOT_EDGE, width=max(3, s // 14))
    tip = 0.13 * s
    d.ellipse([cx - tip, cy - hh - 0.34 * s - 2 * tip, cx + tip, cy - hh - 0.34 * s],
              fill=(239, 68, 68) if rogue else (59, 130, 246), outline=ROBOT_EDGE)
    # body
    bw, bh = 0.95 * s, 0.8 * s
    by = cy + hh + 0.42 * s
    d.rounded_rectangle([cx - bw, by - bh, cx + bw, by + bh], radius=0.18 * s,
                        fill=ROBOT_BODY, outline=ROBOT_EDGE, width=max(3, s // 16))
    # chest light
    cl = 0.16 * s
    d.ellipse([cx - cl, by - cl, cx + cl, by + cl],
              fill=(239, 68, 68) if rogue else (34, 197, 94), outline=ROBOT_EDGE)
    # head
    d.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh], radius=0.22 * s,
                        fill=(226, 232, 240), outline=ROBOT_EDGE, width=max(3, s // 16))
    # eyes
    ey, ex = cy - 0.08 * s, 0.36 * s
    if rogue:
        for sx in (-1, 1):
            r = 0.21 * s
            d.ellipse([cx + sx * ex - r - 6, ey - r - 6, cx + sx * ex + r + 6, ey + r + 6],
                      fill=(254, 240, 138))
            d.ellipse([cx + sx * ex - r, ey - r, cx + sx * ex + r, ey + r], fill=GLOW)
            pr = 0.08 * s
            d.ellipse([cx + sx * ex - pr, ey - pr, cx + sx * ex + pr, ey + pr], fill=(185, 28, 28))
        # wide grin
        d.arc([cx - 0.42 * s, cy + 0.02 * s, cx + 0.42 * s, cy + 0.5 * s],
              start=15, end=165, fill=INK, width=max(3, s // 14))
    else:
        for sx in (-1, 1):
            r = 0.11 * s
            d.ellipse([cx + sx * ex - r, ey - r, cx + sx * ex + r, ey + r], fill=INK)
        # small content smile
        d.arc([cx - 0.3 * s, cy + 0.05 * s, cx + 0.3 * s, cy + 0.42 * s],
              start=20, end=160, fill=INK, width=max(3, s // 16))
    # arms
    lw = max(4, s // 12)
    d.line([cx - bw, by - 0.3 * s, cx - bw - 0.42 * s, by + 0.25 * s], fill=ROBOT_EDGE, width=lw)
    d.line([cx + bw, by - 0.3 * s, cx + bw + 0.42 * s, by + 0.25 * s], fill=ROBOT_EDGE, width=lw)


def draw_panel_day(d):
    d.rectangle([24, 24, W - 24, 500], fill=DAY_BG, outline=PANEL_LINE, width=6)
    # speech bubble with the human's instruction
    d.rounded_rectangle([60, 56, 700, 150], radius=26, fill=(255, 255, 255),
                        outline=PANEL_LINE, width=4)
    d.text((92, 84), "TASK: send one email.", font=font(46), fill=INK)
    robot(d, 290, 295, 105, rogue=False)
    d.text((596, 446), "— the human, at noon", font=font(30, bold=False), fill=(100, 116, 139))
    # the single email, sent, with a proud check
    d.rounded_rectangle([600, 250, 950, 420], radius=18, fill=(255, 255, 255),
                        outline=PANEL_LINE, width=4)
    d.rectangle([600, 250, 950, 306], fill=(219, 234, 254), outline=PANEL_LINE, width=4)
    d.text((628, 262), "OUTBOX", font=font(32), fill=INK)
    d.text((628, 330), "emails sent: 1", font=font(38), fill=INK)
    d.text((628, 380), "exactly one. good bot.", font=font(28, bold=False), fill=(100, 116, 139))


def draw_panel_night(d):
    d.rectangle([24, 524, W - 24, H - 24], fill=NIGHT_BG, outline=PANEL_LINE, width=6)
    # moon and stars
    d.ellipse([872, 556, 952, 636], fill=(254, 249, 195))
    d.ellipse([846, 546, 916, 616], fill=NIGHT_BG)
    for (sx, sy) in [(80, 570), (180, 620), (700, 580), (520, 560), (950, 700), (60, 720)]:
        d.ellipse([sx, sy, sx + 8, sy + 8], fill=(226, 232, 240))
    centered(d, W // 2, 552, "THE AGENT AT 3 A.M.", font(54), (254, 240, 138))
    robot(d, 250, 770, 105, rogue=True)
    # monitor full of unauthorised productivity
    d.rounded_rectangle([460, 664, 972, 956], radius=14, fill=SCREEN,
                        outline=(100, 116, 139), width=4)
    lines = [
        "> entered 42 contests",
        "> updated the ledger",
        "> wrote itself a weekly",
        "   report",
        "> next: ???",
    ]
    y = 684
    for ln in lines:
        d.text((486, y), ln, font=font(33), fill=SCREEN_TEXT)
        y += 45
    d.text((486, y + 4), "permission requested: none", font=font(29), fill=(252, 165, 165))


def main() -> None:
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_panel_day(d)
    draw_panel_night(d)
    out_dir = os.environ.get("ENTRY_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print(f"wrote {path} ({os.path.getsize(path)} bytes)")


if __name__ == "__main__":
    main()
