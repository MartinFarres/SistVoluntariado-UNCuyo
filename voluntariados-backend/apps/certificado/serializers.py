from rest_framework import serializers
from .models import Certificado
from django.db.models import Sum
from apps.asistencia.models import Asistencia

class CertificadoSerializer(serializers.ModelSerializer):
    archivo = serializers.FileField(required=False, allow_null=True)
    voluntario = serializers.PrimaryKeyRelatedField(queryset=None)

    class Meta:
        model = Certificado
        fields = ("id", "voluntario", "voluntariado", "horas", "archivo", "fecha_emision", "creado_por")
        read_only_fields = ("id", "fecha_emision", "creado_por")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set queryset dinamicamente
        if "voluntario" in self.fields:
            self.fields["voluntario"].queryset = __import__("apps.voluntarios.models", fromlist=["Voluntario"]).Voluntario.objects.all()

    def validate(self, data):
        """
        Si no pasan 'horas', calculamos la suma de horas de todas las asistencias presentes
        del voluntario para el voluntariado (si se pasó voluntariado). Si no se pasó voluntariado,
        sumamos todas las asistencias presentes del voluntario.
        """
        voluntario = data.get("voluntario") or getattr(self.instance, "voluntario", None)
        voluntariado = data.get("voluntariado")
        if voluntario is None:
            raise serializers.ValidationError("Se requiere voluntario para generar el certificado.")

        # si usuario no pasó horas, calculamos
        if data.get("horas") in (None, ""):
            qs = Asistencia.objects.filter(inscripcion__voluntario=voluntario, presente=True)
            if voluntariado:
                qs = qs.filter(inscripcion__turno__voluntariado=voluntariado)
            agg = qs.aggregate(total=Sum("horas"))
            total = agg["total"] or 0
            data["horas"] = total
        return data

    def create(self, validated_data):
        # creado_por lo establece la view
        return super().create(validated_data)
    