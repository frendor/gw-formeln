#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: frendor
"""

import numpy as np

osc_initial_values= np.array([   0.,  -10.,  -40., -105.,   30.,  
                               100.,   60.,  -85., -100.,    0.,
                               -50.,  -70.,  -30.,   55.,  -80.,
                                50.,  100.,  125.,  110.,   40., 
                              -100.,   70., -120.,   65.,  110.])
        
osc_initial_slope = {1:-30.,
                     2: -45,
                     3: -45,
                     4: -30.,
                     0: 0}

osc_slope_func = lambda stufe: osc_initial_slope[stufe%5]# + (stufe%25-stufe%5) * osc_slope_diff[stufe%5] 

osc_func = lambda stufe, speed=1:  osc_jump( speed/50. * ( 1/5. * osc_initial_values[stufe%25]\
                                                          + (stufe/25 - stufe/25 % 1)*osc_slope_func(stufe) ) )   

def osc_jump(zahl):
    zahl = zahl - (zahl - zahl%1) # grobe Näherung
    zahl = zahl-1 if abs(zahl-1) < abs(zahl) else zahl+1 if abs(zahl+1) <= abs(zahl) else zahl
    return zahl


base_func = lambda stufe,speed=1: speed*( 20/3. + 1/35.*stufe + 3.*stufe**2 + 3/250.*stufe**3 )

linear_split_func = lambda stufe, speed=1 :speed * (     1/   3. * {0: -5.,
                                                                    1:  1.,
                                                                    2:  4.,
                                                                    3:  4.,
                                                                    4:  1.}[stufe%5]\
                                                    +stufe/1750. * {0:-15.,
                                                                    1: -1.,
                                                                    2:  6.,
                                                                    3:  6.,
                                                                    4: -1.}[stufe%5])\
                                                      

lut_function = lambda stufe, speed=1: base_func(stufe,speed) + linear_split_func(stufe,speed) + osc_func(stufe,speed)
lut_diff_function = lambda stufe, value,speed=1: value - base_func(stufe,speed) - linear_split_func(stufe,speed) - osc_func(stufe,speed)

    
    
