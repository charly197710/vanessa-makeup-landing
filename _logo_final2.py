
from PIL import Image
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_nobg.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src)
print("Original:", img.size, "Mode:", img.mode)

# Verificar transparencia
has_alpha = img.mode == 'RGBA'
print("Has alpha:", has_alpha)

if has_alpha:
    alpha = img.split()[3]
    bbox = alpha.getbbox()
    if bbox:
        x1, y1, x2, y2 = bbox
        print("Content bbox:", bbox)
        cw = x2 - x1
        ch = y2 - y1
        print("Content size:", cw, "x", ch)
        
        # Padding del 8%
        pad = int(max(cw, ch) * 0.08)
        x1 = max(0, x1 - pad)
        y1 = max(0, y1 - pad)
        x2 = min(img.width, x2 + pad)
        y2 = min(img.height, y2 + pad)
        
        # Hacer cuadrado centrado
        w = x2 - x1
        h = y2 - y1
        side = max(w, h)
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        half = side // 2
        x1 = max(0, cx - half)
        y1 = max(0, cy - half)
        x2 = min(img.width, x1 + side)
        y2 = min(img.height, y1 + side)
        
        print("Square crop:", x1, y1, "to", x2, y2, "=", x2-x1, "x", y2-y1)
        img = img.crop((x1, y1, x2, y2))
else:
    print("No alpha - checking corners...")
    for name, x, y in [("TL",0,0), ("TR",img.width-1,0), ("BL",0,img.height-1), ("BR",img.width-1,img.height-1)]:
        print("  ", name, ":", img.getpixel((x,y)))

# Redimensionar a 800x800
img = img.resize((800, 800), Image.LANCZOS)
img.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", img.size)
