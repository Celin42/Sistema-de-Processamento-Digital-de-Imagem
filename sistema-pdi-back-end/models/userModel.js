const pool = require('./db');

const UserModel = {
    createUser: async (matricula, email, senha) => {
        const query = `INSERT INTO users (matricula, email, senha) VALUES ($1, $2, $3) RETURNING *`;
        const values = [matricula, email, senha];
        const result = await pool.query(query, values);
        return result.rows[0];
    },

    getAllUsers: async () => {
        const result = await pool.query('SELECT * FROM users');
        return result.rows;
    },

    getUserById: async (id) => {
        const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
        return result.rows[0];
    },

    findUserByEmail: async (email) => {
        const query = 'SELECT * FROM users WHERE email = $1';
        const values = [email];
        const result = await pool.query(query, values);
        return result.rows[0];
    }
};

module.exports = UserModel;
