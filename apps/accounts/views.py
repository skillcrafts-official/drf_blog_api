from typing import Any
from datetime import datetime

from jsonschema import ValidationError
from apps.accounts.authentication import UnifiedJWTAuthentication
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from apps.accounts.models import User, Email, GuestConsent
from apps.accounts.serializers import (
    UserSerializer, UserPasswordSerializer, UserEmailSerializer,
    MyTokenObtainPairSerializer, GuestTokenObtainSerializer,
    EmailConfirmSerializer
)


class UserView(ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    # filterset_class = ConfirmEmailFilters
    lookup_field = 'pk'

    # @action(detail=False, methods=['post'])
    # def confirmed_email(self, request):
    #     """
    #     Кастомный ендпоинт выдаёт список языков
    #     для компонентов выбора на клиенте
    #     """
    #     data = request.data
    #     confirmed_email = data.get('confirmed_email')
    #     confirm_code = data.get('confirm_code')

    #     return Response({'success': True})
    # def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
    #     print(request.data)
    #     return super().list(request, *args, **kwargs)


class EmailConfirmView(APIView):
    """Ендпоинты для подтверждения Email"""
    serializer_class = EmailConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Проверка email"""
        data = request.data

        user = User.objects.filter(
            primary_email=data.get('primary_email', ''),
            confirmation_code=data.get('confirmation_code', '')
        ).first()

        if user is None:
            raise ValidationError(detail='User not found!')

        # if user.generated_code_at is None:
        #     raise ValidationError(detail='Email verification failed!')

        # print(user.generated_code_at)
        serializer = self.serializer_class(
            instance=user, data=data, partial=True
        )

        if serializer.is_valid():
            return Response({'verification': 'passed'}, status=200)

        return Response({'verification': 'failed'}, status=200)


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
    permission_classes = [AllowAny]


class MyTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class GuestTokenObtainView(APIView):
    """Получение гостевого токена"""
    serializer_class = GuestTokenObtainSerializer  # Используйте исправленный сериализатор
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        ip_address = request.META.get('REMOTE_ADDR', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        # print(f"Creating guest token for IP: {ip_address}")
        # print(f"User-Agent: {user_agent}")

        try:
            serializer = self.serializer_class(
                data={},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data)
        except Exception as e:
            print(f"Error creating guest token: {str(e)}")
            raise


class MigrateGuestToUserView(APIView):
    """Миграция гостя в полноценного пользователя"""

    def post(self, request):
        guest = request.user  # Гость из GuestAuthentication

        # Валидация данных регистрации
        email = request.data.get('email')
        password = request.data.get('password')

        # Создаём пользователя
        user = User.objects.create(
            primary_email=email,
            password=password,
            guest_origin=guest
        )

        # Мигрируем данные гостя
        # if guest.cart_items:
        #     # Переносим корзину
        #     for item in guest.cart_items:
        #         CartItem.objects.create(
        #             user=user,
        #             product_id=item['product_id'],
        #             quantity=item['quantity']
        #         )

        # if guest.preferences:
        #     # Переносим настройки
        #     user.profile.preferences.update(guest.preferences)
        #     user.profile.save()

        # Генерируем обычный JWT для пользователя
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)

        # Помечаем гостя как мигрированного
        guest.migrated_to = user
        guest.save()

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.pk,
            'guest_data_migrated': True
        })


class GuestConsentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Регистрация согласия гостя"""
        guest_id = request.data.get('guest_id')
        consent_type = request.data.get('consent_type', 'basic')

        # Получаем текст политики (актуальную версию)
        policy_text = get_current_policy_text()
        policy_hash = hash_text(policy_text)

        # Сохраняем согласие
        consent = GuestConsent.objects.create(
            guest_id=guest_id,
            consent_type=consent_type,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            consent_text_hash=policy_hash
        )

        return Response({
            'status': 'consent_registered',
            'consent_id': consent.pk,
            'policy_version': policy_hash[:8]
        })


class GuestConsentWithdrawView(APIView):
    def post(self, request):
        """Отзыв согласия (право быть забытым)"""
        guest = request.user

        # Помечаем согласие как отозванное
        GuestConsent.objects.filter(
            guest=guest,
            is_active=True
        ).update(
            is_active=False,
            withdrawn_at=timezone.now()
        )

        # Анонимизируем данные гостя
        guest.user_agent = ''
        guest.ip_address = None
        guest.save()

        return Response({'status': 'consent_withdrawn'})
