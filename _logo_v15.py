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

# Bounding box del contenido
alpha = img.split()[3]
bbox = alpha.getbbox()
x1, y1, x2, y2 = bbox
print("Content bbox:", bbox)

# Crear un canvas transparente cuadrado grande (1200x1200)
canvas_size = 1200
canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))

# Pegar el contenido centrado con padding
content_w = x2 - x1
content_h = y2 - y1
paste_x = (canvas_size - content_w) // 2
paste_y = (canvas_size - content_h) // 2
cropped = img.crop((x1, y1, x2, y2))
canvas.paste(cropped, (paste_x, paste_y))

print("Canvas:", canvas_size, "x", canvas_size)

# Mejorar
canvas = ImageEnhance.Contrast(canvas).enhance(1.2)
canvas = ImageEnhance.Sharpness(canvas).enhance(1.3)

# Redimensionar a 500x500
canvas = canvas.resize((500, 500), Image.LANCZOS)
canvas.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", canvas.size)
