#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: frendor

Die knappe Variante. Wichtig ist das Rundungsverhalten: In Gigrawars wird bei x.5 immer aufgerundet. 
Python3 rundet normalerweise an der Stelle zu geraden Zahlen hin.
"""



import numpy as np
import math 

old_round = lambda x: int(x + math.copysign(0.5, x))

res_factor={"H2O":2.,
            "Fe": 8/5.,
            "Lut":1.,
            "H2C":2., #gilt nur fürs normal Uni
            "H2C_6x": 0.4,
            "H2EC": 5. # gilt nur fürs speed-universum
            }

base_func = lambda stufe:  3*( stufe**2 + 1/250.*stufe**3 ) 

linear_split_func = lambda stufe: (1. + stufe/250.) * {0: 5.,
                                                       1: 7.,
                                                       2: 8.,
                                                       3: 8.,
                                                       4: 7.}[stufe%5]

### Grundformel für Fe, Lut, H2O und H2(Chemie):
res_function = lambda stufe, speed, res_type: old_round(np.round(speed * res_factor[res_type] * (base_func(stufe) + linear_split_func(stufe)) , decimals=6)) 

#Standarduniversum:
fe_function = lambda stufe: res_function(stufe, speed=1, res_type="Fe")
lut_function = lambda stufe: res_function(stufe, speed=1, res_type="Lut" )
h2o_function = lambda stufe: res_function(stufe, speed=1, res_type="H2O" )
h2_chem_function = lambda stufe: res_function(stufe, speed=1, res_type="H2C" ) 

#### Die Erw. Chemie folgt einer anderen Formel
h2_echem_base_func = lambda stufe: 5 * ( 125 + 10 * ( stufe**3 + {0: 5.,
                                                                  1: 4.,
                                                                  2: 2.,
                                                                  3: 3.,
                                                                  4: 1.}[stufe%5]  ) )

h2_echem_osc_func = lambda stufe: 125* (-1)**stufe *{0:1, 1:-1 ,2:-1 ,3:1 ,4:1}[stufe%5]

h2_echem_function = lambda stufe: np.round(h2_echem_base_func(stufe) + h2_echem_osc_func(stufe), decimals=0)

####### Speeduniversum mit 6-facher Geschwindigkeit
fe_6x_function = lambda stufe: res_function(stufe, speed=6, res_type="Fe")
lut_6x_function = lambda stufe: res_function(stufe, speed=6, res_type="Lut")
h2o_6x_function = lambda stufe: res_function(stufe, speed=6, res_type="H2O") 
h2_chem_6x_function = lambda stufe: res_function(stufe, speed=6, res_type="H2C_6x") 
h2_echem_6x_function = lambda stufe: res_function(stufe, speed=6, res_type="H2EC")

