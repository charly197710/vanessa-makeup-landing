const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const src = 'D:\\Escritorio\\maquillaje vanessa';
const dst = 'C:\\Users\\WIN10\\Desktop\\vanessa-makeup\\photos';

// Nuevas portadas especificas
const newCovers = {
  '15-anios': '15 años01.png',
  'novias': 'novia02.png',
  'noche-glam': 'noche glam 10.png',
  'artistico': 'artistico7.png',
  'hallowen': 'hallowen9.png',
  'peinados': 'peinados7.jpeg'
};

// Categorias con TODOS sus archivos
const categories = {
  '15-anios': ['15 años 013.png','15 años.jpeg','15 años.jpg','15 años01.png','15 años010.png','15 años02.png','15 años03.png','15 años04.png','15 años05.png','15 años06.png','15 años07.png','15 años08.png','15 años09.png','15 años1.jpg','15 años10.jpg','15 años11.jpg','15 años12.jpg','15 años14.jpg','15 años15.jpg','15 años2.jpg','15 años3.jpg','15 años4.jpg','15 años5.jpg','15 años6.jpg','15 años7.jpg','15 años8.jpg','15 años9.jpg'],
  'novias': ['novia01.png','novia02.png','novia03.png','novia04.png','novia05.png','novia07.png','novia08.png','novia09.png','novias.jpg','novias1.jpg','novias10.jpg','novias2.jpg','novias3.jpg','novias4.jpg','novias5.jpg','novias6.jpg','novias7.jpg','novias8.jpg','novias9.jpg'],
  'noche-glam': ['noche galm 8.jpg','noche glam 10.png','noche glam.jpg','noche glam1.jpg','noche glam2.jpg','noche glam3.jpg','noche glam4.jpg','noche glam5.jpg','noche glam6.jpg','noche glam7.jpg'],
  'artistico': ['artistico.jpg','artistico1.jpg','artistico10.jpg','artistico11.jpg','artistico12.jpg','artistico13.jpg','artistico14.jpg','artistico2.jpg','artistico3.jpg','artistico4.png','artistico5.png','artistico7.png','artistico8.png','artistico9.jpg'],
  'hallowen': ['hallowen.jpg','hallowen1.jpg','hallowen10.png','hallowen2.jpg','hallowen3.jpg','hallowen4.jpg','hallowen5.jpg','hallowen7.jpg','hallowen8.jpg','hallowen9.png'],
  'peinados': ['peinados.jpeg','peinados1.jpeg','peinados2.jpeg','peinados4.jpeg','peinados5.jpeg','peinados6.jpeg','peinados7.jpeg']
};

const TARGET = 800; // tamaño uniforme
const QUALITY = 85;

async function process(srcPath, dstPath) {
  try {
    await sharp(srcPath)
      .resize(TARGET, TARGET, { fit: 'cover', position: 'center' })
      .jpeg({ quality: QUALITY, mozjpeg: true })
      .toFile(dstPath);
    return true;
  } catch (e) {
    console.error('ERR:' + path.basename(srcPath) + ' ' + e.message);
    return false;
  }
}

(async () => {
  let total = 0, ok = 0;

  for (const [cat, files] of Object.entries(categories)) {
    const catDir = path.join(dst, cat);
    // Limpiar carpeta existente
    if (fs.existsSync(catDir)) fs.rmSync(catDir, { recursive: true });
    fs.mkdirSync(catDir, { recursive: true });

    const coverName = newCovers[cat];
    let coverWritten = false;

    // Procesar cover primero
    const coverSrc = path.join(src, coverName);
    if (fs.existsSync(coverSrc)) {
      const coverDst = path.join(catDir, 'cover.jpg');
      if (await process(coverSrc, coverDst)) {
        const size = fs.statSync(coverDst).size;
        console.log('COVER ' + cat + ': ' + coverName + ' -> cover.jpg (' + Math.round(size / 1024) + 'KB)');
        coverWritten = true;
        ok++;
        total++;
      }
    }

    // Procesar galeria (todas las demas)
    let imgIdx = 1;
    for (const fname of files) {
      if (fname === coverName) continue; // Skip cover
      const fSrc = path.join(src, fname);
      if (!fs.existsSync(fSrc)) continue;
      const fDst = path.join(catDir, 'img' + imgIdx + '.jpg');
      if (await process(fSrc, fDst)) {
        imgIdx++;
        ok++;
      }
      total++;
    }
    console.log(cat + ': 1 cover + ' + (imgIdx - 1) + ' galeria');
  }

  console.log('\nDONE: ' + ok + '/' + total + ' imagenes procesadas a ' + TARGET + 'x' + TARGET);
})();
