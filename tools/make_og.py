#!/usr/bin/env python3
"""og.jpg 1200x630 in the Ink & Ivory style with the real logo mark."""
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
BLACK, CREAM, ROSE = "#1A1A1A", "#F1ECE3", "#D6A8B4"

def font(name, size, variation=None):
    f = ImageFont.truetype(str(TOOLS / name), size)
    if variation:
        try: f.set_variation_by_name(variation)
        except Exception: pass
    return f

W, H = 1200, 630
og = Image.new("RGB", (W, H), BLACK)

# faint rose glyph watermark, left
wm = Image.open(ROOT / "img" / "logo-a-rose.png").convert("RGBA")
r = 620 / wm.width
wm = wm.resize((round(wm.width*r), round(wm.height*r)), Image.LANCZOS)
faded = wm.copy()
faded.putalpha(wm.split()[3].point(lambda a: int(a * 0.22)))
og.paste(faded, (-140, 150), faded)

# portrait in arch, right
p = Image.open(ROOT / "img" / "hero.jpg").convert("RGB")
pw, ph = 380, 520
p = ImageOps.fit(p, (pw, ph), Image.LANCZOS, centering=(0.5, 0.25))
arch = Image.new("L", (pw, ph), 0)
ad = ImageDraw.Draw(arch)
ad.pieslice([0, 0, pw, pw], 180, 360, fill=255)
ad.rounded_rectangle([0, pw//2 - 10, pw, ph], radius=24, fill=255)
og.paste(p, (W - pw - 90, 55), arch)

d = ImageDraw.Draw(og)
d.text((90, 205), "Ailina Sabirova", font=font("CormorantGaramond.ttf", 86, "Medium"), fill=CREAM)
sub = font("Manrope.ttf", 30, "SemiBold")
d.text((92, 320), "SMM  ·  DIGITAL MARKETING  ·  AI", font=sub, fill=CREAM)
d.text((92, 372), "DUBAI, UAE", font=sub, fill=ROSE)
d.text((92, 500), "smm-dubai.com", font=font("Manrope.ttf", 26, "Medium"), fill=ROSE)
og.save(ROOT / "og.jpg", quality=90)
print("og.jpg", og.size)
