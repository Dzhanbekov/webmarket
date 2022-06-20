import firebase_admin
import firebase_admin.auth as auth
from django.contrib.auth.models import User
from rest_framework import serializers
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccount.json")
default_app = firebase_admin.initialize_app(cred)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        firebase_user = auth.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return firebase_user



