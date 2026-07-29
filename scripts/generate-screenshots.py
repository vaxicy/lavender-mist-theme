# -*- coding: utf-8 -*-
"""Generate VS Code interface preview screenshots for Lavender Mist themes.
Outputs:
  screenshots/lavender-mist-light.png
  screenshots/lavender-mist-dark.png
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")
W, H = 1440, 900

PALETTES = {
    "light": {
        "titleBar": "#EDE5F9",
        "titleText": "#4C4368",
        "activityBar": "#E5D9F2",
        "activityIcon": "#7A7194",
        "activityIconActive": "#A594F9",
        "sideBar": "#F5EFFF",
        "sideBarText": "#4C4368",
        "sideBarSub": "#7A7194",
        "tabActive": "#F8F5FF",
        "tabInactive": "#EDE5F9",
        "tabBorder": "#E5D9F2",
        "editorBg": "#F8F5FF",
        "editorText": "#4C4368",
        "lineNumber": "#B9AFD6",
        "lineNumberActive": "#A594F9",
        "statusBar": "#E5D9F2",
        "statusText": "#4C4368",
        "accent": "#A594F9",
        "border": "#E5D9F2",
        "minimap": "#F5EFFF",
        "keyword": "#8064D8",
        "function": "#9B6DFF",
        "string": "#718C7A",
        "number": "#C58AF9",
        "comment": "#A69BB8",
        "type": "#B87BD8",
        "tag": "#8064D8",
        "property": "#6C5BC4",
    },
    "dark": {
        "titleBar": "#171525",
        "titleText": "#D6D0E8",
        "activityBar": "#171525",
        "activityIcon": "#6B6284",
        "activityIconActive": "#B9A7FF",
        "sideBar": "#24203A",
        "sideBarText": "#D6D0E8",
        "sideBarSub": "#9C93B5",
        "tabActive": "#1D1930",
        "tabInactive": "#24203A",
        "tabBorder": "#40365F",
        "editorBg": "#1D1930",
        "editorText": "#D6D0E8",
        "lineNumber": "#5E547E",
        "lineNumberActive": "#B9A7FF",
        "statusBar": "#2D2748",
        "statusText": "#D6D0E8",
        "accent": "#B9A7FF",
        "border": "#40365F",
        "minimap": "#24203A",
        "keyword": "#C7B6FF",
        "function": "#D8C8FF",
        "string": "#9BC7A5",
        "number": "#E0A7FF",
        "comment": "#8E849F",
        "type": "#D8A7F0",
        "tag": "#C7B6FF",
        "property": "#A8B8F5",
    },
}


def hex_to_rgba(h, alpha=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def load_fonts():
    """Try common monospace fonts; fall back to default."""
    candidates = [
        "C:\\Windows\\Fonts\\JetBrainsMono-Regular.ttf",
        "C:\\Windows\\Fonts\\FiraCode-Regular.ttf",
        "C:\\Windows\\Fonts\\Consolas.ttf",
        "C:\\Windows\\Fonts\\Courier New.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return {
                "ui": ImageFont.truetype(path, 16),
                "ui_small": ImageFont.truetype(path, 13),
                "code": ImageFont.truetype(path, 18),
                "code_small": ImageFont.truetype(path, 14),
                "title": ImageFont.truetype(path, 13),
            }
    default = ImageFont.load_default()
    return {"ui": default, "ui_small": default, "code": default, "code_small": default, "title": default}


def draw_rounded_rect(draw, xy, radius, fill):
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_code_line(draw, x, y, tokens, font, line_h):
    cx = x
    for text, color in tokens:
        draw.text((cx, y), text, fill=color, font=font)
        w, _ = text_size(draw, text, font)
        cx += w
    return y + line_h


def build_code_tokens(palette):
    """Return a small React-ish snippet split into syntax-colored tokens."""
    k = palette["keyword"]
    f = palette["function"]
    s = palette["string"]
    n = palette["number"]
    c = palette["comment"]
    t = palette["type"]
    tag = palette["tag"]
    prop = palette["property"]
    txt = palette["editorText"]
    punc = txt

    lines = [
        [("// Lavender Mist — a dreamy React hook", c)],
        [("import ", k), ("{ useState, useEffect }", txt), (" from ", k), ("'react'", s), (";", punc)],
        [("",)],
        [("export ", k), ("const ", k), ("useMoonlight", f), (" = ", punc), ("(", punc), ("initialHue", txt), (": ", punc), ("number", t), (")", punc), (" => ", punc), ("{", punc)],
        [("  const ", k), ("[hue, setHue]", txt), (" = ", punc), ("useState", f), ("(", punc), ("240", n), (");", punc)],
        [("",)],
        [("  useEffect", f), ("(()", punc), (" => ", punc), ("{", punc)],
        [("    const ", k), ("timer", txt), (" = ", punc), ("setInterval", f), ("(()", punc), (" => ", punc), ("{", punc)],
        [("      setHue", f), ("(", punc), ("h", txt), (" => ", punc), ("(h + ", txt), ("1", n), (") % ", txt), ("360", n), (");", punc)],
        [("    }, ", punc), ("16_000", n), (");", punc)],
        [("    return ", k), ("()", punc), (" => ", punc), ("clearInterval", f), ("(timer);", punc)],
        [("  }, []);", punc)],
        [("",)],
        [("  return ", k), ("{ hue, setHue };", txt)],
        [("};", punc)],
        [("",)],
        [("const ", k), ("MistCard", f), (" = ", punc), ("(", punc), ("{ title }", txt), (": ", punc), ("{ title: string }", t), (")", punc), (" => ", punc), ("{", punc)],
        [("  return ", k), ("(", punc)],
        [("    <", punc), ("div", tag), (" className", prop), ("=", punc), ("\"mist-card\"", s), (">", punc)],
        [("      <", punc), ("h2", tag), (">{title}</", punc), ("h2", tag), (">", punc)],
        [("      <", punc), ("p", tag), (">{", punc), ("\"Dream in purple.\"", s), ("}</", punc), ("p", tag), (">", punc)],
        [("    </", punc), ("div", tag), (">", punc)],
        [("  );", punc)],
        [("};", punc)],
    ]
    return lines


def draw_screenshot(variant):
    p = PALETTES[variant]
    img = Image.new("RGBA", (W, H), hex_to_rgba(p["editorBg"]))
    d = ImageDraw.Draw(img)
    fonts = load_fonts()

    # Title bar
    d.rectangle((0, 0, W, 32), fill=hex_to_rgba(p["titleBar"]))
    d.text((96, 9), "Lavender Mist Theme - Visual Studio Code", fill=hex_to_rgba(p["titleText"]), font=fonts["title"])
    # Window controls (macOS style circles)
    for i, color in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        d.ellipse((16 + i * 18, 10, 28 + i * 18, 22), fill=hex_to_rgba(color))

    # Activity bar (left, 52px)
    d.rectangle((0, 32, 52, H - 24), fill=hex_to_rgba(p["activityBar"]))

    def draw_activity_icon(idx, cx, cy, color):
        """Draw simple shape icons that never rely on font glyph coverage."""
        if idx == 0:  # files: stacked rectangles
            d.rounded_rectangle((cx - 8, cy - 10, cx + 8, cy + 10), radius=2, fill=color)
            d.rectangle((cx - 8, cy - 10, cx - 2, cy - 4), fill=color)
        elif idx == 1:  # search: magnifying glass
            d.ellipse((cx - 7, cy - 8, cx + 5, cy + 4), outline=color, width=3)
            d.line((cx + 3, cy + 3, cx + 9, cy + 9), fill=color, width=3)
        elif idx == 2:  # source control: diamond
            d.polygon([(cx, cy - 10), (cx + 10, cy), (cx, cy + 10), (cx - 10, cy)], fill=color)
        elif idx == 3:  # extensions: four squares (active)
            d.rounded_rectangle((cx - 9, cy - 9, cx - 1, cy - 1), radius=2, fill=color)
            d.rounded_rectangle((cx + 1, cy - 9, cx + 9, cy - 1), radius=2, fill=color)
            d.rounded_rectangle((cx - 9, cy + 1, cx - 1, cy + 9), radius=2, fill=color)
            d.rounded_rectangle((cx + 1, cy + 1, cx + 9, cy + 9), radius=2, fill=color)
        elif idx == 4:  # run: play triangle
            d.polygon([(cx - 7, cy - 9), (cx + 9, cy), (cx - 7, cy + 9)], fill=color)
        else:  # settings: gear-ish circle with cross
            d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=color)
            d.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=p["activityBar"])

    for i in range(6):
        y = 56 + i * 46
        color = p["activityIconActive"] if i == 3 else p["activityIcon"]
        if i == 3:
            d.rectangle((0, y - 9, 3, y + 25), fill=hex_to_rgba(p["accent"]))
        draw_activity_icon(i, 26, y + 10, hex_to_rgba(color))

    # Sidebar (200px)
    sb_x, sb_w = 52, 220
    d.rectangle((sb_x, 32, sb_x + sb_w, H - 24), fill=hex_to_rgba(p["sideBar"]))
    d.text((sb_x + 16, 48), "EXPLORER", fill=hex_to_rgba(p["sideBarSub"]), font=fonts["ui_small"])
    d.text((sb_x + 16, 74), "v LAVENDER-MIST", fill=hex_to_rgba(p["sideBarText"]), font=fonts["ui"])
    files = [
        ("  package.json", p["sideBarText"]),
        ("  themes", p["sideBarText"]),
        ("    lavender-mist-light.json", p["sideBarText"]),
        ("    lavender-mist-dark.json", p["accent"]),
        ("  README.md", p["sideBarText"]),
        ("  CHANGELOG.md", p["sideBarText"]),
        ("  LICENSE", p["sideBarText"]),
    ]
    y = 102
    for name, color in files:
        d.text((sb_x + 16, y), name, fill=hex_to_rgba(color), font=fonts["ui_small"])
        y += 26

    # Tabs
    tabs = [("lavender-mist-dark.json", False), ("lavender-mist-light.json", False), ("preview.tsx", True)]
    tab_x = sb_x + sb_w
    tab_y = 32
    tab_h = 38
    for name, active in tabs:
        color = p["tabActive"] if active else p["tabInactive"]
        w, _ = text_size(d, name, fonts["ui"])
        tab_w = w + 56
        d.rectangle((tab_x, tab_y, tab_x + tab_w, tab_y + tab_h), fill=hex_to_rgba(color))
        if active:
            d.rectangle((tab_x, tab_y + tab_h - 2, tab_x + tab_w, tab_y + tab_h), fill=hex_to_rgba(p["accent"]))
        d.text((tab_x + 18, tab_y + 10), name, fill=hex_to_rgba(p["editorText"]), font=fonts["ui"])
        # close icon drawn as a small X to avoid Unicode "×" rendering issues
        cx = tab_x + tab_w - 15
        cy = tab_y + 19
        cross_color = hex_to_rgba(p["sideBarSub"])
        # thinner, sharper 6x6 cross like VS Code's native tab close icon
        d.line((cx - 3, cy - 3, cx + 3, cy + 3), fill=cross_color, width=1)
        d.line((cx + 3, cy - 3, cx - 3, cy + 3), fill=cross_color, width=1)
        tab_x += tab_w

    # Editor area bounds (no minimap)
    editor_x = sb_x + sb_w
    editor_y = tab_y + tab_h
    editor_w = W - editor_x
    editor_h = H - 24 - editor_y
    d.rectangle((editor_x, editor_y, editor_x + editor_w, editor_y + editor_h), fill=hex_to_rgba(p["editorBg"]))

    # Line numbers + code
    code_x = editor_x + 72
    code_y = editor_y + 30
    line_h = 26
    lines = build_code_tokens(p)
    for i, tokens in enumerate(lines):
        ln = i + 1
        ln_x = editor_x + 44
        ln_color = p["lineNumberActive"] if ln == 16 else p["lineNumber"]
        d.text((ln_x, code_y), str(ln), fill=hex_to_rgba(ln_color), font=fonts["code_small"], anchor="ra")
        if tokens and (len(tokens) > 1 or tokens[0][0]):
            draw_code_line(d, code_x, code_y, tokens, fonts["code"], line_h)
        code_y += line_h

    # Status bar
    d.rectangle((0, H - 24, W, H), fill=hex_to_rgba(p["statusBar"]))
    d.text((16, H - 21), "main*", fill=hex_to_rgba(p["statusText"]), font=fonts["ui_small"])
    d.text((180, H - 21), "TypeScript JSX", fill=hex_to_rgba(p["statusText"]), font=fonts["ui_small"])
    d.text((W - 220, H - 21), "Ln 16, Col 18", fill=hex_to_rgba(p["statusText"]), font=fonts["ui_small"])
    d.text((W - 90, H - 21), "UTF-8", fill=hex_to_rgba(p["statusText"]), font=fonts["ui_small"])

    # Subtle outer shadow / rounded frame for the whole window (optional)
    return img


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for variant in ("light", "dark"):
        img = draw_screenshot(variant)
        path = os.path.join(OUT_DIR, f"lavender-mist-{variant}.png")
        img.save(path)
        print("saved:", os.path.abspath(path))


if __name__ == "__main__":
    main()
