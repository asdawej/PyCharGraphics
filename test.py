import sys
import pathlib as plb
sys.path.append(plb.Path('.'))
import pyconio as pco
import pygraphics as pgp

import math
import random as rd

# SIZE
R, C = 25, 100

# 键值
KB_W = 119
KB_A = 97
KB_S = 115
KB_D = 100
KB_FUNC = 224
KB_UP = 72
KB_DOWN = 80
KB_LEFT = 75
KB_RIGHT = 77

# Background
background = [[' ']*C for _ in range(R)]
background[0] = ['=']*C
background[-1] = ['=']*C
for i in range(R):
    background[i][0] = '#'
    background[i][-1] = '#'
background = pgp.PictureObj(background)
background.hollow()

buf = pgp.Buffers(0.01)                                                 # 缓冲区
obj = pgp.DynamicObj([['#']], row=R-2, col=C//2)                        # 自机
enemies = [pgp.DynamicObj([['@']], row=1, col=1) for _ in range(10)]    # 敌机

def enemy_init(enemy: pgp.DynamicObj, board: pgp.PaintBoard):
    '敌机初始化, 随机取一个顶部位置射出'
    board._erase(enemy) # 只是擦除敌机, 没有从画板上去除敌机
    enemy.row = 1
    enemy.col = rd.randint(1, C-2)
    enemy.move_r = 0.25
    enemy.move_c = 0

board = pgp.PaintBoard(R, C)
board.paint(background)
board.paint(obj)
for enemy in enemies:
    board.paint(enemy)
    enemy_init(enemy, board)
board.render_flash(buf)

break_flag: bool = False
while True:
    # 检测键盘
    if pco.py_kbhit():
        c = pco.py_getch()
        if c == KB_W:
            obj.move_r = -1
        elif c == KB_S:
            obj.move_r = 1
        elif c == KB_A:
            obj.move_c = -1
        elif c == KB_D:
            obj.move_c = 1
        elif c == KB_FUNC:
            cc = pco.py_getch()
            if cc == KB_UP:
                obj.move_r = -1
            elif cc == KB_DOWN:
                obj.move_r = 1
            elif cc == KB_LEFT:
                obj.move_c = -1
            elif cc == KB_RIGHT:
                obj.move_c = 1

    for enemy in enemies:
        # 撞上敌机
        if board.detect_obj(obj, enemy):
            break_flag = True
            break
        # 敌机碰到边界
        if board.detect_border(enemy) or board.detect_obj(enemy, background):
            enemy.move_r = enemy.move_c = 0
            enemy_init(enemy, board)
    # 自机碰到边界
    if board.detect_border(obj) or board.detect_obj(obj, background):
        obj.move_r = obj.move_c = 0

    board.render_flash(buf)
    obj.move_r = obj.move_c = 0
    # 撞上敌机
    if break_flag:
        break
