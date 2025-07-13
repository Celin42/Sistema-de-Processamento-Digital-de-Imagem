# Sistema PDI

Plataforma web para ensino de Processamento Digital de Imagens (PDI).  
Permite que alunos façam upload de uma imagem original e de sua própria implementação de um algoritmo, comparem resultados via RMSE e, se a similaridade for satisfatória, recebam o código‑fonte como feedback.

---

## 📋 Sumário

- [Pré-requisitos](#pré-requisitos)  
- [Estrutura do Projeto](#estrutura-do-projeto)  
- [Configuração do Banco de Dados](#configuração-do-banco-de-dados)  
- [Instalação e Execução](#instalação-e-execução)  
  - [Backend](#backend)  
  - [Frontend](#frontend)  
- [Uso](#uso)  
- [Algoritmos Disponíveis](#algoritmos-disponíveis)

---

## ✅ Pré-requisitos

- Node.js (v14+): https://nodejs.org/  
- Python (3.7+): https://www.python.org/  
- PostgreSQL (v12+): https://www.postgresql.org/  

---

## 🗂️ Estrutura do Projeto

```
root/
├── sistema-pdi-back-end/       # Backend (Node.js + Express + scripts Python)
│   ├── py-algorithms/         # Scripts Python (OpenCV)
│   ├── routes/                # Definição de rotas Express
│   ├── services/              # pythonRunner.js, compareService.js
│   ├── models/                # db.js, userModel.js
│   ├── middleware/            # upload.js (Multer)
│   ├── temp/                  # Saída temporária (auto)
│   ├── uploads/               # Uploads de usuários (auto)
│   ├── .env                   # Variáveis de ambiente
│   └── server.js              # Ponto de entrada
└── sistema-pdi-front-end/      # Frontend (Vue.js)
    ├── src/
    │   ├── components/        # Header, Footer, FormInput
    │   ├── views/             # home-page, login, register
    │   ├── auth/              # auth-state.js
    │   ├── routes.js          # Rotas Vue
    │   └── main.js            # Bootstrap Vue
    ├── public/
    └── package.json
```

---

## 🛠️ Configuração do Banco de Dados

1. No PostgreSQL, crie o banco:
   ```sql
   CREATE DATABASE sistema_pdi;
   ```

2. Crie a tabela de usuários:
   ```sql
   CREATE TABLE users (
     id SERIAL PRIMARY KEY,
     matricula VARCHAR(50) NOT NULL,
     email VARCHAR(100) NOT NULL UNIQUE,
     senha VARCHAR(255) NOT NULL
   );
   ```

3. Em `sistema-pdi-backend/.env`, configure suas variáveis:

   ```
   DB_USER=seu_usuario
   DB_HOST=localhost
   DB_DATABASE=sistema_pdi
   DB_PASSWORD=sua_senha
   DB_PORT=5432
   ```

---

## 🚀 Instalação e Execução

### Backend

```bash
cd sistema-pdi-back-end
npm install

# (Opcional) Criar ambiente virtual Python
python -m venv venv

# Ativar ambiente:
# Linux/Mac:
source venv/bin/activate
# Windows:
.env\Scriptsctivate

pip install opencv-python numpy

npm run dev  # ou node server.js
```

> O backend estará disponível em: [http://localhost:3000/api/](http://localhost:3000/api/)

---

### Frontend

```bash
cd sistema-pdi-front-end
npm install
npm run serve
```

> O frontend estará disponível em: [http://localhost:8080/](http://localhost:8080/)

---

## 🧪 Uso

1. Acesse: http://localhost:8080/  
2. Registre-se com matrícula, e-mail e senha  
3. Faça login  
4. Faça upload da imagem Original e da imagem Student (sua implementação)  
5. Escolha o algoritmo e clique em **Processar**  
6. O RMSE será calculado. Se for menor que o limiar, o código-fonte será exibido  

---

## 🧠 Algoritmos Disponíveis

- Negativo  
- Tons de Cinza (Grayscale)  
- Otsu  
- Canny  
- Sobel  
- Suavização Gaussiana  
- Filtro da Média (Mean Filter)  
- Filtro de Realce (Sharpen)  
- Filtro de Realce Genérico (Unsharp Mask)  
- Espelhamento (Mirror)  
- Transposta  
- Rotação 90°  
- Equalização de Histograma  

---
