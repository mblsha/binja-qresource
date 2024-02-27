# Binary Ninja QResource Extractor

Automatically finds all references to [`qRegisterResourceData`](https://wiki.qt.io/QtResources) and extracts all files to a temp directory.

Adds `Plugins → Extract QResources` menu item that does all the work.

See https://observablehq.com/@mblsha/qresource-blob-parser for a JS-based example of parsing QResource data format.
