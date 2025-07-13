const path = require('path');
const fs   = require('fs/promises');
const { execFile } = require('child_process');

async function runPython(scriptName, inputPath) {
  const scriptPath = path.join(__dirname, '..', 'py-algorithms', `${scriptName}.py`);
  const outFile    = path.join('temp', `${path.parse(inputPath).name}_${scriptName}.png`);

  await fs.mkdir('temp', { recursive: true });

  return new Promise((resolve, reject) => {
    const args = [scriptPath, inputPath, outFile];

    execFile('python', args, { maxBuffer: 10 * 1024 * 1024 }, (error, stdout, stderr) => {
      if (error) {
        console.error('[py] stderr:', stderr);
        return reject(error);
      }

      // pega a última linha não‑vazia da saída
      const lines = stdout.trim().split(/\r?\n/).filter(Boolean);
      const last  = lines.pop();

      try {
        const json = JSON.parse(last);
        if (json.status !== 'ok') return reject(new Error(json.msg));
        resolve(json.out); // caminho absoluto do PNG gerado
      } catch (e) {
        console.error('[py] saída inesperada:', stdout);
        reject(new Error('JSON inválido ou ausente na saída Python'));
      }
    });
  });
}

module.exports = { runPython };
