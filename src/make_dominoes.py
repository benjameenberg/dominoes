#!/usr/bin/env python
from __future__ import unicode_literals
import argparse
import logging
import math
import os
import random
import sys
import xml.etree.ElementTree as ET


GROUP = 'g'
CIRCLE = 'circle'
STYLE = 'style'
LINE = 'line'
RECT = 'rect'

DWIDTH = 96
DHEIGHT = 192
ZERO = []
ONE = [(48, 48)]
TWO = [(78, 16), (16, 78)]
THREE = [(78, 16), (48, 48), (16, 78)]
FOUR = [(78, 16), (78, 78), (16, 16), (16, 78)]
FIVE = [(78, 16), (78, 78), (48, 48), (16, 16), (16, 78)]
SIX = [(78, 16), (78, 47), (78, 78), (16, 16), (16, 47), (16, 78)]

PIP_LAYOUT = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX]
TOP = 'matrix(1, 0, 0, 1, 5, 5)'
BOTTOM = 'matrix(1, 0, 0, 1, 5, 101)'

# These get bound to methods in the DominoSVG


def identity_transform(domino):
    return M2x3(1, 0, 0, 1, 0, 0)


pi_div_2 = math.pi/2.0
rotoff = pi_div_2 / 40.0


def rotate_left_unless_double(domino):
    if domino.topnum == domino.bottomnum:
        return M2x3(1, 0, 0, 1, 0, 0)
    return M2x3(0, 1, -1, 0, 0, 0)
    # rot = random.uniform(0.0, rotoff) - pi_div_2
    # return (math.cos(rot), math.sin(rot),
    #        -math.sin(rot), math.cos(rot), 0.0, 0.0)


def indent(elem, level=0):
    i = '\n' + level*'  '
    begin = True
    for subelem in elem:
        if begin:
            begin = False
            if not elem.text or not elem.text.strip():
                elem.text = i + '  '
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        indent(subelem, level+1)
    if begin:  # No subelements, subelem unset
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    else:  # indent after last subelem
        if not subelem.tail or not subelem.tail.strip():
            subelem.tail = i

    return elem


BLACK = '0,0,0'
WHITE = '255,255,255'

WIDTH = 30.0
HEIGHT = 60.0
VIEWWIDTH = 192.0
VIEWHEIGHT = 96.0


def svg_attrs(m2d, xmlns):
    h, w = m2d.extent(HEIGHT, WIDTH)
    vh, vw = m2d.extent(VIEWHEIGHT, VIEWWIDTH)
    attrs = {
        'height': '{:.1f}mm'.format(h),
        'width': '{:.1f}mm'.format(w),
        # 'x': '0.0mm',
        # 'y': '0.0mm',
        'version': '1.1',
        'viewBox': '0.0 0.0 {:.1f} {:.1f}'.format(vw, vh)
    }
    if xmlns:
        attrs['xmlns'] = 'http://www.w3.org/2000/svg'
    return attrs


class M2x3(object):
    '''2 by 2 matrix transform , with translation)'''

    def __init__(self, a11, a12, a21, a22, t31=0.0, t32=0.0):
        self.a11, self.a12, self.a21, self.a22, self.t31, self.t32 = (
            a11, a12, a21, a22, t31, t32)

    def __mul__(self, v2d):
        return (self.a11*v2d[0] + self.a12*v2d[1] + self.t31,
                self.a21*v2d[0] + self.a22*v2d[1] + self.t32)

    def extent(self, w, h):
        ext_w, ext_h = (abs(self.a11)*w + abs(self.a12)*h,
                        abs(self.a21)*w + abs(self.a22)*h)
        return (ext_w, ext_h)

    def __str__(self):
        return str((self.a11, self.a12, self.a21, self.a22, self.t31, self.t32))


class DominoSVG(object):
    def __init__(self, topnum, bottomnum,
                 transform_fn=identity_transform, fg=BLACK, bg=WHITE, xmlns=False):
        assert topnum in range(7) and bottomnum in range(7)
        self.topnum = topnum
        self.bottomnum = bottomnum
        # bind the function to be a method,
        #   see https://stackoverflow.com/a/1015405/500902
        self.transform_meth = transform_fn.__get__(self, DominoSVG)
        self.init_svg(fg, bg, xmlns=xmlns)
        logging.debug('make (%s,%s)', topnum, bottomnum)
        logging.info("%s", dir(self))

    def init_svg(self, fg, bg, xmlns=False):
        m2d = self.transform_meth()
        # Get the transformation matrix in effect, use to calculate svg bounds
        #   in attributes, and store as overall transformation matrix in domino svg
        attrs = svg_attrs(m2d, xmlns)
        self.svg = ET.Element('svg', attrib=attrs)
        self.svg.text = '\n'
        mtrx = 'matrix{}'.format(str(m2d))
        dgrp = ET.SubElement(self.svg, GROUP, transform=mtrx)
        style = 'stroke: rgb({fg}); fill: rgb({bg}); '.format(fg=fg, bg=bg)
        style += 'stroke-width: 2px; '
        style += 'stroke-linejoin: round; stroke-linecap: round; '
        ET.SubElement(dgrp, RECT, x='5', y='5',
                      width=str(DWIDTH), height=str(DHEIGHT),
                      style=style)
        style = 'stroke: rgb({fg}); stroke-width: 1px;'.format(fg=fg)

        ET.SubElement(dgrp, LINE, x1='11', y1='101', x2='95', y2='101',
                      style=style)
        self.tile_grp(dgrp, TOP, self.topnum, fg, bg)
        self.tile_grp(dgrp, BOTTOM, self.bottomnum, fg, bg)

    def tile_grp(self, dgrp, transform, number, fg=WHITE, bg=BLACK):
        pips = PIP_LAYOUT[number]
        if pips:
            grp = ET.SubElement(dgrp, GROUP, transform=transform)
            style = 'stroke: rgb({fg}); fill: rgb({fg})'.format(fg=fg)
            for pip in pips:
                ET.SubElement(grp, CIRCLE, r='7', cx=str(pip[0]), cy=str(pip[1]),
                              style=style)


def mkhtml_str(dominoes, title=None):
    domino_svgs = [DominoSVG(*d)
            for d in dominoes]
    logging.info('Make html from %s dominoes', len(dominoes))
    htmlstr = ET.tostring(mkhtml(domino_svgs, title=title), encoding="utf-8")
    logging.info('Made html')
    return htmlstr


def mkhtml(domino_svgs, title=None):
    html = ET.Element('html', lang='en')
    if title:
        title_elt = ET.SubElement(html, 'title')
        title_elt.text = title
    body = ET.SubElement(html, 'body')
    if title:
        h2 = ET.SubElement(body, 'h2')
        h2.text = title
    p = ET.SubElement(body, 'p')
    p.extend([d.svg for d in domino_svgs])
    return indent(html)
