from django.shortcuts import render

# Create your views here.


def home(request):
    """Render the initial backend landing page; it does not control agents."""
    return render(request, 'dashboard/home.html')

# Purely fictional display data; this is NOT an operational task queue.
DEMO_TASKS = (
    {
        'id': 'DEMO-001',
        'title': 'Prepare a documentation update',
        'description': 'Scope a small, testable edit before choosing an implementation tool.',
        'repository': 'example/docs-lab',
        'status': 'draft',
        'agent': 'Unassigned',
        'next_step': 'Define acceptance criteria',
    },
    {
        'id': 'DEMO-002',
        'title': 'Inspect a sample repository',
        'description': 'Illustrate a read-only review without modifying repository files.',
        'repository': 'example/sample-site',
        'status': 'ready',
        'agent': 'Not connected',
        'next_step': 'Would need independent authorisation',
    },
    {
        'id': 'DEMO-003',
        'title': 'Review fictional test evidence',
        'description': 'Show how a reviewer might assess checks before owner acceptance.',
        'repository': 'example/ui-lab',
        'status': 'review',
        'agent': 'Not connected',
        'next_step': 'Human review in a future workflow',
    },
    {
        'id': 'DEMO-004',
        'title': 'Resolve a simulated blocker',
        'description': 'Demonstrate why missing authorisation must remain visible.',
        'repository': 'example/cli-sandbox',
        'status': 'blocked',
        'agent': 'Unassigned',
        'next_step': 'No action available in this demo',
    },
)

# Display labels reflect docs/TASK_PROTOCOL.md; this does not validate transitions.
DEMO_STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('ready', 'Ready'),
    ('preparing', 'Preparing'),
    ('running', 'Running'),
    ('review', 'Review'),
    ('waiting_approval', 'Waiting approval'),
    ('done', 'Done'),
    ('blocked', 'Blocked'),
    ('failed', 'Failed'),
    ('cancelled', 'Cancelled'),
)


def task_list(request):
    """Show filtered mock cards using a safe read-only GET request."""
    selected_status = request.GET.get('status', '')
    allowed = {key for key, _label in DEMO_STATUS_CHOICES}
    if selected_status not in allowed:
        selected_status = ''

    tasks = [
        task for task in DEMO_TASKS
        if not selected_status or task['status'] == selected_status
    ]
    return render(request, 'dashboard/tasks.html', {
        'tasks': tasks,
        'total_tasks': len(DEMO_TASKS),
        'status_choices': DEMO_STATUS_CHOICES,
        'selected_status': selected_status,
        'is_filtered': bool(selected_status),
    })
