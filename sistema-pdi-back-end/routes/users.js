const express = require('express');
const UsersController = require('../controllers/usersController');
const router = express.Router();

router.post('/', UsersController.createUser);
router.get('/', UsersController.getAllUsers);
router.get('/:id', UsersController.getUserById);
router.post('/login', UsersController.validateUser);


module.exports = router;
