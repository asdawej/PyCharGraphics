#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pychargraphics.pygraphics as pgp
import pychargraphics.pyimage as pim


if __name__ == '__main__':
    im1 = pgp.pic_redraw([
        'ВанХуа Project',
        'By asdawej'
    ])
    im2 = pgp.pic_redraw([
        'Touhou Project',
        'By ZUN'
    ])
    obj1 = pgp.PictureObj(im1)
    obj2 = pgp.DynamicObj(im2)
    pim.imwrite('im.dat', (obj1, obj2))
