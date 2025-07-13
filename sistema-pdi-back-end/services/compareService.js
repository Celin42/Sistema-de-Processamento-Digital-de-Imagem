const sharp = require('sharp');

async function compareImages(img1, img2) {
  // carrega raw de ambas as imagens
  const [ref, stud] = await Promise.all([
    sharp(img1).raw().toBuffer({ resolveWithObject: true }),
    sharp(img2).raw().toBuffer({ resolveWithObject: true }),
  ]);

  // checa largura, altura e canais
  if (
    ref.info.width   !== stud.info.width  ||
    ref.info.height  !== stud.info.height ||
    ref.info.channels!== stud.info.channels
  ) {
    throw new Error('Dimensões das imagens não conferem.');
  }

  // calcula RMSE
  const a = ref.data, b = stud.data;
  let sumSq = 0;
  for (let i = 0; i < a.length; i++) {
    const d = a[i] - b[i];
    sumSq += d * d;
  }
  return Math.sqrt(sumSq / a.length);
}

module.exports = { compareImages };



