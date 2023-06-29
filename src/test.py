# !usr/bin/env python
# -*- coding: utf-8 -*-

# === 前置部分 ===


import pychargraphics.pyconio as pco
import pychargraphics.pygraphics as pgp
import pychargraphics.pyimage as pim

import math
import time
import random as rd
from typing import Callable


# SIZE
R, C = 25, 50

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


# === 对象生成 ===


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
board = pgp.PaintBoard(R, C)                                            # 画板


# === 函数 ===


def keyboard_check(obj: pgp.DynamicObj) -> None:
    '检测键盘'
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


def crush_check(board: pgp.PaintBoard,
                obj: pgp.DynamicObj, enemies: list[pgp.DynamicObj],
                enemy_init: Callable[[pgp.DynamicObj, pgp.PaintBoard], None]) -> pgp.DynamicObj:
    '碰撞检测'
    for enemy in enemies:
        # 撞上敌机
        if board.detect_obj(obj, enemy):
            return enemy
        # 敌机碰到边界
        if board.detect_border(enemy) or board.detect_obj(enemy, background):
            enemy.move_r = enemy.move_c = 0
            enemy_init(enemy, board)
    # 自机碰到边界
    if board.detect_border(obj) or board.detect_obj(obj, background):
        obj.move_r = obj.move_c = 0
    return None


# === 1.开场 ===


t0 = time.time()
board.paint(background)
imst = pim.imread('im.dat')
imst.objs[0].row = R//2-1
imst.objs[0].col = C//2-4
board.paint(imst.objs[0])
while time.time()-t0 <= 3:
    board.render_flash(buf)
board._erase(imst.objs[0])


# === 2.随机斜向弹幕 ===


def enemy_init(enemy: pgp.DynamicObj, board: pgp.PaintBoard) -> None:
    '敌机初始化, 随机取一个顶部位置随机方向射出'
    board._erase(enemy)  # 只是擦除敌机, 没有从画板上去除敌机
    enemy.row = 1
    enemy.col = rd.randint(1, C-2)
    enemy_ang = (rd.random()-0.5)*math.pi/2
    enemy_len = 0.25
    enemy.move_r = enemy_len*math.cos(enemy_ang)
    enemy.move_c = enemy_len*math.sin(enemy_ang)


# 绘制自机、敌机
board.paint(obj)
for enemy in enemies:
    board.paint(enemy)
    enemy_init(enemy, board)
board.render_flash(buf)


t0 = time.time()
t1 = 5
while time.time()-t0 <= t1:
    keyboard_check(obj)
    break_flag = crush_check(board, obj, enemies, enemy_init)
    board.render_flash(buf)
    obj.move_r = obj.move_c = 0
    # 撞上敌机
    if break_flag:
        exit()


# === 3.随机下落弹幕 ===


def enemy_init(enemy: pgp.DynamicObj, board: pgp.PaintBoard) -> None:
    '敌机初始化, 随机取一个顶部位置射出'
    board._erase(enemy)  # 只是擦除敌机, 没有从画板上去除敌机
    enemy.row = 1
    enemy.col = rd.randint(1, C-2)
    enemy.move_r = 0.25
    enemy.move_c = 0


t0 = time.time()
t2 = 100
while time.time()-t0 <= t2:
    keyboard_check(obj)
    break_flag = crush_check(board, obj, enemies, enemy_init)
    # 撞上敌机
    if break_flag:
        board.erase(break_flag)
        enemies.remove(break_flag)
    board.render_flash(buf)
    obj.move_r = obj.move_c = 0
    if not enemies:
        break
