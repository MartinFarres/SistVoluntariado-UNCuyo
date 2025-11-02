from .base import *
import os

DEBUG = True

# Email configuration for development (console backend)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', None)
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 0) or 0) or None
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', None)
if isinstance(EMAIL_USE_TLS, str):
	EMAIL_USE_TLS = EMAIL_USE_TLS.lower() in ('1', 'true', 'yes')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', None)
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@voluntariado.uncuyo.edu.ar')

# Frontend URL for password reset links
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
