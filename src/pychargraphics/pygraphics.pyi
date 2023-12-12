#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------- #
# __author__ = asdawej #
# -------------------- #


from __future__ import annotations
from typing import overload
from win32console import PyConsoleScreenBufferType

CharMap = list[list[str]]
MapSize = tuple[int, int]

whitespace_chars: set[str]


class Buffers:
    wait: float
    buffers: Buffers.Buffer_Loop

    class Buffer_Loop:
        buffer: PyConsoleScreenBufferType
        next: Buffers.Buffer_Loop

        def __init__(self, _next: Buffers.Buffer_Loop = None) -> None: ...

    def __init__(self, _wait: float = 0) -> None: ...

    def print(self, _s: str = '\n') -> None: ...

    def flash(self) -> None: ...


def pic_resize(pic: CharMap, new_size: MapSize) -> CharMap: ...


def pic_redraw(pic: list[str]) -> CharMap: ...


class PictureObj:
    picture: CharMap
    height: int
    width: int
    row: float
    col: float
    detect: list[list[bool]]
    layer: int

    @overload
    def __init__(self, _pic: CharMap,
                 row: float = 0, col: float = 0, layer: int = 0) -> None: ...

    @overload
    def __init__(self, _pic: MapSize,
                 row: float = 0, col: float = 0, layer: int = 0) -> None: ...

    @overload
    def __init__(self, _pic: tuple[CharMap, MapSize],
                 row: float = 0, col: float = 0, layer: int = 0) -> None: ...

    def hollow(self) -> None: ...


class DynamicObj(PictureObj):
    move_r: float
    move_c: float

    @overload
    def __init__(self, _pic: CharMap,
                 row: float = 0, col: float = 0, layer: int = 0,
                 move_r: float = 0, move_c: float = 0) -> None: ...

    @overload
    def __init__(self, _pic: MapSize,
                 row: float = 0, col: float = 0, layer: int = 0,
                 move_r: float = 0, move_c: float = 0) -> None: ...

    @overload
    def __init__(self, _pic: tuple[CharMap, MapSize],
                 row: float = 0, col: float = 0, layer: int = 0,
                 move_r: float = 0, move_c: float = 0) -> None: ...

    def move(self) -> None: ...


class PaintBoard:
    height: int
    width: int
    board: CharMap
    layers: list[list[DynamicObj]]
    objs_map: list[list[PictureObj]]

    def __init__(self, _h: int, _w: int) -> None: ...

    def _paint(self, target_obj: PictureObj) -> None: ...

    def _erase(self, target_obj: PictureObj) -> None: ...

    def paint(self, new_obj: PictureObj) -> None: ...

    def erase(self, old_obj: PictureObj) -> None: ...

    def render(self, buf: Buffers) -> None: ...

    def flash(self, buf: Buffers) -> None: ...

    def render_flash(self, buf: Buffers) -> None: ...

    def detect_border(self, obj: DynamicObj) -> bool: ...

    def detect_obj(self, obj: DynamicObj, target: PictureObj) -> bool: ...
