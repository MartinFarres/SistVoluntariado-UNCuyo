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


## Creating and managing users

The first step, is to create the superuser, used to access the admin panel

```bash
python3 manage.py createsuperuser
```

Then enter to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) with the previously set credentials

There you will be able to create new users with the following roles:
- Administativo
- Delegado
- Voluntario

Then exit the admin panel and go to the api login: [http://127.0.0.1:8000/api-auth/login/](http://127.0.0.1:8000/api-auth/login/). There you will be able to log in with any of the users, and depending on the permissions for the role, you will have access to some of the backend api.


## Setting up OAuth
1. After creating the superuser, login into [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
2. Go to [http://127.0.0.1:8000/admin/sites/site/](http://127.0.0.1:8000/admin/sites/site/) and make sure that update `example.com` fields to 127.0.0.1:8000 and Local Dev. The SITE_ID under `base.py` must match the `id` of this site.
3. Create the Social App [http://127.0.0.1:8000/admin/socialaccount/socialapp/](http://127.0.0.1:8000/admin/socialaccount/socialapp/):
    - Provider: Google
    - Provider id: google
    - Name: Google Login
    - Client ID. Go to [https://console.cloud.google.com/auth](https://console.cloud.google.com/auth), Change project, then go to clients and find the client ID.
    - Secret key: You should already have that one, or create a new one.
