from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager
)
from django.utils import timezone
import jwt
import random
import string
from datetime import datetime, timedelta
from django.conf import settings
from .tasks import user_verification_email
import uuid

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    """
    store the user information 
    """

    username = None
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def create(self, **kwargs):
        """Create and return a `User` with an email, username and password."""
        
        user = User(email=kwargs['email'], first_name=kwargs['first_name'],\
                last_name=kwargs['last_name'])
        user.set_password(kwargs['password'])
        user.save()
        user_id = self.check_email(kwargs['email'])
        user_verification = UserVerification()
        # user_verification.create(user_id, token)
        return user

    objects = UserManager()


    def __str__(self):
        return self.email 
    
    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        generate the access token
        """
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.id,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    def get_user(self, user_id):
        """ check user exist or not """

        user = User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError("user does not exists")
        return user
    

    def check_email(self, email):
        user = User.objects.filter(email=email).first()
        return user


class UserVerification(models.Model):
    """ User verification model to store token of forget password """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def create(self, user_id, token):
        """ Create user verification record in db """
       
        UserVerification.objects.create(user_id=user_id, token=token)
        user = User.objects.filter(id=user_id).first()
        user_verification_email.delay(user.email, token)
        is_active = models.BooleanField(default=True)
        created_at = models.DateField(default=timezone.now)
        updated_at = models.DateField(default=timezone.now)

        return True

    def check_token(self, token):
        """ Check uuid token of reset password is valid or not """

        obj = UserVerification.objects.filter(token=token).first()
        return obj if obj else False

    def check_user_id(user_id):
        """ check the user entry exist or not """

        obj = UserVerification.objects.filter(user_id=user_id).first()
        return obj if obj else False

class UploadFile(models.Model): 
    """
    store the user media URLs
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.CharField(max_length=255, null=False)
    compress_url = models.CharField(max_length=255, null=False)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
        
    def create(self, user_id, original_url, compress_url):
        """ create method for store image URL """

        obj = UploadFile(user_id=user_id, original_url=original_url,\
                compress_url=compress_url)
        obj.save()
        return obj

