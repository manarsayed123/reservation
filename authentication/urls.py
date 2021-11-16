from django.urls import path, include

from authentication.views import CustomLogin

urlpatterns = [
    path('auth/login/', CustomLogin.as_view(), name='custom_login'),
]