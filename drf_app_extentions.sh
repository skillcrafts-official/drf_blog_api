#!bash

PATH_TO_APP=$1

mkdir apps/${PATH_TO_APP}/tests/
touch apps/${PATH_TO_APP}/tests/__init__.py
cat > apps/${PATH_TO_APP}/tests/conftest.py << EOF
"""Local conftest.py"""
EOF
cat > apps/${PATH_TO_APP}/tests/test_models.py << EOF
"""Tests for app models"""
EOF
cat > apps/${PATH_TO_APP}/tests/test_serializers.py << EOF
"""Tests for app serializers"""
EOF
cat > apps/${PATH_TO_APP}/tests/test_views.py << EOF
"""Tests for app views"""
EOF
cat > apps/${PATH_TO_APP}/serializers.py << EOF
"""Serializers for ${PATH_TO_APP}"""

from rest_framework import serializers


# class

EOF
cat > apps/${PATH_TO_APP}/filters.py << EOF
"""The filter extentions for app ${PATH_TO_APP}"""
EOF
cat > apps/${PATH_TO_APP}/signals.py << EOF
"""The signal extentions for app ${PATH_TO_APP}"""
EOF
cat > apps/${PATH_TO_APP}/handlers.py << EOF
"""The handler extentions for app ${PATH_TO_APP}"""
EOF
cat > apps/${PATH_TO_APP}/handlers.py << EOF
"""The viewsets extentions for app ${PATH_TO_APP}"""

from django.db import transaction
from django.db.models.query import QuerySet
from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.serializers import BaseSerializer
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# class

EOF
cat > apps/${PATH_TO_APP}/spectaculars.py << EOF
"""The DRF documentation extends for app ${PATH_TO_APP}"""
# pylint: disable=no-member,inherit-non-class,unnecessary-pass
EOF
cat > apps/${PATH_TO_APP}/urls.py << EOF
"""The urls routing for app ${PATH_TO_APP}"""

from django.urls import path


urlpatterns = [
    
]

EOF

sed -i "6s/.*/    name = 'apps.${PATH_TO_APP}'/" apps/${PATH_TO_APP}/apps.py  # замена 6-й строки
cat >> apps/${PATH_TO_APP}/apps.py << EOF

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel,unused-import
            from apps.${PATH_TO_APP} import spectaculars  # noqa: F401
            # from apps.${PATH_TO_APP} import signals       # noqa: F401
            # from apps.${PATH_TO_APP} import handlers      # noqa: F401
        except ImportError:
            pass
EOF