# Domus-Backend

O **domus-backend** é o serviço principal de backend de uma aplicação construída com FastAPI e SQLAlchemy, destinada a gerenciar dados em banco PostgreSQL. Este README detalha como configurar, executar e conhecer as dependências do projeto.

## 1. Pré-requisitos

Antes de iniciar, é necessário ter instalado em sua máquina:

* **Python 3.13** ou superior.
* **pipx**, para instalação isolada de ferramentas Python (opcional, mas recomendado para Poetry).
* **Docker** e **Docker Compose**, caso opte por orquestrar via contêineres.

## 2. Instalando o Poetry

Para gerenciar dependências e ambientes virtuais, utilizamos o **Poetry**. A forma recomendada de instalação é via **pipx**, que permite executar pacotes Python em ambientes isolados:

```bash
# 1. Instala o pipx no ambiente do usuário
pip install --user pipx

# 2. Garantir que o diretório do pipx esteja no PATH
pipx ensurepath

# 3. Instala a última versão do Poetry de forma isolada
pipx install poetry

# 4. Adiciona o plugin shell para facilitar o uso do Poetry em subshells
pipx inject poetry poetry-plugin-shell
```

* `pip install --user pipx`: instala o **pipx**, ferramenta para executar pacotes Python em ambientes isolados.
* `pipx ensurepath`: ajusta a variável de ambiente PATH, incluindo o diretório de instalação do pipx.
* `pipx install poetry`: baixa e instala a versão mais recente do **Poetry**.
* `pipx inject poetry poetry-plugin-shell`: instala o plugin `poetry-plugin-shell`, permitindo comandos como `poetry shell`.

## 3. Dependências do Projeto

O projeto utiliza as seguintes bibliotecas em produção, conforme definidas no `pyproject.toml`:

| Dependência        | Versão               |
| ------------------ | -------------------- |
| fastapi\[standard] | >=0.115.12, <0.116.0 |
| sqlalchemy         | >=2.0.41, <3.0.0     |
| pydantic-settings  | >=2.9.1, <3.0.0      |
| psycopg\[binary]   | >=3.2.9, <4.0.0      |
| uvicorn            | (usado via Poetry)   |

As dependências de desenvolvimento, fundamentais para testes e lint, estão listadas abaixo:

| Ferramenta | Versão   |
| ---------- | -------- |
| pytest     | ^8.3.5   |
| pytest-cov | ^6.1.1   |
| ruff       | ^0.11.10 |
| taskipy    | ^1.14.1  |

## 4. Configuração do Ambiente

O projeto espera uma variável de ambiente `DATABASE_URL` seguindo o formato:

```
postgresql+psycopg://app_user:app_password@domus_database:5432/app_db
```
Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```dotenv
URL=postgresql+psycopg://app_user:app_password@domus_database:5432/app_db
```

Ela define as credenciais e o endereço de conexão com o banco PostgreSQL.

## 6. Executando com Docker Compose

O projeto também pode ser executado em contêineres Docker para maior isolamento. A definição dos serviços encontra-se em `docker-compose.yml`.

Para subir o ambiente completo:

```bash
sudo docker compose up --build
```

Isso iniciará:

* **domus\_database** (PostgreSQL)
* **domus\_app** (aplicação FastAPI)

Ambos os serviços estarão acessíveis nas portas 5432 e 8000, respectivamente.
