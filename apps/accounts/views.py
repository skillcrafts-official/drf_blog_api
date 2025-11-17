from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema_view, extend_schema
from apps.accounts.models import User
from apps.accounts.serializers import (
    UserSerializer, UserConfirmSerializer,
    MyTokenObtainPairSerializer
)


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'


class UserConfirmView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserConfirmSerializer
    lookup_field = 'pk'


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
