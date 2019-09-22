from .views import (
    RegistrationAPIView, EmailVerificationAPIView, LoginAPIView, FileUploadView
) 
from django.urls import path

urlpatterns = [
    path('user/', RegistrationAPIView.as_view()),
    path('user/verification/<slug:token>', EmailVerificationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('upload_images/', FileUploadView.as_view()),
]
