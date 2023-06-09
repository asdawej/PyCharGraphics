import sys
import pathlib as plb
sys.path.append(plb.Path('.'))
import pyconio as pco
import pygraphics as pgp

import math
import random as rd

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

buf = pgp.Buffers(0.01)                             # 缓冲区
obj = pgp.DynamicObj([['#']], row=R-2, col=C//2)    # 自机
enemy = pgp.DynamicObj([['@']], row=1, col=1)       # 敌机
def enemy_init(enemy: pgp.DynamicObj, board: pgp.PaintBoard):
    '敌机初始化, 随机取一个顶部位置射出'
    board._erase(enemy) # 只是擦除敌机, 没有从画板上去除敌机
    enemy.row = 1
    enemy.col = rd.randint(1, C-2)
    enemy_mov_ang = (rd.random()-0.5)*math.pi
    enemy_mov_len = 0.25
    enemy.move_r = enemy_mov_len*math.cos(enemy_mov_ang)
    enemy.move_c = enemy_mov_len*math.sin(enemy_mov_ang)
board = pgp.PaintBoard(R, C)
board.paint(background)
board.paint(obj)
board.paint(enemy)
enemy_init(enemy, board)
board.render_flash(buf)
while True:
    # 检测键盘
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
    # 撞上敌机
    if board.detect_obj(obj, enemy):
        break
    # 自机碰到边界
    if board.detect_border(obj) or board.detect_obj(obj, background):
        obj.move_r = obj.move_c = 0
    # 敌机碰到边界
    if board.detect_border(enemy) or board.detect_obj(enemy, background):
        enemy.move_r = enemy.move_c = 0
        enemy_init(enemy, board)
    board.render_flash(buf)
    obj.move_r = obj.move_c = 0
