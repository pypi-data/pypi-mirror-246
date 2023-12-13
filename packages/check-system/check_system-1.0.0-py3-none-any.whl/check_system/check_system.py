"""Check system environment markers in accordance to PEP 508.

Ref: https://peps.python.org/pep-0508/
"""

import argparse
import os
import platform
import sys
from typing import Dict, List, Optional


def format_full_version(info):  # type: ignore
    """Copied from PEP 508."""
    version = "{0.major}.{0.minor}.{0.micro}".format(info)  # pylint: disable=C0209
    kind = info.releaselevel
    if kind != "final":
        version += kind[0] + str(info.serial)
    return version


if hasattr(sys, "implementation"):
    implementation_version = format_full_version(
        sys.implementation.version
    )  # type: ignore
else:
    implementation_version = "0"


MARKERS = {
    "os_name": {"value": os.name, "help": ""},
    "sys_platform": {"value": sys.platform, "help": ""},
    "platform_machine": {"value": platform.machine(), "help": ""},
    "platform_python_implementation": {
        "value": platform.python_implementation(),
        "help": "",
    },
    "platform_release": {"value": platform.release(), "help": ""},
    "platform_system": {"value": platform.system(), "help": ""},
    "platform_version": {"value": platform.version(), "help": ""},
    "python_version": {
        "value": ".".join(platform.python_version_tuple()[:2]),
        "help": "",
    },
    "python_full_version": {"value": platform.python_version(), "help": ""},
    "implementation_name": {"value": sys.implementation.name, "help": ""},
    "implementation_version": {"value": implementation_version, "help": ""},
}


def parse_args(argv: Optional[List[str]] = None) -> Dict[str, str]:
    """Utility function for creating parser and parsing arguments."""
    parser = argparse.ArgumentParser()

    for marker, marker_data in MARKERS.items():
        parser.add_argument(
            f"--{marker.replace('_', '-')}",
            type=str,
            default=None,
            help=marker_data["help"],
        )

    args = parser.parse_args(argv)

    return vars(args)


def main(argv: Optional[List[str]] = None) -> None:
    """Main function of the cli"""
    args = parse_args(argv)

    for marker, value in args.items():
        if value:
            if MARKERS[marker]["value"] != value:
                raise SystemExit(
                    f"Check failed: {marker} was "
                    f"{MARKERS[marker]['value']}. Checked against: {value}"
                )


def cli_wrapper() -> None:
    """Wrapper function aroun main that reads arguments with sys.argv."""
    main(sys.argv[1:])
