from django.shortcuts import render
from django.views import View

# Create your views here.


class EmailView(View):
    def get(self, request):
        return render(request, 'emails/confirmation_email.html')
