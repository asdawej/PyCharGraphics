import sys, math
import pathlib as plb
sys.path.append(plb.Path('.'))
import pyconio as pco
import pygraphics as pgp


buf = pgp.Buffers(0.01)
obj = pgp.DynamicObj([['#']])
board = pgp.PaintBoard(30, 50)
board.paint(obj)
k_slow = 0.5
dv = 2
while True:
    if pco.py_kbhit():
        c = pco.py_getch()
        if c == 119:
            obj.move_r -= dv
        elif c == 115:
            obj.move_r += dv
        elif c == 97:
            obj.move_c -= dv
        elif c == 100:
            obj.move_c += dv
    board.render_flash(buf)
    obj.move_r *= k_slow
    obj.move_c *= k_slow
