from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class CustomTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        data['user_id'] = str(self.user.id)
        data['role'] = self.user.role
        data['username'] = self.user.username

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 🔥 esto va dentro del JWT
        token['user_id'] = str(user.id)
        token['role'] = user.role

        return token