#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: frendor
"""

import numpy as np

base_func = lambda stufe, speed=1: speed * 24. * ( 1/3. + 1/750.*stufe + 1/5.*stufe**2 + 1/1250.*stufe**3 )

linear_split_func = lambda stufe, speed=1:  speed * 4/5.* (1/125. * stufe + 2. )* {0:0,1:2.,2:3. ,3:3.,4:2.}[stufe%5]
### {0:0,1:2.,2:3. ,3:3.,4:2.}[stufe%5] ist identisch mit z.B. [0,2,3][min(5-stufe%5,stufe%5)]

### Die Werte für die 25-Oszillationen
osc_initial_values = np.array([   0.,   8.,  32., -41.,  51.,   
                                -55.,  52.,  -7.,  30.,  50.,   
                                -60.,   6., -26., -19.,  39.,   
                                 35.,  45.,  25., -13., -57.,   
                                 30., -31.,  71., -27.,  62.]) 

osc_initial_slope = {1:-11.,
                     2:  1.,
                     3:  6.,
                     4:  4.,
                     0: -5}

osc_slope_diff = {1:  2,
                  2: -1,
                  3:  1,
                  4: -2,
                  0:  0}

osc_slope_func = lambda stufe: osc_initial_slope[stufe%5] + (stufe%25-stufe%5) * osc_slope_diff[stufe%5] 

osc_func = lambda stufe, speed=1: -1 * osc_jump( speed/25. * ( 1/5. * osc_initial_values[stufe%25] + (stufe/25 - stufe/25 % 1)*osc_slope_func(stufe) ) )   

def osc_jump(zahl):
    zahl = zahl - (zahl - zahl%1) # grobe Näherung
    zahl = zahl-1 if abs(zahl-1) <= abs(zahl) else zahl+1 if abs(zahl+1) < abs(zahl) else zahl
    return zahl


iron_function = lambda stufe, speed=1: base_func(stufe,speed) + linear_split_func(stufe,speed) + osc_func(stufe,speed)
iron_diff_function = lambda stufe, value, speed=1: value - base_func(stufe,speed) - linear_split_func(stufe,speed) - osc_func(stufe,speed)


'''
### Nachtrag: Startwerte für das 6x Speed-Universum
### Die empirisch ermittelten Oszillationswerte für das Speed 6-Universum

osc_initial_values = np.array([  0.,  48., -58.,   4.,  56.,  
                                45.,  62., -42.,  55.,  50.,  
                                15.,  36., -31.,  11., -16., 
                               -40.,  20.,  25.,  47.,  33.,  
                                55., -61.,  51., -37.,  -3.]) 

osc_initial_slope = {1:  9,
                     2:  6,
                     3: 11,
                     4: -1,
                     0: -5}

### Die Werte nicht benötigt, da die normalen Startwerte einfach * 6 genommen 
### werden und wegen der Sprungfunktion effektiv mit diesen Werten hier 
### übereinstimmen.
'''
    
    
