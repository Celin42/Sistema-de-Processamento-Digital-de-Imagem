const express = require('express');

const algorithmsRoutes = require('./routes/algorithms');
const usersRoutes = require('./routes/users');

const router = express.Router();

router.use('/algorithms', algorithmsRoutes);
router.use('/users', usersRoutes);

module.exports = router;
