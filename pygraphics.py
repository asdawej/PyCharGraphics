# !usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import math
import time
import win32console as wincon


# Defines
CharMap = list[list[str]]
MapSize = tuple[int, int]

whitespace_chars: set[str] = {'\0', ' ', '\t', '\n', '\r'}


class Buffers:
    '''
    .Buffer_Loop:
        buffer: win32console.PyConsoleScreenBuffer  // The buffer to write in
        next: .Buffer_Loop                          // The Buffer_Loop of the buffer to print out

    wait: float             // The waiting time for flash
    buffers: .Buffer_Loop   // Two buffer areas

    print: (str) -> None
    flash: () -> None
    '''
    class Buffer_Loop:
        def __init__(self, _next: 'Buffers.Buffer_Loop' = None) -> None:
            self.buffer: wincon.PyConsoleScreenBufferType = wincon.CreateConsoleScreenBuffer()
            if not _next:
                self.next = Buffers.Buffer_Loop(_next=self)
            else:
                self.next = _next

    def __init__(self, _wait: float = 0) -> None:
        self.wait = _wait
        self.buffers = Buffers.Buffer_Loop()
        self.buffers.next.buffer.SetConsoleActiveScreenBuffer()

    def print(self, _s: str = '\n') -> None:
        'Write in the console buffer'
        self.buffers.buffer.WriteConsole(_s)

    def flash(self) -> None:
        'Switch console buffer'
        time.sleep(self.wait)
        self.buffers.buffer.SetConsoleActiveScreenBuffer()
        self.buffers = self.buffers.next
        self.buffers.buffer.Close()
        self.buffers.buffer = wincon.CreateConsoleScreenBuffer()


def pic_resize(pic: CharMap, new_size: MapSize) -> CharMap:
    'Resize a char map'
    _size = (len(pic), len(pic[0]))
    if new_size[0] > _size[0]:
        for _ in range(new_size[0]-_size[0]):
            pic.append([' ']*_size[1])
    if new_size[1] > _size[1]:
        for _i in range(new_size[0]):
            for _ in range(new_size[1]-_size[1]):
                pic[_i].append(' ')
    return [
        _l[:new_size[1]]
        for _l in pic[:new_size[0]]
    ]


def pic_redraw(pic: list[str]) -> CharMap:
    'Make a string list into a char map'
    r = len(pic)
    c = max([len(s) for s in pic])
    new_pic = []
    for i in range(r):
        new_pic.append(list(pic[i])+[' ']*(c-len(pic[i])))
    return new_pic


class PictureObj:
    '''
    picture: list[list[str]]    // Character map of the picture
    height: int                 // Height
    width: int                  // Width
    row: float                  // The row coordinate of left-top
    col: float                  // The column coordinate of left-top
    detect: list[list[bool]]    // To detect whether two objs coincide
    layer: int                  // The layer number

    hollow: () -> None
    '''

    def __init__(self, _pic: CharMap | MapSize | tuple[CharMap, MapSize],
                 row: float = 0, col: float = 0, layer: int = 0) -> None:
        if isinstance(_pic[0], list):
            # _pic: CharMap
            if isinstance(_pic[0][0], str):
                self.height = len(_pic)
                self.width = len(_pic[0])
                self.picture = _pic
            # _pic: tuple[CharMap, MapSize]
            else:
                self.height = _pic[1][0]
                self.width = _pic[1][1]
                self.picture = pic_resize(_pic[0], _pic[1])
        # _pic: MapSize
        else:
            self.height = _pic[0]
            self.width = _pic[1]
            self.picture = [[' ']*self.width for _ in range(self.height)]
        self.row = row
        self.col = col
        self.detect = [[True]*self.width for _ in range(self.height)]
        self.layer = layer

    def hollow(self) -> None:
        'Delete all the blank char(null, space, tab, newline, return, etc) from the .detect'
        for i in range(self.height):
            for j in range(self.width):
                if self.picture[i][j] in whitespace_chars:
                    self.detect[i][j] = False


class DynamicObj(PictureObj):
    '''
    [PictureObj]
    move_r: float               // Move in row
    move_c: float               // Move in column

    [PictureObj]
    move: () -> None
    '''

    def __init__(self, _pic: CharMap | MapSize | tuple[CharMap, MapSize],
                 row: float = 0, col: float = 0, layer: int = 0,
                 move_r: float = 0, move_c: float = 0) -> None:
        PictureObj.__init__(self, _pic, row=row, col=col, layer=layer)
        self.move_r = move_r
        self.move_c = move_c

    def move(self) -> None:
        '''Move to another place according to .move_r and .move_c\n
        An example:\n
        .row = 0, .col = 0\n
        .move_r = 1, .move_c = 2\n
        => .row = 1, .col = 2'''
        self.row += self.move_r
        self.col += self.move_c


class PaintBoard:
    '''
    height: int                         // Board height
    width: int                          // Board width
    board: list[list[str]]              // The char map display on the screen
    layers: list[list[DynamicObj]]      // To store the DynamicObj on the board
    objs_map: list[list[PictureObj]]    // The char possession of objs

    paint: (PictureObj) -> None
    erase: (PictureObj) -> None
    render: (Buffers) -> None
    flash: (Buffers) -> None
    render_flash: (Buffers) -> None
    detect_border: (DynamicObj) -> bool
    detect_obj: (DynamicObj, PictureObj) -> bool

    _paint: (int, int) -> None
    _erase: (PictureObj) -> None
    '''

    def __init__(self, _h: int, _w: int) -> None:
        self.height = _h
        self.width = _w
        self.board = [[' ']*_w for _ in range(_h)]
        self.layers: list[list[DynamicObj]] = []
        self.objs_map: list[list[PictureObj]] = [[None]*_w for _ in range(_h)]

    def _paint(self, target_obj: PictureObj) -> None:
        'Original method of painting a PictureObj'
        int_row = int(target_obj.row)
        int_col = int(target_obj.col)
        for i in range(int_row, int_row+target_obj.height):
            for j in range(int_col, int_col+target_obj.width):
                if self.objs_map[i][j] == None or target_obj.layer >= self.objs_map[i][j].layer:
                    if target_obj.detect[i-int_row][j-int_col]:
                        self.objs_map[i][j] = target_obj
                    self.board[i][j] = target_obj.picture[i-int_row][j-int_col]

    def _erase(self, target_obj: PictureObj) -> None:
        'Original method of erasing a PictureObj'
        int_row = int(target_obj.row)
        int_col = int(target_obj.col)
        for i in range(int_row, int_row+target_obj.height):
            for j in range(int_col, int_col+target_obj.width):
                if self.objs_map[i][j] == target_obj:
                    self.objs_map[i][j] = None
                    self.board[i][j] = ' '

    def paint(self, new_obj: PictureObj) -> None:
        'Put a new PictureObj on the PaintBoard'
        if (_length := len(self.layers)) <= new_obj.layer:
            for _ in range(new_obj.layer-(_length-1)):
                self.layers.append([])
        self._paint(new_obj)
        # new_obj: DynamicObj
        if isinstance(new_obj, DynamicObj):
            self.layers[new_obj.layer].append(new_obj)
    
    def erase(self, old_obj: PictureObj) -> None:
        'Remove a PictureObj from the PaintBoard'
        self._erase(old_obj)
        # old_obj: DynamicObj
        if isinstance(old_obj, DynamicObj):
            self.layers[old_obj.layer].remove(old_obj)

    def render(self, buf: Buffers) -> None:
        'Display the board on the screen'
        for _l in self.board:
            buf.print(''.join(_l)+'\n')

    def flash(self, buf: Buffers) -> None:
        'Flash screen'
        buf.flash()
        for _lay in self.layers:
            for _x in _lay:
                self._erase(_x)
                _x.move()
                self._paint(_x)

    def render_flash(self, buf: Buffers) -> None:
        'self.render(buf); self.flash(buf)'
        self.render(buf)
        self.flash(buf)

    def detect_border(self, obj: DynamicObj) -> bool:
        'Check if out of the borders'
        obj_new_r = int(obj.row+obj.move_r)
        obj_new_c = int(obj.col+obj.move_c)
        return (obj_new_r < 0 or obj_new_c < 0) or (obj_new_r >= self.height or obj_new_c >= self.width)

    def detect_obj(self, obj: DynamicObj, target: PictureObj) -> bool:
        'Check if get into another obj'
        obj_new_r = int(obj.row+obj.move_r)
        obj_new_c = int(obj.col+obj.move_c)
        if isinstance(target, DynamicObj):
            target_new_r = int(target.row+target.move_r)
            target_new_c = int(target.col+target.move_c)
            target_new_range_r = range(target_new_r, target_new_r+target.height)
            target_new_range_c = range(target_new_c, target_new_c+target.width)
            for i in range(obj_new_r, obj_new_r+obj.height):
                for j in range(obj_new_c, obj_new_c+obj.width):
                    if i in target_new_range_r and j in target_new_range_c:
                        if obj.detect[i-obj_new_r][j-obj_new_c] and target.detect[i-target_new_r][j-target_new_c]:
                            return True
        else:
            for i in range(obj_new_r, obj_new_r+obj.height):
                for j in range(obj_new_c, obj_new_c+obj.width):
                    if self.objs_map[i][j] == target:
                        return True
        return False


if __name__ == '__main__':
    buf = Buffers(0.01)
    obj = DynamicObj([['#']])
    board = PaintBoard(30, 20)
    board.paint(obj)
    obj.move_r = 1

    def f(x):
        return 10*math.sin(x/math.pi)+10
    for i in range(29):
        obj.move_c = f(0) if i == 0 else f(i)-f(i-1)
        board.render_flash(buf)
        board.paint(PictureObj(obj.picture, obj.row, obj.col, 1))
    import os
    os.system('pause')
