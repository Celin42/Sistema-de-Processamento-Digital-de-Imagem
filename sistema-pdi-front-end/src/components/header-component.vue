<template>
    <header class="header">
        <nav class="navbar">
            <ul class="navbar-links">
                <li><router-link to="/">Início</router-link></li>
                <li v-if="!authState.isLoggedIn"><router-link to="/login">Login</router-link></li>
                <li v-if="!authState.isLoggedIn"><router-link to="/register">Registrar-se</router-link></li>
            </ul>
            <div v-if="authState.isLoggedIn" class="logout-icon" @click="logout" title="Sair">
                <span class="material-icons">logout</span>
            </div>
        </nav>
    </header>
</template>

<script>
import { inject } from 'vue';

export default {
    setup() {
        const authState = inject('authState');

        const logout = () => {
            authState.logout();
            window.location.href = '/';
        };

        return { authState, logout };
    },
};
</script>

<style scoped>
.header {
    background-color: #333;
    padding: 15px 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.navbar-links {
    list-style: none;
    display: flex;
    gap: 20px;
    margin: 0;
    padding: 0;
}

.navbar-links a {
    text-decoration: none;
    color: white;
    font-weight: bold;
    font-size: 16px;
    transition: color 0.3s;
}

.navbar-links a:hover {
    color: #ddd;
}

.logout-icon {
    color: white;
    font-size: 24px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 5px;
    transition: color 0.3s, transform 0.2s;
}

.logout-icon:hover {
    color: #ddd;
    transform: scale(1.1);
}
</style>
