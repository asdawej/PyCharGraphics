# !usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Container

import sys
import pathlib as plb
sys.path.append(plb.Path('.'))
import pygraphics as pgp

import pickle as pkl


class ImStruct:
    '''
    length: int                     // Number of PictureObj
    typemap: list[bool]             // To record PictureObj or DynamicObj
    objs: list[pgp.PictureObj]      // PictureObj in list
    '''

    def __init__(self, objs: pgp.PictureObj | Container[pgp.PictureObj]) -> None:
        if isinstance(objs, pgp.PictureObj):
            self.length = 1
            self.typemap = [isinstance(objs, pgp.DynamicObj)]
            self.objs = [objs]
        else:
            self.length = len(objs)
            self.typemap: list[bool] = []
            self.objs: list[pgp.PictureObj] = []
            for x in objs:
                self.typemap.append(isinstance(x, pgp.DynamicObj))
                self.objs.append(x)


def imwrite(file, objs: pgp.PictureObj | Container[pgp.PictureObj]) -> None:
    'To write one or more PictureObj or DynamicObj into a file'
    with open(file, 'wb') as fp:
        imst = ImStruct(objs)
        pkl.dump(imst, fp)


def imread(file) -> ImStruct:
    'To read some PictureObj or DynamicObj from a file'
    with open(file , 'rb') as fp:
        return pkl.load(fp)


if __name__ == '__main__':
    im = [['#', ' '], ['#', '$']]
    obj = pgp.DynamicObj(im, move_r=1)
    imwrite('im.dat', obj)
    imst = imread('im.dat')
    bf = pgp.Buffers(0.01)
    bd = pgp.PaintBoard(30, 2)
    bd.paint(imst.objs[0])
    while True:
        bd.render_flash(bf)
