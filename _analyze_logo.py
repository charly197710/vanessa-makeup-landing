
from PIL import Image
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_original.png"
img = Image.open(src).convert("RGBA")
w, h = img.size

# Analizar fila por fila donde hay contenido
alpha = img.split()[3]

# Encontrar el centro de masa del contenido
total_x = 0; total_y = 0; count = 0
min_x = w; min_y = h; max_x = 0; max_y = 0

for y in range(h):
    for x in range(w):
        if alpha.getpixel((x, y)) > 10:
            total_x += x; total_y += y; count += 1
            if x < min_x: min_x = x
            if y < min_y: min_y = y
            if x > max_x: max_x = x
            if y > max_y: max_y = y

if count > 0:
    cx = total_x // count
    cy = total_y // count
    print(f"Content bbox: ({min_x},{min_y}) to ({max_x},{max_y})")
    print(f"Content size: {max_x-min_x+1}x{max_y-min_y+1}")
    print(f"Center of mass: ({cx},{cy})")
    print(f"Image center: ({w//2},{h//2})")
    print(f"Offset from center: ({cx-w//2},{cy-h//2})")
    
    # Sugerencia de crop centrado en el centro de masa
    side = max(max_x-min_x+1, max_y-min_y+1) + 60  # padding
    half = side // 2
    sx1 = max(0, cx - half)
    sy1 = max(0, cy - half)
    sx2 = min(w, sx1 + side)
    sy2 = min(h, sy1 + side)
    if sx2 - sx1 < side: sx1 = max(0, sx2 - side)
    if sy2 - sy1 < side: sy1 = max(0, sy2 - side)
    print(f"Suggested crop: ({sx1},{sy1}) to ({sx2},{sy2})")
    print(f"Crop size: {sx2-sx1}x{sy2-sy1}")
