from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "timezone"]

    def create(self, validated_data):
        # OJO: usamos create_user, NO User.objects.create(), porque
        # create_user se encarga de hashear el password correctamente.
        # Si usaras create() directo, el password quedaría guardado en texto plano.
        return User.objects.create_user(**validated_data)