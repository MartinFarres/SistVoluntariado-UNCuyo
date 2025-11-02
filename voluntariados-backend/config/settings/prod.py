from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['your-production-domain.com']

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('1', 'true', 'yes')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@voluntariado.uncuyo.edu.ar')

# Optional: set SERVER_EMAIL (used for error emails)
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

# Note: ensure environment variables are set in your production environment, e.g.:
# EMAIL_HOST_USER=your-account@gmail.com
# EMAIL_HOST_PASSWORD=<app-password-or-smtp-password>