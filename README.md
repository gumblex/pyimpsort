# PyImpSort

Sort the imports in Python scripts by length.

## Usage

    python impsort.py in.py > out.py

## Feature

**WARNING:** Due to a [bug](https://bugs.python.org/issue24447) in `tokenize.untokenize`, the result may not be correct
when using tabs for indentation.

* Sort imports by length without comments.
* Only touch imports at root indentation level.
* `from` imports always comes last.
* Preserve separated import groups.
* Multi-line imports are ignored.
* Stable sort.
* Python 2.5+ (including 3+)

## Example

See `test.py` for more demo.

**Before:**

    import sys
    import struct
    from shutil import copy
    import os # this is os
    import socket
    from os import path
    import threading
    import socketserver
    import multiprocessing

**After:**

    import os # this is os
    import sys
    import struct
    import socket
    import threading
    import socketserver
    import multiprocessing
    from os import path
    from shutil import copy

## License

Public Domain (the Unlicense)
