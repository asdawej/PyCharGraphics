# -------------------- #
# __author__ = asdawej #
# -------------------- #


from __future__ import annotations
from typing import Container, overload

from . import pygraphics as pgp


class ImStruct:
    length: int
    typemap: list[bool]
    objs: list[pgp.PictureObj]

    @overload
    def __init__(self, objs: pgp.PictureObj = None) -> None: ...

    @overload
    def __init__(self, objs: Container[pgp.PictureObj] = None) -> None: ...


def imwrite(file, objs: pgp.PictureObj | Container[pgp.PictureObj], encoding: str = 'utf-8') -> None: ...


def imread(file, encoding: str = 'utf-8') -> ImStruct: ...
