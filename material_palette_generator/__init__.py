# The MIT License (MIT)
 
# Copyright (c) 2015-present Dan Abramov
 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Copyright 2016 Google Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0

# THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
# WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
# MERCHANTABLITY OR NON-INFRINGEMENT.

# See the Apache Version 2.0 License for specific language governing permissions
# and limitations under the License.


#  Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
#  This code may only be used under the BSD style license found at
#  http://polymer.github.io/LICENSE.txt
#  The complete set of authors may be found at
#  http://polymer.github.io/AUTHORS.txt
#  The complete set of contributors may be found at
#  http://polymer.github.io/CONTRIBUTORS.txt
#  Code distributed by Google as part of the polymer project is also
#  subject to an additional IP rights grant found at
#  http://polymer.github.io/PATENTS.txt


__all__ = (
    'get_palettes', 
    'get_primary_palette',
    'get_complementary_palette',
    'get_analogous_palette',
    'get_triadic_palette',
    'preview_palettes'
)

import math
from math import sqrt
from decimal import Decimal, ROUND_HALF_UP

def round2(n):
    return int(Decimal(n).to_integral_value(rounding=ROUND_HALF_UP))

# hb
def hex2(val: int):
    return f"{val:02x}"

# A
def clamp(a, b, c):
    return min(max(a, b), c)

# O
EPS = 2 ** -16

# P
class RGB:
    def __init__(self, red, green, blue, alpha=1):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

# T
class HSL:
    def __init__(self, hue, saturation, lightness, alpha=1):
        self.hue = hue
        self.saturation = saturation
        self.lightness = lightness
        self.alpha = alpha

    def rotate(self, val):
        return HSL(
            (self.hue + val + 360) % 360,
            self.saturation,
            self.lightness,
            self.alpha
        )

# wb
class LCh: 
    def __init__(self, l, c, h, alpha=1):
        self.l = l
        self.c = c
        self.h = h
        self.alpha = alpha

# V
class LAB:
    def __init__(self, l, a, b, alpha=1):
        self.l = l
        self.a = a
        self.b = b
        self.alpha = alpha

# rb
def rgb_to_hsl(rgb_color):
    r, g, b = rgb_color.red, rgb_color.green, rgb_color.blue
    max_v = max(r, g, b)
    min_v = min(r, g, b)
    delta = max_v - min_v

    h = s = 0
    l = clamp(.5 * (max_v + min_v), 0, 1)
    
    if delta > EPS:
        if max_v == r:
            h = 60 * ((g - b) / delta)
        elif max_v == g:
            h = 60 * ((b - r) / delta) + 120
        elif max_v == b:
            h = 60 * ((r - g) / delta) + 240

        if 0 < l <= 0.5:
            s = clamp(delta / (2 * l), 0, 1)
        else:
            s = clamp(delta / (2 - 2 * l), 0, 1)

    h = round2(h + 360) % 360

    return HSL(h, s, l, rgb_color.alpha)

# kb
def hsv_chroma_match_to_rgb(hue, alpha, chroma, _match):
    r = g = b = _match
    hue = (hue % 360) / 60
    x = chroma * (1 - abs(hue % 2 - 1))

    floor_hue = int(hue)
    if floor_hue == 0:
        r += chroma
        g += x
    elif floor_hue == 1:
        r += x
        g += chroma
    elif floor_hue == 2:
        g += chroma
        b += x
    elif floor_hue == 3:
        g += x
        b += chroma
    elif floor_hue == 4:
        r += x
        b += chroma
    elif floor_hue == 5:
        r += chroma
        b += x

    return RGB(r, g, b, alpha)

# lb
def hsl_to_rgb(hsl_color: HSL):
    b = (1 - abs(2 * hsl_color.lightness - 1)) * hsl_color.saturation
    return hsv_chroma_match_to_rgb(hsl_color.hue, hsl_color.alpha, b, max(0, hsl_color.lightness - b/2))

# R
def srgb_to_linear(val):
    return val / 12.92 if val <= 0.04045 else ((val + 0.055) / 1.055) ** 2.4

# yb
def linear_to_srgb(val):
    return 12.92 * val if val <= 0.0031308 else 1.055 * (val ** (1 / 2.4)) - 0.055

# W
def xyz_to_lab_component(val):
    b = 6 / 29
    c = 1 / (3 * (b ** 2))
    if val > b ** 3:
        return val ** (1/3)
    else:
        return c * val + 4 / 29

# zb
def lab_to_xyz_component(val):
    b = 6 / 29
    c = 3 * (b ** 2)
    if val > b:
        return val ** 3
    else:
        return c * (val - 4 / 29)

# nb
def color_from_hex(code):
    code = code.lstrip('#')
    r = int(code[0:2], 16) / 255
    g = int(code[2:4], 16) / 255
    b = int(code[4:6], 16) / 255
    
    return RGB(r, g, b, 1.0)

# Q
def rgb_to_hex(rgb_color):
    r = hex2(round2(255 * rgb_color.red))
    g = hex2(round2(255 * rgb_color.green))
    b = hex2(round2(255 * rgb_color.blue))
    if rgb_color.alpha < 1:
        a_hex = hex2(round2(255 * rgb_color.alpha))
    else:
        a_hex = ""
    return r + g + b + a_hex

# Ab
def cartesian_to_hue(y, x):
    if abs(y) < 1e-4 and abs(x) < 1e-4:
        return 0
    angle = math.degrees(math.atan2(y, x))
    return angle if angle >= 0 else angle + 360

# vb
def rgb_to_lab(rgb_color: RGB):
    r_ = srgb_to_linear(rgb_color.red)
    g_ = srgb_to_linear(rgb_color.green)
    b_ = srgb_to_linear(rgb_color.blue)

    y = 0.2126729 * r_ + 0.7151522 * g_ + 0.072175 * b_

    L = 116 * xyz_to_lab_component(y) - 16
    a = 500 * (xyz_to_lab_component((0.4124564 * r_ + 0.3575761 * g_ + 0.1804375 * b_) / 0.95047) - xyz_to_lab_component(y))
    b = 200 * (xyz_to_lab_component(y) - xyz_to_lab_component((0.0193339 * r_ + 0.119192 * g_ + 0.9503041 * b_) / 1.08883))

    return LAB(L, a, b, rgb_color.alpha)

# xb
def lab_to_lch(lab_color: LAB):
    chroma = sqrt(lab_color.a ** 2 + lab_color.b ** 2)
    hue = (math.degrees(math.atan2(lab_color.b, lab_color.a)) + 360) % 360
    return LCh(lab_color.l, chroma, hue, lab_color.alpha)

# Qb
def find_nearest_palette(lab_color: LAB, b=None):
    if b is None:
        b = GOLDEN_LAB_PALETTES

    if not b or not b[0]:
        raise ValueError("Invalid golden palettes")

    c = float('inf')
    d = b[0]
    e = -1

    for g in range(len(b)):
        for h in range(len(b[g])):
            if c <= 0:
                break

            k = b[g][h]
            l = (k.l + lab_color.l) / 2
            m = sqrt(k.a ** 2 + k.b ** 2)
            q = sqrt(lab_color.a ** 2 + lab_color.b ** 2)
            t = (m + q) / 2
            t = 0.5 * (1 - sqrt((t ** 7) / ((t ** 7) + (25 ** 7))))
            n = k.a * (1 + t)
            r = lab_color.a * (1 + t)
            N = sqrt((n ** 2) + (k.b ** 2))
            H = sqrt(r ** 2 + lab_color.b ** 2)
            t = H - N
            ja = (N + H) / 2
            n = cartesian_to_hue(k.b, n)
            r = cartesian_to_hue(lab_color.b, r)

            if abs(m) < 1e-4 or abs(q) < 1e-4:
                delta_hue = 0
            elif abs(r - n) <= 180:
                delta_hue = r - n
            elif r <= n:
                delta_hue = r - n + 360
            else:
                delta_hue = r - n - 360
            
            N = 2 * sqrt(N * H) * math.sin(math.radians(delta_hue / 2))

            if abs(m) < 1e-4 or abs(q) < 1e-4:
                m = 0
            elif abs(r - n) <= 180:
                m = (n + r) / 2
            elif (n + r) < 360:
                m = (n + r + 360) / 2
            else:
                m = (n + r - 360) / 2

            q = 1 + 0.045 * ja
            H = 1 + 0.015 * ja * (
                1 - 0.17 * math.cos(math.radians(m - 30))
                + 0.24 * math.cos(math.radians(2 * m))
                + 0.32 * math.cos(math.radians(3 * m + 6))
                - 0.2 * math.cos(math.radians(4 * m - 63))
            )
            delta_L = (lab_color.l - k.l) / (
                1 + 0.015 * ((l - 50) ** 2) / math.sqrt(20 + (l - 50) ** 2)
            )
            term1 = delta_L ** 2
            term2 = (t / q) ** 2
            term3 = (N / H) ** 2
            cross = (
                (t / q)
                * math.sqrt((ja ** 7) / ((ja ** 7) + (25 ** 7)))
                * math.sin(math.radians(60 * math.exp(-((m - 275) / 25) ** 2)))
                * -2 * (N / H)
            )
            k = math.sqrt(term1 + term2 + term3 + cross)

            if k < c:
                c = k
                d = b[g]
                e = h

    return {
        'fc': d,
        'ec': e
    }

# X
def _generate_palette(rgb_color, b=None):
    if b is None:
        b = GOLDEN_LAB_PALETTES

    c = rgb_to_lab(rgb_color)
    d = find_nearest_palette(c, b)
    b = d['fc']
    d = d['ec']
    e = b[d]
    g = lab_to_lch(e)
    h = lab_to_lch(c)
    k = lab_to_lch(b[5]).c < 30
    l = g.l - h.l
    m = g.c - h.c
    q = g.h - h.h
    t = LIGHTNESS_WEIGHTS[d]
    n = CHROMA_WEIGHTS[d]
    r = 100

    def convert_color(b_item, idx):
        nonlocal r
        if b_item is e:
            r = max(h.l - 1.7, 0)
            return rgb_color

        b_lch = lab_to_lch(b_item)

        d_val = b_lch.l - LIGHTNESS_WEIGHTS[idx] / t * l
        d_val = min(d_val, r)

        c_lch = LCh(
            clamp(d_val, 0, 100),
            max(0, b_lch.c - m if k else b_lch.c - m * min(CHROMA_WEIGHTS[idx] / n, 1.25)),
            (b_lch.h - q + 360) % 360,
            b_lch.alpha
        )

        r = max(c_lch.l - 1.7, 0)

        angle = math.radians(c_lch.h)
        c_lab = LAB(c_lch.l, c_lch.c * math.cos(angle), c_lch.c * math.sin(angle), c_lch.alpha)

        g_val = (c_lab.l + 16) / 116
        X_val = 0.95047 * lab_to_xyz_component(g_val + c_lab.a / 500)
        Y_val = lab_to_xyz_component(g_val)
        Z_val = 1.08883 * lab_to_xyz_component(g_val - c_lab.b / 200)

        return RGB(
            clamp(linear_to_srgb(3.2404542 * X_val - 1.5371385 * Y_val - 0.4985314 * Z_val), 0, 1),
            clamp(linear_to_srgb(-0.969266 * X_val + 1.8760108 * Y_val + 0.041556 * Z_val), 0, 1),
            clamp(linear_to_srgb(0.0556434 * X_val - 0.2040259 * Y_val + 1.0572252 * Z_val), 0, 1),
            c_lab.alpha
        )

    return [convert_color(item, i) for i, item in enumerate(b)]

def rotate_rgb(color: RGB, angle: int | float):
    return hsl_to_rgb(rgb_to_hsl(color).rotate(angle))

# Bb
GOLDEN_LAB_PALETTES = [
        [
            LAB(94.67497003305085, 7.266715066863771, 1.000743882272359),
            LAB(86.7897416761699, 18.370736761658012, 4.23637133971424),
            LAB(72.0939162832561, 31.7948058298117, 13.2972443996896),
            LAB(61.79353370051851, 44.129498163764545, 20.721477326799608),
            LAB(57.194195398949574, 59.6450006197361, 34.999830012940194),
            LAB(55.603951071861374, 66.01287384845483, 47.67169313982772),
            LAB(51.66348502954747, 64.7487785020625, 43.244876694855286),
            LAB(47.09455666350969, 62.29836039074277, 40.67775424698388),
            LAB(43.77122063388739, 60.28633509183384, 40.31444686692952),
            LAB(39.555187078007386, 58.703681355389975, 41.66495027798629)
        ],
        [
            LAB(92.68053776327665, 9.515385232804263, -.8994072969754852),
            LAB(81.86756643628922, 25.05688089723257, -1.9475235115390621),
            LAB(70.90987389545768, 42.21705257720526, -1.095154624057959),
            LAB(61.08140805216186, 58.871233307587204, 2.1008764804626434),
            LAB(54.97970219986448, 68.56530938366889, 7.327430728560569),
            LAB(50.872250340749176, 74.60459195925529, 15.353576256896073),
            LAB(47.27738650144558, 70.77855776427805, 11.70434273264508),
            LAB(42.58424189486517, 65.5411953138309, 7.595596439803797),
            LAB(37.977492407254836, 60.74362621842075, 2.9847124951453474),
            LAB(29.699290034849604, 51.90485023721311, -4.830186634107636)
        ],
        [
            LAB(92.4362655169016, 7.542927467702299, -6.039842848605881),
            LAB(81.07399776904751, 19.563870217805036, -15.719625491986044),
            LAB(68.71394717711831, 33.79992812490556, -26.49539972339321),
            LAB(56.596161226236305, 47.5856631835152, -36.480816605410915),
            LAB(48.002791217624434, 57.30866443934879, -43.2561127152548),
            LAB(40.66211534692161, 64.01910773818436, -48.05930162591041),
            LAB(37.690702208992185, 61.13762767732481, -49.384803274243026),
            LAB(33.56291870731981, 57.637381239254104, -51.39557249855828),
            LAB(29.865391314234515, 54.29737439901333, -52.6601973712463),
            LAB(23.16724235420436, 48.51764437280498, -55.16267949015293)
        ],
        [
            LAB(92.49103426017201, 4.712320025752947, -6.532868071709763),
            LAB(81.24668319505597, 11.50642734909485, -16.666600637245367),
            LAB(68.61488216554629, 20.395329051982824, -28.522018851715416),
            LAB(55.60369793053023, 30.933537768905005, -41.16439122358484),
            LAB(45.834566190969426, 39.28806272235674, -50.523322052772635),
            LAB(36.608620229358664, 47.29686002828143, -59.111766586186846),
            LAB(34.189791237562616, 46.60426065139123, -59.53961627676729),
            LAB(30.52713367338361, 46.01498224754519, -60.19975052509064),
            LAB(27.44585524877222, 44.96180431854785, -60.46395810756433),
            LAB(21.98627670328218, 44.29296076245473, -60.93653655172098)
        ],
        [
            LAB(92.86314411983918, 1.5318147061061937, -6.025243528950552),
            LAB(81.8348073705298, 4.460934955458907, -15.873561009736136),
            LAB(69.7796913795672, 7.9043652558912765, -26.3170846346932),
            LAB(57.48786519938736, 12.681019504822533, -37.23202012914528),
            LAB(47.74592578811101, 18.520799302452374, -46.47540679000397),
            LAB(38.334403614455404, 25.57700668170812, -55.28224153299287),
            LAB(35.15116453901552, 26.231812080381168, -54.53700978785404),
            LAB(31.080429988007957, 27.07394930110124, -53.97505274579958),
            LAB(27.026672080454922, 28.165266427558983, -53.28987325482218),
            LAB(19.751201587921678, 30.60784576895101, -52.13866519297474)
        ],
        [
            LAB(94.70682457348717, -2.835484735987326, -6.978044694792707),
            LAB(86.8839842970016, -5.16908728759552, -17.88561192754956),
            LAB(79.0451532401558, -6.817753527015746, -28.968537490432176),
            LAB(71.15083697242613, -5.994763756850707, -39.72549451158927),
            LAB(65.48106058907833, -2.735745792537936, -48.15471238926561),
            LAB(60.43009440850862, 2.079928897321559, -55.10935847069616),
            LAB(55.62267676922188, 4.998684384486918, -55.02164729429915),
            LAB(49.27006645904875, 8.470398370314381, -54.494796838457546),
            LAB(43.16828856394358, 11.968483076143844, -53.972567377977974),
            LAB(32.17757793894193, 18.96054990229354, -53.45146365049088)
        ],
        [
            LAB(95.35713467762652, -4.797149155388203, -6.550002550504308),
            LAB(88.27942649540043, -10.836006614583892, -16.359361821940375),
            LAB(81.10009044900976, -15.323054522981716, -26.419121191320947),
            LAB(74.44713958259777, -16.664432625362547, -35.19702686900037),
            LAB(69.87836465637318, -14.291515332054693, -41.827430329755174),
            LAB(65.68851259178913, -9.612635721963692, -47.34091616039191),
            LAB(60.88357994308973, -7.252819027184943, -46.67753731595634),
            LAB(54.26166495426166, -3.8141836897908066, -45.97939475762498),
            LAB(48.10661895072673, -1.378998784464347, -44.34466750206778),
            LAB(36.34401147057282, 5.067812404713545, -43.11786257561915)
        ],
        [
            LAB(95.69295154599753, -6.898716127301141, -3.994284229654421),
            LAB(89.52842524059004, -16.412398289601725, -9.260466069266693),
            LAB(83.32031214655748, -24.83036840728098, -14.568673583304603),
            LAB(77.35338313752958, -30.201708572215104, -18.92358284721101),
            LAB(73.45322093857781, -31.88590390189383, -21.130459992513686),
            LAB(69.97638465064783, -30.679850324547953, -23.186685661136707),
            LAB(64.44491716553777, -29.08337434584457, -21.154935769156214),
            LAB(56.99816432961103, -27.31081477279451, -17.86988815767443),
            LAB(49.75464182255671, -25.335383503694242, -15.024722591662787),
            LAB(36.52725894264432, -22.129641744194515, -9.176159146894303)
        ],
        [
            LAB(94.18453941589918, -6.08351703428972, -1.5488916051161983),
            LAB(85.68177077414457, -15.333179440298606, -2.8519825761476048),
            LAB(76.85067847190405, -24.844059173189713, -3.8750785132192656),
            LAB(68.02762242570138, -32.566861154120716, -4.015231084407134),
            LAB(61.667257304525464, -36.06752603289354, -3.4734046401753815),
            LAB(55.67310397390196, -36.66069960626328, -2.125617915169653),
            LAB(51.059149495197715, -34.65019160301408, -1.3910484300432513),
            LAB(45.269081019218405, -32.13244775422941, -.4526371852697775),
            LAB(39.36899076059384, -29.25264468583161, -.03562564673170732),
            LAB(28.58363043701477, -24.585465516136413, 1.8037402162492389)
        ],
        [
            LAB(95.30530183565223, -6.430415645739263, 4.292950594459599),
            LAB(88.49014579152143, -15.23147744952702, 10.848261177683138),
            LAB(81.22616870575376, -24.993886168551583, 18.144696803330884),
            LAB(74.30361721558802, -35.56088696067356, 26.781515251907727),
            LAB(69.0430995277442, -42.61556126595995, 33.17109563126665),
            LAB(63.977421814072926, -48.54292673319982, 39.73241526342939),
            LAB(58.777960853461366, -46.1153692478013, 37.838910745225576),
            LAB(52.41108688974904, -43.21761792485762, 35.62250659009424),
            LAB(46.2813873076426, -40.25816227675361, 33.32343229338761),
            LAB(34.685655305814514, -34.75343878510312, 28.866739034359767)
        ],
        [
            LAB(96.70518169355954, -4.929987845095463, 6.397084523168894),
            LAB(91.66416061199438, -12.057032041945693, 16.054604579275143),
            LAB(86.2244395865449, -19.613646834080622, 26.384906423454236),
            LAB(80.83404879636919, -27.080171840756893, 37.378493742021334),
            LAB(76.79543725108964, -32.76659719736752, 45.912190572444445),
            LAB(72.90025297028019, -37.549139223927384, 53.51959496103027),
            LAB(67.21532310272079, -36.56304870773486, 50.49629051268894),
            LAB(59.91051142210195, -35.77011466063357, 46.56465847976187),
            LAB(52.51015841084511, -34.47903440699235, 42.20723868724268),
            LAB(39.41191983353878, -32.80460974352642, 35.255490585630014)
        ],
        [
            LAB(97.99506057883428, -4.059632482741494, 9.355797602381521),
            LAB(94.80926235976536, -9.237091467352855, 23.230650064824985),
            LAB(91.85205843526167, -15.053917327011114, 38.86115182206598),
            LAB(88.75812142080242, -19.542900400164097, 53.71785675783709),
            LAB(86.27404180729515, -22.173992891121596, 63.978639065232514),
            LAB(84.20566835376492, -24.270643520989342, 72.79624067033038),
            LAB(78.27915100603997, -21.181850056402496, 68.82763412297965),
            LAB(70.82385811892824, -17.788148932525672, 64.00327817988128),
            LAB(62.936867012868035, -13.697412111684903, 58.513000509287835),
            LAB(49.498610881452535, -6.485230564384715, 49.67432722833751)
        ],
        [
            LAB(98.93885129752759, -3.0098470288543178, 10.765736833790008),
            LAB(97.22689784824074, -6.174599368734491, 26.22932417355146),
            LAB(95.58092947828766, -8.907132848473886, 43.56297291446567),
            LAB(94.09009515702486, -10.509628942710735, 60.20019514231188),
            LAB(93.06546746683087, -11.008558476013008, 71.76500826005477),
            LAB(92.12975017760128, -10.830023094868302, 80.9090559640089),
            LAB(87.12188349168609, -2.3764300099239355, 78.14868195373407),
            LAB(80.96200442419905, 8.849333792729064, 75.05050700092679),
            LAB(75.00342770718086, 20.340173566879283, 72.24841925958934),
            LAB(65.48207757431567, 39.647064970476094, 68.34872841768654)
        ],
        [
            LAB(97.5642392074337, -1.445525639405032, 11.881254316297674),
            LAB(93.67057953749456, -1.8693096862072434, 30.02888670415651),
            LAB(89.94571492804107, -1.0224503814769692, 49.649542361642276),
            LAB(86.71009164153801, 1.0496066396428194, 68.77377342409739),
            LAB(83.78773993319211, 5.248231820098425, 78.92920457852716),
            LAB(81.52191382080228, 9.403655370707199, 82.69257112982746),
            LAB(78.17240973804697, 16.628512886531887, 81.09358318806208),
            LAB(73.80899654381052, 26.53614315250874, 78.21754052181723),
            LAB(70.1134511665764, 35.3007623359744, 75.87510992138593),
            LAB(63.86460405565717, 50.94648214505959, 72.17815682124423)
        ],
        [
            LAB(96.30459517801387, .923151172282477, 10.598439446083074),
            LAB(90.68320082865087, 4.103774964681062, 26.485793721916128),
            LAB(85.00055287186233, 9.047181758866651, 44.51407622580792),
            LAB(79.42428495742953, 16.452610724439875, 62.08721739074201),
            LAB(75.47792699289774, 23.395742928451867, 72.64347611236501),
            LAB(72.04246561548388, 30.681921012382098, 77.08579298904603),
            LAB(68.94724338946975, 35.22014778433863, 74.88425044595111),
            LAB(64.83017495535229, 40.91200730099703, 71.9596053545428),
            LAB(60.8534207471871, 46.41483590510681, 69.18061963415211),
            LAB(54.77571742962287, 55.282751019360035, 65.10193403547922)
        ],
        [
            LAB(93.69219844671957, 5.763979334358293, 3.1700162796469034),
            LAB(86.04629434276428, 15.750843803958192, 14.828476927090994),
            LAB(77.54010042938336, 27.90113842540043, 25.99645229289065),
            LAB(69.74095456707857, 41.14487377552256, 39.443320178900024),
            LAB(64.37085344539341,51.890379620443575, 50.81312471046415),
            LAB(60.06780837277435, 61.65258736118817, 61.54771829165221),
            LAB(57.28707915232363, 60.3250664308812, 60.07341536376447),
            LAB(53.810052616293845, 58.36760943780162, 58.19586806694884),
            LAB(50.301352405105874, 56.40104898089937, 55.924141992404344),
            LAB(43.86477994548343, 52.970887703910726, 52.30067989225532)
        ],
        [
            LAB(93.29864888069987, .9915456090475727, 1.442353076378411),
            LAB(82.80884359004081, 3.116221903342209, 3.3523059451463055),
            LAB(70.95493047668185, 5.469742193344784, 5.449009494553492),
            LAB(58.712934619103066, 7.990991075363385, 8.352488495367627),
            LAB(49.150208552875895, 10.570984981000397, 10.831440151197924),
            LAB(39.63200151837749, 13.138881961627241, 13.531574711511885),
            LAB(35.600996682015754, 12.40352847757295, 12.10432183902449),
            LAB(30.084271265759952, 11.317148149878081, 10.547484304296217),
            LAB(24.555014696416578, 10.816613316782464, 8.506555306791984),
            LAB(18.35055226514404, 10.225725550338765, 7.058582769882571)
        ],
        [
            LAB(98.27202740980219, -1.6418393644634932E-5, 6.567357457853973E-6),
            LAB(96.53749336548567, -1.616917905122861E-5, 6.467671598286984E-6),
            LAB(94.0978378987781, -1.581865383126768E-5, 6.327461532507073E-6),
            LAB(89.17728373493613, -1.511167768697419E-5, 6.044671074789676E-6),
            LAB(76.61119902231323, -1.330620591488696E-5, 5.322482343750323E-6),
            LAB(65.11424774127516, -1.1654345155598378E-5, 4.661738062239351E-6),
            LAB(49.238989620828065, -9.373417431124409E-6, 3.7493669724497636E-6),
            LAB(41.14266843804848, -8.210152946386273E-6, 3.2840611896567395E-6),
            LAB(27.974857206003705, -6.318226192236764E-6, 2.5272904768947058E-6),
            LAB(12.740011331302725, -4.129311698131133E-6, 1.6517246792524531E-6)
        ],
        [
            LAB(94.27665212516236, -.637571046109342, -1.313515378996688),
            LAB(85.77788001492097, -2.2777811084512822, -3.0177758416151557),
            LAB(76.12296325015231, -3.401502988883809, -5.16867892977908),
            LAB(66.16340108908365, -4.819627183079045, -7.520697631614404),
            LAB(58.35752478513645, -5.7195089100892105, -9.165988916613488),
            LAB(50.70748082202715, -6.837992965799455, -10.956055112409357),
            LAB(44.85917867647632, -6.411990559239578, -9.74511982878765),
            LAB(36.92458930566504, -5.319878610845596, -8.341943474561553),
            LAB(29.115334784637618, -4.168907828645069, -6.8629962199973304),
            LAB(19.958338450799914, -3.3116721453186617, -5.4486142104736786)
        ]
    ]

# Cb
LIGHTNESS_WEIGHTS = [2.048875457, 5.124792061, 8.751659557, 12.07628774, 13.91449542,
      15.92738893, 15.46585818, 15.09779227, 15.13738673, 15.09818372]

# Db
CHROMA_WEIGHTS = [1.762442714, 4.213532634, 7.395827458, 11.07174158, 13.89634504,
      16.37591477, 16.27071136, 16.54160806, 17.35916727, 19.88410864]


# Public functions
SHADES = '50', '100', '200', '300', '400', '500', '600', '700', '800', '900'

def get_palette(hex_color, angles: list | None = None, base_colors: list = None):
    rgb = color_from_hex(hex_color)

    output = []
    if not angles:
        palette = _generate_palette(rgb)
        return dict(zip(SHADES, (map(lambda x: f'#{rgb_to_hex(x)}', palette))))
    for angle in angles:
        rotated_rgb = rotate_rgb(rgb, angle)
        if base_colors is not None:
            base_colors.append(f'#{rgb_to_hex(rotated_rgb)}')
        palette = _generate_palette(rotated_rgb)
        output.append(dict(zip(SHADES, (map(lambda x: f'#{rgb_to_hex(x)}', palette)))))

    return output

def get_primary_palette(
        hex_color: str, 
        base_colors: dict | None = None
    ) -> dict[str, str]:
    """
    Generate primary color palette based on hex color.

    Returns a dictionary of 10 shades code and hex color.

    If you want to get the primary base color, provide
    :param:`base_colors` dictionary. After function runs
    completely, `base_colors` will have type base colors
    included. By default, this dictionary is `None`.
    """
    
    if base_colors is not None:
        base_colors['primary'] = hex_color.lower()
    return get_palette(hex_color)

def get_complementary_palette(
        hex_color: str, 
        base_colors: dict | None = None
    ) -> dict[str, str]:
    """
    Generate complementary color palette of base hex color.

    Returns a dictionary of 10 shades code and hex color.

    If you want to get the complementary base color, provide
    :param:`base_colors` dictionary. After function runs
    completely, `base_colors` will have complementary base color
    included. By default, this dictionary is `None`.
    """

    if base_colors is not None:
        base_colors_list = []
        output = get_palette(hex_color, angles=(180,), base_colors=base_colors_list)
        base_colors['complementary'] = base_colors_list[0]
        return output[0]

    return get_palette(hex_color, angles=(180,))[0]

def get_analogous_palette(
        hex_color: str,
        base_colors: dict | None = None
    ) -> dict[str, dict[str, str]]:
    """
    Generate two analogous color palettes of base hex color.

    Returns a dictionary of two dictionaries (Analogous-1 and
    Analogous-2) each containing 10 shades code and hex color.

    If you want to get the analogous base colors, provide
    :param:`base_colors` dictionary. After function runs
    completely, `base_colors` will have analogous base colors
    included. By default, this dictionary is `None`.
    """

    names = ['Analogous-1', 'Analogous-2']

    if base_colors is not None:
        base_colors_list = []
        output = get_palette(hex_color, angles=(-30, 30), base_colors=base_colors_list)
        base_colors['analogous-1'] = base_colors_list[0]
        base_colors['analogous-2'] = base_colors_list[1]

        return dict(zip(names, output))
    
    output = get_palette(hex_color, angles=(-30, 30))
    return dict(zip(names, output))
    
def get_triadic_palette(
        hex_color: str,
        base_colors: dict | None = None
    ) -> dict[str, dict[str, str]]:
    """
    Generate two triadic color palettes of base hex color.

    Returns a dictionary of two dictionaries (Triadic-1 and
    Triadic-2) each containing 10 shades code and hex color.

    If you want to get the triadic base colors, provide
    :param:`base_colors` dictionary. After function runs
    completely, `base_colors` will have triadic base colors
    included. By default, this dictionary is `None`.
    """

    names = ['Triadic-1', 'Triadic-2']

    if base_colors is not None:
        base_colors_list = []
        output = get_palette(hex_color, angles=(60, 120), base_colors=base_colors_list)
        base_colors['triadic-1'] = base_colors_list[0]
        base_colors['triadic-2'] = base_colors_list[1]

        return dict(zip(names, output))
    
    output = get_palette(hex_color, angles=(60, 120))
    return dict(zip(names, output))

def get_palettes(
        hex_color: str, 
        types: tuple[str] | None = None,
        base_colors: dict = None
    ) -> dict[str, dict[str, str]]:
    """
    Generate one or more types of color palettes of base hex color.

    Returns a dictionary of color types each containing 10 
    shades code and hex color. If :param:`types` is `None`
    then all types are provided. Valid color types are:
    `'primary'`, `'complementary'`, `'analogous'`, `'triadic'`.

    If you want to get the type base colors, provide
    :param:`base_colors` dictionary. After function runs
    completely, `base_colors` will have type base colors
    included. By default, this dictionary is `None`.
    """

    output = {}
    if types is None:
        types = 'primary', 'complementary', 'analogous', 'triadic'
    
    if 'primary' in types:
        output['Primary'] = get_primary_palette(hex_color, base_colors)

    if 'complementary' in types:
        output['Complementary'] = get_complementary_palette(hex_color, base_colors)

    if 'analogous' in types:
        output.update(get_analogous_palette(hex_color, base_colors))

    if 'triadic' in types:
        output.update(get_triadic_palette(hex_color, base_colors))

    return output

# Bonus
def preview_palettes(palette: dict) -> None:
    """
    Displays horizontal preview image of the given 
    color palette using the `Pillow` library.

    `palette` format should be same as returned 
    dict from `get_{type}_palette` function.
    """

    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return "`PIL` module is not installed. `pip install pillow` to install the module."
    
    palette = reversed((palette.values()))
    size = 50
    img = Image.new("RGB", (size*10, size))
    draw = ImageDraw.Draw(img)
    
    for i, color in enumerate(palette):
        draw.rectangle([i*size, 0, (i+1)*size, size], fill=color)
    
    img.show()


# Test
if __name__ == '__main__':
    output = get_primary_palette("#E91E63")
    preview_palettes(output)