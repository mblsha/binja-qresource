# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class QresourceTree(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.root = QresourceTree.Tree(3, self._io, self, self._root)

    class Tree(KaitaiStruct):
        def __init__(self, version, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.version = version
            self._read()

        def _read(self):
            self.name_offset = self._io.read_u4be()
            self.flags = self._io.read_u2be()
            if self.directory:
                self.children_count = self._io.read_u4be()

            if self.directory:
                self.first_child_index = self._io.read_u4be()

            if not (self.directory):
                self.locale = QresourceTree.LocaleInfo(self._io, self, self._root)

            if not (self.directory):
                self.data_offset = self._io.read_u4be()

            if self.version >= 2:
                self.last_modified = self._io.read_u8be()


        @property
        def compressed_zstd(self):
            if hasattr(self, '_m_compressed_zstd'):
                return self._m_compressed_zstd

            self._m_compressed_zstd = (self.flags & 4) != 0
            return getattr(self, '_m_compressed_zstd', None)

        @property
        def node_size(self):
            if hasattr(self, '_m_node_size'):
                return self._m_node_size

            self._m_node_size = (22 if self.version >= 2 else 14)
            return getattr(self, '_m_node_size', None)

        @property
        def directory(self):
            if hasattr(self, '_m_directory'):
                return self._m_directory

            self._m_directory = (self.flags & 2) != 0
            return getattr(self, '_m_directory', None)

        @property
        def compressed(self):
            if hasattr(self, '_m_compressed'):
                return self._m_compressed

            self._m_compressed = (self.flags & 1) != 0
            return getattr(self, '_m_compressed', None)

        @property
        def children(self):
            if hasattr(self, '_m_children'):
                return self._m_children

            if self.directory:
                io = self._root._io
                _pos = io.pos()
                io.seek((self.first_child_index * self.node_size))
                self._m_children = []
                for i in range(self.children_count):
                    self._m_children.append(QresourceTree.Tree(self.version, io, self, self._root))

                io.seek(_pos)

            return getattr(self, '_m_children', None)


    class LocaleInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.territory = self._io.read_u2be()
            self.language = self._io.read_u2be()



