# -*- coding: utf-8 -*-
"""This module is reponsible to handle a celestial body."""
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from enum import Enum
from string import Template
from typing import Optional
from typing import Union


class IAU_REPORT:  # pylint: disable=invalid-name,too-few-public-methods
    """Version of the IAU report."""

    VERSION: str = "2015"
    DOI_IAU: str = "doi://10.1007/s10569-017-9805-5"
    SOURCE_IAU: str = "Source of IAU Coordinate systems: " + DOI_IAU


class ReferenceShape(Enum):
    """The different shapes of the celestial body."""

    SPHERE = "Sphere"
    ELLIPSE = "Ellipse"
    TRIAXIAL = "Triaxial"


class IBody(metaclass=ABCMeta):
    """Interface describing a celestial body."""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "wkt")
            and callable(subclass.wkt)
            and hasattr(subclass, "name")
            and callable(subclass.name)
            and hasattr(subclass, "shape")
            and callable(subclass.shape)
            and hasattr(subclass, "warning")
            and callable(subclass.warning)
            or NotImplemented
        )

    @abstractproperty  # pylint: disable=bad-option-value,deprecated-decorator
    def name(self) -> str:
        """Returns the name of the shape.

        Raises:
            NotImplementedError: Not implemented

        Returns:
            str: the name of the shape
        """
        raise NotImplementedError("Not implemented")

    @abstractproperty  # pylint: disable=bad-option-value,deprecated-decorator
    def shape(self) -> ReferenceShape:
        """Returns the name of the shape.

        Raises:
            NotImplementedError: Not implemented

        Returns:
            ReferenceShape: the name of the shape
        """
        raise NotImplementedError("Not implemented")

    @abstractproperty  # pylint: disable=bad-option-value,deprecated-decorator
    def warning(self) -> Optional[str]:
        """Returns the warning during the creation of the shape.

        Raises:
            NotImplementedError: Not implemented

        Returns:
            str: the warning during the creation of the shape
        """
        raise NotImplementedError("Not implemented")

    @warning.setter
    def warning(self, value: Optional[str]):
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def wkt(self) -> str:
        """Returns the WKT of the shape.

        Raises:
            NotImplementedError: Not implemented

        Returns:
            str: the WKT of the shape
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    def create(  # pylint: disable=invalid-name,too-few-public-methods,too-many-arguments
        shape: ReferenceShape,
        name: str,
        semi_major: float,
        semi_minor: float,
        axisb: float,
        mean: float,
    ) -> "IBody":
        """Create a shape.

        Rules to compute the sphere radius:
        * mean = -1 => Use R_m = (a+b+c)/3 as mean radius
        * semi major = -1 or semi minor = -1 => Use mean radius as sphere radius
        * semi major < semi minor => Use mean radius as sphere radius
        * triaxial bodies => Use mean radius as sphere radius
        * semi major = semi minor = axis b => Use mean radius
        * biaxial bodies => Use semi major as sphere radius

        Args:
            shape (ReferenceShape): type of shape
            name (str): name of the shape
            semi_major (float): semi major axis in meter
            semi_minor (float): semi minor axis in meter
            axisb (float): third axis in meter
            mean (float): mean radius in meter

        Raises:
            ValueError: Unsupported shape

        Returns:
            IBody: A celectial body
        """
        mean_radius: float
        warning: Optional[str] = None

        result: IBody
        if shape == ReferenceShape.SPHERE:
            if mean == -1:
                mean_radius = (semi_major + semi_minor + axisb) / 3
                warning = "Use R_m = (a+b+c)/3 as mean radius. Use mean radius as sphere radius for interoperability. "
            elif semi_major == -1 or semi_minor == -1:
                mean_radius = mean
                warning = (
                    "Use mean radius as sphere radius for interoperability. "
                )
            elif semi_major < semi_minor:  # Hartley case
                mean_radius = mean
                warning = (
                    "Use mean radius as sphere radius for interoperability. "
                )
            elif axisb not in (semi_major, semi_minor):  # Triaxial case
                mean_radius = mean
                warning = (
                    "Use mean radius as sphere radius for interoperability. "
                )
            elif (
                semi_major == axisb and semi_minor == axisb
            ):  # Sun or moon case (No approximation)
                mean_radius = mean
            else:
                mean_radius = semi_major  # Biaxial case
                warning = "Use semi-major radius as sphere radius for interoperability. "
            result = Sphere(name, mean_radius)
        elif shape == ReferenceShape.ELLIPSE:
            inverse_flat: float
            if semi_major == semi_minor:
                inverse_flat = 0
            else:
                inverse_flat = semi_major / (semi_major - semi_minor)
            result = Ellipsoid(name, semi_major, inverse_flat)
        elif shape == ReferenceShape.TRIAXIAL:
            result = Triaxial(name, semi_major, axisb, semi_minor)
        else:
            raise ValueError(f"Unsuported shape: {shape}")
        result.warning = warning
        return result


@IBody.register
class Ellipsoid(IBody):
    """An Ellipoid shape."""

    TEMPLATE = """ELLIPSOID["$ellipsoide_name ($version)", $radius, $inverse_flat,
\t\tLENGTHUNIT["metre", 1, ID["EPSG", 9001]]]"""

    def __init__(self, name: str, radius: float, inverse_flat: float):
        """Create an ellipsoid shape.

        Args:
            name (str): name of the shape
            radius (float): radius of the shape in meter
            inverse_flat (float): inverse flatenning of the shape in meter
        """
        self.__name: str = name
        self.__radius: float = radius
        self.__inverse_flat: float = inverse_flat
        self.__warning: Optional[str] = None

    @property
    def name(self) -> str:
        """The body name.

        :getter: Returns the body name
        :type: str
        """
        return self.__name

    @property
    def radius(self) -> float:
        """The radius in meter.

        :getter: Returns the radius
        :type: float
        """
        return self.__radius

    @property
    def inverse_flat(self) -> float:
        """The inverse flatenning.

        :getter: Returns the inverse flatenning
        :type: float
        """
        return self.__inverse_flat

    @property
    def shape(self) -> ReferenceShape:
        """The shape.

        :getter: Returns the shape
        :type: ReferenceShape
        """
        return ReferenceShape.ELLIPSE

    @property
    def warning(self) -> Optional[str]:
        """The warning related to the body description creation.

        :getter: Returns the warning
        :setter: the warning value
        :type: Optional[str]
        """
        return self.__warning

    @warning.setter
    def warning(self, value: Optional[str]):
        self.__warning = value

    def _convert(  # pylint: disable=no-self-use
        self, number: float
    ) -> Union[int, float]:
        result: Union[int, float]
        if abs(number - round(number, 0)) <= 1e-10:
            result = int(number)
        else:
            result = number
        return result

    def wkt(self) -> str:
        """Returns the WKT of the ellipsoidal body.

        Returns:
            str: the WKT of the shape
        """
        datum_template: Template = Template(Ellipsoid.TEMPLATE)
        datum = datum_template.substitute(
            version=IAU_REPORT.VERSION,
            ellipsoide_name=self.name,
            radius=self._convert(self.radius),
            inverse_flat=self.inverse_flat,
        )
        return datum


@IBody.register
class Sphere(IBody):
    """A sphere shape."""

    TEMPLATE = """ELLIPSOID["$ellipsoide_name ($version) - Sphere", $radius, 0,
\t\tLENGTHUNIT["metre", 1, ID["EPSG", 9001]]]"""

    def __init__(self, name: str, radius: float):
        """Create a sphere desctription

        Args:
            name (str): body name
            radius (float): radius in meter of the sphere
        """
        self.__name: str = name
        self.__radius: float = radius
        self.__warning: Optional[str] = None

    @property
    def name(self) -> str:
        """The body name.

        :getter: Returns the body name
        :type: str
        """
        return self.__name

    @property
    def radius(self) -> float:
        """The radius in meter.

        :getter: Returns the radius in meter
        :type: float
        """
        return self.__radius

    @property
    def shape(self) -> ReferenceShape:
        """The shape.

        :getter: Returns the shape
        :type: ReferenceShape
        """
        return ReferenceShape.SPHERE

    @property
    def warning(self) -> Optional[str]:
        """The warning related to the body description creation.

        :getter: Returns the warning
        :setter: the warning value
        :type: Optional[str]
        """
        return self.__warning

    @warning.setter
    def warning(self, value: Optional[str]):
        self.__warning = value

    def _convert(  # pylint: disable=no-self-use
        self, number: float
    ) -> Union[int, float]:
        result: Union[int, float]
        if abs(number - round(number, 0)) <= 1e-10:
            result = int(number)
        else:
            result = number
        return result

    def wkt(self) -> str:
        """Returns the WKT of the spherical body.

        Returns:
            str: the WKT of the shape
        """
        datum_template: Template = Template(Sphere.TEMPLATE)
        datum = datum_template.substitute(
            ellipsoide_name=self.name,
            version=IAU_REPORT.VERSION,
            radius=self._convert(self.radius),
        )
        return datum


@IBody.register
class Triaxial(IBody):
    """A triaxial shape."""

    TEMPLATE = """TRIAXIAL["$ellipsoide_name ($version)", $semi_major, $semi_median, $semi_minor,
\t\tLENGTHUNIT["metre", 1, ID["EPSG", 9001]]]"""

    def __init__(
        self,
        name: str,
        semi_major: float,
        semi_median: float,
        semi_minor: float,
    ):
        """Create a triaxial shape.

        Args:
            name (str): body name
            semi_major (float): axis one
            semi_median (float): axis two
            semi_minor (float): axis third
        """
        self.__name: str = name
        self.__semi_major: float = semi_major
        self.__semi_minor: float = semi_minor
        self.__semi_median: float = semi_median
        self.__warning: Optional[str] = None

    @property
    def name(self) -> str:
        """The body name.

        :getter: Returns the body name
        :type: str
        """
        return self.__name

    @property
    def semi_major(self) -> float:
        """The semi major axis.

        :getter: Returns the length of the semi major axis
        :type: float
        """
        return self.__semi_major

    @property
    def semi_minor(self) -> float:
        """The semi minor axis.

        :getter: Returns the length of the semi minor axis
        :type: float
        """
        return self.__semi_minor

    @property
    def semi_median(self) -> float:
        """The semi median.

        :getter: Returns the length of the semi median axis
        :type: float
        """
        return self.__semi_median

    @property
    def shape(self) -> ReferenceShape:
        """The shape.

        :getter: Returns the shape
        :type: ReferenceShape
        """
        return ReferenceShape.TRIAXIAL

    @property
    def warning(self) -> Optional[str]:
        """The warning related to the body description creation.

        :getter: Returns the warning
        :setter: the warning value
        :type: Optional[str]
        """
        return self.__warning

    @warning.setter
    def warning(self, value: Optional[str]):
        self.__warning = value

    def wkt(self) -> str:
        """Returns the WKT of the triaxial body.

        Returns:
            str: the WKT of the shape
        """
        datum_template: Template = Template(Triaxial.TEMPLATE)
        datum = datum_template.substitute(
            ellipsoide_name=self.name,
            version=IAU_REPORT.VERSION,
            semi_major=self.semi_major,
            semi_median=self.semi_median,
            semi_minor=self.semi_minor,
        )
        return datum
