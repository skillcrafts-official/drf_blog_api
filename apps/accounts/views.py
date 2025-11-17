from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView, status
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema_view, extend_schema
from apps.accounts.models import User
from apps.accounts.serializers import (
    UserSerializer, UserConfirmSerializer,
    UserPasswordSerializer, UserEmailSerializer,
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


class UpdateUserPasswordView(APIView):
    serializer_class = UserPasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # user = request.user
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = request.user
            user.password = make_password(
                serializer.validated_data['password']
            )
            user.save()
            return Response(
                data={
                    "message": "Password has been saved successful!"
                }, status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class UpdateUserEmailView(APIView):
    serializer_class = UserEmailSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # user = request.user
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = request.user
            user.password = serializer.validated_data['email']
            user.save()
            return Response(
                data={
                    "message": "Email has been saved successful!"
                }, status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
