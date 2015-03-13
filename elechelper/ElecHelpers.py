# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
from ElecUnits import O, unitsC, valuesC, F, K, Hz, unitsR, valuesR

"""
Helper functions for electronics design
"""

__author__ = "naruhodo-ryuichi"


def parallel(r1, r2):
    """
    Returns the parallel of two components
    :param r1: first component value
    :param r2: second component value
    :return: Ohms object with parallel value
    """
    return O(r1*r2/(r1+r2))


def normalize(number):
    """
    Returns the corresponding formatted IS units for a given value
    :param number: number to format
    :return: formatted number
    """
    prefixes = {
        2: 'M',
        1: 'K',
        0: '',
        -1: 'm',
        -2: 'u',
        -3: 'n',
        -4: 'p'
    }
    exponent = math.log10(number) // 3
    prefix = prefixes[exponent]
    value = number / 10 ** (exponent * 3)
    return value, prefix


def filterDesign(frequency, r=None, c=None, v_pass=None):
    """
    Calculates r and c for a wanted frequency
    :param frequency: wanted frequency
    :param r: optional resistor value
    :param c: optional capacitor value
    :param v_pass: value of pass filterDesign (L: low, H: high)
    :return:
    """
    if not r and not c:
        for un in unitsC:
            for v in reversed(valuesC[:-1]):
                c = F(v*un)
                r = O(1/(2*math.pi*c*frequency)).round()
                if 1*K<r<100*K:
                    f1 = Hz(1/(2*math.pi*c*r))
                    return r,c, f1
    elif r:
        frecs = []
        for un in unitsC:
            for v in reversed(valuesC[:-1]):
                c = F(v*un)
                f = Hz(1/(2*math.pi*c*r))
                if (v_pass == "L" and f<frequency) or (v_pass == "H" and f>frequency) or not v_pass:
                    frecs.append((c,f))
        return min(frecs, key=lambda x: abs(x[1] - frequency))
    elif c:
        frecs = []
        for un in unitsR:
            for v in reversed(valuesR[:-1]):
                r = O(v*un)
                f = Hz(1/(2*math.pi*c*r))
                if (v_pass == "L" and f<frequency) or (v_pass == "H" and f>frequency) or not v_pass:
                    frecs.append((r,f))
        return min(frecs, key=lambda x: abs(x[1] - frequency))