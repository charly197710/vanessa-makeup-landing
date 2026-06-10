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

# Shrink minimo
cw, ch = x2-x1, y2-y1
x1+=int(cw*0.02); y1+=int(ch*0.02); x2-=int(cw*0.02); y2-=int(ch*0.02)

# Hacer cuadrado
side = max(x2-x1, y2-y1)
cx, cy = (x1+x2)//2, (y1+y2)//2
nx1=max(0,cx-side//2); ny1=max(0,cy-side//2)
nx2=min(img.width,nx1+side); ny2=min(img.height,ny1+side)

img = img.crop((nx1, ny1, nx2, ny2))
img = ImageEnhance.Contrast(img).enhance(1.2)
img = ImageEnhance.Sharpness(img).enhance(1.3)
img = img.resize((1000, 1000), Image.LANCZOS)
img.save(dst, "PNG")
print("Done:", img.size)
