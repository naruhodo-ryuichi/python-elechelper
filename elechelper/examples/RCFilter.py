# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ElecHelpers import filterDesign
from ElecUnits import *


"""
Resistor and capacitor values calculator based on wanted frequency
"""

# Datos
Pwanted = W(2.3, "p")
headroom = A(0, "db")
Vin = V(2, v_type="p")
ZL = O(8)
Fmax = Hz(1.5 * K)
Fmin = Hz(100)

# Amp
Rfint = O(30 * K)
Rsint = O(180)

# Calculations
VoutMax = V(math.sqrt(Pwanted * ZL), "p")
VccMin = V(VoutMax + 2 * 3, "dc")
AvWanted = A(VoutMax / Vin)
cf = F(10 * n)
rf, ftest = filterDesign(Fmax, c=cf, v_pass="a")
rs = O(rf / AvWanted).round()
cin, ftest = filterDesign(Fmin / math.sqrt(2), r=rs, v_pass="b")
print "Calculated frequency: ", ftest
cout, ftest = filterDesign(Fmin / math.sqrt(2), r=ZL, v_pass="b")
print "Calculated frequency: ", ftest
print "Wanted Gain ",AvWanted.db()
print "Calculated values: ", rf, cf, rs, cin, cout