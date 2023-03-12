# !usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import math
import time
import win32console as wincon


# Defines
CharMap = list[list[str]]
MapSize = tuple[int, int]


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


class PictureObj:
    '''
    picture: list[list[str]]    // Character map of the picture
    height: int                 // Height
    width: int                  // Width
    row: float                  // The row coordinate of left-top
    col: float                  // The column coordinate of left-top
    detect: list[list[bool]]    // To detect whether two objs coincide
    layer: int                  // The layer number
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


class DynamicObj(PictureObj):
    '''
    [PictureObj]
    move_length: float          // Step length of the next move
    move_angle: float           // Direction of the next move

    move: () -> None
    '''

    def __init__(self, _pic: CharMap | MapSize | tuple[CharMap, MapSize],
                 row: float = 0, col: float = 0, layer: int = 0,
                 move_length: float = 0, move_angle: float = 0) -> None:
        PictureObj.__init__(self, _pic, row=row, col=col, layer=layer)
        self.move_length = move_length
        self.move_angle = move_angle

    def move(self) -> None:
        '''Move to another place according to .move_length and .move_angle\n
        An example:\n
        .move_length = 1, .move_angle = math.pi/2\n
        <=> move up 1 <=> .row--'''
        self.row -= self.move_length*math.sin(self.move_angle)
        self.col += self.move_length*math.cos(self.move_angle)


class PaintBoard:
    '''
    height: int                     // Board height
    width: int                      // Board width
    board: list[list[str]]          // The char map display on the screen
    layers: list[list[DynamicObj]]  // To store the DynamicObj on the board

    paint: (PictureObj) -> None
    render: (Buffers) -> None
    flash: (Buffers) -> None
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


if __name__ == '__main__':
    buf = Buffers(0.05)
    obj = DynamicObj([['1', '2'], ['3', '4'], ['5', '6']], 0, 0, 0, 1, -math.pi/4)
    board = PaintBoard(30, 30)
    board.paint(obj)
    for _ in range(int(board.height/math.sin(math.pi/4))-3):
        board.render(buf)
        board.flash(buf)
    obj.move_angle = math.pi+obj.move_angle
    for _ in range(int(board.height/math.sin(math.pi/4))-3):
        board.render(buf)
        board.flash(buf)
