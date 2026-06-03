import os, shutil
from pathlib import Path

src = Path(r"D:\\Escritorio\\maquillaje vanessa")
dst = Path(r"C:\\Users\\WIN10\\Desktop\\vanessa-makeup\\photos")

covers = {
    "15-anios": "15 años01.png",
    "novias": "novia02.png",
    "noche-glam": "noche glam 10.png",
    "artistico": "artistico7.png",
    "hallowen": "hallowen9.png",
    "peinados": "peinados7.jpeg"
}

cats = {
    "15-anios": ["15 años 013.png","15 años.jpeg","15 años.jpg","15 años01.png","15 años010.png","15 años02.png","15 años03.png","15 años04.png","15 años05.png","15 años06.png","15 años07.png","15 años08.png","15 años09.png","15 años1.jpg","15 años10.jpg","15 años11.jpg","15 años12.jpg","15 años14.jpg","15 años15.jpg","15 años2.jpg","15 años3.jpg","15 años4.jpg","15 años5.jpg","15 años6.jpg","15 años7.jpg","15 años8.jpg","15 años9.jpg"],
    "novias": ["novia01.png","novia02.png","novia03.png","novia04.png","novia05.png","novia07.png","novia08.png","novia09.png","novias.jpg","novias1.jpg","novias10.jpg","novias2.jpg","novias3.jpg","novias4.jpg","novias5.jpg","novias6.jpg","novias7.jpg","novias8.jpg","novias9.jpg"],
    "noche-glam": ["noche galm 8.jpg","noche glam 10.png","noche glam.jpg","noche glam1.jpg","noche glam2.jpg","noche glam3.jpg","noche glam4.jpg","noche glam5.jpg","noche glam6.jpg","noche glam7.jpg"],
    "artistico": ["artistico.jpg","artistico1.jpg","artistico10.jpg","artistico11.jpg","artistico12.jpg","artistico13.jpg","artistico14.jpg","artistico2.jpg","artistico3.jpg","artistico4.png","artistico5.png","artistico7.png","artistico8.png","artistico9.jpg"],
    "hallowen": ["hallowen.jpg","hallowen1.jpg","hallowen10.png","hallowen2.jpg","hallowen3.jpg","hallowen4.jpg","hallowen5.jpg","hallowen7.jpg","hallowen8.jpg","hallowen9.png"],
    "peinados": ["peinados.jpeg","peinados1.jpeg","peinados2.jpeg","peinados4.jpeg","peinados5.jpeg","peinados6.jpeg","peinados7.jpeg"]
}

try:
    from PIL import Image
    HAS_PIL = True
    print("PIL OK")
except ImportError:
    HAS_PIL = False
    print("SIN PIL")

if dst.exists():
    shutil.rmtree(dst)
dst.mkdir()

MAX_HD = 1920
QUALITY = 92

def process_img(src_path, dst_path):
    """Redimensiona a Full HD manteniendo aspect ratio si es muy grande"""
    if not HAS_PIL:
        shutil.copy2(src_path, dst_path)
        return True
    try:
        img = Image.open(src_path)
        w, h = img.size
        
        # Solo redimensionar si es mas grande que Full HD
        if w > MAX_HD or h > MAX_HD:
            ratio = min(MAX_HD / w, MAX_HD / h)
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
        
        # Convertir a RGB si necesario (para guardar como JPEG)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        img.save(dst_path, "JPEG", quality=QUALITY)
        return True
    except Exception as e:
        print(f"ERR: {e}")
        shutil.copy2(src_path, dst_path)
        return False

total = 0; ok = 0

for cat, files in cats.items():
    cat_dir = dst / cat
    cat_dir.mkdir()
    cover_name = covers[cat]
    
    # Cover
    cover_src = src / cover_name
    if cover_src.exists():
        cover_dst = cat_dir / "cover.jpg"
        if process_img(cover_src, cover_dst):
            ok += 1
        total += 1
        print(f"COVER {cat}: {cover_name} -> {os.path.getsize(cover_dst)//1024}KB")
    
    # Gallery
    i = 1
    for fname in files:
        if fname == cover_name: continue
        fsrc = src / fname
        if not fsrc.exists(): continue
        fdst = cat_dir / f"img{i}.jpg"
        if process_img(fsrc, fdst):
            ok += 1
        i += 1
        total += 1
    print(f"{cat}: 1 cover + {i-1} gallery")

print(f"DONE: {ok}/{total}")
