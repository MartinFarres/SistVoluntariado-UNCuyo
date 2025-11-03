#!/bin/bash
set -euo pipefail

# Export container env for cron context
if [ -f /app/container.env ]; then
  set -a
  # shellcheck disable=SC1091
  . /app/container.env
  set +a
fi

cd /app
python manage.py send_shift_reminders
