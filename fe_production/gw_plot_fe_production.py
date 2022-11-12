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
from gw_feprod import iron_function, iron_diff_function
from gw_feprod import base_func, linear_split_func, osc_func


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



with open("ingame-werte/gw_uni4_eiseninfo","r") as prodinfo:
    eisen_info_file = prodinfo.read()

fe_angaben_1x = [(int(row.split("\t")[0]),int(row.split("\t")[3].replace(".","")) ) for row in eisen_info_file.split("\n")  ]

with open("ingame-werte/gw_speed6uni_eisenprod","r") as prodinfo:
    eisen_info_file = prodinfo.read()

fe_angaben_6x = [(int(row.split()[0]),int(row.split()[1]) ) for row in eisen_info_file.split("\n") if row ]


def plot_eisenproduktion(save_fig=False, speed_factor=1):
    
    fe_angaben_dict = {1:fe_angaben_1x,6:fe_angaben_6x}
    if speed_factor in fe_angaben_dict:
        fe_angaben = fe_angaben_dict[speed_factor]
    else:
        print("Keine Vergleichswerte für die gewünschte Geschwindigkeit gefunden. Keine weitere Ausgabe.")
        return

    fe_values_absolut = [(stf, iron_function(stf,speed_factor) )  for stf,_ in fe_angaben]
    fe_values_diff = [(s, iron_diff_function(s, v, speed=speed_factor))  for s,v in fe_angaben]

    fig1 ,(ax_abs,ax_diff) = plt.subplots(2, figsize=[8.0,5.0])
    
    ax_abs.set_title("Eisenproduktion in Gigrawars")
    ax1_label = ["Ingame Werte", "Formel"]
    ax1_marker = [".","-"]
    
    for nr, line in enumerate([fe_angaben, fe_values_absolut]):    
        stufen_list, val_list = zip(*line)    
        ax_abs.plot(stufen_list, val_list,ax1_marker[nr], label=ax1_label[nr])
    ax_abs.legend(bbox_to_anchor=(1,1), loc="upper left")
    ax_abs.set_xlabel("Stufe Eisenmine")
    ax_abs.set_ylabel("Eisenproduktion")
    
    ax_diff.plot(*zip(*fe_values_diff),".-", label="Differenz")    
    ax_diff.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    fig1.text(0.65,0.12,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)
    
    plt.tight_layout()
    if save_fig:
        plt.savefig(f"{PNG_FOLDER}{RUNDE}_{UNI[speed_factor]}_absolute_Eisenproduktion+Funktion.png")
   
    plt.show()
    

    #### Zeigen wir mal die Teile der Funktion:
    fig2, (ax_base, ax_split, ax_osci) = plt.subplots(3, figsize=[10.0,8.0])

    max_lvl = len(fe_angaben) 

    ax_base.set_title("Bestandteile der Formel für die Gigrawars-Eisenproduktion")
    ax_base.plot(*zip(*[(stf,base_func(stf)) for stf in range(max_lvl)]), label="Basisfunktion")
    ax_base.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    
    ax_split.plot([], [], " ", label="Lineare Verschiebungen")
    for branch in [0,1,2]:
        ax_split.plot(*zip(*[(stf,linear_split_func(stf)) for stf in range(max_lvl) if stf%5 == branch]),label=f"Stufe%5 == {branch} und {5-branch}" if branch > 0 else f"Stufe%5 == {branch}")
    ax_split.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    ax_osci.plot(*zip(*[(stf,osc_func(stf)) for stf in range(max_lvl)]),label="25-Teilige Oszillation")
    ax_osci.legend(bbox_to_anchor=(1,1), loc="upper left")
    
    fig2.text(0.65,0.06,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)
    plt.tight_layout()
    if save_fig:
        plt.savefig(f"{PNG_FOLDER}{RUNDE}_{UNI[speed_factor]}_EisenProdFunktion_Einzelterme.png")

    plt.show()
    
    ##### Die 25-Teilige Oszillation ####
    
    fig3, ax_25 = plt.subplots(5,5, figsize=[10.,10.], sharex = True, sharey=True )
    ax_25[0,2].set_title("25-Teilige Oszillation")
    
    for branch in range(25):
        x_vals = np.arange(branch, 21*25,25)
        x_vals = np.arange(branch, max_lvl,25)
        ax_25[branch%5,int(branch/5)%5].plot(*zip(*[(s,osc_func(s)) for s in x_vals]),".-", label=f"Stufe%{branch}")
    fig3.text(0.65,0.16,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)

    if save_fig:
        plt.savefig(f"{PNG_FOLDER}{RUNDE}_{UNI[speed_factor]}_EisenProdFunktion_Oszillationen.png")

    plt.show()
    ####
    
    print("Stufe","Ingame-Wert", "Funktion".rjust(13), "Differenz".rjust(10))
    for s,v in fe_angaben[:20]+fe_angaben[-20:]:
        print(f"{s:3d}  {v:12.0f}  {iron_function(s,speed_factor):12.2f}  {iron_diff_function(s,v,speed_factor): .2e}" )
        
if __name__ == '__main__':
    for speed in [1,6]:
        plot_eisenproduktion(save_fig=False,speed_factor=speed)
