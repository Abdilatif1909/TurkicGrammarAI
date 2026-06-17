#!/usr/bin/env python
"""Django command-line utility for TurkicGrammarAI."""
import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    # Ensure the manage.py directory is on sys.path so that running
    # `python backend/manage.py test` from the repository root still
    # imports project packages (config, apps.*) correctly.
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir and script_dir not in sys.path:
            sys.path.insert(0, script_dir)
    except Exception:
        pass
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
