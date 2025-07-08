from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from .models import UserAccount

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserAccount
        fields = (
            "id", "email", "username", "cnpj", "password", "re_password", "porte", "setor"
        )

    def to_internal_value(self, data):
        print("TO_INTERNAL_VALUE:", data)
        return super().to_internal_value(data)