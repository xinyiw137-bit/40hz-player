import math
from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/arialbd.ttf"


def make(size, path):
    top = (16, 120, 216)
    bottom = (7, 70, 140)
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        t = y / (size - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(size):
            px[x, y] = (r, g, b)

    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(FONT, int(size * 0.26))
    except Exception:
        font = ImageFont.load_default()

    text = "40Hz"
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    tx = (size - tw) / 2 - bb[0]
    ty = size * 0.36 - th / 2 - bb[1]
    d.text((tx, ty), text, fill=(255, 255, 255), font=font)

    # 正弦波（代表 40Hz 调制）
    pad = int(size * 0.08)
    amp = size * 0.10
    cy = size * 0.66
    cycles = 2.5
    pts = []
    N = 240
    for i in range(N):
        x = pad + (size - 2 * pad) * i / (N - 1)
        y = cy + amp * math.sin(2 * math.pi * cycles * i / (N - 1))
        pts.append((x, y))
    d.line(pts, fill=(255, 255, 255), width=max(2, int(size * 0.035)), joint="curve")

    img.save(path)


make(192, "icon-192.png")
make(512, "icon-512.png")
make(180, "apple-touch-icon.png")
print("icons done")
