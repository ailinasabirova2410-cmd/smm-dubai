#!/usr/bin/env python3
"""Generate og.jpg (1200x630) and favicons for smm-dubai.com."""
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
CREAM, NAVY, PINK, BLACK = "#F1ECE3", "#1F2B48", "#D6A8B4", "#1A1A1A"

def font(name, size, variation=None):
    f = ImageFont.truetype(str(TOOLS / name), size)
    if variation:
        try: f.set_variation_by_name(variation)
        except Exception: pass
    return f

# ---- og.jpg ----
W, H = 1200, 630
og = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(og)

# watermark "a"
wm_f = font("Italianno.ttf", 620)
d.text((-40, -140), "a", font=wm_f, fill=PINK)

# portrait in arch on the right
p = Image.open(ROOT / "img" / "hero.jpg").convert("RGB")
pw, ph = 380, 520
p = ImageOps.fit(p, (pw, ph), Image.LANCZOS, centering=(0.5, 0.25))
mask = Image.new("L", (pw, ph), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([0, 0, pw, ph], radius=24, fill=255)
md.pieslice([0, 0, pw, pw], 180, 360, fill=255)
md.rectangle([0, pw // 2, pw, ph], fill=255)
arch = Image.new("L", (pw, ph), 0)
ad = ImageDraw.Draw(arch)
ad.pieslice([0, 0, pw, pw], 180, 360, fill=255)
ad.rounded_rectangle([0, pw // 2 - 10, pw, ph], radius=24, fill=255)
og.paste(p, (W - pw - 90, 55), arch)

name_f = font("CormorantGaramond.ttf", 86, "Medium")
d.text((90, 205), "Ailina Sabirova", font=name_f, fill=NAVY)
sub_f = font("Manrope.ttf", 30, "SemiBold")
d.text((92, 320), "SMM  ·  DIGITAL MARKETING  ·  AI", font=sub_f, fill=NAVY)
d.text((92, 372), "DUBAI, UAE", font=sub_f, fill=PINK)
site_f = font("Manrope.ttf", 26, "Medium")
d.text((92, 500), "smm-dubai.com", font=site_f, fill=NAVY)
og.save(ROOT / "og.jpg", quality=90)
print("og.jpg", og.size)

# ---- favicons: black circle + cream Italianno "a" ----
def favicon(size, out):
    s = size * 4
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.ellipse([0, 0, s - 1, s - 1], fill=BLACK)
    f = font("Italianno.ttf", int(s * 0.82))
    bb = dd.textbbox((0, 0), "a", font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    dd.text(((s - tw) / 2 - bb[0], (s - th) / 2 - bb[1] - s * 0.04), "a", font=f, fill=CREAM)
    im = im.resize((size, size), Image.LANCZOS)
    im.save(ROOT / out)
    print(out, size)

favicon(32, "favicon-32.png")
favicon(192, "favicon-192.png")
favicon(180, "apple-touch-icon.png")
