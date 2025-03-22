from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from users.models import User, Payments


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['username'] = user.username
        token['email'] = user.email

        return token


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
