#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
import pychargraphics.pygraphics as pgp

if __name__ == '__main__':
    buf = pgp.Buffers(0.01)
    obj = pgp.DynamicObj([['#']])
    board = pgp.PaintBoard(30, 20)
    board.paint(obj)
    obj.move_r = 1

    def f(x):
        return 10 * math.sin(x / math.pi) + 10
    for i in range(29):
        obj.move_c = f(0) if i == 0 else f(i) - f(i - 1)
        board.render_flash(buf)
        board.paint(pgp.PictureObj(obj.picture, obj.row, obj.col, 1))
    os.system('pause')
