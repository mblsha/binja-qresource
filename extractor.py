from binaryninja import (
    BinaryView,
    BackgroundTaskThread,
    BinaryReader,
    MediumLevelILOperation,
    show_message_box,
)

import os
import re
import tempfile
from typing import List, NamedTuple, Optional

from .qresource import QResource

PATTERN = re.compile(r"^(?:qInitResources_)?(.+)(?:\(.*)?$")


class Call(NamedTuple):
    bv: BinaryView
    function_name: str
    version: int
    tree_ptr: int
    names_ptr: int
    payload_ptr: int


def find_calls(bv):
    for sym in bv.get_symbols_by_name("qRegisterResourceData"):
        for caller in bv.get_callers(sym.address):
            for f in bv.get_functions_containing(caller.address):
                for b in f.mlil:
                    for i in b:
                        if i.operation == MediumLevelILOperation.MLIL_CALL:
                            if sym.address != i.dest.value.value:
                                continue
                            if len(i.params) != 4:
                                raise ValueError("unexpected params")
                            version = i.params[0].value.value
                            if version > 3:
                                raise ValueError("unexpected version")
                            tree_ptr = i.params[1].value.value
                            names_ptr = i.params[2].value.value
                            payload_ptr = i.params[3].value.value
                            function_name = f.symbol.full_name
                            match = PATTERN.match(function_name)
                            if match:
                                function_name = match.group(1)
                            else:
                                function_name = hex(f.symbol.address)
                            yield Call(
                                bv,
                                function_name,
                                version,
                                tree_ptr,
                                names_ptr,
                                payload_ptr,
                            )


class ExtractResult(NamedTuple):
    tmp_dir: str
    num_resources: int
    num_files: int


def extract(bv):
    num_resources = 0
    num_files = 0

    res = QResource()
    tmp_dir = tempfile.mkdtemp(prefix="qresource_")
    print(f"Extracting to: {tmp_dir}")
    calls = find_calls(bv)
    for c in calls:
        num_resources += 1
        print(c)
        tree = bv[c.tree_ptr :]
        names = bv[c.names_ptr :]
        payload = bv[c.payload_ptr :]
        files = res.get_files(tree, names, payload)
        for f in files:
            num_files += 1
            fname = f.name[2:]
            outname = os.path.join(tmp_dir, fname)
            dirname = os.path.dirname(outname)
            os.makedirs(dirname, exist_ok=True)
            # print(f"{fname}: {f.last_modified}")
            with open(outname, "wb") as out:
                out.write(f.data)
            os.utime(
                outname, (f.last_modified.timestamp(), f.last_modified.timestamp())
            )
    print(f"Extracted to: {tmp_dir}")
    return ExtractResult(tmp_dir, num_resources, num_files)


class ExtractQResources(BackgroundTaskThread):
    def __init__(self, bv):
        BackgroundTaskThread.__init__(self, "", True)
        self.progress = "QResource: working..."
        self.bv = bv

    def run(self):
        res = extract(self.bv)
        msg = f"Extracted {res.num_resources} resources ({res.num_files} files) to:\n{res.tmp_dir}"
        show_message_box("QResource", msg)
