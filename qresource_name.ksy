meta:
  id: qresource_name
  file-extension: qrcbin
  license: MIT
  endian: be
# https://github.com/qt/qtbase/blob/dev/src/corelib/io/qresource.cpp

seq:
  - id: node_name
    type: name_entry

types:
  name_entry:
    seq:
      - id: len
        type: u2
      - id: hash
        type: u4
      - id: name
        type: str
        size: len * 2
        encoding: UTF-16BE
    -webide-representation: '"{name}" {hash}'

