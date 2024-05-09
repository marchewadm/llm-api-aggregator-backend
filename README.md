# chattyAI

Chatty AI is a tool that allows you to store your chats from various LLMs in one place. Its backend is built on FastAPI, SQLAlchemy for communicating with a PostgreSQL database, and Pydantic for creating schemas.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 15.6 or higher

## Installation

### Clone a repository

```bash
git clone https://github.com/marchewadm/chattyai_backend.git
```

### Navigate to the root directory

```bash
cd chattyai_backend
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

- For Windows by using Powershell:

```bash
./venv/Scripts/Activate.ps1
```

- For Linux:

```bash
source venv/bin/activate
```

### Install all necessary dependencies

```bash
pip install -r requirements/requirements.txt
```

## Before usage

Before running the application, make sure that PostgreSQL is installed and running on your machine.

Then, create a new database. You can call it whatever you wish, it doesn't really matter. However, what really matters is creating a `.env` file in the root directory of the project, otherwise the server won't boot up.

The `.env` file should look like this:

```
DB_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
JWT_SECRET_KEY=YOUR_SECRET_KEY
```

NOTE:<br />Remember to adjust DB_URL according to your database username and password. If the project is running locally, you should set the host and port as `localhost:5432` (or `127.0.0.1:5432` if it doesn't work) since it is running on your local machine and `5432` is the default port for PostgreSQL.

You can generate the JWT_SECRET_KEY by executing this command in your console:

```bash
openssl rand -hex 32
```

And that's it! Now you can proceed to the next step: running your new, freshly installed and configured app.

## Usage

```bash
# NOTE:
# Command below should be executed from the root directory

uvicorn src.main:app --reload
```

After executing the command, the server should start listening at the address `127.0.0.1:8000`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
