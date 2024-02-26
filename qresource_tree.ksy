meta:
  id: qresource_tree
  file-extension: qrcbin
  license: MIT
  endian: be
# https://github.com/qt/qtbase/blob/dev/src/corelib/io/qresource.cpp

seq:
  - id: root
    type: tree(3)

types:
  tree:
    params:
      - id: version
        type: u1
    instances:
      node_size:
        value: "version >= 2 ? 22 : 14"
      compressed:
        value: (flags & 0x01) != 0
      directory:
        value: (flags & 0x02) != 0
      compressed_zstd:
        value: (flags & 0x04) != 0

      children:
        io: _root._io
        pos: first_child_index * node_size
        type: tree(version)
        repeat: expr
        repeat-expr: children_count
        if: directory
    seq:
      - id: name_offset
        type: u4 # 4
      - id: flags
        type: u2 # 6

      # directory
      - id: children_count
        type: u4 # 10
        if: directory
      - id: first_child_index
        type: u4 # 14
        if: directory

      # file
      - id: locale
        type: locale_info # 10
        if: not directory
      - id: data_offset
        type: u4 # 14
        if: not directory

      # must be at offset 14
      - id: last_modified
        type: u8 # 22
        if: version >= 2

    -webide-representation: '{data_offset} offs:{name_offset}'

  locale_info:
    seq:
      - id: territory
        type: u2
      - id: language
        type: u2
    -webide-representation: '{territory:dec}_{language:dec}'
