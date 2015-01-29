# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 22:03:19 2015

@author: Summer
"""

import numpy as np
import os
from conf import *
from matplotlib.pylab import *
import matplotlib.pylab as plt
from operator import itemgetter

if __name__ == '__main__':
    filenamesExp3 = [x for x in os.listdir(save_addressExp3) if 'csv' in x]
    filenamesUCB1 = [x for x in os.listdir(save_addressUCB1) if 'csv' in x]
      
    for x in filenamesExp3:
        filename = os.path.join(save_addressExp3, x)
        if '0.3_Hour'in x:
            with open(filename, 'r')as f:
                randa = {}
                randc = {}
                exp3a = {}
                exp3c = {}
                ucb1a = {}
                ucb1c = {}
                greedya = {}
                greedyc = {}
                exp3CTRRatio = {}
                ucb1CTRRatio = {}
                greedyCTRRatio = {}
                tim = {}
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i],exp3a[i],exp3c[i], ucb1a[i], ucb1c[i], greedya[i], greedyc[i], exp3CTRRatio[i], ucb1CTRRatio[i], greedyCTRRatio[i]= [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])
                plt.plot(tim.values(),exp3CTRRatio.values(), label = 'Exp31_0.3MultipleDay')
                plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'UCB1_0.3MultipleDay')
                plt.plot(tim.values(), greedyCTRRatio.values(), label = 'UCB1_0.3MultipleDay')
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
        
        
        
        if '0.5_Hour'in x:
            with open(filename, 'r')as f:
                randa = {}
                randc = {}
                exp3a = {}
                exp3c = {}
                ucb1a = {}
                ucb1c = {}
                greedya = {}
                greedyc = {}
                exp3CTRRatio = {}
                ucb1CTRRatio = {}
                greedyCTRRatio = {}
                tim = {}
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i],exp3a[i],exp3c[i], ucb1a[i], ucb1c[i], greedya[i], greedyc[i], exp3CTRRatio[i], ucb1CTRRatio[i], greedyCTRRatio[i]= [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])
                plt.plot(tim.values(),exp3CTRRatio.values(), label = 'Exp31_0.3MultipleDay')
                plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'UCB1_0.3MultipleDay')
                plt.plot(tim.values(), greedyCTRRatio.values(), label = 'Exp31_0.3MultipleDay')
        
        
        if '0.7_Hour'in x:
            with open(filename, 'r')as f:
                randa = {}
                randc = {}
                exp3a = {}
                exp3c = {}
                ucb1a = {}
                ucb1c = {}
                greedya = {}
                greedyc = {}
                exp3CTRRatio = {}
                ucb1CTRRatio = {}
                greedyCTRRatio = {}
                tim = {}
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i],exp3a[i],exp3c[i], ucb1a[i], ucb1c[i], greedya[i], greedyc[i],exp3CTRRatio[i], ucb1CTRRatio[i], greedyCTRRatio[i]= [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])
                plt.plot(tim.values(),exp3CTRRatio.values(), label = 'Exp31_0.3MultipleDay')
                plt.plot(tim.values(), ucb1CTRRatio.values(), linestyle = ':',label = 'UCB1_0.3MultipleDay')
                plt.plot(tim.values(), greedyCTRRatio.values(), label = 'Exp31_0.3MultipleDay')
                #plt.plot(tim.values(), greedyCTRRatio.values(), label = 'UCB1_0.3MultipleDay')
    
    
        
    
