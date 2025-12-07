#!bash

PATH_TO_APP=$1

mkdir ${PATH_TO_APP}/tests/
cd ${PATH_TO_APP}/tests/
touch __init__.py
echo '"""Local conftest.py"""' > conftest.py
echo '"""Tests for app models"""' > test_models.py
echo '"""Tests for app serializers"""' > test_serializers.py
echo '"""Tests for app views"""' > test_views.py
cd ..
echo '"""Serializers for $PATH_TO_APP"""' > serializers.py
echo '"""The DRF documentation extends for app $PATH_TO_APP"""' > spectaculars.py
echo '"""The urls routing for app $PATH_TO_APP"""' > urls.py
