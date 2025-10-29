from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        try:
            user = self.user
            # update last_login on successful token obtain
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])
        except Exception as e:
            print(f"Error updating last_login for user {self.user.email}: {str(e)}")
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
