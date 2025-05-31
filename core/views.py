from django.shortcuts import render

# To handle HTTP requests and responses in home page
def home(request):
    return render(request, 'core/base.html') 