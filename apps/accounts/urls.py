from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from apps.accounts.views import (
    UserView, UserConfirmView, MyTokenObtainPairView,
    UpdateUserPasswordView, UpdateUserEmailView
)


urlpatterns = [
    path(
        'user/', UserView.as_view({'get': 'list', 'post': 'create'}),
        name='user_registration'
    ),
    path(
        'user/<pk>/', UserView.as_view({'get': 'retrieve'}),
        name='user_info'
    ),
    path(
        'user/password/', UpdateUserPasswordView.as_view(),
        name='change_password'
    ),
    path(
        'user/email/', UpdateUserEmailView.as_view(),
        name='change_email'
    ),
    path(
        'user/<pk>/confirm/', UserConfirmView.as_view({'put': 'update'}),
        name='user_confirm'
    ),
    path(
        'user/token/', MyTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'user/token/refresh/', TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'user/token/verify/', TokenVerifyView.as_view(),
        name='token_verify'
    ),
]
