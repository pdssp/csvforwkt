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
"""csvForWKT is a python script that creates a WKT-crs for solar system bodies.
The physical content of the WKT-crs comes from the IAU Working Group on
Cartographic Coordinates and Rotational Elements report."""
import logging.config
import os
from logging import NullHandler

from ._version import __author__
from ._version import __author_email__
from ._version import __copyright__
from ._version import __description__
from ._version import __license__
from ._version import __name_soft__
from ._version import __title__
from ._version import __url__
from ._version import __version__
from .custom_logging import LogRecord
from .custom_logging import UtilsLogs

logging.getLogger(__name__).addHandler(NullHandler())

UtilsLogs.add_logging_level("TRACE", 15)
try:
    PATH_TO_CONF = os.path.dirname(os.path.realpath(__file__))
    logging.config.fileConfig(
        os.path.join(PATH_TO_CONF, "logging.conf"),
        disable_existing_loggers=False,
    )
    logging.debug(f"file {os.path.join(PATH_TO_CONF, 'logging.conf')} loaded")
except Exception as exception:  # pylint: disable=broad-except
    logging.warning(f"cannot load logging.conf : {exception}")
logging.setLogRecordFactory(LogRecord)  # pylint: disable=no-member
