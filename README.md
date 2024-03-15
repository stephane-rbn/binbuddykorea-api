# binbuddykorea-api
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python 3.12.2](https://img.shields.io/badge/python-3.12.2-blue.svg)](https://www.python.org/downloads/release/python-312/)

## Project setup

- Clone project via CLI: `git clone git@github.com:stephane-rbn/binbuddykorea-api.git`
- Enter project folder: `cd binbuddykorea-api`

> **Note:** This project does not use Docker yet but it will be added in the future. For now, you need to have Python and PostgreSQL installed on your machine.

### Install dependencies using [Pipenv](https://github.com/pypa/pipenv) and Pipfile

- On macOS, you can install Pipenv via [homebrew](https://brew.sh/): `brew install pipenv`
- (If python is already globally installed on your machine, you can also run `pip install pipenv` instead)
- Install project dependencies based on Pipfile: `pipenv install`
- Activate virtual environment: `pipenv shell` (to deactivate a virtual environment: `exit`)

### Setup PostgreSQL database
- Install PostgreSQL on your machine (you can use [Postgres.app](https://postgresapp.com/) on macOS)
- Create a new database called "BinBuddyKorea" (you can use [pgAdmin](https://www.pgadmin.org/download/) to create a new database)
- Create a new `.env` file in the root of the project and add the following environment variables:
  ```bash
  DB_USER=postgres # or the user you use to connect to your database
  DB_PASSWORD=root # or the password you use to connect to your database
  DB_HOSTNAME=localhost # or the hostname you use to connect to your database
  DB_PORT=5432 # or the port you use to connect to your database
  DB_NAME=BinBuddyKorea # or the name of the database you created
  ```
- Run the database migrations to build the database schema: `alembic upgrade head`
- Finally, you can run the project using the following command: `uvicorn main:app --reload`

That's it. You're ready to go! ✅

If needed, you can also install additional dependencies using pipenv. For example:
- Install additional dependencies: `pipenv install <package-name>`
- Install additional development dependencies: `pipenv install --dev <package-name>`

### API Database Diagram ([link to project](https://dbdiagram.io/d/BinBuddyKorea-API-65ddbb645cd0412774e91ee1))

![API Database Diagram](db-diagram.png)

### Code conventions

- Use [ruff](https://github.com/astral-sh/ruff) for code linting and formatting.
