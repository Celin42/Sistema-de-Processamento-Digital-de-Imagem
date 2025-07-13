const express = require('express');
const path    = require('path');
const fs      = require('fs/promises');

const upload  = require('../middleware/upload');          // passo 3
const { runPython } = require('../services/pythonRunner'); // passo 4
const { compareImages } = require('../services/compareService'); // passo 5

const router = express.Router();

/*
   Configurações
*/
const SUPPORTED = [
  'grayscale',
  'negative',
  'otsu',
  'canny',
  'mirror',
  'transpose',
  'rotate',
  'sobel',
  'gaussian_blur',
  'hist_equalization',
  'mean_filter',
  'sharpen',
  'unsharp_mask',
];

const THRESHOLD = 20

/*
   GET /api/algorithms
 */
router.get('/', (_, res) => {
  res.json({ available: SUPPORTED });
});

/* 
   POST /api/algorithms/:name/compare
*/
router.post('/:name/compare', upload, async (req, res, next) => {
  try {
    console.log('► [alg] requisição recebida');

    const { name } = req.params;

    // valida nome
    if (!SUPPORTED.includes(name)) {
      console.log('► [alg] nome inválido:', name);
      return res.status(400).json({ message: 'Algoritmo inválido.' });
    }

    // valida arquivos
    const original = req.files.original?.[0];
    const student  = req.files.student?.[0];
    if (!original || !student) {
      console.log('► [alg] imagens ausentes');
      return res.status(400).json({ message: 'Envie as duas imagens (original e student).' });
    }

    // passo 1: Python
    console.log('► [alg] chamando Python…');
    const platformOut = await runPython(name, original.path);
    console.log('► [alg] Python OK:', platformOut);

    // passo 2: RMSE
    console.log('► [alg] calculando RMSE…');
    // agora passamos "name" como terceiro argumento
    const rmse = await compareImages(platformOut, student.path);
    console.log('► [alg] RMSE =', rmse);

    const success = rmse <= THRESHOLD;

    // passo 3: lê fonte (se sucesso)
    let sourceCode = null;
    if (success) {
      const srcPath = path.join(__dirname, '..', 'py-algorithms', `${name}.py`);
      sourceCode = await fs.readFile(srcPath, 'utf-8');
      console.log('► [alg] enviando código-fonte');
    }

    // resposta
    console.log('► [alg] enviando resposta JSON');
    return res.json({ rmse, success, sourceCode });

  } catch (err) {
    // qualquer erro cai aqui e evita pendência
    console.error('► [alg] ERRO:', err.message);
    next(err);
  }
});

module.exports = router;
