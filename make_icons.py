from PIL import Image, ImageDraw

WALNUT = (62, 42, 30, 255)
AMBER = (226, 149, 75, 255)
AMBER_BRIGHT = (244, 184, 96, 255)
BRASS = (169, 123, 79, 255)
CREAM = (242, 232, 211, 255)

def make_icon(size, maskable=False, filename="icon.png"):
    img = Image.new("RGBA", (size, size), WALNUT)
    d = ImageDraw.Draw(img)

    # safe zone for maskable icons (~80% center circle gets shown after OS crop)
    pad = size * (0.10 if maskable else 0.06)

    # outer brass ring (the radio dial bezel)
    ring_box = [pad, pad, size - pad, size - pad]
    d.ellipse(ring_box, fill=BRASS)

    # inner amber dial face
    inset = size * 0.045
    face_box = [pad + inset, pad + inset, size - pad - inset, size - pad - inset]
    d.ellipse(face_box, fill=AMBER)

    # subtle highlight (top-left glow) using a soft offset ellipse
    hl_box = [
        pad + inset + size * 0.06,
        pad + inset + size * 0.04,
        pad + inset + size * 0.55,
        pad + inset + size * 0.40,
    ]
    d.ellipse(hl_box, fill=AMBER_BRIGHT)

    # re-draw face slightly smaller on top to blend the highlight edge (soft look)
    face_box2 = [pad + inset + size*0.02, pad + inset + size*0.02, size - pad - inset - size*0.02, size - pad - inset - size*0.02]
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    od.ellipse(face_box2, fill=(226,149,75,90))
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)

    # center play triangle (cream)
    cx, cy = size/2, size/2
    tri_h = size * 0.30
    tri_w = size * 0.26
    offset_x = size * 0.02  # optical centering for triangle
    points = [
        (cx - tri_w/2 + offset_x, cy - tri_h/2),
        (cx - tri_w/2 + offset_x, cy + tri_h/2),
        (cx + tri_w/2 + offset_x, cy),
    ]
    d.polygon(points, fill=CREAM)

    # small tick mark at top of ring (the dial needle home position)
    tick_w = size * 0.012
    d.rectangle([cx - tick_w/2, pad - size*0.005, cx + tick_w/2, pad + size*0.035], fill=CREAM)

    img.save(filename)
    print("saved", filename, size)

make_icon(512, maskable=True, filename="icons/icon-512.png")
make_icon(192, maskable=True, filename="icons/icon-192.png")
make_icon(180, maskable=False, filename="icons/apple-touch-icon.png")
make_icon(32, maskable=False, filename="icons/favicon-32.png")
make_icon(16, maskable=False, filename="icons/favicon-16.png")
