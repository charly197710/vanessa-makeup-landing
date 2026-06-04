
from PIL import Image
import sys, os

src = sys.argv[1]
dst = sys.argv[2]

img = Image.open(src)
if img.mode == 'RGBA':
    img = img.convert('RGB')
img.save(dst, "JPEG", quality=92)
print(f"OK: {os.path.basename(src)}")
