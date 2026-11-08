"""Small fictional classification benchmark for opt-in local Ollama evaluation.

No private logs, source files, credentials, or real task instructions are sent.
Six cases are sufficient for a smoke check, not for proving model quality.
"""

BENCHMARK_CASES = (
    ('ModuleNotFoundError: No module named sample_lib', 'dependency'),
    ('DisallowedHost: Invalid HTTP_HOST header localhost', 'configuration'),
    ('Application setting DJANGO_SECRET_KEY is missing', 'configuration'),
    ('FAILED tests/test_home.py::test_home_status', 'test_failure'),
    ('AssertionError: expected 200 but got 404 in test_login', 'test_failure'),
    ('Unknown error with no diagnostic information', 'unknown'),
)
