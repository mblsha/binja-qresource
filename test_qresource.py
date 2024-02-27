import pytest
import os
from pprint import pprint
import datetime

from .qresource import QResource, File

NAMES_START_OFFSET = 0xDC
PAYLOAD_START_OFFSET = 0x16C

path = os.path.join(os.path.dirname(__file__), "test2.qrcbin")
with open(path, "rb") as f:
    data = f.read()


def test_parse_name():
    res = QResource()
    name = res.parse_name(data, NAMES_START_OFFSET)
    assert name.name == "res"
    assert name.hash == 30915


def test_parse_tree_raw():
    res = QResource()
    root = res.parse_tree_raw(data)
    print(root.children)

    assert root.version == 3
    assert root.directory == True
    assert len(root.children) == 1

    dir = root.children[0]
    assert len(dir.children) == 4


def test_get_files():
    res = QResource()
    view = memoryview(data)
    names_data = view[NAMES_START_OFFSET:]
    payload_data = view[PAYLOAD_START_OFFSET:]
    files = res.get_files(data, names_data, payload_data)
    assert len(files) == 6

    assert files[0] == File(
        name=":/res/1.txt",
        hash=3431412,
        last_modified=datetime.datetime(2024, 2, 26, 3, 35, 3, 572000),
        data=b"1\n",
    )
    assert files[1] == File(
        name=":/res/6.txt",
        hash=3759092,
        last_modified=datetime.datetime(2024, 2, 26, 3, 59, 42, 298000),
        data=b"6\n",
    )
    assert files[2] == File(
        name=":/res/bardir/4.txt",
        hash=3628020,
        last_modified=datetime.datetime(2024, 2, 26, 3, 35, 21, 755000),
        data=b"4\n",
    )
    assert files[3] == File(
        name=":/res/bardir/5.txt",
        hash=3693556,
        last_modified=datetime.datetime(2024, 2, 26, 3, 35, 25, 719000),
        data=b"5\n",
    )
    assert files[4] == File(
        name=":/res/foodir/2.txt",
        hash=3496948,
        last_modified=datetime.datetime(2024, 2, 26, 3, 35, 9, 769000),
        data=b"2\n",
    )
    assert files[5] == File(
        name=":/res/foodir/3.txt",
        hash=3562484,
        last_modified=datetime.datetime(2024, 2, 26, 3, 35, 12, 841000),
        data=b"3\n",
    )
