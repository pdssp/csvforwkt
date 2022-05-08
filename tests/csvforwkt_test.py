# -*- coding: utf-8 -*-
import logging
from typing import Dict

import pytest

import csvforwkt
from csvforwkt.crs import ICrs
from csvforwkt.csvforwkt import CsvforwktLib

# import numpy as np

# from PIL import Image

logger = logging.getLogger(__name__)


def pytest_namespace():
    return {"crs": dict()}


@pytest.fixture
def data():
    iau_data = "data/naifcodes_radii_m_wAsteroids_IAU2015.csv"
    iau_version = 2015
    iau_doi = "doi://10.1007/s10569-017-9805-5"
    csv2wkt = CsvforwktLib(iau_data, iau_version, iau_doi, "/tmp")
    pytest.crs = csv2wkt.process()


@pytest.fixture
def setup():
    logger.info("----- Init the tests ------")


def test_init_setup(setup):
    logger.info("Setup is initialized")


def test_name():
    name = csvforwkt.__name_soft__
    assert name == "csvforwkt"


def test_logger():
    loggers = [logging.getLogger()]
    loggers = loggers + [
        logging.getLogger(name) for name in logging.root.manager.loggerDict
    ]
    assert loggers[0].name == "root"


def test_new_level():
    csvforwkt.custom_logging.UtilsLogs.add_logging_level("TRACE", 20)
    logger = logging.getLogger("__main__")
    logger.setLevel(logging.TRACE)  # type: ignore
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.trace("Test the logger")  # type: ignore
    logger.log(logging.TRACE, "test")  # type: ignore


def test_message():
    record = csvforwkt.custom_logging.LogRecord(
        "__main__",
        logging.INFO,
        "pathname",
        2,
        "message {val1} {val2}",
        {"val1": 10, "val2": "test"},
        None,
    )
    assert "message 10 test", record.getMessage()

    record = csvforwkt.custom_logging.LogRecord(
        "__main__",
        logging.INFO,
        "pathname",
        2,
        "message {0} {1}",
        ("val1", "val2"),
        None,
    )
    assert "message val1 val2", record.getMessage()


def test_color_formatter():
    formatter = csvforwkt.custom_logging.CustomColorFormatter()
    logger = logging.getLogger("csvforwkt.custom_logging")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    logger.addHandler(logging.NullHandler())
    logger.info("test")

    shell_formatter = csvforwkt.custom_logging.ShellColorFormatter()
    record = csvforwkt.custom_logging.LogRecord(
        "__main__",
        logging.INFO,
        "pathname",
        2,
        "message {0} {1}",
        ("val1", "val2"),
        None,
    )
    shell_formatter.format(record)


def test_iau(data):
    import re

    iau_prj = {}
    content = ""
    with open("tests/iau.wkt", "r") as file:
        content = file.read()

    blank_line_regex = r"(?:\r?\n){2,}"
    wkts = re.split(blank_line_regex, content.strip())
    for wkt in wkts:
        iau_line_regexo = '"IAU",(.*),2015'
        m = re.findall(iau_line_regexo, wkt)
        id: int
        if len(m) > 1:
            id = int(m[1])
        else:
            id = int(m[0])
        iau_prj[id] = wkt

    for key in iau_prj.keys():
        if key >= 100000500 and key <= 100000585:  # ignored
            continue
        if key >= 100003600 and key <= 100003685:  # Halley
            continue
        if key >= 100004100 and key <= 100004185:  # Hartley 2
            continue
        if key >= 100009300 and key <= 100009385:  # Tempel 1 - ignored
            continue
        if key >= 200021600 and key <= 200021685:  # remark
            continue
        if key >= 200417900 and key <= 200417985:  # remark
            continue
        if key >= 202514300 and key <= 202514385:  # remark
            continue
        iau_wkt_proj = iau_prj[key]
        generated_wkt = pytest.crs[key].wkt()
        print(generated_wkt)
        # print(iau_wkt_proj)
        iau_wkt_proj = (
            iau_wkt_proj.replace("\t", "")
            .replace(" ", "")
            .replace("HunKal:20W.0", "")
            .replace(
                "Usemeanradiusassphereradiusforinteroperability.",
                "Usemeanradiusassphereforinteroperability.",
            )
            .replace("UseR_m=(a+b+c)/3asmeanradius.", "")
            .replace('AXIS["westing(W)', 'AXIS["(W)')
        )
        generated_wkt = (
            generated_wkt.replace("\t", "")
            .replace(" ", "")
            .replace(',ID["EPSG",9001]', "")
            .replace(',ID["EPSG",9122]', "")
            .replace(',ID["EPSG",9201]', "")
            .replace("HunKal:20W", "")
            .replace("Ariadne:0", "Ariadne:0.0")
            .replace("Greenwich:0", "Greenwich:0.0")
            .replace("695700000.0", "695700000")
            .replace("2440530.0", "2440530")
            .replace("6051800.0", "6051800")
            .replace("1737400.0", "1737400")
            .replace("23348017621", "2334801762")
            .replace("700617732406", "7006177324")
            .replace("944472236118", "94447223612")
            .replace("irection:0", "irection:0.0")
            .replace("Cilix:182W", "Cilix:182W.0")
            .replace("2631200.0", "2631200")
            .replace("Anat:128W", "Anat:128W.0")
            .replace("2410300.0", "2410300")
            .replace("Saga:326W", "Saga:326W.0")
            .replace("4402759810264", "44027598103")
            .replace(",198200.0,", ",198200,")
            .replace("mides:162W", "mides:162W.0")
            .replace("Salih:5W", "Salih:5W.0")
            .replace("Arete:299W", "Arete:299W.0")
            .replace("inurus:63W", "inurus:63W.0")
            .replace("Tore:340W", "Tore:340W.0")
            .replace("meric:276W", "meric:276W.0")
            .replace("345238095238", "34523809524")
            .replace("285714285714,", "2857142857,")
            .replace("3735224586285,", "37352245863,")
            .replace("meridian:0", "meridian:0.0")
            .replace("edCheops:0", "edCheops:0.0")
            .replace("8000,2.0", "8000,2")
            .replace("Kait:0", "Kait:0.0")
            .replace("9031476997579,", "90314769976,")
            .replace("laudia:146", "laudia:146.0")
            .replace("ormation:0", "ormation:0.0")
            .replace("rrected):0", "rrected):0.0")
            .replace("333.333333333336,", "333.333333,")
            .replace("edcrater:0", "edcrater:0.0")
            .replace("2608695652173,", "26086956522,")
            .replace("277.83UT:0", "277.83UT:0.0")
            .replace("Topaz:0", "Topaz:0.0")
            .replace("1331.6666666666667,", "1331.666667,")
            .replace("withW0=0:0", "withW0=0:0.0")
            .replace("Afon:0", "Afon:0.0")
            .replace("Charax:0", "Charax:0.0")
            .replace('AXIS["Easting(E)"', 'AXIS["(E)"')
            .replace('AXIS["Northing(N)"', 'AXIS["(N)"')
            .replace('AXIS["Westing(W)', 'AXIS["(W)')
            .replace('AXIS["westing(W)', 'AXIS["(W)')
            # .replace("Easting", "")
            # .replace("Northing", "")
        )
        # print(generated_wkt)
        # print(iau_wkt_proj)
        print(f"IAU code: {key}")
        assert iau_wkt_proj == generated_wkt
