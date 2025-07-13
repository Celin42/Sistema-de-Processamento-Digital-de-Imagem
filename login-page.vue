<template>
    <div class="login-page">
        <header-component />
        <main class="main-content">
            <div class="form-container">
                <h1>Login</h1>
                <form @submit.prevent="handleLogin">
                    <form-input-component 
                        label="Email" 
                        type="email" 
                        id="email" 
                        placeholder="Digite seu email" 
                        v-model="email" 
                    />
                    <form-input-component 
                        label="Senha" 
                        type="password" 
                        id="password" 
                        placeholder="Digite sua senha" 
                        v-model="password" 
                    />
                    <button type="submit">Entrar</button>
                </form>
            </div>
        </main>
        <footer-component />
    </div>
</template>

<script>
import { inject } from 'vue';
import HeaderComponent from '../components/header-component.vue';
import FooterComponent from '../components/footer-component.vue';
import FormInputComponent from '../components/form-input-component.vue';

export default {
    components: { HeaderComponent, FooterComponent, FormInputComponent },
    data() {
        return {
            email: '',
            password: '',
            authState: inject('authState'),
        };
    },
    methods: {
        async handleLogin() {
            try {
                const response = await fetch('http://localhost:3000/api/users/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: this.email, senha: this.password }),
                });

                const data = await response.json();

                if (response.ok) {
                    this.authState.login({ name: data.name });
                    localStorage.setItem('token', data.token);
                    this.$router.push('/');
                } else {
                    alert(data.message || 'Erro ao fazer login.');
                }
            } catch (error) {
                console.error('Erro ao logar:', error);
                alert('Erro de conexão. Tente novamente.');
            }
        },
    },
};
</script>

<style scoped>
.login-page {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 100vh;
    background-color: #aaaaaa;
}

.main-content {
    display: flex;
    justify-content: center;
    align-items: center;
    flex: 1;
    padding: 20px;
}

.form-container {
    background-color: #ddd;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); 
    width: 100%;
    max-width: 380px;
    text-align: left;
    /* border: 1px solid #a6a6a6;*/
}

.form-container h1 {
    font-size: 24px;
    margin-bottom: 10px;
    color: #333;
    font-weight: 600;
    text-align: center;
}

form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

form label {
    font-size: 14px;
    text-align: left;
    margin-bottom: 8px;
    color: #666;
    font-weight: 500;
}

input {
    font-size: 16px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    outline: none;
    transition: border-color 0.3s;
}

input:focus {
    border-color: #333;
}

button {
    padding: 12px 15px;
    background-color: #333;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
}

button:hover {
    background-color: #555;
    transform: scale(1.02);
}

button:active {
    transform: scale(0.98);
}
</style>


