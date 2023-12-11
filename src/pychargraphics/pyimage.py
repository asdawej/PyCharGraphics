# -------------------- #
# __author__ = asdawej #
# -------------------- #


from __future__ import annotations
from typing import Container

from . import pygraphics as pgp


class ImStruct:
    '''
    member:
    - `length`: `int`                   // Number of `PictureObj`
    - `typemap`: `list[bool]`           // To record `PictureObj` or `DynamicObj`
    - `objs`: `list[pgp.PictureObj]`    // `PictureObj` in list
    '''

    def __init__(self, objs: pgp.PictureObj | Container[pgp.PictureObj] = None) -> None:
        if not objs:
            self.length = 0
            self.typemap = []
            self.objs = []
            return
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


def imwrite(file, objs: pgp.PictureObj | Container[pgp.PictureObj], encoding: str = 'utf-8') -> None:
    'To write one or more `PictureObj` or `DynamicObj` into a file'
    with open(file, 'w', encoding=encoding) as fp:
        imst = ImStruct(objs)
        fp.write(str(imst.length) + '\n')
        for x in imst.typemap:
            fp.write(str(int(x)))
        fp.write('\n')
        for obj in imst.objs:
            # PictureObj
            fp.write(str(obj.height) + ' ' +
                     str(obj.width) + ' ' +
                     str(obj.row) + ' ' +
                     str(obj.col) + ' ' +
                     str(obj.layer) + '\n')
            for i in range(obj.height):
                for j in range(obj.width):
                    fp.write(str(int(obj.detect[i][j])))
                fp.write('\n')
            for i in range(obj.height):
                for j in range(obj.width):
                    fp.write(obj.picture[i][j])
                fp.write('\n')
            # DynamicObj
            if isinstance(obj, pgp.DynamicObj):
                fp.write(str(obj.move_r) + ' ' + str(obj.move_c) + '\n')


def imread(file, encoding: str = 'utf-8') -> ImStruct:
    'To read some `PictureObj` or `DynamicObj` from a file'
    with open(file, 'r', encoding=encoding) as fp:
        length = int(fp.readline())
        typemap = [x == '1' for x in fp.readline()]
        objs: list[pgp.PictureObj] = []
        for i in range(length):
            attr1 = [int(s) for s in fp.readline().split(' ')]
            detect: list[list[bool]] = []
            for j in range(attr1[0]):
                detect.append([])
                for _ in range(attr1[1]):
                    detect[j].append(bool(int(fp.read(1))))
                fp.read(1)
            picture: pgp.CharMap = []
            for j in range(attr1[0]):
                picture.append([])
                for _ in range(attr1[1]):
                    picture[j].append(fp.read(1))
                fp.read(1)
            # DynamicObj
            if typemap[i]:
                attr2 = [int(s) for s in fp.readline().split(' ')]
                obj = pgp.DynamicObj((picture, (attr1[0], attr1[1])),
                                     row=attr1[2], col=attr1[3],
                                     layer=attr1[4],
                                     move_r=attr2[0], move_c=attr2[1])
            # PictureObj
            else:
                obj = pgp.PictureObj((picture, (attr1[0], attr1[1])),
                                     row=attr1[2], col=attr1[3],
                                     layer=attr1[4])
            objs.append(obj)
        imst = ImStruct()
        imst.length = length
        imst.typemap = typemap
        imst.objs = objs
        return imst
