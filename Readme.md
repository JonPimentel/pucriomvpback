# 📡 API de Usuários - Flask + SQLite

Este projeto implementa uma API RESTful em Python utilizando Flask, com suporte a operações CRUD de usuários e seus respectivos endereços. Também conta com documentação Swagger e persistência de dados via SQLite.

## 🚀 Funcionalidades

- Cadastrar usuário (com endereço)
- Buscar todos os usuários
- Buscar usuário por ID
- Deletar usuário
- Documentação Swagger acessível via /apidocs

## 🧰 Tecnologias

- Python 3.10+
- Flask
- SQLite
- SQLAlchemy
- Flasgger (Swagger UI)
- Flask-CORS

---

## 🛠️ Instruções de Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/api-flask-usuarios.git
cd api-flask-usuarios

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt

python app.py