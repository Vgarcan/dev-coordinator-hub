from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .models import Repository

# Create your views here.


@staff_member_required
def repository_list(request):
    """Show staff the local inventory without dispatching any agent work."""
    repositories = Repository.objects.all()
    return render(
        request,
        'repositories/list.html',
        {'repositories': repositories},
    )
