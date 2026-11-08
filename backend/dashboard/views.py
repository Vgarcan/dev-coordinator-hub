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
    {
        'id': 'DEMO-005',
        'title': 'Codex session needs attention',
        'description': 'Illustrate an expired CLI sign-in before any authorised work starts.',
        'repository': 'example/auth-codex',
        'status': 'auth_required',
        'agent': 'Codex CLI (fictional)',
        'auth_provider': 'codex',
        'next_step': 'Sign in manually; verify and reconcile before any future resumption.',
    },
    {
        'id': 'DEMO-006',
        'title': 'Claude Code session needs attention',
        'description': 'Illustrate the same pause for a different CLI provider.',
        'repository': 'example/auth-claude',
        'status': 'auth_required',
        'agent': 'Claude Code (fictional)',
        'auth_provider': 'claude',
        'next_step': 'Sign in manually; verify and reconcile before any future resumption.',
    },
)

# Display labels reflect docs/TASK_PROTOCOL.md; this does not validate transitions.
DEMO_STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('ready', 'Ready'),
    ('preparing', 'Preparing'),
    ('auth_required', 'Authentication required'),
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

    # The display label is sourced from the one allowlisted state catalogue.
    status_labels = dict(DEMO_STATUS_CHOICES)
    tasks = [
        {**task, 'status_label': status_labels[task['status']]}
        for task in DEMO_TASKS
        if not selected_status or task['status'] == selected_status
    ]
    return render(request, 'dashboard/tasks.html', {
        'tasks': tasks,
        'total_tasks': len(DEMO_TASKS),
        'status_choices': DEMO_STATUS_CHOICES,
        'selected_status': selected_status,
        'is_filtered': bool(selected_status),
    })

# Fictional capability catalogue: labels are design intent, not live discovery.
# Do not infer CLI availability, Ollama inventory, authentication or GPU usage.
DEMO_AGENT_PROFILES = (
    {
        'id': '01',
        'key': 'codex',
        'name': 'Codex CLI',
        'category': 'External CLI · proposed',
        'role': 'Scoped implementation',
        'summary': 'Potentially handles bounded code changes and test-driven fixes.',
        'appropriate_for': 'A reviewed task with a precise repository scope and acceptance checks.',
        'guardrail': 'No execution until CLI eligibility, credentials and sandbox policy are validated.',
    },
    {
        'id': '02',
        'key': 'claude',
        'name': 'Claude Code',
        'category': 'External CLI · proposed',
        'role': 'Implementation or independent review',
        'summary': 'Potentially reviews another worker’s diff or implements a separately approved task.',
        'appropriate_for': 'Evidence-based review with the approved specification and relevant changes.',
        'guardrail': 'Organisation permission and supported headless usage remain unverified.',
    },
    {
        'id': '03',
        'key': 'ollama',
        'name': 'Ollama · local',
        'category': 'Local model · experimental',
        'role': 'Small, low-risk diagnostics',
        'summary': 'A future option for narrow classifications with deterministic validation.',
        'appropriate_for': 'Non-sensitive text examples after measuring quality on the local machine.',
        'guardrail': 'The separate opt-in smoke pilot is not connected to this page or task dispatch.',
    },
)


def agent_gallery(request):
    """Render an invented, read-only catalogue; never probe or start agents."""
    return render(request, 'dashboard/agents.html', {
        'agents': DEMO_AGENT_PROFILES,
    })
