#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    if sys.argv[1] == 'test':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hyrodactil.settings.test")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hyrodactil.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)