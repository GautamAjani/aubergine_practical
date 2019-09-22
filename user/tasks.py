import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
from random import randint
from django.core.mail import EmailMessage
from datetime import datetime
from PIL import Image
import requests
import os
import pdb

@shared_task
def user_verification_email(email, token):
    """ send email function for user verification. """
    
    link = """<html><a href=http://127.0.0.1/api/v1/user/verification/{token}>link</a>
            </html>""".format(token=token)
    msg = EmailMessage(
            'Email Verification', 'You can click on this ' + link + ' to verify '
            'your email-ID ', to=[email]
        )
    msg.content_subtype = 'html'
    msg.send()

    return True
