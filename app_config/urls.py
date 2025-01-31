from django.urls import path, include

urlpatterns=[
    path('auth/', include('applications.auth.auth_urls'))
]