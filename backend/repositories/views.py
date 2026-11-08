from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .models import Repository

# Create your views here.


@staff_member_required
def repository_list(request):
    """Filter the staff-only inventory without dispatching agent work."""
    repositories = Repository.objects.all()

    # GET parameters only narrow the staff-visible inventory; they never
    # authorise repository access or trigger any external GitHub operation.
    search = request.GET.get('q', '').strip()[:100]
    status = request.GET.get('status', '').strip()
    allowed_statuses = {
        value for value, _label in Repository.TrackingStatus.choices
    }
    if status not in allowed_statuses:
        status = ''

    if search:
        repositories = repositories.filter(full_name__icontains=search)
    if status:
        repositories = repositories.filter(tracking_status=status)

    return render(
        request,
        'repositories/list.html',
        {
            'repositories': repositories,
            'search': search,
            'selected_status': status,
            'status_choices': Repository.TrackingStatus.choices,
            'is_filtered': bool(search or status),
        },
    )
