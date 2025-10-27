from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from datetime import date, timedelta, time

from apps.organizacion.models import Organizacion
from apps.voluntariado.models import Voluntariado, DescripcionVoluntariado, Turno
from django.contrib.auth import get_user_model
from decimal import Decimal

from apps.persona.models import Voluntario as VoluntarioModel
from apps.voluntariado.models import InscripcionTurno
from apps.asistencia.models import Asistencia


class Command(BaseCommand):
    help = 'Create sample Organizaciones and Voluntariados for testing (creates few orgs, voluntariados and turnos)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--orgs', type=int, default=2, help='Number of extra sample organizaciones to create (excluding UNCuyo)'
        )
        parser.add_argument(
            '--vols-per-org', type=int, default=2, help='Number of voluntariados to create per organization'
        )

    def handle(self, *args, **options):
        org_count = options['orgs']
        vols_per_org = options['vols_per_org']

        try:
            with transaction.atomic():
                created_orgs = []

                # Ensure UNCuyo exists or create minimal if not
                uncuyo, created = Organizacion.objects.get_or_create(
                    nombre='UNCuyo',
                    defaults={
                        'activo': True,
                        'descripcion': 'Universidad Nacional de Cuyo (organización ejemplo)',
                        'contacto_email': 'info@uncu.edu.ar'
                    }
                )
                created_orgs.append(uncuyo)

                # Create additional example organizations
                for i in range(1, org_count + 1):
                    name = f'Organizacion de Prueba {i}'
                    org, c = Organizacion.objects.get_or_create(
                        nombre=name,
                        defaults={
                            'activo': True,
                            'descripcion': f'Organizacion de prueba número {i} para testing',
                            'contacto_email': f'prueba{i}@example.org'
                        }
                    )
                    created_orgs.append(org)

                self.stdout.write(self.style.SUCCESS(f'Created/ensured {len(created_orgs)} organizaciones'))

                # For each organization, create some voluntariados with turnos
                today = date.today()
                for org in created_orgs:
                    for v_idx in range(1, vols_per_org + 1):
                        nombre = f'Voluntariado {org.nombre} #{v_idx}'

                        # Simple description object
                        desc = DescripcionVoluntariado.objects.create(
                            descripcion=f'Descripción para {nombre}',
                            resumen=f'Resumen {nombre}'
                        )

                        # Define dates: convocatoria starts in 7 days
                        fecha_inicio_conv = today + timedelta(days=7)
                        fecha_fin_conv = fecha_inicio_conv + timedelta(days=7)
                        fecha_inicio_cursado = fecha_fin_conv + timedelta(days=7)
                        fecha_fin_cursado = fecha_inicio_cursado + timedelta(days=30)

                        voluntariado = Voluntariado.objects.create(
                            nombre=nombre,
                            descripcion=desc,
                            organizacion=org,
                            fecha_inicio_convocatoria=fecha_inicio_conv,
                            fecha_fin_convocatoria=fecha_fin_conv,
                            fecha_inicio_cursado=fecha_inicio_cursado,
                            fecha_fin_cursado=fecha_fin_cursado,
                            latitud= -32.890842,
                            longitud= -68.844849,
                            place_id='test-place'
                        )

                        # Create a couple of turnos inside cursado period
                        turno_date_1 = fecha_inicio_cursado + timedelta(days=2)
                        turno_date_2 = fecha_inicio_cursado + timedelta(days=5)

                        Turno.objects.create(
                            voluntariado=voluntariado,
                            fecha=turno_date_1,
                            hora_inicio=time(hour=9, minute=0),
                            hora_fin=time(hour=12, minute=0),
                            cupo=10,
                            lugar='Sede Principal'
                        )

                        Turno.objects.create(
                            voluntariado=voluntariado,
                            fecha=turno_date_2,
                            hora_inicio=time(hour=14, minute=0),
                            hora_fin=time(hour=17, minute=0),
                            cupo=8,
                            lugar='Sede Secundaria'
                        )

                        # ---- Create a test volunteer user and inscribe them into the first turno ----
                        # Create (or get) a test Voluntario persona and user so the frontend calendar
                        # can show an inscribed turno out-of-the-box.
                        User = get_user_model()

                        test_vol, _created_vol = VoluntarioModel.objects.get_or_create(
                            dni='00000000',
                            defaults={
                                'nombre': 'Test',
                                'apellido': 'Voluntario',
                            }
                        )

                        user_email = 'test_vol@example.org'
                        user_defaults = {
                            'is_active': True,
                            'role': getattr(User.Roles, 'VOLUNTARIO', 'VOL')
                        }

                        # Use create_user when creating a new user so the password is set
                        # before any model full_clean/save hooks run. If a user already
                        # exists with that email, reuse it.
                        user = User.objects.filter(email=user_email).first()
                        if not user:
                            # create_user will set the password correctly
                            user = User.objects.create_user(email=user_email, password='testpass123', **user_defaults)

                        # link persona to user if not already linked
                        if not getattr(user, 'persona', None):
                            user.persona = test_vol
                            user.save()

                        # Find the first turno we just created for this voluntariado (by date/hora)
                        first_turno = voluntariado.turnos.order_by('fecha', 'hora_inicio').first()
                        if first_turno:
                            insc, _insc_created = InscripcionTurno.objects.get_or_create(
                                turno=first_turno,
                                voluntario=test_vol,
                                defaults={
                                    'estado': InscripcionTurno.Status.INSCRITO,
                                }
                            )

                            # Create an Asistencia record for the inscripcion so horas are present
                            try:
                                Asistencia.objects.get_or_create(
                                    inscripcion=insc,
                                    defaults={
                                        'presente': True,
                                        'horas': Decimal('3.50'),
                                        'observaciones': 'Asistencia creada por create_test_organizaciones_voluntariados'
                                    }
                                )
                            except Exception:
                                # Absorb any edge-case errors (e.g., decimal/validation) so command remains useful
                                pass

                self.stdout.write(self.style.SUCCESS('✓ Sample voluntariados and turnos created successfully'))

        except Exception as e:
            raise CommandError(f'Failed to create test data: {e}')
