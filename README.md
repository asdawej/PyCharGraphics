# PyCharGraphics

[Github](https://github.com/asdawej/pygraphics_char)

This package `pychargraphics` contains 3 sub-modules - `pygraphics`, `pyimage` and `pyconio`.

`pygraphics` is the most important part, which realizes the construction of double-buffers and an object-oriented character graphics in Command Line Interface (CLI).

`pyimage` provides two methods (`imwrite` and `imread`) to deal with file I/O, or more detailed, pack `PictureObj` into a file or extract them from.

`pyconio` is a `.pyd` module. It is actually the Python version of C Language's `conio.h`:

| C | Python |
| - | - |
| `int _kbhit(void)` | `py_kbhit() -> bool` |
| `char _getch(void)` | `py_getch() -> int` |

_Import statement:_

```Python
import pychargraphics
```