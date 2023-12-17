import logging
import shutil
from pathlib import Path

import pytest

from twlib.environment import ROOT_DIR

_log = logging.getLogger(__name__)
log_fmt = r"%(asctime)-15s %(levelname)s %(name)s %(funcName)s:%(lineno)d %(message)s"
logging.basicConfig(format=log_fmt, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")
logging.getLogger("botocore").setLevel(logging.INFO)
logging.getLogger("boto3").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)

SENTINEL = "test_proj-1234"
TEST_PROJ = ROOT_DIR / "tests/resources/test_proj"
REF_PROJ = ROOT_DIR / "tests/resources/ref_proj"
TEMP_DIR = "/tmp/xxx"


# run fixture before all tests
@pytest.fixture(autouse=True)
def setup():
    # scope to class if necessary: https://stackoverflow.com/a/50135020
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)
    northwind_db = ROOT_DIR / "./tests/resources/northwind.db"
    northwind_original_db = ROOT_DIR / "./tests/resources/northwind.original.db"
    shutil.copy(northwind_original_db, northwind_db)

    # shutil.rmtree(TEST_PROJ, ignore_errors=True)
    # shutil.copytree(REF_PROJ, TEST_PROJ)


def test_setup():
    assert True
