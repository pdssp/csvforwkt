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
Cartographic Coordinates and Rotational Elements report.

The workflow to generate the WKTs is described as follows:

.. uml::

    start

    :Skip records from IAU report;
    :Split bodies;
    if (biaxial?) then (yes)
        :Compute planetocentric description for sphere using median radius\n for Interoperability case;
        :Add this CRS in the list;
        if (is a body a Sphere?) then (yes)
        else (no)
            :compute planetocentric CRS;
            :Add this CRS in the list;
        endif
        if (is a body a Sphere and (historical reason or retrograde movement) ?) then (yes)
        else (no)
            :Compute planetographic CRS;
            :Add this CRS in the list;
        endif
    else (no)
        :Create planetocentric description for sphere using median radius\n for Interoperability case;
        :Add this CRS in the list;
        :compute planetocentric CRS;
        :Add this CRS in the list;
        :Compute planetographic CRS;
        :Add this CRS in the list;
    endif
    :merge CRS;
    :Compute projected CRS;

    stop
"""
import logging.config
import os
from logging import debug
from logging import getLogger
from logging import NullHandler
from logging import setLogRecordFactory
from logging import warning

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

getLogger(__name__).addHandler(NullHandler())

UtilsLogs.add_logging_level("TRACE", 15)
try:
    PATH_TO_CONF = os.path.dirname(os.path.realpath(__file__))
    logging.config.fileConfig(
        os.path.join(PATH_TO_CONF, "logging.conf"),
        disable_existing_loggers=False,
    )
    debug(f"file {os.path.join(PATH_TO_CONF, 'logging.conf')} loaded")
except Exception as exception:  # pylint: disable=broad-except
    warning(f"cannot load logging.conf : {exception}")
setLogRecordFactory(LogRecord)  # pylint: disable=no-member
