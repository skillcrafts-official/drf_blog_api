from drf_spectacular.utils import inline_serializer

from rest_framework import serializers
from rest_framework.exceptions import (
    AuthenticationFailed, NotAuthenticated, PermissionDenied
)


NOT_AUTHENTICATED = inline_serializer(
    name='NOT_AUTHENTICATED',
    fields={
        'detail': serializers.CharField(
            default=NotAuthenticated.default_detail
        )
    }
)

PERMISSION_DENIED = inline_serializer(
    name='PERMISSION_DENIED',
    fields={
        'detail': serializers.CharField(
            default=PermissionDenied.default_detail
        )
    }
)
