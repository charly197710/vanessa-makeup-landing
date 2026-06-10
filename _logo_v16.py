from PIL import Image, ImageEnhance
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_new3.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src).convert("RGBA")
w, h = img.size

# Quitar fondo
corners = [img.getpixel((0,0)), img.getpixel((w-1,0)), img.getpixel((0,h-1)), img.getpixel((w-1,h-1))]
bg_r = sum(c[0] for c in corners) // 4
bg_g = sum(c[1] for c in corners) // 4
bg_b = sum(c[2] for c in corners) // 4
pixels = img.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if abs(r-bg_r)<35 and abs(g-bg_g)<35 and abs(b-bg_b)<35:
            pixels[x, y] = (0, 0, 0, 0)

# Bounding box
alpha = img.split()[3]
bbox = alpha.getbbox()
x1, y1, x2, y2 = bbox

# Canvas cuadrado con el contenido centrado
side = max(x2-x1, y2-y1)
canvas = Image.new("RGBA", (side + 100, side + 100), (0,0,0,0))
cropped = img.crop((x1, y1, x2, y2))
canvas.paste(cropped, ((side+100 - cropped.width)//2, (side+100 - cropped.height)//2))

canvas = ImageEnhance.Contrast(canvas).enhance(1.2)
canvas = ImageEnhance.Sharpness(canvas).enhance(1.3)
canvas = canvas.resize((800, 800), Image.LANCZOS)
canvas.save(dst, "PNG")
print("Done:", canvas.size)
