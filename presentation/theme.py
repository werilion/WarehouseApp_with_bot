# -*- coding: utf-8 -*-
"""Дизайн-система и помощники для сборки презентации (ReportLab)."""
import os
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# ---------- шрифты ----------
pdfmetrics.registerFont(TTFont("PTSans", os.path.join(FONT_DIR, "PTSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("PTSans-Bold", os.path.join(FONT_DIR, "PTSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("PTSans-Italic", os.path.join(FONT_DIR, "PTSans-Italic.ttf")))
pdfmetrics.registerFontFamily(
    "PTSans", normal="PTSans", bold="PTSans-Bold",
    italic="PTSans-Italic", boldItalic="PTSans-Bold",
)
FONT = "PTSans"
FONT_B = "PTSans-Bold"
FONT_I = "PTSans-Italic"

# ---------- палитра ----------
NAVY = HexColor("#122033")
NAVY_2 = HexColor("#1B3049")
NAVY_3 = HexColor("#253D5B")
BLUE = HexColor("#2C6FB0")
BLUE_L = HexColor("#5B9BD5")
BLUE_PALE = HexColor("#EAF2FA")
ORANGE = HexColor("#D97E38")
ORANGE_PALE = HexColor("#FBF0E6")
GREEN = HexColor("#27AE60")
GREEN_PALE = HexColor("#E9F7EF")
RED = HexColor("#D9534F")
RED_PALE = HexColor("#FBEAEA")
YELLOW = HexColor("#F2B544")
TEXT = HexColor("#1B2638")
MUTED = HexColor("#6D7C90")
MUTED_2 = HexColor("#93A1B3")
BORDER = HexColor("#DFE5EE")
LIGHT = HexColor("#F5F7FA")
LIGHT_2 = HexColor("#EEF2F7")
WHITE = HexColor("#FFFFFF")
SIDEBAR = HexColor("#22364F")

W, H = 960, 540
M = 48

# ---------- базовые утилиты ----------

def sw(text, font=FONT, size=10):
    return pdfmetrics.stringWidth(text, font, size)


def fit(text, max_w, font=FONT_B, size=26, min_size=12):
    while size > min_size and sw(text, font, size) > max_w:
        size -= 0.5
    return size


def text(c, x, y, s, font=FONT, size=10, color=TEXT, align="l"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "l":
        c.drawString(x, y, s)
    elif align == "c":
        c.drawCentredString(x, y, s)
    else:
        c.drawRightString(x, y, s)
    return sw(s, font, size)


def wrap_lines(s, width, font=FONT, size=10):
    return simpleSplit(s, font, size, width)


def para(c, x, top, width, s, size=10.5, leading=None, color=TEXT,
         font=FONT, align=TA_LEFT, space_after=0):
    style = ParagraphStyle(
        "p", fontName=font, fontSize=size, leading=leading or size * 1.35,
        textColor=color, alignment=align, spaceAfter=space_after,
    )
    p = Paragraph(s, style)
    _, ph = p.wrapOn(c, width, 10000)
    p.drawOn(c, x, top - ph)
    return ph


def rounded(c, x, y, w, h, r=8, fill=WHITE, stroke=None, lw=0.8, alpha=None):
    if alpha is not None:
        c.saveState()
        c.setFillAlpha(alpha)
    c.setFillColor(fill)
    if stroke is None:
        c.roundRect(x, y, w, h, r, fill=1, stroke=0)
    else:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
        c.roundRect(x, y, w, h, r, fill=1, stroke=1)
    if alpha is not None:
        c.restoreState()


def card(c, x, y, w, h, fill=WHITE, stroke=BORDER, r=8, accent=None, accent_w=3):
    rounded(c, x, y, w, h, r=r, fill=fill, stroke=stroke, lw=0.8)
    if accent:
        c.setFillColor(accent)
        c.rect(x, y + 10, accent_w, h - 20, fill=1, stroke=0)


def line(c, x1, y1, x2, y2, color=BORDER, lw=0.8, dash=None):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    if dash:
        c.setDash(dash)
    c.line(x1, y1, x2, y2)
    if dash:
        c.setDash()


def arrow(c, x1, y1, x2, y2, color=BLUE, lw=1.2, head=5, dash=None):
    import math
    line(c, x1, y1, x2, y2, color, lw, dash)
    ang = math.atan2(y2 - y1, x2 - x1)
    for s in (0.5, -0.5):
        c.line(x2, y2, x2 - head * math.cos(ang - s), y2 - head * math.sin(ang - s))
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    for s in (0.5, -0.5):
        c.line(x2, y2, x2 - head * math.cos(ang - s), y2 - head * math.sin(ang - s))


def bullet(c, x, y, color=ORANGE, r=2.2):
    c.setFillColor(color)
    c.circle(x + r, y + r, r, fill=1, stroke=0)


def bullets(c, x, top, width, items, size=10.3, leading=14.2, gap=6,
            color=TEXT, bullet_color=ORANGE, font=FONT):
    y = top
    for item in items:
        bold = False
        if isinstance(item, tuple):
            item, bold = item
        lines = wrap_lines(item, width - 14, FONT_B if bold else font, size)
        bullet(c, x, y - size * 0.72, bullet_color, 2.0)
        yy = y
        for ln in lines:
            text(c, x + 12, yy - size, ln, FONT_B if bold else font, size, color)
            yy -= leading
        y = yy - gap
    return y


def numbered(c, x, y, n, d=20, color=BLUE, fg=WHITE, size=9):
    c.setFillColor(color)
    c.circle(x + d / 2, y - d / 2, d / 2, fill=1, stroke=0)
    text(c, x + d / 2, y - d / 2 - size * 0.35, str(n), FONT_B, size, fg, "c")


def check(c, x, y, s=9, color=GREEN, lw=1.7):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x, y + s * 0.45, x + s * 0.35, y + s * 0.1)
    c.line(x + s * 0.35, y + s * 0.1, x + s, y + s * 0.85)


def cross(c, x, y, s=7, color=RED, lw=1.5):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x, y, x + s, y + s)
    c.line(x, y + s, x + s, y)


def pill(c, x, y, label, size=7.6, fg=BLUE, bg=BLUE_PALE, border=None, pad=7, h=16, font=FONT_B):
    w = sw(label, font, size) + pad * 2
    rounded(c, x, y, w, h, r=h / 2, fill=bg, stroke=border, lw=0.7)
    text(c, x + pad, y + h / 2 - size * 0.35, label, font, size, fg)
    return w


# ---------- изображения ----------

def image(c, path, x, y, max_w, max_h, border=True, pad=5, bg=WHITE, radius=4):
    iw, ih = PILImage.open(path).size
    s = min((max_w - pad * 2) / iw, (max_h - pad * 2) / ih)
    w, h = iw * s, ih * s
    bx = x + (max_w - w) / 2
    by = y + (max_h - h) / 2
    if border:
        rounded(c, bx - pad, by - pad, w + pad * 2, h + pad * 2, r=radius,
                fill=bg, stroke=BORDER, lw=0.7)
    c.drawImage(path, bx, by, w, h, mask="auto")
    return bx, by, w, h


# ---------- каркас слайда ----------

def page_bg(c, dark=False):
    c.setFillColor(NAVY if dark else HexColor("#FAFBFD"))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    if not dark:
        # едва заметная сетка
        c.setStrokeColor(HexColor("#F0F3F8"))
        c.setLineWidth(0.5)
        for gx in range(0, W, 32):
            c.line(gx, 0, gx, H)
        for gy in range(0, H, 32):
            c.line(0, gy, W, gy)


def header(c, kicker, title, subtitle=None, title_size=25):
    text(c, M, 502, kicker.upper(), FONT_B, 8.2, ORANGE)
    c.setFillColor(ORANGE)
    c.rect(M, 491, 24, 2, fill=1, stroke=0)
    size = fit(title, W - M * 2, FONT_B, title_size, 15)
    text(c, M, 466, title, FONT_B, size, TEXT)
    if subtitle:
        para(c, M, 448, W - M * 2, subtitle, 10.2, 13.5, MUTED)
        return 424
    return 438


def footer(c, num, dark=False):
    col = HexColor("#7F8FA6") if not dark else HexColor("#8FA0B8")
    c.setStrokeColor(HexColor("#E6EBF2") if not dark else HexColor("#2A3B52"))
    c.setLineWidth(0.6)
    c.line(M, 36, W - M, 36)
    text(c, M, 24, "Складской учёт PRO", FONT, 7.4, col)
    text(c, W - M, 24, str(num), FONT_B, 7.8, col, "r")


def section_number(c, x, y, n, color=ORANGE):
    text(c, x, y, n, FONT_B, 40, color)
