# -*- coding: utf-8 -*-
"""This module is responsible to handle a datum."""
from string import Template

from .body import IAU_REPORT
from .body import IBody
from .body import ReferenceShape


class Anchor:
    """Anchor."""

    TEMPLATE = '\tANCHOR["$name"]'

    def __init__(self, name: str = ""):
        """Creates an anchor

        Args:
            name (str, optional): name of the anchor. Defaults to "".
        """
        self.__name = name

    @property
    def name(self) -> str:
        """Anchor name.

        :getter: Returns the anchor name
        :type: str
        """
        return self.__name

    def wkt(self) -> str:
        """Returns the WKT.

        Returns:
            str: WKT of Anchor
        """
        anchor: str
        if self.name in ("", "nan : nan"):
            anchor = ""
        else:
            anchor_template: Template = Template(Anchor.TEMPLATE)
            anchor = "\n\t" + anchor_template.substitute(name=self.name)
        return anchor


class Datum:
    """A datum is a model of a planet that is used in mapping. The datum
    consists of a series of numbers that define the shape and size of the
    ellipsoid. A datum is chosen to give the best possible fit to the true
    shape of the planet.
    """

    TEMPLATE = """DATUM["$datum_name ($version)",
        $body$anchor],
    PRIMEM["Reference Meridian", 0,
        ANGLEUNIT["degree", 0.0174532925199433, ID["EPSG", 9122]]]"""

    TEMPLATE_SPHERE = """DATUM["$datum_name ($version) - Sphere",
        $body$anchor],
    PRIMEM["Reference Meridian", 0,
        ANGLEUNIT["degree", 0.0174532925199433, ID["EPSG", 9122]]]"""

    def __init__(
        self, name: str, body: IBody, anchor: Anchor, template: str
    ) -> None:
        """Creates a datum description for a body.

        Args:
            name (str): datum name
            body (IBody): body
            anchor (Anchor): anchor
            template (str): template
        """
        self.__name: str = name
        self.__body: IBody = body
        self.__anchor: Anchor = anchor
        self.__template: str = template

    @staticmethod
    def create(
        biaxial_body: ReferenceShape,
        name: str,
        body: IBody,
        anchor: Anchor,
    ) -> "Datum":
        """Create a datum

        Args:
            biaxial_body (ReferenceShape): type of shape
            name (str): datum name
            body (IBody): body description
            anchor (Anchor): anchor description

        Returns:
            Datum: datum description
        """
        result: Datum
        if biaxial_body == ReferenceShape.SPHERE:
            result = Datum(name, body, anchor, Datum.TEMPLATE_SPHERE)
        else:
            result = Datum(name, body, anchor, Datum.TEMPLATE)
        return result

    @property
    def name(self) -> str:
        """Datum name.

        :getter: Returns the datum name
        :type: str
        """
        return self.__name

    @property
    def body(self) -> IBody:
        """Body description.

        :getter: Returns the body description
        :type: IBody
        """
        return self.__body

    @property
    def anchor(self) -> Anchor:
        """Anchor name.

        :getter: Returns the anchor description
        :type: Anchor
        """
        return self.__anchor

    def wkt(self) -> str:
        """Returns the datum WKT.

        Returns:
            str: WKT description
        """
        datum_template = Template(self.__template)
        datum = datum_template.substitute(
            version=IAU_REPORT.VERSION,
            datum_name=self.name,
            body=self.body.wkt()
            if self.anchor.wkt() == ""
            else self.body.wkt() + ",",
            anchor=self.anchor.wkt(),
        )
        return datum
