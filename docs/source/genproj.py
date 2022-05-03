# -*- coding: utf-8 -*-
import os
import sys

from jinja2 import Template
from jinja2.filters import FILTERS

sys.path.insert(0, os.path.abspath("../"))

from csvforwkt.crs import ProjectionBody  # noqa: E402


def make_unique_cte(constants):
    for key in constants.keys():
        res = {}

        for key_cte, value in constants[key].items():
            if value not in res.values():
                res[key_cte] = value

        constants[key] = res


def rst_list():
    """Return a RST list of all constants."""
    # Read the template
    content = ""
    with open("./source/proj.template", "r", encoding="utf-8") as rstfile:
        content = rstfile.read()

    template = Template(content, trim_blocks=True)
    projections = ProjectionBody.PROJECTION_DATA
    print(template.render(projections=projections))


if __name__ == "__main__":
    rst_list()
