from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        max_length=150,
        regex=r'^[\w.@+-]+'
    )
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве `username` запрещено."
            )
        return value


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        max_length=150,
        regex=r'^[\w.@+-]+'
    )
    confirmation_code = serializers.CharField(
        max_length=150
    )

    class Meta:
        model = User
        fields = ("username", "confirmation_code")
