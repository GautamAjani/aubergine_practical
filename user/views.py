from django.shortcuts import render
from .models import User, UserVerification, UploadFile
from rest_framework.views import APIView
from .serializers import(
    UserSerializer, LoginSerializer, EmailVerificationSerializer
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ValidationError
from .utils import store_orignal_image, compress_image
from rest_framework import generics, mixins, status, viewsets
import uuid
import os
import requests
import pdb

# Create your views here.

class RegistrationAPIView(APIView):

    serializer_class = UserSerializer

    def post(self, request):
       
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'user created successfully!'},\
            status=status.HTTP_201_CREATED)
            

class EmailVerificationAPIView(APIView):
    """ email verification view class """

    serializer_class = EmailVerificationSerializer

    def get(self, request, token):
        
        try:
            instance = UserVerification()
            user_verify_obj = instance.check_token(token)
            if not user_verify_obj:
                raise ValidationError('Token is not valid')
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User()
            user = user.get_user(user_verify_obj.user_id)
            user_verify_obj.delete()
            result =  Response({'message': 'Email-ID Verified successfully'})
        except Exception as e:
            result = Response({"message": e}, status=400)
        return result


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
   
    def post(self, request):

        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'login successfully',\
            'user':serializer.data}, status=200)
            

class FileUploadView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        try:
            obj_upload_file = UploadFile()
            data = request.data
            user = request.user.id
            if not data['urls']:
                raise ValidationError('Urls should be not blank')
            for url in data['urls']:
                image_name = url.split('/')[-1]
                file_name = store_orignal_image(url, image_name)
                compress_file = compress_image(file_name, image_name)
                obj_upload_file.create(user, file_name, compress_file)
            result = Response({'message': 'all image url stored successfully'})
        except Exception as e:
            result = Response({"message": e}, status=400)
        return result

        