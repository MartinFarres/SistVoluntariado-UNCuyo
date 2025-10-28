"""
Management command to set up initial database data.

This command:
1. Creates Argentina with all its Provincias, Departamentos, and Localidades
2. Creates UNCuyo Facultades and Carreras
3. Creates an initial admin account

Usage:
    python manage.py setup_initial_data --email admin@example.com --password secretpass123
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.ubicacion.models import Pais, Provincia, Departamento, Localidad
from apps.facultad.models import Facultad, Carrera
from apps.users.models import User
from apps.persona.models import Administrativo
from apps.organizacion.models import Organizacion


class Command(BaseCommand):
    help = 'Set up initial database data: geographic data for Argentina, UNCuyo academic data, and create main admin account'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Email for the main admin account'
        )
        parser.add_argument(
            '--password',
            type=str,
            required=True,
            help='Password for the main admin account'
        )
        parser.add_argument(
            '--skip-geo',
            action='store_true',
            help='Skip geographic data setup (only create admin)'
        )
        parser.add_argument(
            '--skip-admin',
            action='store_true',
            help='Skip admin creation (only setup geographic data)'
        )
        parser.add_argument(
            '--skip-facultades',
            action='store_true',
            help='Skip facultades and carreras setup'
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        skip_geo = options['skip_geo']
        skip_admin = options['skip_admin']
        skip_facultades = options['skip_facultades']

        if skip_geo and skip_admin and skip_facultades:
            raise CommandError('Cannot skip all setup operations')

        try:
            with transaction.atomic():
                if not skip_geo:
                    self.setup_geographic_data()
                
                if not skip_facultades:
                    self.setup_facultades_carreras()
                
                if not skip_admin:
                    self.create_admin_account(email, password)
                
                self.stdout.write(self.style.SUCCESS('✓ Initial setup completed successfully!'))
        
        except Exception as e:
            raise CommandError(f'Setup failed: {str(e)}')

    def setup_geographic_data(self):
        """Set up Argentina's geographic data"""
        self.stdout.write('Setting up geographic data for Argentina...')
        
        # Check if Argentina already exists
        if Pais.objects.filter(nombre='Argentina').exists():
            self.stdout.write(self.style.WARNING('  → Argentina already exists, skipping geographic data'))
            return
        
        # Create Argentina
        argentina = Pais.objects.create(nombre='Argentina')
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created country: {argentina.nombre}'))
        
        # Argentina's provinces with departments and their localities
        # Structure: { 'Provincia': { 'Departamento': ['Localidad1', 'Localidad2', ...] } }
        provincias_data = {
            "Mendoza": {
                "Capital": ["Mendoza", "La Favorita"],
                "Godoy Cruz": ["Godoy Cruz", "Villa Hipódromo", "San Francisco del Monte"],
                "Guaymallén": ["Guaymallén", "Dorrego", "San José", "Rodeo de la Cruz"],
                "Las Heras": ["Las Heras", "El Algarrobal", "El Challao", "El Plumerillo", "El Zapallar", "Uspallata"],
                "Maipú": ["Maipú", "Coquimbito", "Luzuriaga", "Rodeo del Medio", "Fray Luis Beltrán", "Russell"],
                "Luján de Cuyo": ["Luján de Cuyo", "Chacras de Coria", "Vistalba", "Carrodilla", "Perdriel", "Agrelo", "Ugarteche"],
                "San Martín": ["San Martín", "Palmira", "Chapanay", "Nueva California"],
                "Rivadavia": ["Rivadavia", "La Libertad", "Medrano", "Los Campamentos"],
                "Junín": ["Junín", "Philipps", "Los Barriales"],
                "Santa Rosa": ["Santa Rosa", "Las Catitas", "La Dormida"],
                "La Paz": ["La Paz", "Desaguadero", "Villa Antigua"],
                "San Carlos": ["San Carlos", "Eugenio Bustos", "La Consulta", "Chilecito"],
                "Tunuyán": ["Tunuyán", "Vista Flores", "Colonia Las Rosas"],
                "Tupungato": ["Tupungato", "La Arboleda", "El Peral", "San José"],
                "San Rafael": ["San Rafael", "Cuadro Nacional", "Las Paredes", "Rama Caída", "Monte Comán", "Real del Padre", "Villa Atuel"],
                "General Alvear": ["General Alvear", "Bowen", "Carmensa", "Colonia Alvear Este"],
                "Malargüe": ["Malargüe", "Bardas Blancas", "Río Grande", "Agua Escondida"]
                },
            "Buenos Aires": {
                "Buenos Aires": ["Buenos Aires"]
                },
            "Catamarca": {
                "Catamarca": ["Catamarca"]
                },
            "Chaco": {
                "Chaco": ["Chaco"]
                },
            "Chubut": {
                "Chubut": ["Chubut"]
                },
            "Córdoba": {
                "Córdoba": ["Córdoba"]
                },
            "Corrientes": {
                "Corrientes": ["Corrientes"]
                },
            "Entre Ríos": {
                "Entre Ríos": ["Entre Ríos"]
                },
            "Formosa": {
                "Formosa": ["Formosa"]
                },
            "Jujuy": {
                "Jujuy": ["Jujuy"]
                },
            "La Pampa": {
                "La Pampa": ["La Pampa"]
                },
            "La Rioja": {
                "La Rioja": ["La Rioja"]
                },
            "Misiones": {
                "Misiones": ["Misiones"]
                },
            "Neuquén": {
                "Neuquén": ["Neuquén"]
                },
            "Río Negro": {
                "Río Negro": ["Río Negro"]
                },
            "Salta": {
                "Salta": ["Salta"]
                },
            "San Juan": {
                "San Juan": ["San Juan"]
                },
            "San Luis": {
                "San Luis": ["San Luis"]
                },
            "Santa Cruz": {
                "Santa Cruz": ["Santa Cruz"]
                },
            "Santa Fe": {
                "Santa Fe": ["Santa Fe"]
                },
            "Santiago del Estero": {
                "Santiago del Estero": ["Santiago del Estero"]
                },
            "Tierra del Fuego": {
                "Tierra del Fuego": ["Tierra del Fuego"]
                },
            "Tucumán": {
                "Tucumán": ["Tucumán"]
            }
        }

        
        provincia_count = 0
        departamento_count = 0
        localidad_count = 0
        
        for provincia_nombre, departamentos_dict in provincias_data.items():
            # Create province
            provincia = Provincia.objects.create(
                nombre=provincia_nombre,
                pais=argentina
            )
            provincia_count += 1
            
            for departamento_nombre, localidades_list in departamentos_dict.items():
                # Create department
                departamento = Departamento.objects.create(
                    nombre=departamento_nombre,
                    provincia=provincia
                )
                departamento_count += 1
                
                # Create all localities for this department
                for localidad_nombre in localidades_list:
                    Localidad.objects.create(
                        nombre=localidad_nombre,
                        departamento=departamento
                    )
                    localidad_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Created {provincia_count} provinces, '
            f'{departamento_count} departments, and '
            f'{localidad_count} localities'
        ))

    def setup_facultades_carreras(self):
        """Set up UNCuyo's Facultades and Carreras"""
        self.stdout.write('Setting up Facultades and Carreras for UNCuyo...')
        
        # Check if facultades already exist
        if Facultad.objects.exists():
            self.stdout.write(self.style.WARNING('  → Facultades already exist, skipping setup'))
            return
        
        # UNCuyo's facultades with their carreras
        facultades_data = {
            "Facultad de Artes y Diseño (FAD)": [
                "Licenciatura en Artes Plásticas",
                "Profesorado de Grado Universitario en Artes Visuales",
                "Profesorado y Licenciatura en Historia de las Artes Plásticas",
                "Profesorado de Grado Universitario y Licenciatura en Historia del Arte",
                "Licenciatura en Producción y Gestión de Artes Visuales",
                "Licenciatura en Cerámica Industrial",
                "Licenciatura en Cerámica Artística",
                "Profesorado de Grado Universitario en Cerámica Artística",
                "Licenciatura en Arte Dramático",
                "Profesorado de Grado Universitario en Teatro",
                "Diseño Escenográfico",
                "Licenciatura en Gestión y Producción Teatral",
                "Diseño Industrial",
                "Diseño Gráfico",
                "Profesorado de Grado Universitario de Diseño",
                "Licenciatura en Canto",
                "Licenciatura en Composición Musical",
                "Licenciatura en Dirección Coral",
                "Licenciatura en Instrumentos",
                "Profesorado de Grado Universitario de Música",
                "Profesorado de Grado Universitario de Teorías Musicales",
                "Licenciatura en Música Popular"
            ],
            "Facultad de Ciencias Económicas (FCE)": [
                "Contador Público Nacional y Perito Partidor",
                "Licenciatura en Administración",
                "Licenciatura en Economía",
                "Licenciatura en Gestión de Negocios Regionales",
                "Licenciatura en Logística"
            ],
            "Facultad de Ciencias Exactas y Naturales (FCEN)": [
                "Licenciatura en Ciencias Básicas con Orientación en Biología",
                "Licenciatura en Ciencias Básicas con Orientación en Física",
                "Licenciatura en Ciencias Básicas con Orientación en Matemática",
                "Licenciatura en Ciencias Básicas con Orientación en Química",
                "Licenciatura en Geología",
                "Profesorado de Grado Universitario en Ciencias Básicas con Orientación en Biología",
                "Profesorado de Grado Universitario en Ciencias Básicas con Orientación en Física",
                "Profesorado de Grado Universitario en Ciencias Básicas con Orientación en Matemática",
                "Profesorado de Grado Universitario en Ciencias Básicas con Orientación en Química"
            ],
            "Facultad de Ciencias Médicas (FCM)": [
                "Licenciatura en Enfermería",
                "Ciclo de Licenciatura en Higiene y Seguridad en el Trabajo",
                "Medicina",
                "Enfermería Universitaria",
                "Tecnicatura en Anestesia",
                "Tecnicatura en Laboratorio",
                "Tecnicatura en Quirófano",
                "Tecnicatura en Hemoterapia",
                "Tecnicatura en Diagnóstico por Imágenes",
                "Tecnicatura en Oftalmología",
                "Tecnicatura en Hemodiálisis",
                "Doctorado en Ciencias Biológicas",
                "Doctorado en Medicina",
                "Maestría en Bioética",
                "Maestría en Investigación Clínica",
                "Especialización en Tocoginecología",
                "Especialización en Medicina del Trabajo",
                "Especialización en Medicina Legal",
                "Especialización en Salud Pública",
                "Especialización en Geriatría",
                "Diplomatura en Enfermería en Cuidados Críticos",
                "Diplomatura en Educación para Profesionales de la Salud",
                "Diplomatura en VIH e ITS",
                "Diplomatura en Atención Primaria de ENT",
                "Diplomatura en Telemedicina",
                "Diplomatura en Dramaterapia"
            ],
            "Facultad de Ciencias Políticas y Sociales (FCPYS)": [
                "Licenciatura en Sociología",
                "Licenciatura en Ciencia Política y Administración Pública",
                "Licenciatura en Trabajo Social",
                "Licenciatura en Comunicación Social",
                "Licenciatura en Gestión y Administración Universitaria",
                "Ciclo de Licenciatura en Producción en Medios de Comunicación",
                "Profesorado en Sociología",
                "Profesorado en Ciencias Políticas y Administración Pública",
                "Profesorado en Trabajo Social",
                "Profesorado en Comunicación Social",
                "Tecnicatura en Gestión Universitaria",
                "Tecnicatura en Gestión y Administración de Organizaciones",
                "Tecnicatura en Producción Audiovisual",
                "Tecnicatura en Gestión y Administración en Instituciones Públicas",
                "Tecnicatura en Gestión de Políticas Públicas",
                "Ciclo de Formación Básica en Ciencias Sociales en Territorio"
            ],
            "Facultad de Derecho (FD)": [
                "Abogacía",
                "Tecnicatura Universitaria en Administración de Edificios de Propiedad Horizontal y Conjuntos Inmobiliarios"
            ],
            "Facultad de Filosofía y Letras (FFyL)": [
                "Licenciatura y Profesorado en Filosofía",
                "Licenciatura y Profesorado en Letras",
                "Licenciatura en Arqueología",
                "Licenciatura y Profesorado en Historia",
                "Licenciatura y Profesorado en Geografía",
                "Geógrafo Profesional",
                "Licenciatura en Francés",
                "Profesorado de Grado Universitario en Lengua y Literatura Francesa",
                "Profesorado de Grado Universitario en Portugués",
                "Licenciatura en Filología Inglesa",
                "Profesorado de Grado Universitario en Lengua y Cultura Inglesas",
                "Profesorado de Grado Universitario en Lengua y Cultura Italianas",
                "Licenciatura y Profesorado en Ciencias de la Educación",
                "Tecnicatura en Cartografía, SIG y Teledetección",
                "Tecnicatura Universitaria de Francés",
                "Traductorado Bilingüe Inglés–Español",
                "Licenciatura en Educación Física",
                "Licenciatura en Literatura Infantil y Juvenil",
                "Licenciatura en Tiempo Libre para el Deporte y el Turismo",
                "Profesorado para Profesionales Universitarios"
            ],
            "Facultad de Ingeniería (FI)": [
                "Ingeniería Civil",
                "Ingeniería Industrial",
                "Ingeniería en Petróleos",
                "Ingeniería en Mecatrónica",
                "Arquitectura",
                "Licenciatura en Ciencias de la Computación"
            ],
            "Facultad de Odontología (FO)": [
                "Odontología",
                "Asistente Dental",
                "Prótesis Dental"
            ],
            "Facultad de Educación (FEEyE)": [
                "Profesorado Universitario de Educación Primaria",
                "Profesorado Universitario de Educación Inicial",
                "Profesorado Universitario de Educación para Personas Sordas",
                "Profesorado Universitario de Pedagogía Terapéutica en Discapacidad Visual",
                "Profesorado Universitario de Pedagogía Terapéutica en Discapacidad Intelectual",
                "Licenciatura en Terapia del Lenguaje",
                "Tecnicatura Universitaria en Interpretación de Lengua de Señas",
                "Profesorado Universitario en Informática"
            ],
            "Facultad de Ciencias Agrarias (FCA)": [
                "Ingeniería Agronómica",
                "Bromatología",
                "Licenciatura en Bromatología",
                "Ingeniería en Recursos Naturales Renovables",
                "Tecnicatura Universitaria en Enología y Viticultura"
            ],
            "Facultad de Ciencias Aplicadas a la Industria (FCAI)": [
                "Ingeniería en Industrias de la Alimentación",
                "Ingeniería Química - Orientación Petroquímica",
                "Ingeniería Química - Orientación Mineralurgia",
                "Ingeniería Química - Orientación Medio Ambiente",
                "Ingeniería Mecánica",
                "Profesorado Universitario en Química",
                "Licenciatura en Bromatología",
                "Tecnicatura Universitaria en Enología y Viticultura",
                "Licenciatura en Enología"
            ],
            "Instituto Tecnológico Universitario (ITU)": [
                "Tecnicatura en Redes de Datos y Telecomunicaciones",
                "Tecnicatura en Producción Industrial y Automatización",
                "Tecnicatura en Mantenimiento e Instalaciones Industriales",
                "Tecnicatura en Logística y Transporte",
                "Tecnicatura en Marketing",
                "Tecnicatura en Gestión de Empresas",
                "Tecnicatura en Electricidad y Sistemas de Control Industriales",
                "Tecnicatura en Higiene y Seguridad en el Trabajo"
            ],
            "Instituto Universitario de Seguridad Pública (IUSP)": [
                "Tecnicatura en Seguridad Pública",
                "Tecnicatura en Seguridad Penitenciaria",
                "Licenciatura en Seguridad Pública",
                "Licenciatura en Seguridad Penitenciaria",
                "Auxiliar en Seguridad Pública"
            ]
        }
        
        facultad_count = 0
        carrera_count = 0
        
        for facultad_nombre, carreras_list in facultades_data.items():
            # Create facultad
            facultad = Facultad.objects.create(
                nombre=facultad_nombre,
                activo=True
            )
            facultad_count += 1
            
            # Create carreras for this facultad
            for carrera_nombre in carreras_list:
                Carrera.objects.create(
                    nombre=carrera_nombre,
                    facultad=facultad,
                    activo=True
                )
                carrera_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Created {facultad_count} facultades and {carrera_count} carreras'
        ))

    def setup_organizacion(self):
        """Create the main UNCuyo organization entry if not present."""
        self.stdout.write('Ensuring main organization UNCuyo exists...')
        org_name = 'UNCuyo'
        if Organizacion.objects.filter(nombre=org_name).exists():
            self.stdout.write(self.style.WARNING(f'  → Organizacion "{org_name}" already exists, skipping'))
            return

        # Try to attach to a sensible localidad (Mendoza capital) if available
        localidad = None
        try:
            localidad = Localidad.objects.filter(nombre__iexact='Mendoza').first()
        except Exception:
            localidad = None

        org = Organizacion.objects.create(
            nombre=org_name,
            activo=True,
            descripcion='Organización Universidad Nacional de Cuyo - entidad promotora de voluntariados',
            contacto_email='info@uncu.edu.ar',
            localidad=localidad,
            direccion='Ciudad Universitaria, Mendoza'
        )
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created organization: {org.nombre}'))

    def create_admin_account(self, email, password):
        """Create the initial admin account"""
        self.stdout.write(f'Creating admin account: {email}...')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            raise CommandError(f'User with email {email} already exists')
        
        # Create User with ADMIN role
        user = User.objects.create_user(
            email=email,
            password=password,
            role=User.Roles.ADMINISTRATIVO,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            settled_up=False
        )
        
        # Create Administrativo persona
        user.save()
        
        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Created admin account: {email}\n'
            f'  ✓ Created Administrativo persona: {user.persona.nombre} {user.persona.apellido}'
        ))
