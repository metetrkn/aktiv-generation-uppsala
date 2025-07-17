"""
Core Application Views.

This module contains the view functions and classes for the core application.
It handles the main page views and any core functionality views that don't
belong to other specific applications.

The views are responsible for:
- Rendering the main pages
- Handling core application logic
- Processing user requests
"""

from django.shortcuts import render

from apps.photo.models import Photo
from .models import Activity


# To handle HTTP requests and responses in home page
def home(request):
    photos = Photo.objects.all()
    context = {"photos": photos}
    return render(request, "core/base.html", context)


def privacy_policy(request):
    return render(request, "core/includes/privacy_policy.html")


def cookies(request):
    return render(request, "core/includes/cookies.html")


def activities(request):
    activities = Activity.objects.prefetch_related('images').all()
    activity_list = []
    for activity in activities:
        images = [
            {
                'url': img.image.url,
                'alt': f"{activity.title} image"
            }
            for img in activity.images.all()
        ]
        activity_list.append({
            'title': activity.title,
            'date': activity.date,
            'location': activity.location,
            'description': activity.description,
            'images': images,
        })
    context = {'activities': activity_list}
    return render(request, "core/includes/activities.html", context)
