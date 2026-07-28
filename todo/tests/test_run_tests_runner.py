"""Test that run_tests.py works correctly with the fixed makemigrations target."""
import subprocess
import sys


def test_run_tests_no_error():
    """
    Test that calling run_tests.py with 'todo' app does not raise CommandError.
    
    This verifies the fix for the bug where makemigrations was being called
    with "tests" (not a Django app) instead of "todo" (the actual app).
    """
    # Run the test runner with the todo app
    result = subprocess.run(
        [sys.executable, "run_tests.py", "todo"],
        cwd="/Users/alexander/PycharmProjects/films-todo",
        capture_output=True,
        text=True,
    )
    
    # Check that it doesn't fail with CommandError about "tests" app
    assert "No app named 'tests'" not in result.stderr, (
        "run_tests.py is still trying to run makemigrations on 'tests' app"
    )
    
    # The command should succeed or fail with test failures, not with migration errors
    # Exit code 0 = all tests passed, other codes = test failures (acceptable)
    # We just want to ensure no CommandError about missing app
    assert "django.core.management.base.CommandError" not in result.stderr or "No app named 'tests'" not in result.stderr
