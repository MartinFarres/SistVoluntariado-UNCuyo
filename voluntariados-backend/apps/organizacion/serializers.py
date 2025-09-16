from rest_framework import serializers
from .models import Organizacion
from apps.persona.models import Persona  
from apps.ubicacion.models import Localidad

class OrganizacionSerializer(serializers.ModelSerializer):
    contacto_persona = serializers.PrimaryKeyRelatedField(
        queryset=Persona.objects.all(), required=False, allow_null=True
    )
    localidad = serializers.PrimaryKeyRelatedField(
        queryset=Localidad.objects.all(), required=False, allow_null=True
    )
    # para lectura anidada opcional: si querés exponer datos de persona/localidad
    contacto_persona_data = serializers.SerializerMethodField(read_only=True)
    localidad_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organizacion
        fields = (
            "id", "nombre", "descripcion", "contacto_email",
            "contacto_persona", "contacto_persona_data",
            "localidad", "localidad_data",
            "direccion", "activa", "created_at"
        )
        read_only_fields = ("id", "created_at", "contacto_persona_data", "localidad_data")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # setear querysets runtime para evitar import circulares
        from apps.persona.models import Persona as PersonaModel
        from apps.ubicacion.models import Localidad as LocalidadModel
        self.fields["contacto_persona"].queryset = PersonaModel.objects.all()
        self.fields["localidad"].queryset = LocalidadModel.objects.all()

    def get_contacto_persona_data(self, obj):
        persona = getattr(obj, "contacto_persona", None)
        if not persona:
            return None
        # devolver subset para no exponer todo: id, nombre, apellido, email, telefono
        return {
            "id": persona.id,
            "nombre": persona.nombre,
            "apellido": persona.apellido,
            "email": persona.email,
            "telefono": persona.telefono,
        }

    def get_localidad_data(self, obj):
        loc = getattr(obj, "localidad", None)
        if not loc:
            return None
        return {
            "id": loc.id,
            "nombre": loc.nombre,
            "departamento": getattr(loc.departamento, "nombre", None),
            "provincia": getattr(getattr(loc.departamento, "provincia", None), "nombre", None),
        }

    def validate(self, data):
        # validaciones simples: si hay contacto_email y contacto_persona, ambos pueden coexistir
        return data
    def create(self, validated_data):
        # creado_por lo establece la view
        return super().create(validated_data)
    def update(self, instance, validated_data):
        # actualizado_por lo establece la view
        return super().update(instance, validated_data) 
    