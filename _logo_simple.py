
from PIL import Image
import os

# Usar la imagen con fondo removido que ya existe
src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_original.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src)
print(f"Original: {img.size}, Mode: {img.mode}")

# Simplemente redimensionar a 800x800 manteniendo la imagen completa
# No hacer ningun recorte - la imagen ya tiene el fondo removido
img = img.resize((800, 800), Image.LANCZOS)

# Guardar como PNG para mantener transparencia
img.save(dst, "PNG")
print(f"Saved: {os.path.getsize(dst)//1024}KB - {img.size}")
