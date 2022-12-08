#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: frendor

Diese Variante beinhalte Oszillationsfunktionen, die um -0.5 und 0.5 springen 
und wie eine Rundungsfunktion wirken. Mit diesen Oszillationsfunktionen kommt 
man recht genau auf die Ingame-Werte. 
Ein normales Runden auf 10**-6 behebt normale Abweichungen (10**-8 und kleiner)
der Programmiersprache. 
Damit kann man Rundungsartefakte vermeiden, die z.B. bei Runden zu geraden 
Zahlen hin auftreten können. 
"""

import numpy as np

res_factor={"H2O":2.,
            "Fe": 8/5.,
            "Lut":1.,
            "H2C":2., #gilt nur fürs normal Uni
            "H2C_6x": 2.4, #da steckt schon die 6-fache Geschwindigkeit mit drin 
            "H2EC":5., #gilt nur fürs SpeedUni 6x
            }

base_func = lambda stufe:  3*( stufe**2 + 1/250.*stufe**3 ) 

linear_split_func = lambda stufe: (1. + stufe/250.) * {0: 5.,
                                                       1: 7.,
                                                       2: 8.,
                                                       3: 8.,
                                                       4: 7.}[stufe%5]

### Fe, Lut, H2O und H2 (Chemie) folgen einer Formel:
res_function = lambda stufe, speed, res_type: np.round(speed * res_factor[res_type] * (base_func(stufe) + linear_split_func(stufe)) \
                                                       + osc_func(stufe, res_type, speed), decimals=6)
                                                            
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


h2_echem_function = lambda stufe: np.round(h2_echem_base_func(stufe) + h2_echem_osc_func(stufe), decimals=6)


####### Speeduniversum mit 6-facher Geschwindigkeit


h2_echem_6x_osc_func = lambda stufe: 1/5. * osc_initial_values_dict["H2EC_6x"][stufe%25] 


fe_6x_function = lambda stufe: res_function(stufe, speed=6, res_type="Fe")
lut_6x_function = lambda stufe: res_function(stufe, speed=6, res_type="Lut")
h2o_6x_function = lambda stufe: res_function(stufe, speed=6, res_type="H2O")
h2_chem_6x_function = lambda stufe: res_function(stufe, speed=1.2, res_type="H2C") 
h2_chem_6x_function = lambda stufe: res_function(stufe, speed=1, res_type="H2C_6x") 

h2_echem_6x_function = lambda stufe: np.round( res_factor["H2EC"] * 6 * (base_func(stufe) + linear_split_func(stufe))\
                                              + h2_echem_6x_osc_func(stufe) ,decimals=6)

### 25-Teilige Oszillation
osc_slope_func = lambda stufe, res_type: osc_initial_slope_dict[res_type][stufe%5] + (stufe%25-stufe%5) * osc_slope_diff_dict[res_type][stufe%5] 

osc_func = lambda stufe, res_type, speed=1:  osc_jump( speed/50. * ( 1/5. * osc_initial_values_dict[res_type][stufe%25]\
                                                          + (stufe/25 - stufe/25 % 1)*osc_slope_func(stufe,res_type) ) )   

def osc_jump(zahl):
    zahl = zahl - (zahl - zahl%1) # grobe Näherung
    zahl = zahl-1 if abs(zahl-1) < abs(zahl) else zahl+1 if abs(zahl+1) <= abs(zahl) else zahl
    return zahl

osc_initial_values_dict = {"H2O":np.array([   0.,  -20.,  -80.,   40.,   60.,
                                            -50.,  120.,   80.,   50.,    0.,
                                           -100.,  110.,  -60.,  110.,   90.,
                                            100.,  -50.,    0.,  -30.,   80.,
                                             50., -110.,   10., -120.,  -30.]),
                            "Fe":np.array([   0,  -16,  -64,   82, -102,  
                                            110, -104,   14,  -60, -100, 
                                            120,  -12,   52,   38,  -78,  
                                            -70,  -90,  -50,   26,  114,  
                                            -60,   62, -142,   54, -124]),
                           "Lut":np.array([   0.,  -10.,  -40., -105.,   30.,  
                                            100.,   60.,  -85., -100.,    0.,
                                            -50.,  -70.,  -30.,   55.,  -80.,
                                             50.,  100.,  125.,  110.,   40., 
                                           -100.,   70., -120.,   65.,  110.]),
    
                           "H2C":np.array([   0.,  -20.,  -80.,   40.,   60.,
                                            -50.,  120.,   80.,   50.,    0.,
                                           -100.,  110.,  -60.,  110.,   90.,
                                            100.,  -50.,    0.,  -30.,   80.,
                                             50., -110.,   10., -120.,  -30.]),
                           ##### Speed-Universum ####
                           "H2EC_6x":np.array([0, -1,  1,   2, -2,
                                               0,  1, -1,   0,  0,
                                               0, -2,  2,  -2,  2,
                                               0,  0,  0,   1, -1,
                                               0,  2, -2,  -1,  1]), 
                           "H2C_6x":np.array([   0,  -24,  -96,   -2,  -28,
                                                40,   94, -104,  -90,  100,
                                               -70,  -18,   78,  -68,    8,
                                                20,  -10,   50,  -86,   46,
                                               -90,  -32,  -88,  -44,   64]),
                          } 

osc_initial_slope_dict = { "H2O":    {0:   0., 1: -10., 2:  10., 3:  10., 4: -10.},
                           "Lut":    {0:   0., 1: -30., 2: -45., 3: -45., 4: -30.},
                           "Fe":     {0: 10.,1: 22.,2: -2.,3:-12.,4: -8.},
                           "H2C":    {0:   0., 1: -10., 2:  10., 3:  10., 4: -10.},
                           
                           "H2C_6x": {0: -10., 1:   8,  2:  22,  3: -18,  4: -12.},
                         }


osc_slope_diff_dict = { "H2O":{k:0 for k in range(5)},
                        "Lut":{k:0 for k in range(5)},
                        "Fe":{0:  0, 1: -4, 2:  2, 3: -2, 4:  4},
                        "H2C":{k:0 for k in range(5)},
                        
                        "H2C_6x": {0:  0., 1: +4., 2: -2, 3: +2., 4: -4.},
                      }
