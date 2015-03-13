# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ElecUnits import *

"""
A slight attempt to model typical negative feedback audio amp calculations
"""


class Amp():
    def __init__(self, name):
        #amp name
        self.name = name
        #amp gain
        self.av = None
        #input impedance
        self.rin = None

# vin+ to gnd:10k
#vout to v-:32.5k, 31.0k

a1 = Amp("KA2206")
a1.av = A(45, "dbs")
a1.rin = O(30 * K)
a1.r1 = O(32*K)
a1.r2 = O(a1.r1 / a1.av)

print "Calculated resistor values: r1: %s, r2: %s" % (a1.r1, a1.r2)

