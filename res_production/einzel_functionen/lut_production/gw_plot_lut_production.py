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
from gw_lutprod import lut_function, lut_diff_function
from gw_lutprod import base_func, linear_split_func, osc_func


PNG_FOLDER = "plots/"
RUNDE = "Gigrawars"
UNI = {1:"Uni4",
       6:"Speeduni_x6"}
RES_ART = "Lutinum"
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



with open("ingame-werte/gw_uni4_lutvalues","r") as prodinfo:
    info_file = prodinfo.read()

orig_values_1x = [(int(row.split()[0]),int(row.split()[3].replace(".","")) ) for row in info_file.split("\n") if row ]

with open("ingame-werte/gw_speed6uni_lutprod","r") as prodinfo:
    info6_file = prodinfo.read()

orig_values_6x = [(int(row.split()[0]),int(row.split()[1]) ) for row in info6_file.split("\n") if row ]


def plot_produktion(save_fig=False, ingame_values=orig_values_1x, res_function = lut_function, res_diff_function = lut_diff_function , speed_factor=1):

    func_values_absolut = [(stf, res_function(stf,speed_factor) )  for stf,_ in ingame_values]
    func_values_diff = [(s, res_diff_function(s, v, speed=speed_factor))  for s,v in ingame_values]

    fig1 ,(ax_abs,ax_diff) = plt.subplots(2, figsize=[8.0,5.0])
    
    ax_abs.set_title(f"{RES_ART}produktion in Gigrawars")
    ax1_label = ["Ingame Werte", "Formel"]
    ax1_marker = [".","-"]
    
    for nr, line in enumerate([ingame_values, func_values_absolut]):    
        stufen_list, val_list = zip(*line)    
        ax_abs.plot(stufen_list, val_list,ax1_marker[nr], label=ax1_label[nr])
    ax_abs.legend(bbox_to_anchor=(1,1), loc="upper left")
    ax_abs.set_xlabel(f"Stufe {RES_ART}mine")
    ax_abs.set_ylabel(f"{RES_ART}produktion")
    
    ax_diff.plot(*zip(*func_values_diff),".-", label="Differenz")    
    ax_diff.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    fig1.text(0.65,0.12,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)
    
    plt.tight_layout()
    if save_fig:
        plt.savefig(f"{PNG_FOLDER}{RUNDE}_{UNI[speed_factor]}_absolute_{RES_ART}produktion+Funktion.png")
   
    plt.show()
    

    #### Zeigen wir mal die Teile der Funktion:
    fig2, (ax_base, ax_split, ax_osci) = plt.subplots(3, figsize=[10.0,8.0])

    max_lvl = len(ingame_values) 

    ax_base.set_title(f"Bestandteile der Formel für die Gigrawars-{RES_ART}produktion")
    ax_base.plot(*zip(*[(stf,base_func(stf,speed_factor)) for stf in range(max_lvl)]), label="Basisfunktion")
    ax_base.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    
    ax_split.plot([], [], " ", label="Lineare Verschiebungen")
    for branch in [0,1,2]:
        ax_split.plot(*zip(*[(stf,linear_split_func(stf,speed_factor)) for stf in range(max_lvl) if stf%5 == branch]),label=f"Stufe%5 == {branch} und {5-branch}" if branch > 0 else f"Stufe%5 == {branch}")
    ax_split.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    ax_osci.plot(*zip(*[(stf,osc_func(stf,speed_factor)) for stf in range(max_lvl)]),label="25-Teilige Oszillation")
    ax_osci.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    fig2.text(0.65,0.06,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)
    plt.tight_layout()
    if save_fig:
        plt.savefig(f"{PNG_FOLDER}{RUNDE}_{UNI[speed_factor]}_{RES_ART}ProdFunktion_Einzelterme.png")

    plt.show()
    
    ##### Die 25-Teilige Oszillation ####
    
    fig3, ax_25 = plt.subplots(5,5, figsize=[10.,10.], sharex = True, sharey=True )
    ax_25[0,2].set_title("25-Teilige Oszillation")
    
    for branch in range(25):
        x_vals = np.arange(branch, 21*25,25)
        x_vals = np.arange(branch, max_lvl,25)
        ax_25[branch%5,int(branch/5)%5].plot(*zip(*[(s,osc_func(s,speed_factor)) for s in x_vals]),".-", label=f"Stufe%{branch}")
    fig3.text(0.65,0.16,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)

    if save_fig:
        plt.savefig(f"{PNG_FOLDER}{RUNDE}_{UNI[speed_factor]}_{RES_ART}ProdFunktion_Oszillationen.png")

    plt.show()
    ####
    
    print("Stufe","Ingame-Wert", "Funktion".rjust(13), "Differenz".rjust(10))
    for s,v in ingame_values[:20]+ingame_values[-20:]:
        print(f"{s:3d}  {v:12.0f}  {lut_function(s,speed_factor):12.2f}  {lut_diff_function(s,v,speed_factor): .2e}" )
        
if __name__ == '__main__':


    for speed in [1,6]:    
        orig_values = {1:orig_values_1x,6:orig_values_6x}[speed]
        plot_produktion(save_fig=False,
                        ingame_values = orig_values, 
                        res_function=lut_function, 
                        res_diff_function=lut_diff_function, 
                        speed_factor=speed)

