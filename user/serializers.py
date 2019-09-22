from .models import User, UserVerification, UploadFile
from rest_framework import serializers
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from datetime import datetime
import uuid
import pdb

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']    

    def create(self, validated_data):
        token = uuid.uuid4().hex
        user = User()
        user = user.create(**validated_data)
        user_verification = UserVerification()
        user_verification.create(user.id, token)
        return user 


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user_obj = User.objects.filter(email=email, is_active=True).first()
        user_verification = UserVerification.check_user_id(user_obj.id)
        if user_verification:
            raise serializers.ValidationError(
                'Please the verify the email after try to login.'
            )
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
            'token': user.token,
        }


class EmailVerificationSerializer(serializers.ModelSerializer):
    """ email verification serializer """

    class Meta:
        model = User
        fields = ('token',)

    
        