#!/usr/bin/env python3
"""Composes a full game screen from the generated art (view, hands, gems,
brand, vignette) into build/preview/screen_<view>.png for quick review."""
import sys
from PIL import Image

view, lit, deaths, level = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
GEMS = [(20, 113), (33, 108), (46, 106)]
BRAND = (173, 113)
im = Image.open(f'build/preview/{view}.png').convert('RGBA').resize((240, 160), Image.NEAREST)
im.alpha_composite(Image.open('assets/hands.png').crop((8, 48, 248, 208)))
gem = Image.open('assets/gem.png')
for i, (x, y) in enumerate(GEMS):
    fr = gem.crop((0, 0, 16, 16)) if i < lit else gem.crop((0, 16, 16, 32))
    im.alpha_composite(fr, (x - 8, y - 8))
im.alpha_composite(Image.open('assets/brand.png').crop((0, 16 * deaths, 32, 16 * deaths + 16)), BRAND)
if level:
    im.alpha_composite(Image.open(f'assets/vignette_{level}.png').crop((8, 48, 248, 208)))
im.resize((480, 320), Image.NEAREST).save(f'build/preview/screen_{view}_{level}.png')
