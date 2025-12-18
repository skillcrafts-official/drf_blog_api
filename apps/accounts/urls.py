from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from apps.accounts.views import (
    UserView, MyTokenObtainPairView, GuestTokenObtainView,
    UpdateUserPasswordView, UpdateUserEmailView
)
from apps.accounts.authentication import UnifiedJWTAuthentication


urlpatterns = [
    path(
        'users/', UserView.as_view({'get': 'list', 'post': 'create'}),
        name='user_registration'
    ),
    path(
        'users/password/', UpdateUserPasswordView.as_view(),
        name='change_password'
    ),
    path(
        'users/<int:pk>/', UserView.as_view({'get': 'retrieve'}),
        name='user_info'
    ),
    path(
        'emails/', UpdateUserEmailView.as_view(),
        name='add_email'
    ),
    # path(
    #     'emails/confirm/', EmailConfirmView.as_view({'put': 'update'}),
    #     name='email_confirm'
    # ),
    path(
        'auth/token/', MyTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/token/refresh/', TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'auth/token/verify/', TokenVerifyView.as_view(),
        name='token_verify'
    ),
    # path(
    #     'auth/guest-token/', GuestTokenObtainView.as_view(),
    #     name='gest_token_obtain_pair'
    # ),
    # path(
    #     'auth/token/refresh/', TokenRefreshView.as_view(),
    #     name='token_refresh'
    # ),
    # path(
    #     'auth/token/verify/', TokenVerifyView.as_view(),
    #     name='token_verify'
    # ),
]
