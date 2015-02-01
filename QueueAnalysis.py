# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 14:38:45 2015

<<<<<<< HEAD
@author: Summer
=======
@author: Qingyun Wu
>>>>>>> cda2480e37c6817a19d09b24822fd576a2c892f6
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 22:09:48 2015

<<<<<<< HEAD
@author: Summer
=======
@author: Qingyun Wu
>>>>>>> cda2480e37c6817a19d09b24822fd576a2c892f6
"""

import numpy as np
import os
from conf import *
from matplotlib.pylab import *
from operator import itemgetter

if __name__ == '__main__':
    filenamesExp3 = [x for x in os.listdir(save_addressExp3) if 'csv' in x]
    filenamesUCB1 = [x for x in os.listdir(save_addressUCB1) if 'csv' in x] 
    filenamesQueue = [x for x in os.listdir(save_addressQueue) if 'csv' in x]
    
    for x in filenamesExp3:
        filename = os.path.join(save_addressExp3, x)
        if '0.3_Multi'in x:
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
                plt.plot(tim.values(),exp3CTRRatio.values(),label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'Hour')
<<<<<<< HEAD
                #plt.plot(tim.values(), greedyCTRRatio.values(), label = 'UCB1_0.3MultipleDay')
=======
                plt.plot(tim.values(), greedyCTRRatio.values(), label = 'UCB1_0.3MultipleDay')
>>>>>>> cda2480e37c6817a19d09b24822fd576a2c892f6
                #plt.legend('H')
        
    for x in filenamesQueue:
        filename = os.path.join(save_addressQueue, x)
        if '0.3_Multi'in x:
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
                plt.plot(tim.values(),exp3CTRRatio.values(),linestyle = ":", label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1CTRRatio.values(), linestyle = ":", label = 'Hour')
<<<<<<< HEAD
                #plt.plot(tim.values(), greedyCTRRatio.values(), linestyle= ":", label = 'UCB1_0.3MultipleDay')
=======
                plt.plot(tim.values(), greedyCTRRatio.values(), linestyle= ":", label = 'UCB1_0.3MultipleDay')
>>>>>>> cda2480e37c6817a19d09b24822fd576a2c892f6
                #plt.legend('H')
        
        '''        
        if '0.3_SingleDay'in x:
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
                #plt.plot(tim.values(),exp3CTRRatio.values(),label = 'Exp31_0.3SingleDay')
                plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'UCB1_0.3SingleDay')
                plt.plot(tim.values(), greedyCTRRatio.values(), label = 'UCB1_0.3MultipleDay')
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
        
        
        if '0.7_MultipleDay'in x:
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
                #plt.plot(tim.values(),exp3CTRRatio.values(),label = 'Exp31_0.3SingleDay')
                plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'UCB1_0.3SingleDay')
                plt.plot(tim.values(), greedyCTRRatio.values(), label = 'UCB1_0.3MultipleDay')
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
         '''     

    