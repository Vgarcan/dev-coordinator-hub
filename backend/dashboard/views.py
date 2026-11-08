from django.shortcuts import render

# Create your views here.


def home(request):
    """Render the initial backend landing page; it does not control agents."""
    return render(request, 'dashboard/home.html')
