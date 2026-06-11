from PIL import Image, ImageEnhance
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_new3.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src).convert("RGBA")
w, h = img.size

pixels = img.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        pr, pg, pb, pa = pixels[0,0]
        if abs(r-pr)<35 and abs(g-pg)<35 and abs(b-pb)<35:
            pixels[x, y] = (0, 0, 0, 0)

alpha = img.split()[3]
bbox = alpha.getbbox()
x1, y1, x2, y2 = bbox
cw, ch = x2-x1, y2-y1
side = max(cw, ch)
cx, cy = (x1+x2)//2, (y1+y2)//2
nx1=max(0,cx-side//2); ny1=max(0,cy-side//2)
nx2=min(img.width,nx1+side); ny2=min(img.height,ny1+side)

img = img.crop((nx1, ny1, nx2, ny2))
img = ImageEnhance.Contrast(img).enhance(1.2)
img = ImageEnhance.Sharpness(img).enhance(1.3)
img = img.resize((800, 800), Image.LANCZOS)
img.save(dst, "PNG")
print("Done:", img.size)
