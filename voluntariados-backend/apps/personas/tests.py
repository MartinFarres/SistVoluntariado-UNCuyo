from django.test import TestCase
from datetime import date, timedelta
from apps.personas.serializers import PersonaSerializer
from apps.ubicacion.models import Pais, Provincia, Departamento, Localidad


class PersonaModelTests(TestCase):

    def setUp(self):
        # Creamos una localidad valida para la persona
        self.pais = Pais.objects.create(nombre="Argentina", codigo=1)
        self.provincia = Provincia.objects.create(nombre="Mendoza", pais=self.pais)
        self.departamento = Departamento.objects.create(nombre="Lujan de Cuyo", provincia=self.provincia)
        self.localidad = Localidad.objects.create(nombre="Chacras de Coria", departamento=self.departamento, codigo_postal="5505")

    def get_valid_data(self, **overrides):
        """Devuelve un diccionario válido de datos de Persona, con posibilidad de sobrescribir campos."""
        data = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "dni": "12345678",
            "fecha_nacimiento": str(date(1990, 5, 20)),
            "telefono": "+549261123456",
            "email": "juan@example.com",
            "direccion": "Calle Falsa 123",
            "localidad": self.localidad.id,
        }
        data.update(overrides)
        return data

    def test_persona_null_nombre(self):
        data = self.get_valid_data(nombre="")
        serializer = PersonaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("nombre", serializer.errors)

    def test_persona_null_apellido(self):
        data = self.get_valid_data(apellido="")
        serializer = PersonaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("apellido", serializer.errors)

    def test_persona_dni_letras(self):
        data = self.get_valid_data(dni="ABC123")
        serializer = PersonaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("dni", serializer.errors)

    def test_persona_nacimiento_futuro(self):
        data = self.get_valid_data(fecha_nacimiento=str(date.today() + timedelta(days=1)))
        serializer = PersonaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("fecha_nacimiento", serializer.errors)
