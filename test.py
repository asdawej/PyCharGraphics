import sys
import pathlib as plb
sys.path.append(plb.Path('.'))
import pyconio as pco
import pygraphics as pgp

import math

# SIZE
R, C = 25, 50

# Background
background = [[' ']*C for _ in range(R)]
background[0] = ['=']*C
background[-1] = ['=']*C
for i in range(R):
    background[i][0] = '#'
    background[i][-1] = '#'
background = pgp.PictureObj(background)
background.hollow()

buf = pgp.Buffers(0.01)
obj = pgp.DynamicObj([['#']], row=1, col=1)
enemy = pgp.DynamicObj([['@']], row=R-2, col=C-2)
board = pgp.PaintBoard(R, C)
board.paint(obj)
board.paint(enemy)
board.paint(background)
board.render_flash(buf)
while True:
    enemy_mov_ang = math.atan2(obj.col-enemy.col, obj.row-enemy.row)
    enemy_mov_len = 0.05
    enemy.move_r = enemy_mov_len*math.cos(enemy_mov_ang)
    enemy.move_c = enemy_mov_len*math.sin(enemy_mov_ang)
    if pco.py_kbhit():
        c = pco.py_getch()
        if c == 119:
            obj.move_r = -1
        if c == 115:
            obj.move_r = 1
        if c == 97:
            obj.move_c = -1
        if c == 100:
            obj.move_c = 1
    if board.detect_obj(obj, enemy):
        break
    if board.detect_border(obj) or board.detect_obj(obj, background):
        obj.move_r = obj.move_c = 0
    if board.detect_border(enemy) or board.detect_obj(enemy, background):
        enemy.move_r = enemy.move_c = 0
    board.render_flash(buf)
    obj.move_r = obj.move_c = 0
