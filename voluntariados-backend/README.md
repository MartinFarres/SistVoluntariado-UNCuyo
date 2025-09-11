# Voluntariados Backend

Backend Django project for Sistema de Voluntariado UNCuyo.

## Set up

1. Create python virtual environment and install dependencies

    ```bash
    # crear y activar un virtualenv
    python3 -m venv .venv
    source .venv/bin/activate

    # instalar dependencias
    pip install -r requirements.txt
    ```

2. Create a `.env` file with the structure of `.env.example` and fill it's contents

3. Make migrations

    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

## Running

Run the server

```bash
python3 manage.py runserver
```


## Tests

```bash
python3 manage.py test
```