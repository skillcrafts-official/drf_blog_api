#!/bin/bash

PATH_TO_APP=$1

echo '"""The urls routing for app ${PATH_TO_APP}"""' > ${PATH_TO_APP}/urls.py
mkdir -p ${PATH_TO_APP}/templates/emails
mkdir -p ${PATH_TO_APP}/static/emails/css
mkdir -p ${PATH_TO_APP}/static/emails/js
mkdir -p ${PATH_TO_APP}/tests
rm tests.py
touch ${PATH_TO_APP}/tests/__init__.py
echo '"""Local conftest.py"""' > ${PATH_TO_APP}/tests/conftest.py
echo '"""Tests for app models"""' > ${PATH_TO_APP}/tests/test_models.py
echo '"""Tests for app views"""' > ${PATH_TO_APP}/tests/test_views.py
echo '"""Tests for app urls"""' > ${PATH_TO_APP}/tests/test_urls.py
