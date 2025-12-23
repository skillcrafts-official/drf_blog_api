#!bash

PATH_TO_APP=$1

mkdir ${PATH_TO_APP}/tests/
touch __init__.py
echo '"""Local conftest.py"""' > ${PATH_TO_APP}/tests/conftest.py
echo '"""Tests for app models"""' > ${PATH_TO_APP}/tests/test_models.py
echo '"""Tests for app serializers"""' > ${PATH_TO_APP}/tests/test_serializers.py
echo '"""Tests for app views"""' > ${PATH_TO_APP}/tests/test_views.py
echo '"""Serializers for $PATH_TO_APP"""' > ${PATH_TO_APP}/serializers.py
echo '"""The filter extentions for app $PATH_TO_APP"""' > ${PATH_TO_APP}/filters.py
echo '"""The signal extentions for app $PATH_TO_APP"""' > ${PATH_TO_APP}/signals.py
echo '"""The handler extentions for app $PATH_TO_APP"""' > ${PATH_TO_APP}/handlers.py
echo '"""The DRF documentation extends for app $PATH_TO_APP"""' > ${PATH_TO_APP}/spectaculars.py
echo '# pylint: disable=no-member,inherit-non-class,unnecessary-pass' >> ${PATH_TO_APP}/spectaculars.py
echo '"""The urls routing for app $PATH_TO_APP"""' > ${PATH_TO_APP}/urls.py
