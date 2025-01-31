from django.urls import path
from applications.auth.auth_views import register

urlpatterns= [
    path('register/', register, name='register')
]