#!/usr/bin/env python

import sys
from multiprocessing import Process

from run_tests import run_tests, parse_args, parse_arg


all_apps = [
    "todo",
]


def all_apps_things():
    return [parse_arg(x) for x in all_apps]


def run_tests_(*args, **kwargs):
    failures = run_tests(*args, **kwargs)
    sys.exit(bool(failures))


def run_app_tests(**kwargs):
    p = Process(target=run_tests_, kwargs={**kwargs, "makemigrations": False})
    try:
        p.start()
        p.join()
        return p.exitcode
    finally:
        p.close()


def main():
    args = parse_args(nargs="*")

    # If nothing given, then run all tests for all the apps.
    things = args if args else all_apps_things()

    for thing in things:
        exitcode = run_app_tests(**thing)
        if exitcode:
            sys.exit(exitcode)


if __name__ == "__main__":
    main()
