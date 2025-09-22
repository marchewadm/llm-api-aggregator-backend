# LLM API Aggregator (Backend)

LLM API Aggregator is a tool that allows you to store your chats from various LLMs in one place, making it easier to manage them.
Its backend is built on FastAPI, SQLAlchemy for communicating with a PostgreSQL database along with Alembic for migrations, Redis for caching and Pydantic for performing data validation.

The repository with the application's frontend is located at [this link](https://github.com/marchewadm/llm-api-aggregator-frontend). Make sure to set it up if you want to use it with a user interface.

## Table Of Contents

- [Demo](#demo)
- [Supported APIs](#supported-apis)
- [Prerequisites](#prerequisites)
- [Before Usage](#before-usage)
  - [Note](#note)
  - [.env.docker-example](#envdocker-example)
  - [.env.example](#envexample)
- [Installation](#installation)
  - [Cloning The Repository](#cloning-the-repository)
    - [Running The Project Via Docker Compose (Recommended)](#running-the-project-via-docker-compose-recommended)
    - [Running The Project Without Docker](#running-the-project-without-docker)
- [License](#license)

## Demo

https://github.com/user-attachments/assets/4d0dd8c1-d570-44ac-9942-9cd799fb8c0c

## Supported APIs

- OpenAI
- Google Gemini

## Prerequisites

- Project was develoepd using **Python 3.12**, **PostgreSQL 15.6** and **Redis 7.2.5**.
- **Docker** - it is not required, but highly recommended to simplify the installation of all dependencies and minimize manual configuration, using Docker Compose.

## Before Usage

Before installing the application, make sure that a `.env` file is created. To populate the `.env` file, you can use either the `.env.docker-example` or `.env.example` as a template. Copy the contents of example file to `.env` and fill in the required values.

### Note:

- Remember to adjust DATABASE_URL according to your database username and password. If the project is running locally, you should set the host and port as `localhost:5432` (or `127.0.0.1:5432` if it doesn't work) since it is running on your local machine and `5432` is the default port for PostgreSQL.

- The REDIS_SERVER_HOST and REDIS_SERVER_PORT variables should be set to the address and port of your Redis server. If you are running Redis locally, you should set it to `localhost` and `6379` respectively.

- The ALLOWED_ORIGIN variable should be set to the address of the API consumer. If you are running the frontend locally, you should set it to `http://localhost:5173` as it is the default address for the frontend running on Vite.

- You can generate JWT_AUTH_SECRET_KEY by executing this command in your console:

  ```bash
  openssl rand -hex 32
  ```

- To generate FERNET_MASTER_KEY, you can use the following code snippet, e.g. in Python console:
  ```bash
  >>> from cryptography.fernet import Fernet
  >>> key = Fernet.generate_key()
  >>> key.decode()
  'YwBQY5h4XpXiFsffgrq-RJmZerMmAvjHFVgY4e9hx48='
  ```
  Then you should copy the key as `YwBQY5h4XpXiFsffgrq-RJmZerMmAvjHFVgY4e9hx48=` (without the quotes) and paste it into the `.env` file.

### `.env.docker-example`

Values in this file, compared to `.env.example`, are mostly prepared to work in a local environment.

```bash
POSTGRES_USER=postgres
# Remember to change the password ;)
POSTGRES_PASSWORD=topsecretpassword
POSTGRES_DB=llm-api-aggregator

REDIS_SERVER_HOST=redis
REDIS_SERVER_PORT=6379

# Docker image of the frontend runs on host 3000
ALLOWED_ORIGIN=http://localhost:3000

AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY
AWS_REGION=YOUR_AWS_REGION
AWS_S3_BUCKET_NAME=YOUR_S3_BUCKET_NAME

JWT_AUTH_SECRET_KEY=YOUR_GENERATED_AUTH_SECRET_KEY
FERNET_MASTER_KEY=YOUR_GENERATED_FERNET_MASTER_KEY
```

### `.env.example`

```bash
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE

REDIS_SERVER_HOST=YOUR_REDIS_SERVER_URL
REDIS_SERVER_PORT=YOUR_REDIS_SERVER_PORT

ALLOWED_ORIGIN=YOUR_API_CONSUMER

AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY
AWS_REGION=YOUR_AWS_REGION
AWS_S3_BUCKET_NAME=YOUR_S3_BUCKET_NAME

JWT_AUTH_SECRET_KEY=YOUR_GENERATED_AUTH_SECRET_KEY
FERNET_MASTER_KEY=YOUR_GENERATED_FERNET_MASTER_KEY
```

## Installation

### Cloning The Repository

```bash
git clone https://github.com/marchewadm/llm-api-aggregator-backend.git
cd llm-api-aggregator-backend
```

#### Running The Project Via Docker Compose (Recommended)

1. **Build Docker Image**

```bash
docker compose build
```

2. **Run The Container**

```bash
docker compose up -d
```

3. **Stop The Container**

```bash
docker compose down
```

#### Running The Project Without Docker

1. **Create Virtual Environment**

```bash
python -m venv venv
```

2. **Activate Virtual Environment**

- For Windows by using Powershell:

```bash
./venv/Scripts/Activate.ps1
```

- For GNU/Linux and macOS by using bash shell:

```bash
source venv/bin/activate
```

3. **Install All Necessary Dependencies**

```bash
pip install -r requirements/requirements.txt
```

4. **Running Migrations**

```bash
alembic upgrade head
```

5. **Initializing API Providers**

Once the database tables have been created, run the following command from the root directory to execute the script that will initialize the API providers in the database:

```bash
python -m src.core.init_api_providers
```

And that's it! Now you can proceed to the next step: running your new, freshly installed and configured app.

6. **Usage**

```bash
# NOTE:
# Command below should be executed from the root directory

uvicorn src.main:app --reload
```

After executing the command, the server should start listening at the address `127.0.0.1:8000`.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
