from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse 

# To handle HTTP requests and responses in home page
def home(request):
    return render(request, 'core/base.html') 

from django.shortcuts import render
from django.conf import settings

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def cookies(request):
    return render(request, 'core/cookies.html')