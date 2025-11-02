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

## Sending shift reminder emails

A management command is provided to send reminder emails to volunteers one day before their scheduled shift (Turno).

- Dry run (prints what would be sent without dispatching emails):

```bash
python manage.py send_shift_reminders --dry-run
```

- Send real emails for tomorrow:

```bash
python manage.py send_shift_reminders
```

- Test for a specific date (treats the given date as "today" for the command):

```bash
python manage.py send_shift_reminders --date 2025-11-02 --dry-run
```

- Force sending emails even if they were already sent for that shift (useful for testing):

```bash
python manage.py send_shift_reminders --date 2025-11-19 --dry-run --force-send
```

Notes:

- In development the project uses the console email backend by default (see `config/settings/dev.py`), so emails will appear in the terminal.
- Ensure `DEFAULT_FROM_EMAIL` and SMTP settings are configured in production (`config/settings/prod.py`) before running the command in a live environment.

Scheduling (cron example):

```bash
# Run daily at 08:00 using the project's virtualenv and production settings
0 8 * * * /path/to/venv/bin/python /path/to/repo/voluntariados-backend/manage.py send_shift_reminders --settings=config.settings.prod >> /var/log/shift_reminders.log 2>&1
```

## Activation notifications (Convocatoria → Activo)

As of 2025-11-02, acceptance emails are no longer sent when a volunteer is accepted to the convocatoria. Instead, emails are sent once the Voluntariado enters the "Activo" stage. Recipients are all volunteers with InscripcionConvocatoria in ACEPTADO for that Voluntariado.

Command to dispatch pending activation notifications:

```bash
python manage.py send_activation_notifications
```

Notes:

- A notification is sent only once per Voluntariado and tracked via the field `notificacion_activo_enviada_at`.
- The system also triggers this check when a gestionador acepta/rechaza inscripciones, in case resolving pending applications switches the stage from "Preparación" to "Activo".
- For Voluntariados that become active simply by date, schedule the command daily (cron example):

```bash
# Run daily at 07:00 using the project's virtualenv and production settings
0 7 * * * /path/to/venv/bin/python /path/to/repo/voluntariados-backend/manage.py send_activation_notifications --settings=config.settings.prod >> /var/log/activation_notifications.log 2>&1
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
