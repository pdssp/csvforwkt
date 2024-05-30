# -*- coding: utf-8 -*-
import logging
import re
import subprocess
from typing import Dict

import pytest

import csvforwkt
from csvforwkt.crs import ICrs
from csvforwkt.csvforwkt import CsvforwktLib

# import numpy as np

# from PIL import Image
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def pytest_namespace():
    return {"crs": dict()}


@pytest.fixture
def data():
    iau_data = "data/naifcodes_radii_m_wAsteroids_IAU2015.csv"
    iau_version = 2015
    iau_doi = "doi:10.1007/s10569-017-9805-5"
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
    """Test the library output with the GDAL output.

    Also fix :
      - some number with float precision between GDAL and library output
      - some extra spaces
      - the DOI URL by waiting we regenerate the DOI URL with GDAL

    """
    iau_prj = {}
    content = ""
    with open("tests/iau.wkt", "r") as file:
        content = file.read()

    blank_line_regex = r"(?:\r?\n){2,}"
    wkts = re.split(blank_line_regex, content.strip())
    for wkt in wkts:
        iau_line_regexo = '"IAU", (.*), 2015'
        m = re.findall(iau_line_regexo, wkt)
        # print(f"{m} -> {wkt}")
        id: int
        if len(m) > 1:
            id = int(m[1])
        else:
            id = int(m[0])
        iau_prj[id] = wkt

    for key in iau_prj.keys():
        if key >= 100003600 and key <= 100003685:  # Halley
            continue
        if key >= 200021600 and key <= 200021685:  # remark
            continue
        if key >= 200417900 and key <= 200417985:  # remark
            continue
        if key >= 202514300 and key <= 202514385:  # remark
            continue
        iau_wkt_proj = iau_prj[key]
        generated_wkt = pytest.crs[key].wkt()
        iau_wkt_proj = (
            iau_wkt_proj.replace("\t", "")
            .replace(" ", "")
            .replace(
                "Usemeanradiusassphereradiusforinteroperability.",
                "Usemeanradiusassphereforinteroperability.",
            )
            .replace(
                "usassphereforinteroperability.",
                "usassphereradiusforinteroperability.",
            )
            .replace("UseR_m=(a+b+c)/3asmeanradius.", "")
        )
        generated_wkt = (
            generated_wkt.replace("\t", "")
            .replace(" ", "")
            .replace(',ID["EPSG",9201]', "")
            .replace(
                'SCALEUNIT["unity",1]', 'SCALEUNIT["unity",1,ID["EPSG",9201]]'
            )
        )
        print(generated_wkt)
        print("-------")
        print(iau_wkt_proj)
        print(f"IAU code: {key}")
        print("=============")
        print("=============")
        assert iau_wkt_proj == generated_wkt, f"IAU code: {key}"


def test_gdal(data):
    """Test if the projections are in GDAL"""
    ids_wkt = []
    content = ""
    with open("tests/iau.wkt", "r") as file:
        content = file.read()

    blank_line_regex = r"(?:\r?\n){2,}"
    wkts = re.split(blank_line_regex, content.strip())
    for wkt in wkts:
        if "TRIAXIAL" in wkt:
            # Skip triaxial : not supported in GDAL
            continue
        iau_line_regexo = '"IAU", (.*), 2015'
        m = re.findall(iau_line_regexo, wkt)
        id: int
        if len(m) > 1:
            id = int(m[1])
        else:
            id = int(m[0])
        ids_wkt.append(id)

    errors = []
    for id in ids_wkt:
        output = subprocess.run(
            ["/usr/bin/gdalsrsinfo", f"IAU_2015:{id}"], stderr=subprocess.PIPE
        )
        result = output.stderr.decode("UTF-8")
        if "failed to load SRS" in result:
            logger.error(f"Not found in GDAL for projection {id}")
            errors.append(result)
        else:
            logger.info(f"No problem for projection {id}")

    assert len(errors) == 0
