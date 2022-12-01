#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: frendor
"""

import numpy as np
import locale
locale.setlocale( locale.LC_ALL, 'de_DE.UTF-8' )
import matplotlib.pyplot as plt
import matplotlib as mpl 
import datetime
import os
import gw_resprod as gw_res

PNG_FOLDER = "plots/"
RUNDE = "Gigrawars"
UNI = {1:"Uni4",
       6:"Speeduni_x6"}

import locale
locale.setlocale( locale.LC_ALL, 'de_DE.UTF-8' )

#    plt.rc('font', **{'sans-serif' : 'Source Sans', 'family' : 'sans-serif'})
#    plt.rcParams.update({'font.sans-serif': 'Source Sans', 'font.family': 'sans-serif'})
mpl.rcParams['axes.linewidth'] = 1.5 #set the value globally
mpl.rcParams['mathtext.default'] = 'sf'
mpl.rcParams['xtick.major.size'] = 5
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['ytick.major.size'] = 5
mpl.rcParams['ytick.major.width'] =2
mpl.rcParams['ytick.minor.size'] = 4
mpl.rcParams['ytick.minor.width'] =1
#mpl.rcParams['text.usetex'] = True
mpl.rcParams['figure.dpi'] = 72
mpl.rcParams['savefig.dpi'] = 72
mpl.rcParams['figure.figsize'] = [8.0,5.0]
mpl.rcParams['savefig.transparent']=False
###Linux-Einstellungen
mpl.rcParams['grid.linestyle'] = ':'
mpl.rcParams['grid.linewidth'] = 0.2
mpl.rcParams['grid.color']='k'
mpl.rcParams['legend.framealpha']=1
mpl.rcParams['legend.fancybox'] = True
mpl.rcParams['legend.fontsize'] = u'medium'
mpl.rcParams['font.size']=12
if os.name == "posix":
    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['ytick.right'] = True
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'


res_functions = {1:{"Fe":gw_res.fe_function,
                    "Lut":gw_res.lut_function,
                    "H2O": gw_res.h2o_function,
                    "H2C":gw_res.h2_chem_function,
                    "H2EC":gw_res.h2_echem_function},
                 6: {"Fe":gw_res.fe_6x_function,
                    "Lut":gw_res.lut_6x_function,
                    "H2O": gw_res.h2o_6x_function,
                    "H2C":gw_res.h2_chem_6x_function,
                    "H2EC":gw_res.h2_echem_6x_function},
                }


def load_values(res_type,speed_factor):
    filename_base = {6:"ingame-werte/gw_speeduni_6x_",
                     1:"ingame-werte/gw_uni4_"}[speed_factor]
    with open(filename_base + res_type.lower(), "r") as data_file:
        orig_values_raw = data_file.read()
        
    if speed_factor == 1:
        values = [(int(row.split()[0]),int(row.split()[3].replace(".","")) ) for row in orig_values_raw.split("\n") if row ]
    elif speed_factor == 6:
        values = [(int(row.split()[0]),int(row.split()[1]) ) for row in orig_values_raw.split("\n") if row ]

    return values   
        

def plot_produktion(save_fig=False, speed_factor=1):
    
    angaben_dict = {k:load_values(k,speed_factor) for k in res_functions[speed_factor].keys()}
    
    fig1 ,(ax_abs,ax_diff) = plt.subplots(2, figsize=[8.0,10.0])
        
    ax_abs.set_title(f"Resproduktion in Gigrawars: {UNI[speed_factor]}")
    ax_diff.plot([],[], " ", label ="Differenz")
    for res_type, res_values_absolut in angaben_dict.items():
        
        ax_abs.plot(*zip(*res_values_absolut), ".", label=f"{res_type} Ingame-Werte" )
        ax_abs.plot(*zip(*[(s,res_functions[speed_factor][res_type](s)) for s, v in res_values_absolut]), "-", label=f"{res_type} Funktion" )
    
        ax_diff.plot(*zip(*[(s,v-res_functions[speed_factor][res_type](s)) for s, v in res_values_absolut]),"-", label=f"{res_type} Funktion + Oszillation")    
        ax_diff.plot(*zip(*[(s,v-res_functions[speed_factor][res_type](s,use_osc=False)) for s, v in res_values_absolut]),".-", label=f"{res_type} Funktion gerundet")    
        
        
    
    ax_abs.legend(bbox_to_anchor=(1,1), loc="upper left")
    ax_abs.set_xlabel("Minenstufe")
    ax_abs.set_ylabel("Produktionswert")
    ax_abs.set_yscale("log")
    ax_diff.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    
    fig1.text(0.55,0.12,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)
    
    plt.tight_layout()
    if save_fig:
        plt.savefig(f"{PNG_FOLDER}{RUNDE}_{UNI[speed_factor]}_absolute_Eisenproduktion+Funktion.png")
   
    plt.show()
    

    #### Zeigen wir mal die Teile der Funktion:
    fig2, (ax_base, ax_split, ax_osci) = plt.subplots(3, figsize=[10.0,8.0])

    max_lvl = 999

    ax_base.set_title("Bestandteile der Formel für die Gigrawars-Eisenproduktion")
    ax_base.plot(*zip(*[(stf,gw_res.base_func(stf)) for stf in range(max_lvl)]), label="Basisfunktion")
    ax_base.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    
    ax_split.plot([], [], " ", label="Lineare Verschiebungen")
    for branch in [0,1,2]:
        ax_split.plot(*zip(*[(stf,gw_res.linear_split_func(stf)) for stf in range(max_lvl) if stf%5 == branch]),label=f"Stufe%5 == {branch} und {5-branch}" if branch > 0 else f"Stufe%5 == {branch}")
    ax_split.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    ax_osci.plot(*zip(*[(stf,gw_res.osc_func(stf,"Fe",speed_factor)) for stf in range(max_lvl)]),label="25-Teilige Oszillation\nals Rundungsfunktion")
    ax_osci.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    fig2.text(0.65,0.06,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)
    plt.tight_layout()
    if save_fig:
        plt.savefig(f"{PNG_FOLDER}{RUNDE}_{UNI[speed_factor]}_EisenProdFunktion_Einzelterme.png")

    plt.show()
    
    ##### Die 25-Teilige Oszillation ####
    
    fig3, ax_25 = plt.subplots(5,5, figsize=[10.,10.], sharex = True, sharey=True )
    ax_25[0,2].set_title("25-Teilige Oszillation (Rundungsfunktion)")
    
    for branch in range(25):
        x_vals = np.arange(branch, 21*25,25)
        x_vals = np.arange(branch, max_lvl,25)
        ax_25[branch%5,int(branch/5)%5].plot(*zip(*[(s,gw_res.osc_func(s,"Fe",speed_factor)) for s in x_vals]),".-", label=f"Stufe%{branch}")
    fig3.text(0.65,0.16,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)

    if save_fig:
        plt.savefig(f"{PNG_FOLDER}{RUNDE}_{UNI[speed_factor]}_EisenProdFunktion_Oszillationen.png")

    plt.show()
    ####
    
    print("Stufe","Ingame-Wert", "Funktion".rjust(13), "Differenz".rjust(10))
    for s,v in angaben_dict["Fe"][:20]+angaben_dict["Fe"][-20:]:
        print(f"{s:3d}  {v:12.0f}  {res_functions[speed_factor]['Fe'](s):12.2f}  {v-res_functions[speed_factor]['Fe'](s): .2e}" )
        
if __name__ == '__main__':
    for speed in [1,6]:
        plot_produktion(save_fig=True,speed_factor=speed)
