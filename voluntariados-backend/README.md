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

3. Initialize the database and seed demo data:

   ```bash
   # Reset DB (Django-managed tables)
   python manage.py flush --no-input

   # Apply migrations
   python manage.py migrate

   # Seed complete demo dataset (users, organizaciones, voluntariados, turnos, inscripciones, asistencias, capacitaciones)
   python manage.py init_demo_data --with-superuser
   ```

   Optional flags:

   ```bash
   # Customize volumes
   python manage.py init_demo_data \
     --orgs 3 \
     --vols-per-org 3 \
     --volunteers-per-org 5 \
     --turnos-per-vol 3 \
     --caps-per-vol 2 \
     --with-superuser

   # Use a different admin account
   python manage.py init_demo_data --with-superuser --admin-email admin@example.org --admin-pass "S3cret!"

   # Reset previously generated DEMO data and reseed
   python manage.py init_demo_data --reset --with-superuser
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
