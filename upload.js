const multer = require('multer');
const path   = require('path');
const { v4: uuid } = require('uuid');

const storage = multer.diskStorage({
  destination: 'uploads',
  filename: (_, file, cb) => cb(null, uuid() + path.extname(file.originalname)),
});

module.exports = multer({ storage }).fields([
  { name: 'original', maxCount: 1 },
  { name: 'student',  maxCount: 1 },
]);
