"""Build the partner-logo images for the website from the logo files used in the
teaching material (TAI_materials, robotics/Figures/Logos).

  website/assets/images/logos.png       3 x 2 grid (home page, section pages)
  website/assets/images/logos_vert.png  2 x 3 grid (About page)

Run from the repo root:  python tools/make_logo_strip.py
"""
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / "TAI_materials" / "materials" / "part-2-ai-science" / "robotics" / "Figures" / "Logos"
OUT = ROOT / "website" / "assets" / "images"

# (file, relative height) - same proportions as on the title pages of the material
LOGOS = [
    ("universitaet-innsbruck-logo-cmyk-farbe.jpg", 1.5),
    ("logotipuab-v1-verd.png", 1.5),
    ("EN Co-funded by the EU_POS.jpg", 1.5),
    ("IMG_1189.PNG", 1.5),
    ("2nd Lyceum of Kos logo.jpg", 2.0),
    ("VIBENSHUS B.png", 0.88),
]
UNIT = 110          # pixels per "cm" of logo height
PAD_X, PAD_Y = 70, 45


def load(name):
    im = Image.open(SRC / name).convert("RGBA")
    flat = Image.new("RGB", im.size, "white")
    flat.paste(im, mask=im.split()[3])
    # trim the white border
    diff = ImageChops.difference(flat, Image.new("RGB", flat.size, "white"))
    bbox = diff.convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
    return flat.crop(bbox) if bbox else flat


def grid(cols, path):
    ims = []
    for name, h in LOGOS:
        im = load(name)
        target = int(h * UNIT)
        ims.append(im.resize((max(1, round(im.width * target / im.height)), target), Image.LANCZOS))
    rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
    cell_w = max(im.width for im in ims)
    row_h = [max(im.height for im in r) for r in rows]
    W = cols * cell_w + (cols + 1) * PAD_X
    H = sum(row_h) + (len(rows) + 1) * PAD_Y
    canvas = Image.new("RGB", (W, H), "white")
    y = PAD_Y
    for r, rh in zip(rows, row_h):
        for c, im in enumerate(r):
            x = PAD_X + c * (cell_w + PAD_X) + (cell_w - im.width) // 2
            canvas.paste(im, (x, y + (rh - im.height) // 2))
        y += rh + PAD_Y
    canvas.save(path, optimize=True)
    print(path.name, canvas.size)


if __name__ == "__main__":
    grid(3, OUT / "logos.png")
    grid(2, OUT / "logos_vert.png")
