from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})
    password_confirmation = serializers.CharField(
        style={"input_type": "password"})

    def save(self):
        email = self.validated_data["email"]
        password = self.validated_data["password"]
        password_confirmation = self.validated_data["password_confirmation"]

        if password != password_confirmation:
            raise serializers.ValidationError(
                {"passoword": "Passwords must match"})
        user = User.objects.create_user(email, email, password)
        return user
