#!/usr/bin/env python3
"""Recolor case screenshots to match the site palette.

- proffer.jpg / etagi.jpg: teal "before/after" labels in the top strip -> pink
- leadgen.jpg: blue chart line -> navy, white background -> cream
Client logos are left untouched (only the top 200 px strip is processed
for the before/after screens). Re-run safe: always starts from img/*.jpg.
"""
import numpy as np
from PIL import Image
from pathlib import Path

IMG = Path(__file__).resolve().parent.parent / "img"
PINK = np.array([214, 168, 180], float)   # #D6A8B4
NAVY = np.array([31, 43, 72], float)      # #1F2B48
CREAM = np.array([241, 236, 227], float)  # #F1ECE3

def load(name):
    return np.asarray(Image.open(IMG / name).convert("RGB")).astype(float)

def save(arr, name):
    Image.fromarray(arr.clip(0, 255).astype("uint8")).save(IMG / name, quality=88)
    print("saved", name)

def teal_mask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (g > 110) & (b > 110) & (g > r + 25) & (b > r + 15) & (abs(g - b) < 90)

def recolor_labels(name, strip=200):
    a = load(name)
    top = a[:strip]
    m = teal_mask(top)
    if m.sum() == 0:
        print(name, "- no teal found in top strip, skipped"); return
    # keep luminance, move hue to pink
    lum = top[m].mean(axis=1, keepdims=True) / 255.0
    top[m] = PINK * (0.35 + 0.65 * lum)
    a[:strip] = top
    save(a, name)

def recolor_chart(name="leadgen.jpg"):
    a = load(name)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    blue = (b > 120) & (b > r + 30) & (b > g + 20)
    white = (r > 225) & (g > 225) & (b > 225)
    lum = a[blue].mean(axis=1, keepdims=True) / 255.0
    a[blue] = NAVY * (0.3 + 0.9 * lum)
    a[white] = CREAM
    save(a, name)

if __name__ == "__main__":
    recolor_labels("proffer.jpg")
    recolor_labels("etagi.jpg")
    recolor_chart()
