
from PIL import Image
import os

# Usar el archivo CON FONDO REMOVIDO
src = r"C:\Users\WIN10\Desktop\vanessa-makeup\..\..\..\..\descargas\ChatGPT_Image_27_may_2026__18_33_31-removebg-preview.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src)
print("Original:", img.size, "Mode:", img.mode)

# Verificar si tiene transparencia
if img.mode == 'RGBA':
    alpha = img.split()[3]
    bbox = alpha.getbbox()
    if bbox:
        x1, y1, x2, y2 = bbox
        print("Content bbox:", bbox)
        print("Content size:", x2-x1, "x", y2-y1)
        
        # Crop al contenido + padding
        padding = 30
        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(img.width, x2 + padding)
        y2 = min(img.height, y2 + padding)
        
        # Hacer cuadrado
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
        
        print("Crop:", x1, y1, "to", x2, y2)
        img = img.crop((x1, y1, x2, y2))

# Redimensionar a 800x800
img = img.resize((800, 800), Image.LANCZOS)
img.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", img.size)
