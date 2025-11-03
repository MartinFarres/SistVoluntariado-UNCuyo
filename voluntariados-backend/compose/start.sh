#!/bin/bash
set -euo pipefail

# Default schedule: every day at 08:00
CRON_SCHEDULE_SHIFT_REMINDERS=${CRON_SCHEDULE_SHIFT_REMINDERS:-"0 8 * * *"}

cd /app

# Apply DB migrations and collectstatic
python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

# Persist current container environment for cron jobs
# Keep only simple KEY=VALUE rows (uppercase, digits and underscore)
printenv | grep -E '^[A-Z0-9_]+=' > /app/container.env || true

# Ensure cron wrapper is executable
chmod +x /app/compose/run_shift_reminders.sh || true

# Create cron.d entry
cat > /etc/cron.d/shift_reminders <<EOF
SHELL=/bin/bash
# Load all env at runtime via wrapper script
${CRON_SCHEDULE_SHIFT_REMINDERS} root /app/compose/run_shift_reminders.sh >> /var/log/cron.log 2>&1
EOF
chmod 0644 /etc/cron.d/shift_reminders

# Start cron in background
cron

# Start the app server
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
