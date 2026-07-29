# -*- coding: utf-8 -*-
"""Generate Lavender Mist Theme extension icon.
256x256 transparent PNG: lavender crescent moon + white </> code symbol + soft mist waves.
Drawn at 1024px and downscaled to 256px for smooth anti-aliasing.
"""
from PIL import Image, ImageDraw
import os

S = 1024  # supersample canvas
OUT = 256

LAVENDER = (165, 148, 249, 255)   # #A594F9 primary lavender (moon)
SOFT = (205, 193, 255, 255)       # #CDC1FF soft purple (mist)
LIGHT = (229, 217, 242, 235)      # #E5D9F2 light lavender (far mist)
DEEP = (128, 100, 216, 255)       # #8064D8 deep lavender (accents)
WHITE = (255, 255, 255, 255)

img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

# ---- crescent moon (via mask: full circle minus offset circle) ----
moon_mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(moon_mask)
# main circle
mc_l, mc_t, mc_r, mc_b = 250, 130, 810, 690
md.ellipse((mc_l, mc_t, mc_r, mc_b), fill=255)
# punch-out circle (upper-right offset) -> crescent opening to top-right
md.ellipse((mc_l + 150, mc_t - 110, mc_r + 150, mc_b - 110), fill=0)

moon_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
moon_layer.paste(Image.new("RGBA", (S, S), LAVENDER), (0, 0), moon_mask)
img = Image.alpha_composite(img, moon_layer)

# ---- small stars (tiny dots near the moon opening) ----
d = ImageDraw.Draw(img)
for (sx, sy, sr) in [(760, 240, 14), (680, 150, 9), (830, 360, 10)]:
    d.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=SOFT)

# ---- code symbol </> on the moon body ----
cx, cy = 470, 470
cw = 26          # stroke width
ah, aw = 60, 44  # bracket half-height / width
gap = 84         # distance from center to each bracket

# left bracket <
lx = cx - gap
d.line((lx, cy - ah, lx - aw, cy), fill=WHITE, width=cw)
d.line((lx - aw, cy, lx, cy + ah), fill=WHITE, width=cw)
# right bracket >
rx = cx + gap
d.line((rx, cy - ah, rx + aw, cy), fill=WHITE, width=cw)
d.line((rx + aw, cy, rx, cy + ah), fill=WHITE, width=cw)
# slash /
d.line((cx - 24, cy + ah + 8, cx + 24, cy - ah - 8), fill=WHITE, width=cw)
# round the stroke ends
r = cw // 2
for (px, py) in [
    (lx, cy - ah), (lx - aw, cy), (lx, cy + ah),
    (rx, cy - ah), (rx + aw, cy), (rx, cy + ah),
    (cx - 24, cy + ah + 8), (cx + 24, cy - ah - 8),
]:
    d.ellipse((px - r, py - r, px + r, py + r), fill=WHITE)

# ---- mist waves (three soft rounded bands across the bottom) ----
def mist_band(y, x0, x1, h, color):
    d.rounded_rectangle((x0, y, x1, y + h), radius=h // 2, fill=color)

mist_band(742, 150, 780, 58, SOFT)     # near mist (overlaps moon base)
mist_band(836, 260, 900, 52, LIGHT)    # middle mist
mist_band(922, 180, 700, 46, (205, 193, 255, 200))  # far mist, slightly sheer

out_path = os.path.join(os.path.dirname(__file__), "..", "icon.png")
img.resize((OUT, OUT), Image.LANCZOS).save(os.path.abspath(out_path))
print("icon saved:", os.path.abspath(out_path))
