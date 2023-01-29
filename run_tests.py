#!/usr/bin/env python

import sys
import os

from argparse import ArgumentParser

import django
from django.core import management
from django.test.utils import get_runner

# Debug asyncio
os.environ["PYTHONASYNCIODEBUG"] = "1"


def parse_arg(x):
    "Given a string `x`, figure out the app name and the namespace with tests."
    # When x is a namespace.
    if "." in x:
        app = x.split(".")[0]
        ns = x
    # When x is an app name.
    else:
        app = x
        ns = f"{x}.tests"

    return dict(app=app, ns=ns)


def parse_args(*, nargs):
    """
    Accept `nargs` of positional args,
    each of which is either an app name or a namespace with tests:
        - if it is with a `.`, then it is a namespace
        - otherwise it is an app name
    """
    parser = ArgumentParser()
    parser.add_argument("x", nargs=nargs)
    args = parser.parse_args()

    return [parse_arg(x) for x in args.x]


def run_tests(*, app, ns, makemigrations):
    """
    Initially a copy-paste from
    http://djbook.ru/rel1.8/topics/testing/advanced.html#using-the-django-test-runner-to-test-reusable-applications
    """
    # Init django.
    os.environ["DJANGO_SETTINGS_MODULE"] = f"{app}.tests.settings"
    django.setup()
    from django.conf import settings

    # Init the app.
    if makemigrations:
        management.call_command("makemigrations", "tests", interactive=False)

    # Get test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=99, debug_sql=False, interactive=False)

    # Run the tests and return failures
    print(f" * Test * : app = {app}; ns = {ns}")
    return test_runner.run_tests([ns])


def main():
    """
    This function expects exactly one thing to test.
    """
    thing = parse_args(nargs=1)[0]
    failures = run_tests(**thing, makemigrations=True)
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
