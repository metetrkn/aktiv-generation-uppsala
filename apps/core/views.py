def home(request):
    """
    Renders the home page with a list of all photos.

    Retrieves all Photo objects from the database and passes them
    to the 'core/base.html' template for display.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response with photos.
    """
    photos = Photo.objects.all()
    context = {"photos": photos}
    return render(request, "core/base.html", context)
