const sharp=require('sharp'),fs=require('fs'),path=require('path');
const src='D:\Escritorio\maquillaje vanessa';
const dst='C:\Users\WIN10\Desktop\vanessa-makeup\photos';
if(fs.existsSync(dst))fs.rmSync(dst,{recursive:true});
fs.mkdirSync(dst,{recursive:true});
const cats={
  '15-anios':{cover:'15 años01.png',files:['15 años 013.png','15 años.jpeg','15 años.jpg','15 años01.png','15 años010.png','15 años02.png','15 años03.png','15 años04.png','15 años05.png','15 años06.png','15 años07.png','15 años08.png','15 años09.png','15 años1.jpg','15 años10.jpg','15 años11.jpg','15 años12.jpg','15 años14.jpg','15 años15.jpg','15 años2.jpg','15 años3.jpg','15 años4.jpg','15 años5.jpg','15 años6.jpg','15 años7.jpg','15 años8.jpg','15 años9.jpg']},
  'novias':{cover:'novia01.png',files:['novia01.png','novia02.png','novia03.png','novia04.png','novia05.png','novia07.png','novia08.png','novia09.png','novias.jpg','novias1.jpg','novias10.jpg','novias2.jpg','novias3.jpg','novias4.jpg','novias5.jpg','novias6.jpg','novias7.jpg','novias8.jpg','novias9.jpg']},
  'noche-glam':{cover:'noche glam 10.png',files:['noche galm 8.jpg','noche glam 10.png','noche glam.jpg','noche glam1.jpg','noche glam2.jpg','noche glam3.jpg','noche glam4.jpg','noche glam5.jpg','noche glam6.jpg','noche glam7.jpg']},
  'artistico':{cover:'artistico4.png',files:['artistico.jpg','artistico1.jpg','artistico10.jpg','artistico11.jpg','artistico12.jpg','artistico13.jpg','artistico14.jpg','artistico2.jpg','artistico3.jpg','artistico4.png','artistico5.png','artistico7.png','artistico8.png','artistico9.jpg']},
  'hallowen':{cover:'hallowen9.png',files:['hallowen.jpg','hallowen1.jpg','hallowen10.png','hallowen2.jpg','hallowen3.jpg','hallowen4.jpg','hallowen5.jpg','hallowen7.jpg','hallowen8.jpg','hallowen9.png']},
  'peinados':{cover:'peinados.jpeg',files:['peinados.jpeg','peinados1.jpeg','peinados2.jpeg','peinados4.jpeg','peinados5.jpeg','peinados6.jpeg','peinados7.jpeg']}
};
async function proc(srcP,dstP){
  try{
    const img=sharp(srcP),m=await img.metadata();
    let p=img;
    if(m.width>1200||m.height>1200)p=p.resize(1200,1200,{fit:'inside',withoutEnlargement:true});
    await p.jpeg({quality:85,mozjpeg:true}).toFile(dstP);
    return true;
  }catch(e){console.error('ERR:'+path.basename(srcP)+' '+e.message);return false;}
}
(async()=>{
  let total=0,ok=0;
  for(const[cat,data]of Object.entries(cats)){
    const cDir=path.join(dst,cat);fs.mkdirSync(cDir,{recursive:true});
    console.log('\n'+cat);
    for(let i=0;i<data.files.length;i++){
      const fn=data.files[i],sP=path.join(src,fn);
      if(!fs.existsSync(sP)){console.log('SKIP:'+fn);continue;}
      const isCov=fn===data.cover;
      const oN=isCov?'cover.jpg':'img'+(i+1)+'.jpg';
      const dP=path.join(cDir,oN);
      if(await proc(sP,dP)){
        console.log('OK:'+oN+' '+Math.round(fs.statSync(dP).size/1024)+'KB');ok++;
      }total++;
    }
  }
  console.log('\nDONE:'+ok+'/'+total);
})();
