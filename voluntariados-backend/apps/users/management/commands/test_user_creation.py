from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.persona.models import Voluntario, Administrativo, Delegado

User = get_user_model()


class Command(BaseCommand):
    help = 'Test user creation with automatic persona creation'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email for the test user')
        parser.add_argument('role', type=str, choices=['VOL', 'ADMIN', 'DELEG'], help='Role for the user')
        parser.add_argument('--password', type=str, default='testpass123', help='Password for the user')

    def handle(self, *args, **options):
        email = options['email']
        role = options['role']
        password = options['password']

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f'User with email {email} already exists')
            )
            return

        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            role=role
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created user {user.email} with role {user.get_role_display()}')
        )

        if user.persona:
            persona_type = user.persona.__class__.__name__
            self.stdout.write(
                self.style.SUCCESS(f'Automatically created {persona_type} with ID {user.persona.id}')
            )
        else:
            self.stdout.write(
                self.style.ERROR('No persona was created for the user')
            )

        # Test role immutability
        try:
            user.role = 'ADMIN'  # Try to change role
            user.save()
            self.stdout.write(
                self.style.ERROR('ERROR: Role change was allowed (this should not happen)')
            )
        except Exception as e:
            self.stdout.write(
                self.style.SUCCESS(f'Role immutability working correctly: {str(e)}')
            )