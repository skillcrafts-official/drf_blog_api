"""The urls routing for app ${PATH_TO_APP}"""
from django.urls import path
from apps.emails.views import EmailView


app_name = 'emails'

urlpatterns = [
    path('', EmailView.as_view(), name='preview'),
]