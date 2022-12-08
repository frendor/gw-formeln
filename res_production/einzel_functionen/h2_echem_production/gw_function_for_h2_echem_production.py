#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 10:47:41 2022

@author: frendor
"""

import numpy as np
import locale
locale.setlocale( locale.LC_ALL, 'de_DE.UTF-8' )
from scipy.optimize import curve_fit
from string import ascii_lowercase
import matplotlib.pyplot as plt
import matplotlib as mpl 
import datetime
import os


PNG_FOLDER = "plots/"
RES_ART = "H2 (Erw. Chem)"
RES_SHORT = "H2 (EC)"
filename_1x = "gw_uni4_h2_echem_info"
filename_6x = "gw_speeduni_6x_h2_echem"

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
#mpl.rcParams['axes.formatter.useoffset'] = False

# from https://stackoverflow.com/questions/3154460/python-human-readable-large-numbers
millnames = ['',' Tausend',' Mio.',' Mrd.',' Bio.']

with open(f"ingame-werte/{filename_1x}","r") as prodinfo:
    orig_data = prodinfo.read()

orig_values = [(int(row.split()[0]),int(row.split()[3].replace(".","")) ) for row in orig_data.split("\n") if row ]

with open(f"ingame-werte/{filename_6x}","r") as prodinfo:
    orig_data_6x = prodinfo.read()

orig_values_6x = [(int(row.split()[0]),int(row.split()[1]) ) for row in orig_data_6x.split("\n") if row ]

##### Ganz andere Form der Funktion für Erweiterte Chemie:

base_func_1x = lambda stufe: 5 * ( 125 + 10 * ( stufe**3 + {0: 5.,
                                                            1: 4.,
                                                            2: 2.,
                                                            3: 3.,
                                                            4: 1.}[stufe%5]  ) )

osc_func_echem = lambda stufe: 125* (-1)**stufe *{0:1, 1:-1 ,2:-1 ,3:1 ,4:1}[stufe%5]


res_func_1x = lambda stufe: base_func_1x(stufe) + 0*osc_func_echem(stufe)


###### Im SpeedUniversum sah es anders aus:

osc_values = np.array([0, -1,  1,   2, -2,
                       0,  1, -1,   0,  0,
                       0, -2,  2,  -2,  2,
                       0,  0,  0,   1, -1,
                       0,  2, -2,  -1,  1])

osc_func = lambda stufe, speed=1: 1/5. * osc_values[stufe%25] 


def osc_jump(zahl):
    zahl = zahl - (zahl - zahl%1) # grobe Näherung
    zahl = zahl-1 if abs(zahl-1) < abs(zahl) else zahl+1 if abs(zahl+1) <= abs(zahl) else zahl
    return zahl

base_func = lambda stufe, speed=6:  speed * 5 * 3*( stufe**2 + 1/250. * stufe**3 )

linear_split_func = lambda stufe, speed=6:   speed*5* (1+stufe/250.)* {0: 5,
                                                                       1: 7,
                                                                       2: 8,
                                                                       3: 8,
                                                                       4: 7}[stufe%5]


res_func_6x = lambda stufe: base_func(stufe) + linear_split_func(stufe) + osc_func(stufe)
                                                        

res_function = lambda stufe, speed=1: np.round({1:res_func_1x,
                                                6:res_func_6x}[speed](stufe) , decimals=3)


res_diff_function = lambda stufe, value,speed=1: value - res_function(stufe,speed)

res_fit_func = lambda stufe, a=1: a * ( 3*( 1. + stufe/250. + stufe**2 + 1/250. * stufe**3 ) )
res_fit_initial_params = [1.]

lin_fit_func = lambda stufe, a=1,b=1: a +b *stufe
lin_fit_initial_params = [1.,1.]

cube_fit_func = lambda stufe, a=1,b=1,c=1,d=1:  a +b/250. *stufe + c* stufe**2 + d/250.*stufe**3
cube_fit_initial_params = [1.,1.,1.,1.]



def res_fit(vlist, prod_func = lambda stufe, a,b: a+b*stufe, initial_params = [1.,1.]):
    stufen_list, val_list = zip(*vlist)
    
    #initial_params = [1.,1.,1.,1.]
    
    bounds = (tuple([-np.inf for elem in initial_params]), tuple([np.inf for elem in initial_params]))
    

    popt,pcov = curve_fit(prod_func,stufen_list, val_list, bounds = bounds, p0=initial_params)
    for i in range(100):
        if bounds: 
            popt,pcov = curve_fit(prod_func,stufen_list, val_list,
                          bounds=bounds,
                          p0=tuple(popt))
        else:
            popt,pcov = curve_fit(prod_func,stufen_list, val_list,
                          p0=tuple(popt))
    #print(popt, pcov) 
    return popt


def plot_resproduction(savefig=False, res_line = orig_values,
                                      show_absolut_fit_plots=True,
                                      show_absolut_plots=True, 
                                      show_5split=True, 
                                      show_diff_plots=True, 
                                      show_25split=True,
                                      show_micro_steps = True,
                                      show_osc_stepwidth = True,
                                      speed_factor=1 
                                      ):

    if show_absolut_fit_plots:
        fig1, (ax_absolut, ax_diff) = plt.subplots(2, figsize=[8.0,5.0], sharex=True)
    
        stufen_list, val_list = zip(*res_line[:100])    
        ax_absolut.plot(*zip(*res_line[:100]),label = f"{RES_ART} Produktion" )
        fit_func = cube_fit_func
        fit_params = res_fit(res_line, fit_func, cube_fit_initial_params)
        for nr2,val in enumerate(fit_params):
            print(f"{ascii_lowercase[nr2]}: {val:.12f}")
    
        ax_absolut.plot(*zip(*[(s, fit_func(s,*fit_params) ) for s in stufen_list]) , label=f"Fit" )
        
        diff_line = [(s, v - fit_func(s,*fit_params)) for s,v in res_line[:100]]
        ax_diff.plot (*zip(*diff_line), label = "Differenz" )
        
        ax_absolut.legend(bbox_to_anchor=(1,1), loc="upper left")
        ax_absolut.set_ylabel(f"{RES_ART}produktion")
        ax_absolut.set_title(f"{RES_ART}produktion in Gigrawars")
            
        fig1.text(0.65,0.12,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)
        plt.tight_layout()
        plt.show()

    
    if show_absolut_plots:
        fig1, (ax_absolut, ax_diff) = plt.subplots(2, figsize=[8.0,5.0], sharex=True)
    
        stufen_list, val_list = zip(*res_line)    
        ax_absolut.plot(*zip(*res_line[:100]),label = f"{RES_ART} Produktion" )
            
        ax_absolut.plot(*zip(*[(s,res_function(s,speed_factor) ) for s,v in res_line[:100]]) , label=f"{RES_ART} Funktion" )
        
        diff_line = [(s, res_diff_function(s,v,speed_factor)) for s,v in res_line[:100]]
        ax_diff.plot (*zip(*diff_line), label = "Differenz" )
        
        ax_absolut.legend(bbox_to_anchor=(1,1), loc="upper left")
        ax_absolut.set_ylabel(f"{RES_ART}produktion")
        ax_absolut.set_title(f"{RES_ART}produktion in Gigrawars")
            
        fig1.text(0.65,0.12,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)
        plt.tight_layout()
        plt.show()


    if show_diff_plots:
        fig1, ax_dp = plt.subplots(2, figsize=[8.0,5.0], sharex=True)
    
        rest_line = [(s, res_diff_function(s, v, speed_factor)) for s,v in res_line ]
        stufen_list, val_list = zip(*rest_line)    
        ax_dp[0].plot(*zip(*rest_line[:200]),label = f"{RES_SHORT} Rest Funktion" )
        fit_func = lin_fit_func
        fit_params = res_fit(rest_line, fit_func, lin_fit_initial_params)
        for nr2,val in enumerate(fit_params):
            print(f"{ascii_lowercase[nr2]}: {val:.12f}")
    
        ax_dp[0].plot(*zip(*[(s,fit_func(s,*fit_params) ) for s in stufen_list[:200]]) , label=f"Fit" )
        diff_line = [(s, v - fit_func(s,*fit_params)) for s,v in rest_line]
        ax_dp[1].plot (*zip(*diff_line[:200]), label = "Differenz" )
        
        ax_dp[0].legend(bbox_to_anchor=(1,1), loc="upper left")
        ax_dp[0].set_ylabel(f"{RES_ART}produktion")
        ax_dp[0].set_title(f"{RES_ART}produktion in Gigrawars")
            
        fig1.text(0.65,0.12,"{} {}".format("fReN",datetime.datetime.now().date()),size=9)
        
        plt.tight_layout()
        plt.show()        
        
    ## die 5 Äste der Funktion
    if show_5split:    
        
        limit = 5
        for subline_nr in range(limit):
            subline = [(s,res_diff_function(s,v,speed_factor)) for s,v in res_line if s%limit == subline_nr]
            
            stufen_list, val_list = zip(*subline[:50])
            fig2, ax = plt.subplots(1,figsize=[8.0,5.0])
            fit_func = lambda stufe, a=1,b=1: a + b *stufe
            ax.plot(stufen_list, val_list, ".-", label=f"{subline_nr%5} {subline_nr}")
            if speed_factor==1:
                ax.plot(*zip(*[(s, osc_func_echem(s)) for s in stufen_list]), label="Osc EChem")
            
            params = res_fit(subline,fit_func,lin_fit_initial_params)
            ax.plot(*zip(*[(s,fit_func(s,*params)) for s in stufen_list] ), ".-", label=f"{subline_nr}")
            ax.legend()
            plt.show()
            
            for nr2,val in enumerate(params):
                print(f"{ascii_lowercase[nr2]}: {val:.12f}")

    ## die 25 Äste der Funktion
    if show_25split or show_osc_stepwidth:    
        diff_line = [(s, res_diff_function(s,v,speed_factor)+osc_func(s,speed_factor)) for s,v in res_line]
        output = {elem:"" for elem in range(25)}
        null_werte = np.zeros(25)
        limit = 25
        for subline_nr in range(limit):
            #if subline_nr % 5 not in [4]:
            #    continue
            subline = [(s,v) for s,v in diff_line if s%limit == subline_nr]
            stufen_list, val_list = zip(*subline)
            null_werte[subline_nr] = val_list[0]
            osc_stufen, osc_vals = zip(*[(s,osc_func(s,speed_factor) )  for s in stufen_list ])
            
            if show_25split:
                fig2, ax = plt.subplots(1,figsize=[8.0,5.0])
                ax.plot(stufen_list, val_list, ".-", label=f"{subline_nr%5} {subline_nr}")
                ax.plot(osc_stufen, osc_vals, ".-", label="osc_func" )
                ax.legend()
                plt.show()
            

            if show_osc_stepwidth:
                pos = [0,0]
                neg = [0,0]
                
                for nr, vlist in enumerate([val_list, osc_vals]):
                    for p1,p2 in zip(vlist,vlist[1:]):
                        if (p2-p1)> 0:
                            pos[nr] = (p2-p1)
                        else: 
                            neg[nr] = (p2-p1)
                    
                key = subline_nr
                osc_slope_suggestion = neg[0] if abs(neg[0]) < abs(pos[0]) else pos[0]
                output[key] = f"{key:2n} {key%5:2n}  {pos[0]:+.2f} / {neg[0]:+.2f} | {min(val_list): .2f} bis {max(val_list): .2f} | osc_func: {pos[1]:+.2f} / {neg[1]:+.2f} (osc_slope: {osc_slope_suggestion*50: .1f})"
    
 
    
    
    if show_osc_stepwidth:    
        for i in range(5):
            print(i)
            for j in range(25):
                if j%5==i%5:
                    print(output[j])#, f"Ansatz Schrittweite: {schritt(j):.3f}")
        
        print("".center(20,"-"))
        print("Nullwerte: ", np.round(null_werte,decimals=3))
        nw_output = "Nullwerte * 250: \n["
        for i in range(5):
            nw_output+=",".join([f"{z*250: 7.1f}" for z in null_werte[5*i:5*i+5]]) + ",\n "

        print(nw_output[:-3]+"]" )
        print("".center(20,"-")) 
    
    
    
  
    if show_micro_steps:
        
        for rest in range(5):
            
            subline = [(s,res_diff_function(s,v,speed_factor)) for s,v in res_line if s%limit == rest]
        
            
            subline_dict = {sline_nr:[val for nr2,val in enumerate(subline) if nr2%5==sline_nr] for sline_nr in range(5)}    
            
            plt.figure()
            ax6 = plt.subplot(111)
            step_dict = {}
            for nr,line in subline_dict.items():
                x_vals, y_vals = zip(*line[:6])
    
                ax6.plot(x_vals, y_vals, ".-", label=f"{rest}: {nr}")
                
                po_line,pc_line = curve_fit(lambda x,a,b: a +b*x , x_vals, y_vals, p0=[1.,1.])
                step_dict[nr] = po_line[0]
                #print("Micro-Abstände:  Teil: ", rest)
                #for nr3,fv in enumerate(po_line):
                #    print(f"  {nr} {ascii_lowercase[nr3]}: {fv:.12f}")        
    
            ax6.legend()
            plt.show()
            #steps = np.array(list(step_dict.values()))
            
            print("Micro-Schritte: ")
            
            for nr,step in step_dict.items():
                print(f"{nr} ({nr*5+rest}):  {step:.5f} ({step*2*125:+.5f})")
                #null_dict[nr*5+rest]-= step
                #neues_null_dict[nr*5+rest]= null_dict[nr*5+rest]
                
            #print((steps - steps.min())/(steps[1]-steps.min()))
            #ssteps = sorted(steps)
            #print("Y-Werte: ",steps)
            #print(1/(steps[1]-steps.min()) )
            #po,pc = curve_fit(lambda x,a,b: a + b*x , list(range(5)), ssteps, p0=[1.,1.])
            #print("Micro-Steigung:")
            #for nr3,fv in enumerate(po):
            #    print(f"{ascii_lowercase[nr3]}: {fv:.12f}")        
            #            plt.figure()
            #            ax7 = plt.subplot(111)
            #            ax7.plot(list(range(5)),steps,"o" ,label="steps")
            #            ax7.plot(list(range(5)),ssteps,".-" ,label="steps")
            #            
            #            ax7.plot(list(range(5)), [(lambda x,a,b: a + b*x)(s,*po) for s in range(5)],"-", label="Fit")
            #            ax7.plot(range(5), [{0:1,1:-2,2:2,3:-1,4:0}[s]*po[1]*-1 for s in range(5)],"^",label="Ansatz")
            #            ax7.legend()
            #            plt.show()
            #step_size = po[1]
            #if steps[1]!= steps.min():
            #    step_size = steps[1]- steps.min()
            #    print(f"Micro-Steigung: {step_size:.12f} " , (steps - steps.min())/step_size)
            #    
            #for p1,p2 in sorted([(elem,elem/step_size) for elem in range(10000) if not 0.0002 < (elem/step_size)%1  < 1-0.0002],key=operator.itemgetter(1))[:20]:
            #    print(f"{p1:5.0f} {p2:.3f}")
        #nw = [null_dict[n] for n in range(25)]
        #nnw = np.round([neues_null_dict[n] for n in range(25)],decimals=3)
        #print("Neue Nullwerte: ", np.array(nw)*125)
        #print("Neue Werte: ", nnw)

            
    
if __name__ == '__main__':
    for speed in [6]:
        plot_resproduction(savefig=False,
                           show_absolut_fit_plots=False,
                           show_absolut_plots=True,
                           show_diff_plots=False,
                           show_5split=True,
                           show_25split=True,
                           show_osc_stepwidth = False,
                           show_micro_steps=False,
                           
                           speed_factor=speed,
                           res_line={1:orig_values, 6:orig_values_6x}[speed]
                       )
    
    
    
    
