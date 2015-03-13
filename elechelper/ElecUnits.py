# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
from ElecHelpers import normalize, parallel

"""
Physical Units helpers for electronics
"""
__author__ = "naruhodo-ryuichi"

M = 10 ** 6
K = 10 ** 3
m = 10 ** -3
u = 10 ** -6
n = 10 ** -9
p = 10 ** -12
unitsC = (100*u, 10*u, u, 100*n, 10*n, n, 100*p, 10*p, p)
unitsR = (100, 1*K, 10*K, 100*K)
valuesR = (10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91, 100)
valuesC = (10, 15, 22, 33, 47, 68, 100)


class V(float):
    """
    A volts voltage value
    """
    def __new__(cls, value=0, v_type=None):
        if "pp" in v_type.lower():
            value /= 2*math.sqrt(2)
            v_type = "rms"
        elif "p" in v_type.lower():
            value /= math.sqrt(2)
            v_type = "rms"
        i = float.__new__(cls, value)
        i.v_type = v_type
        return i

    def norm(self):
        (self.norm, self.prefix, self.unit) = normalize(self) + ("V",)

    def __str__(self):
        chain = "%.02f%s%s" % (self.norm, self.prefix, self.unit)
        if self.v_type:
            chain += self.v_type
        return chain


class W(float):
    """
    A Watts power value
    """
    def __new__(cls, value, v_type=None):
        if "pp" in v_type.lower():
            value /= 2*math.sqrt(2)
            v_type = "rms"
        elif "p" in v_type.lower():
            value /= math.sqrt(2)
            v_type = "rms"
        i = float.__new__(cls, value)
        i.v_type = v_type
        return i

    def norm(self):
        (self.norm, self.prefix, self.unit) = normalize(self) + ("W",)

    def __str__(self):
        self.norm()
        cadena = "%.02f%s%s" % (self.norm, self.prefix, self.unit)
        if self.v_type:
            cadena += self.v_type
        return cadena


class O(float):
    """
    An ohms resistor value
    """
    def __new__(cls, value, v_type=None):
        i = float.__new__(cls, value)
        i.v_type = v_type
        i.value = value
        return i

    def normal(self, value):
        (self.norm, self.prefix, self.unit) = normalize(value) + ("ohm",)

    def round(self):
        rounded = self * 10 / 10 ** math.floor(math.log10(self))
        value = min(valuesR, key=lambda x: abs(x - rounded))
        return O(value * 10 ** math.floor(math.log10(self) - 1))

    def __repr__(self):
        self.normal(self.value)
        cadena = "%.02f%s%s" % (self.norm, self.prefix, self.unit)
        if self.v_type:
            cadena += self.v_type
        return cadena

    def paralelo(self):
        valuees = []
        for un1 in unitsR:
            for v1 in reversed(valuesR[:-1]):
                r1 = O(v1*un1)
                for un2 in unitsR:
                    for v2 in reversed(valuesR[:-1]):
                        r2 = O(v2*un2)
                        value = parallel(r1,r2)
                        valuees.append([value, r1, r2])
        return sorted(valuees, key=lambda x: abs(x[0].value - self.value))


class Hz(float):
    """
    Hetzs frequency value
    """
    def __new__(cls, value, v_type=None):
        i = float.__new__(cls, value)
        i.v_type = v_type
        i.value = value
        return i

    def norm(self):
        (self.norm, self.prefix, self.unit) = normalize(self.value) + ("Hz",)

    def __str__(self):
        self.norm()
        chain = "%.02f%s%s" % (self.norm, self.prefix, self.unit)
        if self.v_type:
            chain += self.v_type
        return chain


class F(float):
    """
    Farads capacitor value
    """
    def __new__(cls, value, v_type=None):
        i = float.__new__(cls, value)
        i.v_type = v_type
        i.value = value
        return i

    def normal(self):
        (self.norm, self.prefix, self.unit) = normalize(self.value) + ("F",)

    def round(self):
        rounded = self * 10 / 10 ** math.floor(math.log10(self))
        value = min(valuesC, key=lambda x: abs(x - rounded))
        return value * 10 ** math.floor(math.log10(self) - 1)

    def __str__(self):
        self.normal()
        chain = "%.02f%s%s" % (self.norm, self.prefix, self.unit)
        if self.v_type:
            chain += self.v_type
        return chain


class A(float):
    """
    Amplification (natural or db) value
    """
    def __new__(cls, value, v_type=None):
        if v_type and "db" in v_type.lower():
            i = float.__new__(cls, 10 ** (float(value) / 20))
        else:
            i = float.__new__(cls, value)
        i.v_type = v_type
        return i

    def db(self):
        dbs = 20 * math.log10(self)
        return "%.02fdBs" % dbs

    def __str__(self):
        return "%.02f" % self