# -*- coding: utf-8 -*-
"""This module contains the library to convert a body description in CSV to
WKT-CRS."""
import collections
import logging
import os
from typing import cast
from typing import Dict
from typing import Tuple

import pandas as pd  # pylint: disable=import-error

from ._version import __name_soft__
from .body import IAU_REPORT
from .body import ReferenceShape
from .crs import BodyCrs
from .crs import ICrs
from .crs import Planetocentric
from .crs import Planetographic
from .crs import ProjectionBody

logger = logging.getLogger(__name__)


class CsvforwktLib:
    """The library"""

    def __init__(
        self,
        iau_report: str,
        iau_version: int,
        iau_doi: str,
        directory: str,
        *args,
        **kwargs,
    ):
        # pylint: disable=unused-argument
        if "level" in kwargs:
            CsvforwktLib._parse_level(kwargs["level"])

        self.__directory = directory
        # self.__data_file: str = "/home/malapert/Dev/test/csvForWKT/data/naifcodes_radii_m_wAsteroids_IAU2015.csv"
        self.__iau_report: str = iau_report
        self.__iau_version: int = iau_version
        self.__iau_doi: str = iau_doi
        self.__df_bodies: pd.DataFrame = self._init_iau_report()

    @staticmethod
    def _parse_level(level: str):
        """Parse level name and set the rigt level for the logger.
        If the level is not known, the INFO level is set

        Args:
            level (str): level name
        """
        logger_main = logging.getLogger(__name_soft__)
        if level == "INFO":
            logger_main.setLevel(logging.INFO)
        elif level == "DEBUG":
            logger_main.setLevel(logging.DEBUG)
        elif level == "WARNING":
            logger_main.setLevel(logging.WARNING)
        elif level == "ERROR":
            logger_main.setLevel(logging.ERROR)
        elif level == "CRITICAL":
            logger_main.setLevel(logging.CRITICAL)
        elif level == "TRACE":
            logger_main.setLevel(logging.TRACE)  # type: ignore # pylint: disable=no-member
        else:
            logger_main.warning(
                "Unknown level name : %s - setting level to INFO", level
            )
            logger_main.setLevel(logging.INFO)

    @property
    def iau_report(self) -> str:
        """The IAU report as CSV file.

        :getter: Returns the path of the CSV file
        :type: str
        """
        return self.__iau_report

    @property
    def iau_version(self) -> int:
        """The IAU version.

        :getter: Returns the IAU version
        :type: int
        """
        return self.__iau_version

    @property
    def iau_doi(self) -> str:
        """The IAU DOI.

        :getter: Returns the IAU Doi
        :type: str
        """
        return self.__iau_doi

    @property
    def directory(self) -> str:
        """The output directory.

        :getter: Returns the output directory
        :type: str
        """
        return self.__directory

    def _init_iau_report(self) -> pd.DataFrame:
        """Init the IAU_REPORT class."""
        logger.info(
            f"Creating WKT-CRS for {self.iau_version} - {self.iau_doi} ..."
        )
        IAU_REPORT.DOI_IAU = self.iau_doi
        IAU_REPORT.VERSION = str(self.iau_version)
        return pd.read_csv(self.iau_report)

    def _skip_records(self):
        """Skip records when IAU2015_Semimajor != -1 and IAU2015_Axisb != -1 and IAU2015_Semiminor != -1"""
        nb_records: int = self.__df_bodies.shape[0]
        self.__df_bodies = self.__df_bodies.query(
            "IAU2015_Semimajor != -1 and IAU2015_Axisb != -1 and IAU2015_Semiminor != -1"
        )
        nb_records_for_processing: int = self.__df_bodies.shape[0]
        nb_records_skip: int = nb_records - nb_records_for_processing
        logger.info(f"\t\t{nb_records_skip} records have been skipped")

    def _split_body(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Split the bodies in two parts : biaxial and triaxial

        Triaxial bodies is defined when IAU2015_Semimajor, IAU2015_Semiminor,
        IAU2015_Axisb are different

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: biaxial and triaxial bodies
        """
        triaxial: pd.DataFrame = self.__df_bodies.query(
            "IAU2015_Semimajor != IAU2015_Axisb \
            and IAU2015_Semiminor != IAU2015_Axisb \
            and IAU2015_Semiminor != IAU2015_Semimajor"
        ).copy()
        biaxial: pd.DataFrame = self.__df_bodies.drop(triaxial.index).copy()
        logger.info(
            f"\tSplit biaxial ({biaxial.shape[0]} records) and triaxial ({triaxial.shape[0]} records) ... OK"
        )
        return biaxial, triaxial

    def _is_sphere(  # pylint: disable=no-self-use
        self, row: pd.Series
    ) -> bool:
        """Check if the current body is a sphere.

        The verification is done by comparing :
        * IAU2015_Semimajor, IAU2015_Semiminor and IAU2015_Axisb

        Args:
            row (pd.Series): current body description

        Returns:
            bool: True when the shape off the body is a sphere otherwise False
        """
        return (
            row["IAU2015_Semimajor"] == row["IAU2015_Semiminor"]
            and row["IAU2015_Semimajor"] == row["IAU2015_Axisb"]
        )

    def _is_retrograde(  # pylint: disable=no-self-use
        self, row: pd.Series
    ) -> bool:
        """Check if the rotation of the body is retrograde.

        Args:
            row (pd.Series): current body description

        Returns:
            bool: True when the rotation of the body is retrograde otherwise False
        """
        return row["rotation"] == "Retrograde"

    def _is_historic(  # pylint: disable=no-self-use
        self, row: pd.Series
    ) -> bool:
        """Check if the body is part of a historical Coordinate Reference System.

        Args:
            row (pd.Series): current body description

        Returns:
            bool: True when the body is part of a historical CRS otherwise False
        """
        return row["Body"] in ["Sun", "Earth", "Moon"]

    def _process_body_crs_biaxial(self, body: pd.DataFrame) -> Dict[int, ICrs]:
        """Process biaxial bodies and avoid duplicate desriptions.

        The Rules are the following to avoid duplication:
        * For each shape, we approximate the shape as a sphere and we create
          a planetocentric (or planetographic) reference frame with east direction.
        * if the shape is a sphere => planetocentric based on an ellipsoid is
          not needed  else planetocentric description is created
        * if the shape is a sphere and (retrograde movement or historical) =>
          planetographic is not needed because the planetographic = planetocentric
          else plantetographic description is created

        Args:
            body (pd.DataFrame): bodies
            ref_shape (ReferenceShape): Type of the shape

        Returns:
            Dict[int, ICrs]: IAU code and CRS description
        """
        crs: Dict[int, ICrs] = dict()
        for _, row in body.iterrows():
            sphere_crs = Planetocentric(row, ReferenceShape.SPHERE)
            crs[sphere_crs.crs.iau_code] = sphere_crs.crs
            if not self._is_sphere(row):
                ocentric_crs = Planetocentric(row, ReferenceShape.ELLIPSE)
                crs[ocentric_crs.crs.iau_code] = ocentric_crs.crs
            if not (
                self._is_sphere(row)
                and (self._is_retrograde(row) or self._is_historic(row))
            ):
                ographic = Planetographic(row, ReferenceShape.ELLIPSE)
                crs[ographic.crs.iau_code] = ographic.crs
        logger.info(f"\t\tNumber of processed bodies: {len(crs.keys())}")
        return crs

    def _process_body_crs_triaxial(  # pylint: disable=no-self-use
        self, body: pd.DataFrame
    ) -> Dict[int, ICrs]:
        """Process triaxial bodies.

        Args:
            body (pd.DataFrame): bodies
            ref_shape (ReferenceShape): Type of the shape

        Returns:
            Dict[int, ICrs]: IAU code and CRS description
        """
        crs: Dict[int, ICrs] = dict()
        for _, row in body.iterrows():
            sphere_crs = Planetocentric(row, ReferenceShape.SPHERE)
            crs[sphere_crs.crs.iau_code] = sphere_crs.crs
            ocentric_crs = Planetocentric(row, ReferenceShape.TRIAXIAL)
            crs[ocentric_crs.crs.iau_code] = ocentric_crs.crs
            ographic = Planetographic(row, ReferenceShape.TRIAXIAL)
            crs[ographic.crs.iau_code] = ographic.crs
        logger.info(f"\t\tNumber of processed bodies: {len(crs.keys())}")
        return crs

    def _process_body_projection_crs(  # pylint: disable=no-self-use
        self, crs: Dict[int, ICrs]
    ) -> Dict[int, ICrs]:
        """Process the projection description based on a body CRS.

        Args:
            crs (Dict[int, ICrs]): bodies CRS

        Returns:
            Dict[int, ICrs]: projections CRS
        """
        crs_projection: Dict[int, ICrs] = dict()
        for _, value in crs.items():
            body_crs: BodyCrs = cast(BodyCrs, value)
            for projection in ProjectionBody.iter_projection(body_crs):
                crs_projection[projection.iau_code] = projection
        return crs_projection

    def process(self) -> Dict[int, ICrs]:
        """Process the bodies.

        Returns:
            Dict[int, ICrs]: CRS
        """
        crs: Dict[int, ICrs] = {}
        nb_records: int = self.__df_bodies.shape[0]
        logger.info(f"\tNumber of bodies in IAU report {nb_records}")
        self._skip_records()
        nb_records = self.__df_bodies.shape[0]
        logger.info(f"\t\t{nb_records} records for processing")

        biaxial: pd.DataFrame
        triaxial: pd.DataFrame
        biaxial, triaxial = self._split_body()

        logger.info("\n\tProcessing of biaxial body")
        biaxial_crs: Dict[int, ICrs] = self._process_body_crs_biaxial(biaxial)
        crs.update(biaxial_crs)
        logger.info("\t\tprocess WKT for biaxial bodies ... OK")

        logger.info("\n\tProcessing of triaxial body")
        triaxial_crs: Dict[int, ICrs] = self._process_body_crs_triaxial(
            triaxial
        )
        crs.update(triaxial_crs)
        logger.info("\t\tprocess WKT for triaxial bodies ... OK")

        logger.info(
            "\n\tProcessing of projected CRS for both baxial and triaxial"
        )
        crs.update(self._process_body_projection_crs(crs))
        logger.info("\t\tprocess WKT for projected CRS ... OK")

        return collections.OrderedDict(sorted(crs.items()))

    def save(self, crs: Dict[int, ICrs]):
        """Save the result as file

        Args:
            crs (Dict[int, ICrs]): CRS
        """
        with open(
            os.path.join(self.directory, "iau.wkt"), "w", encoding="utf-8"
        ) as file:
            for _, wkt in crs.items():
                file.write(wkt.wkt())
                file.write("\n\n")
        logger.info(
            f"\n\tSave the WKTs in {os.path.join(self.directory, 'iau.wkt')} ... OK"
        )
        logger.info("Finished.")
