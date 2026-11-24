#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news poster (1024x1024 PNG).

Stdlib only. Deterministic: fixed layout, no randomness, no time, no
network. Writes entry.png next to this file (or to argv[1]).

Stories (all reported on 24 Nov 2026, sources: Reuters, AP, Times of
India, Indian Express):
  LEAD  Indonesia candy-factory fire kills at least 24, ~30 missing.
  2     Ukraine says it sank a Russian warship (corvette) in Benghazi, Libya.
  3     Jensen Huang reinstated as Nvidia CEO; shares jump over 30%.
  4     COP31 climate talks in Turkey collapse with no deal.
  5     NATO to send AWACS early-warning aircraft to Poland after
        three Russian missiles landed there.
  6     Israeli strikes kill at least 3 in Gaza, incl. an UNRWA worker.
  7     India-Nepal: Saryu-Kamala Express flagged off; Rs 15,000 cr package.
  8     Sport: Alcaraz wins maiden ATP Finals; chess title match begins.
"""

import struct
import sys
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- canvas
PIX = bytearray(W * H * 3)


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        PIX[i], PIX[i + 1], PIX[i + 2] = c


def rect(x, y, w, h, c):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            i = base + (xx - x0) * 3
            PIX[i], PIX[i + 1], PIX[i + 2] = c


def hline(x0, x1, y, c):
    for x in range(max(0, x0), min(W, x1)):
        px(x, y, c)


def vline(x, y0, y1, c):
    for y in range(max(0, y0), min(H, y1)):
        px(x, y, c)


def circle(cx, cy, r, c):
    for dy in range(-r, r + 1):
        dx = int((r * r - dy * dy) ** 0.5)
        for x in range(cx - dx, cx + dx + 1):
            px(x, cy + dy, c)


def disc(cx, cy, r, c):
    circle(cx, cy, r, c)


def tri(x0, y0, x1, y1, x2, y2, c):
    # barycentric fill
    minx, maxx = min(x0, x1, x2), max(x0, x1, x2)
    miny, maxy = min(y0, y1, y2), max(y0, y1, y2)
    d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if d == 0:
        return
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            a = ((y1 - y2) * (x - x2) + (x2 - x1) * (y - y2)) / d
            b = ((y2 - y0) * (x - x2) + (x0 - x2) * (y - y2)) / d
            g = 1 - a - b
            if a >= 0 and b >= 0 and g >= 0:
                px(x, y, c)


# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 bits, '#' = on.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
}


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, c):
    """Draw upper-case text; returns width drawn."""
    s = s.upper()
    cx = x
    for ch in s:
        g = FONT.get(ch, FONT["?"])
        for r in range(7):
            row = g[r]
            for col in range(5):
                if row[col] == "1":
                    rect(cx + col * scale, y + r * scale, scale, scale, c)
        cx += 6 * scale
    return cx - x - scale


def draw_center(x, y, w, s, scale, c):
    draw_text(x + (w - text_w(s, scale)) // 2, y, s, scale, c)


def wrap(s, max_chars):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        nxt = (cur + " " + wd).strip()
        if len(nxt) <= max_chars:
            cur = nxt
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def para(x, y, w, s, scale, c, leading=None):
    """Draw wrapped paragraph; returns y after last line."""
    max_chars = max(1, w // (6 * scale))
    lh = leading if leading is not None else 9 * scale
    for line in wrap(s, max_chars):
        draw_text(x, y, line, scale, c)
        y += lh
    return y


# ---------------------------------------------------------------- palette
NAVY = (13, 27, 46)
NAVY2 = (18, 38, 62)
PAPER = (247, 243, 232)
INK = (16, 24, 36)
RED = (198, 40, 32)
ORANGE = (232, 96, 24)
AMBER = (245, 176, 44)
GOLD = (212, 160, 32)
WHITE = (255, 255, 255)
GREY = (210, 216, 224)
DARKGREY = (120, 130, 142)
SEA = (24, 84, 122)
SEA2 = (16, 58, 88)
GREEN = (28, 140, 74)
GREEN2 = (18, 100, 54)
TEAL = (18, 110, 108)
BROWN = (92, 58, 32)
SMOKE = (70, 74, 82)


def panel(x, y, w, h, bg, tag, tag_bg, accent):
    rect(x, y, w, h, bg)
    rect(x, y, w, 6, accent)
    rect(x, y, 150, 30, tag_bg)
    draw_text(x + 12, y + 8, tag, 2, WHITE)
    rect(x, y + h - 2, w, 2, accent)


def flame(x, y, s, c1, c2):
    """Stylised flame of height ~s at (x, y) top-left."""
    tri(x, y + s, x + s // 2, y, x + s, y + s, c1)
    tri(x + s // 4, y + s, x + s // 2, y + s // 3, x + 3 * s // 4, y + s, c2)


def draw():
    rect(0, 0, W, H, NAVY)

    # ---- masthead ------------------------------------------------------
    rect(0, 0, W, 118, PAPER)
    rect(0, 112, W, 6, RED)
    draw_center(0, 14, W, "THE WORLD IN ONE IMAGE", 5, INK)
    draw_center(0, 58, W, "TUESDAY 24 NOVEMBER 2026", 4, RED)
    draw_center(0, 88, W, "THE DAY'S NEWS, IN A SINGLE PICTURE", 2, DARKGREY)

    # ---- LEAD: Indonesia factory fire ---------------------------------
    lx, ly, lw, lh = 16, 134, 664, 330
    panel(lx, ly, lw, lh, (64, 22, 16), "LEAD  -  INDONESIA", RED, ORANGE)
    # burning factory silhouette, bottom of panel
    rect(lx, ly + 250, lw, 80, (38, 14, 10))
    rect(lx + 40, ly + 200, 130, 130, (52, 20, 12))
    rect(lx + 190, ly + 220, 100, 110, (52, 20, 12))
    rect(lx + 310, ly + 180, 34, 150, (52, 20, 12))
    rect(lx + 360, ly + 230, 150, 100, (52, 20, 12))
    for wx in (60, 100, 140, 210, 250, 380, 420, 460):
        rect(lx + wx, ly + 218, 16, 16, AMBER)
    # smoke (top-right corner, clear of the headline)
    disc(lx + 560, ly + 62, 18, SMOKE)
    disc(lx + 592, ly + 48, 22, SMOKE)
    disc(lx + 624, ly + 40, 15, SMOKE)
    # flames over the roofline (below the sub-text)
    flame(lx + 60, ly + 185, 60, ORANGE, AMBER)
    flame(lx + 150, ly + 175, 70, RED, ORANGE)
    flame(lx + 260, ly + 195, 50, ORANGE, AMBER)
    flame(lx + 400, ly + 180, 60, RED, ORANGE)
    draw_text(lx + 20, ly + 48, "FACTORY FIRE", 6, WHITE)
    draw_text(lx + 20, ly + 92, "KILLS 24 IN INDONESIA", 5, AMBER)
    para(lx + 20, ly + 132, lw - 40, "CANDY PLANT BLAZE; ABOUT 30 WORKERS STILL MISSING AS RESCUERS SEARCH THE RUINS", 2, (235, 225, 210), leading=18)

    # ---- RIGHT: Ukraine sinks Russian warship in Libya ------------------
    rx, ry, rw, rh = 696, 134, 312, 330
    panel(rx, ry, rw, rh, SEA2, "WAR AT SEA", SEA, (90, 180, 230))
    # sea + ship
    rect(rx, ry + 210, rw, 120, SEA)
    for wy in (ry + 222, ry + 300, ry + 318):
        for wx in range(rx + 10, rx + rw - 10, 46):
            hline(wx, wx + 26, wy, (120, 200, 240))
    # ship hull + tower, listing
    tri(rx + 40, ry + 205, rx + 270, ry + 205, rx + 250, ry + 168, (40, 48, 58))
    rect(rx + 130, ry + 130, 26, 78, (40, 48, 58))
    rect(rx + 168, ry + 148, 40, 14, (40, 48, 58))
    flame(rx + 150, ry + 168, 44, ORANGE, AMBER)
    disc(rx + 120, ry + 118, 20, SMOKE)
    disc(rx + 150, ry + 96, 26, SMOKE)
    draw_text(rx + 14, ry + 44, "UKRAINE SINKS", 3, WHITE)
    draw_text(rx + 14, ry + 76, "RUSSIAN WARSHIP", 3, WHITE)
    draw_text(rx + 14, ry + 108, "IN LIBYA PORT", 3, AMBER)
    para(rx + 14, ry + 318 - 84, rw - 28, "CORVETTE HIT BY DRONES AT BENGHAZI; THE WAR SPREADS BEYOND EUROPE", 2, (205, 225, 240), leading=18)

    # ---- MIDDLE ROW ----------------------------------------------------
    my, mh = 480, 240
    mw = 322
    # Nvidia / Huang
    x = 16
    panel(x, my, mw, mh, GREEN2, "TECH", GREEN, GREEN)
    rect(x + 26, my + 52, 74, 74, (8, 40, 24))
    rect(x + 40, my + 66, 46, 46, GREEN)
    draw_text(x + 46, my + 76, "AI", 4, WHITE)
    for i in range(5):
        vline(x + 36 + i * 14, my + 44, my + 52, GOLD)
        vline(x + 36 + i * 14, my + 126, my + 134, GOLD)
    # rising arrow
    tri(x + 236, my + 66, x + 262, my + 66, x + 249, my + 44, AMBER)
    rect(x + 241, my + 66, 16, 58, AMBER)
    draw_text(x + 16, my + 146, "HUANG IS BACK", 4, WHITE)
    para(x + 16, my + 182, mw - 32, "NVIDIA REINSTATES ITS CEO; SHARES JUMP OVER 30% IN A DAY", 2, (205, 235, 215), leading=18)
    # COP31 collapse
    x = 351
    panel(x, my, mw, mh, (14, 58, 58), "CLIMATE", TEAL, TEAL)
    disc(x + 70, my + 96, 46, (40, 150, 140))
    rect(x + 40, my + 60, 60, 8, (40, 150, 140))
    tri(x + 70, my + 60, x + 86, my + 96, x + 54, my + 96, (20, 90, 90))
    draw_text(x + 130, my + 66, "COP31", 5, WHITE)
    draw_text(x + 130, my + 104, "NO DEAL", 4, AMBER)
    draw_text(x + 16, my + 140, "CLIMATE TALKS", 4, WHITE)
    draw_text(x + 16, my + 172, "COLLAPSE", 4, WHITE)
    para(x + 16, my + 204, mw - 32, "TALKS IN TURKEY END WITH NO DEAL ON FOSSIL FUELS", 2, (200, 230, 228), leading=17)
    # NATO / Poland
    x = 686
    panel(x, my, mw, mh, NAVY2, "NATO", (60, 90, 130), (90, 140, 200))
    # AWACS plane silhouette
    tri(x + 40, my + 96, x + 280, my + 96, x + 160, my + 78, (200, 210, 225))
    rect(x + 120, my + 84, 90, 10, (200, 210, 225))
    disc(x + 165, my + 72, 14, (200, 210, 225))
    for wx in (60, 110, 160, 210, 260):
        disc(x + wx, my + 122, 3, AMBER)
    draw_text(x + 16, my + 132, "NATO SENDS AWACS", 3, WHITE)
    draw_text(x + 16, my + 160, "TO POLAND", 3, WHITE)
    para(x + 16, my + 192, mw - 32, "THREE RUSSIAN MISSILES LANDED IN POLAND", 2, (205, 218, 235), leading=17)

    # ---- BOTTOM ROW ----------------------------------------------------
    by, bh = 736, 200
    bw = 322
    # Gaza
    x = 16
    panel(x, by, bw, bh, (58, 26, 30), "GAZA", RED, RED)
    draw_text(x + 16, by + 46, "GAZA STRIKES", 4, WHITE)
    draw_text(x + 16, by + 78, "KILL 3", 4, WHITE)
    para(x + 16, by + 116, bw - 32, "ISRAELI STRIKES KILL AT LEAST THREE, INCLUDING A WORKER WITH THE UN PALESTINIAN AGENCY UNRWA", 2, (235, 215, 210), leading=18)
    # India-Nepal
    x = 351
    panel(x, by, bw, bh, (58, 40, 14), "INDIA - NEPAL", (150, 90, 20), AMBER)
    # train
    rect(x + 16, by + 52, 180, 34, AMBER)
    rect(x + 196, by + 60, 60, 26, AMBER)
    for wx in (30, 60, 90, 120, 150):
        rect(x + wx, by + 62, 18, 14, (58, 40, 14))
    disc(x + 50, by + 96, 10, INK)
    disc(x + 150, by + 96, 10, INK)
    disc(x + 220, by + 96, 10, INK)
    hline(x + 16, x + 290, by + 110, DARKGREY)
    draw_text(x + 16, by + 112, "NEW RAIL LINK", 4, WHITE)
    para(x + 16, by + 144, bw - 32, "SARYU-KAMALA EXPRESS FLAGGED OFF; RS 15,000 CRORE PACKAGE", 2, (240, 225, 200), leading=17)
    # Sport
    x = 686
    panel(x, by, bw, bh, (30, 44, 66), "SPORT", (70, 100, 150), GOLD)
    disc(x + 34, by + 62, 16, GOLD)
    draw_text(x + 60, by + 48, "ALCARAZ WINS", 3, WHITE)
    draw_text(x + 60, by + 80, "ATP FINALS", 4, AMBER)
    draw_text(x + 16, by + 120, "CHESS TITLE MATCH", 3, WHITE)
    para(x + 16, by + 150, bw - 32, "GUKESH DEFENDS CROWN VS SINDAROV IN GENEVA", 2, (210, 220, 235), leading=18)

    # ---- footer ---------------------------------------------------------
    rect(0, 952, W, 72, PAPER)
    rect(0, 952, W, 4, RED)
    draw_center(0, 966, W, "SOURCES: REUTERS - AP - TIMES OF INDIA - INDIAN EXPRESS", 2, INK)
    draw_center(0, 988, W, "ONE DAY. ONE IMAGE.  -  24 NOVEMBER 2026", 2, DARKGREY)


def png_bytes():
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(PIX[y * W * 3:(y + 1) * W * 3])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", comp)
        + chunk(b"IEND", b"")
    )


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    draw()
    data = png_bytes()
    with open(out, "wb") as f:
        f.write(data)
    print(f"wrote {out}: {len(data)} bytes, {W}x{H}")


if __name__ == "__main__":
    main()
