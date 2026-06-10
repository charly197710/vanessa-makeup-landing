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

# Shrink minimo 1%
cw, ch = x2-x1, y2-y1
sx = int(cw*0.01)
sy = int(ch*0.01)
x1+=sx; y1+=sy; x2-=sx; y2-=sy

# Hacer cuadrado centrado
side = max(x2-x1, y2-y1)
cx, cy = (x1+x2)//2, (y1+y2)//2
half = side//2
nx1=max(0,cx-half); ny1=max(0,cy-half)
nx2=min(img.width,nx1+side); ny2=min(img.height,ny1+side)

print("Crop:", nx1, ny1, "to", nx2, ny2, "=", nx2-nx1, "x", ny2-ny1)
img = img.crop((nx1, ny1, nx2, ny2))

# Mejorar
img = ImageEnhance.Contrast(img).enhance(1.2)
img = ImageEnhance.Sharpness(img).enhance(1.3)

# Redimensionar a 500x500
img = img.resize((500, 500), Image.LANCZOS)
img.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", img.size)
