
from PIL import Image, ImageFilter
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_original.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src).convert("RGBA")
w, h = img.size
print(f"Original: {img.size}")

# Crear canal alpha basado en brillo
pixels = img.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        brightness = (r + g + b) / 3
        if brightness < 50:
            pixels[x, y] = (0, 0, 0, 0)

# Encontrar bounding box del contenido
alpha = img.split()[3]
bbox = alpha.getbbox()
if bbox:
    x1, y1, x2, y2 = bbox
    print(f"Raw bbox: {bbox}")
    cw = x2 - x1
    ch = y2 - y1
    print(f"Content: {cw}x{ch}")
    
    # Hacer cuadrado centrado exactamente en el contenido
    side = max(cw, ch)
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    
    # Expandir el crop para incluir todo el logo con padding uniforme
    padding = int(side * 0.05)  # 5% padding
    side = side + (padding * 2)
    
    half = side // 2
    crop_x1 = max(0, cx - half)
    crop_y1 = max(0, cy - half)
    crop_x2 = min(img.width, crop_x1 + side)
    crop_y2 = min(img.height, crop_y1 + side)
    
    # Ajustar si se sale de los limites
    if crop_x2 - crop_x1 < side:
        crop_x1 = max(0, crop_x2 - side)
    if crop_y2 - crop_y1 < side:
        crop_y1 = max(0, crop_y2 - side)
    
    print(f"Final crop: ({crop_x1},{crop_y1}) to ({crop_x2},{crop_y2})")
    print(f"Crop size: {crop_x2-crop_x1}x{crop_y2-crop_y1}")
    
    img = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))

# Redimensionar a 800x800 con maxima calidad
img = img.resize((800, 800), Image.LANCZOS)
img.save(dst, "PNG")
print(f"Saved: {os.path.getsize(dst)//1024}KB - {img.size}")
