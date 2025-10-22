from .base import *

DEBUG = True

# Email configuration for development (console backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@voluntariado.uncuyo.edu.ar'

# Frontend URL for password reset links
FRONTEND_URL = 'http://localhost:5173'
