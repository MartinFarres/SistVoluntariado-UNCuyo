from rest_framework import serializers
from .models import Certificado
from django.db.models import Sum
from apps.asistencia.models import Asistencia
from apps.voluntarios.models import Voluntario

class CertificadoSerializer(serializers.ModelSerializer):
    archivo = serializers.FileField(required=False, allow_null=True)
    voluntario = serializers.PrimaryKeyRelatedField(queryset=Voluntario.objects.all())

    class Meta:
        model = Certificado
        fields = (
            "id", "voluntario", "voluntariado", "horas",
            "archivo", "fecha_emision", "creado_por"
        )
        read_only_fields = ("id", "fecha_emision", "creado_por")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # import dinámico para evitar ciclos
        from apps.voluntarios.models import Voluntario
        self.fields["voluntario"].queryset = Voluntario.objects.all()

    def validate(self, data):
        """
        Si no pasan 'horas', calculamos la suma de horas de todas las asistencias presentes
        del voluntario (opcionalmente filtrando por voluntariado).
        """
        voluntario = data.get("voluntario") or getattr(self.instance, "voluntario", None)
        voluntariado = data.get("voluntariado") or getattr(self.instance, "voluntariado", None)

        if voluntario is None:
            raise serializers.ValidationError("Se requiere voluntario para generar el certificado.")

        # calcular horas si no se pasaron
        if not data.get("horas"):
            qs = Asistencia.objects.filter(inscripcion__voluntario=voluntario, presente=True)
            if voluntariado:
                qs = qs.filter(inscripcion__turno__voluntariado=voluntariado)
            agg = qs.aggregate(total=Sum("horas"))
            data["horas"] = agg["total"] or 0

        return data

    def create(self, validated_data):
        # creado_por lo establece la view
        return super().create(validated_data)
