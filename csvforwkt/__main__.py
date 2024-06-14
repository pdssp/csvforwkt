# -*- coding: utf-8 -*-
# csvForWKT - csvForWKT is a python script that creates a WKT-crs for some bodies from the solar system. The content that is filled in the WKT-crs comes from the report of IAU Working Group on Cartographic.
# Copyright (C) 2022 - CNES (Jean-Christophe Malapert for Pôle Surfaces Planétaires)
#
# This file is part of csvForWKT.
#
# csvForWKT is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v3  as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# csvForWKT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License v3  for more details.
#
# You should have received a copy of the GNU Lesser General Public License v3
# along with csvForWKT.  If not, see <https://www.gnu.org/licenses/>.
"""Main program."""
import argparse
import logging
import os
import signal
import sys
from typing import Dict

from .csvforwkt import CsvforwktLib
from csvforwkt import __author__
from csvforwkt import __copyright__
from csvforwkt import __description__
from csvforwkt import __version__
from csvforwkt.crs import ICrs


class SmartFormatter(argparse.HelpFormatter):
    """Smart formatter for argparse - The lines are split for long text"""

    def _split_lines(self, text, width):
        if text.startswith("R|"):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(  # pylint: disable=protected-access
            self, text, width
        )


class SigintHandler:  # pylint: disable=too-few-public-methods
    """Handles the signal"""

    def __init__(self):
        self.SIGINT = False  # pylint: disable=invalid-name

    def signal_handler(self, sig: int, frame):
        """Trap the signal

        Args:
            sig (int): the signal number
            frame: the current stack frame
        """
        # pylint: disable=unused-argument
        logging.error("You pressed Ctrl+C")
        self.SIGINT = True
        sys.exit(2)


def str2bool(string_to_test: str) -> bool:
    """Checks if a given string is a boolean

    Args:
        string_to_test (str): string to test

    Returns:
        bool: True when the string is a boolean otherwise False
    """
    return string_to_test.lower() in ("yes", "true", "True", "t", "1")


def parse_cli() -> argparse.Namespace:
    """Parse command line inputs.

    Returns
    -------
    argparse.Namespace
        Command line options
    """
    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=SmartFormatter,
        epilog=__author__ + " - " + __copyright__,
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )

    parser.add_argument(
        "--iau_report",
        required=True,
        help="The location of the IAU CSV file.",
    )

    parser.add_argument(
        "--iau_version",
        type=int,
        required=True,
        help="Year of the IAU report (ex: 2015)",
    )

    parser.add_argument(
        "--iau_doi",
        required=True,
        help="DOI of the IAU report (ex: doi:10.1007/s10569-017-9805-5)",
    )

    parser.add_argument(
        "--output_directory",
        default=os.getcwd(),
        help="The output directory where the data products are created (default: %(default)s)",
    )

    parser.add_argument(
        "--level",
        choices=[
            "INFO",
            "DEBUG",
            "WARNING",
            "ERROR",
            "CRITICAL",
            "TRACE",
        ],
        default="INFO",
        help="set Level log (default: %(default)s)",
    )

    return parser.parse_args()


def run():
    """Main function that instantiates the library."""
    handler = SigintHandler()
    signal.signal(signal.SIGINT, handler.signal_handler)
    try:
        options_cli = parse_cli()

        csvforwkt = CsvforwktLib(
            options_cli.iau_report,
            options_cli.iau_version,
            options_cli.iau_doi,
            options_cli.output_directory,
            level=options_cli.level,
        )
        crs: Dict[int, Dict[int, ICrs]] = csvforwkt.process()
        csvforwkt.save(crs)
        sys.exit(0)
    except Exception as error:  # pylint: disable=broad-except
        logging.exception(error)
        sys.exit(1)


if __name__ == "__main__":
    # execute only if run as a script
    run()
