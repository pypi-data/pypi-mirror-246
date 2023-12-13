"""Module entrypoint for check_system.

Enables running the module as:

  $ python3 -m check_system --help

as well as the standard

  $ check-system --help
"""

from check_system import cli_wrapper

cli_wrapper()
