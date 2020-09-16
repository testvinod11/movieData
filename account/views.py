# Create your views here.

from rest_framework import viewsets


from .serializers import RegistrationSerializer, LoginSerializer


class SignupView(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    http_method_names = ('post',)


class LoginView(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    http_method_names = ('post',)
