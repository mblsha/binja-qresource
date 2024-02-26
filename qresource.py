import struct
from typing import List, NamedTuple, Optional
from datetime import datetime

from kaitaistruct import KaitaiStream, BytesIO
from .qresource_tree import QresourceTree
from .qresource_name import QresourceName


def msec_since_epoch_to_datetime(msec) -> datetime:
    sec = msec / 1000.0
    return datetime.utcfromtimestamp(sec)


class File(NamedTuple):
    name: str
    hash: int
    last_modified: int
    data: bytes


class QResource:
    def __init__(self):
        pass

    def parse_tree_raw(self, data: bytes) -> QresourceTree.Tree:
        ks = KaitaiStream(BytesIO(data))
        r = QresourceTree(ks)
        return r.root

    def parse_name(self, data: bytes, offset: int) -> QresourceName:
        ks = KaitaiStream(BytesIO(data[offset:]))
        r = QresourceName(ks)
        return r.node_name

    def get_files_recursive(
        self,
        names_data: bytes,
        payload_data: bytes,
        entries,
        path=":/",
    ) -> List[File]:
        r = []
        for e in entries:
            name = self.parse_name(names_data, e.name_offset)
            p = path + name.name
            if e.directory:
                r = r + self.get_files_recursive(
                    names_data,
                    payload_data,
                    e.children,
                    p + "/",
                )
            else:
                last_modified = msec_since_epoch_to_datetime(e.last_modified)
                size = struct.unpack_from(">I", payload_data, e.data_offset)[0]
                arr = payload_data[e.data_offset + 4 : e.data_offset + 4 + size]
                r.append(File(p, name.hash, last_modified, arr))
        return r

    def get_files(self, tree_data: bytes, names_data: bytes, payload_data: bytes):
        root = self.parse_tree_raw(tree_data)
        return self.get_files_recursive(
            names_data,
            payload_data,
            entries=root.children,
        )
