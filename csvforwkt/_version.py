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
# You should have received a copy of the GNU Lesser General Public License
# along with csvForWKT.  If not, see <https://www.gnu.org/licenses/>.
"""Project metadata."""
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

__name_soft__ = "csvforwkt"
try:
    __version__ = get_distribution(__name_soft__).version
except DistributionNotFound:
    __version__ = "0.0.0"
__title__ = "csvForWKT"
__description__ = "csvForWKT is a python script that creates a WKT-crs for some bodies from the solar system. The content that is filled in the WKT-crs comes from the report of IAU Working Group on Cartographic."
__url__ = "https://github.com/pole-surfaces-planetaires/csvforwkt"
__author__ = "Jean-Christophe Malapert"
__author_email__ = "jean-christophe.malapert@cnes.fr"
__license__ = "GNU Lesser General Public License v3"
__copyright__ = (
    "2022, CNES (Jean-Christophe Malapert for Pôle Surfaces Planétaires)"
)
