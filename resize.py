import os, shutil
from pathlib import Path

src = Path(r"D:\\Escritorio\\maquillaje vanessa")
dst = Path(r"C:\\Users\\WIN10\\Desktop\\vanessa-makeup\\photos")
TARGET = 800

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
    print("PIL OK - redimensionando a 800x800")
except ImportError:
    HAS_PIL = False
    print("SIN PIL - copiando tal cual")

if dst.exists():
    shutil.rmtree(dst)
dst.mkdir()

total = 0; ok = 0

for cat, files in cats.items():
    cat_dir = dst / cat
    cat_dir.mkdir()
    cover_name = covers[cat]
    
    cover_src = src / cover_name
    if cover_src.exists():
        cover_dst = cat_dir / "cover.jpg"
        if HAS_PIL:
            try:
                img = Image.open(cover_src)
                w, h = img.size; side = min(w, h)
                x = (w-side)//2; y = (h-side)//2
                img = img.crop((x, y, x+side, y+side))
                img = img.resize((TARGET, TARGET), Image.LANCZOS)
                img.save(cover_dst, "JPEG", quality=85)
                ok += 1
            except Exception as e:
                print(f"ERR {e}")
                shutil.copy2(cover_src, cat_dir / f"cover{cover_src.suffix}")
        else:
            shutil.copy2(cover_src, cat_dir / f"cover{cover_src.suffix}")
        total += 1
    
    i = 1
    for fname in files:
        if fname == cover_name: continue
        fsrc = src / fname
        if not fsrc.exists(): continue
        fdst = cat_dir / f"img{i}.jpg"
        if HAS_PIL:
            try:
                img = Image.open(fsrc)
                w, h = img.size; side = min(w, h)
                x = (w-side)//2; y = (h-side)//2
                img = img.crop((x, y, x+side, y+side))
                img = img.resize((TARGET, TARGET), Image.LANCZOS)
                img.save(fdst, "JPEG", quality=85)
                ok += 1
            except Exception as e:
                shutil.copy2(fsrc, cat_dir / f"img{i}{fsrc.suffix}")
        else:
            shutil.copy2(fsrc, cat_dir / f"img{i}{fsrc.suffix}")
        i += 1; total += 1
    print(f"{cat}: 1 cover + {i-1} gallery")

print(f"DONE: {ok}/{total}")
