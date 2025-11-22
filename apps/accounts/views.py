from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import User, Email
from apps.accounts.serializers import (
    UserSerializer, UserConfirmSerializer,
    UserPasswordSerializer, UserEmailSerializer,
    MyTokenObtainPairSerializer
)


class UserView(ModelViewSet):
    queryset = User.objects.filter(is_active=True)
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

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                Email.objects.create(**data, user=user)
                return Response(
                    data={
                        "message": "Email has been saved successful!"
                    }, status=status.HTTP_201_CREATED
                )
            except IntegrityError as e:
                error_message = str(e)
                if "unique_any_email_per_user" in error_message:
                    return Response(
                        data={
                            "message": "Email already exists for you!"
                        },
                        status=status.HTTP_409_CONFLICT
                    )
                return Response(
                    data={
                        "message": error_message
                    },
                    status=status.HTTP_409_CONFLICT
                )
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
