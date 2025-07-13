const UserModel = require('../models/userModel');
const bcrypt = require('bcrypt');

const UsersController = {
    createUser: async (req, res) => {
        try {
            const { matricula, email, senha } = req.body;

            if (!matricula || !email || !senha) {
                return res.status(400).json({ message: 'Campos obrigatórios faltando.' });
            }

            const hashedPassword = await bcrypt.hash(senha, 10);

            const newUser = await UserModel.createUser(matricula, email, hashedPassword);
            res.status(201).json(newUser);
        } catch (error) {
            console.error(error);
            res.status(500).json({ message: 'Erro ao criar usuário.' });
        }
    },

    getAllUsers: async (req, res) => {
        try {
            const users = await UserModel.getAllUsers();
            res.status(200).json(users);
        } catch (error) {
            console.error(error);
            res.status(500).json({ message: 'Erro ao buscar usuários.' });
        }
    },

    getUserById: async (req, res) => {
        try {
            const { id } = req.params;
            const user = await UserModel.getUserById(id);
            if (user) {
                res.status(200).json(user);
            } else {
                res.status(404).json({ message: 'Usuário não encontrado.' });
            }
        } catch (error) {
            console.error(error);
            res.status(500).json({ message: 'Erro ao buscar usuário.' });
        }
    },

    validateUser: async (req, res) => {
        try {
            const { email, senha } = req.body;
    
            if (!email || !senha) {
                return res.status(400).json({ message: 'Email e senha são obrigatórios.' });
            }
    
            const user = await UserModel.findUserByEmail(email);
            if (!user) {
                return res.status(404).json({ message: 'Usuário não encontrado.' });
            }
    
            const isPasswordValid = await bcrypt.compare(senha, user.senha);
            if (!isPasswordValid) {
                return res.status(401).json({ message: 'Senha incorreta.' });
            }
    
            res.status(200).json({
                message: 'Usuário validado com sucesso!',
                name: user.matricula || user.email,
            });
        } catch (error) {
            console.error(error);
            res.status(500).json({ message: 'Erro ao validar usuário.' });
        }
    },
};

module.exports = UsersController;
