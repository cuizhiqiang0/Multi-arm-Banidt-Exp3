
"""
Created on Sun Jan 25 22:09:48 2015

@author: Summer
"""
#Analysis: Multipleday(reset) performs better than SingleDay(reset), and SingleDay performs better than Hours




import numpy as np
import os
from conf import *
from matplotlib.pylab import *
from operator import itemgetter

if __name__ == '__main__':
    filenamesExp3 = [x for x in os.listdir(save_addressExp3) if 'csv' in x]
    filenamesUCB1 = [x for x in os.listdir(save_addressUCB1) if 'csv' in x]  
    filenamesExp3Greedy = [x for x in os.listdir(save_addressExp3Greedy) if 'csv' in x]
    filenamesQueue = [x for x in os.listdir(save_addressQueue) if 'csv' in x]
    filenamesTimeDecay = [x for x in os.listdir(save_addressTimeDecay) if 'csv' in x]
    filenamesDebugUCB1 = [x for x in os.listdir(save_addressDebugUCB1) if 'csv' in x]
    
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
                    randa[i],randc[i],exp3a[i],exp3c[i], ucb1a[i], ucb1c[i], greedya[i], greedyc[i], exp3CTRRatio[i], ucb1CTRRatio[i], greedyCTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])                
                #plt.plot(tim.values(),exp3CTRRatio.values(), linestyle = "--", label = 'Exp31_0.3SingleDay')
                #plt.annotate('Exp3', xy=(1.24e+09, 1.04479), xytext=(1.242e+09, 0.94), arrowprops=dict(facecolor='black', shrink=0.05),)
                #plt.plot(tim.values(), ucb1CTRRatio.values(), linestyle = ":",  label = 'Hour')
                #plt.plot(tim.values(), greedyCTRRatio.values(),linestyle = "--", label = 'greedy_Hour')
                #plt.legend('H')
                

        
        
        if '0.3_MultipleDay'in x:
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
                plt.plot(tim.values(),exp3CTRRatio.values(),label = 'Exp31_0.3SingleDay')
               
                #plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'UCB1_0.3SingleDay')
                #plt.plot(tim.values(), greedyCTRRatio.values(), label = 'greedy_0.3MultipleDay')
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
           
    for x in filenamesTimeDecay:
        filename = os.path.join(save_addressTimeDecay, x)
        if 'Multiple' in x:
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
                
                plt.plot(tim.values(),exp3CTRRatio.values(), linestyle= "--", label = 'Exp31_0.3SingleDay')
                #plt.annotate('Exp3', xy=(1.24e+09, 1.04479), xytext=(1.242e+09, 0.94), arrowprops=dict(facecolor='black', shrink=0.05),)
                #plt.plot(tim.values(), ucb1CTRRatio.values(), linestyle = "--",  label = 'Hour')
                #plt.plot(tim.values(), greedyCTRRatio.values(), linestyle = "--",  label = 'greedy_0.3MultipleDay')
                #plt.legend('H')
                
                
    
    for x in filenamesQueue:
        filename = os.path.join(save_addressQueue, x)
        if 'Multiple'in x:
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
                #plt.plot(tim.values(),exp3CTRRatio.values(), linestyle= "--", label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1CTRRatio.values(), linestyle = "--", label = 'UCB1_0.3SingleDay')
                #plt.plot(tim.values(), greedyCTRRatio.values(),linestyle = "--",  label = 'UCB1_0.3MultipleDay')
                plt.xlabel('MultipleDay')
                plt.ylabel('CTR-Ratio')
                
    for x in filenamesExp3Greedy:
        filename = os.path.join(save_addressExp3Greedy, x)
        if 'Multiple'in x:
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
                extremeGreedyCTRRatio = {}
                tim = {}
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i],exp3a[i],exp3c[i], ucb1a[i], ucb1c[i], greedya[i], greedyc[i], exp3CTRRatio[i], ucb1CTRRatio[i], greedyCTRRatio[i], extremeGreedyCTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1]) 
                #plt.plot(tim.values(),exp3CTRRatio.values(), linestyle = ":", label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1CTRRatio.values(), linestyle = ":",  label = 'UCB1_0.3SingleDay')
                #plt.plot(tim.values(), greedyCTRRatio.values(), linestyle = "--")
                #plt.plot(tim.values(), extremeGreedyCTRRatio.values(), label = 'MultipleDay')
                plt.xlabel('Multiple_gamma0.3_Queue50')
                plt.ylabel('CTR-Ratio')
    
    for x in filenamesDebugUCB1:
        filename = os.path.join(save_addressDebugUCB1, x)
        if 'Multiple'in x:
            with open(filename, 'r')as f:
                randa = {}
                randc = {}
                ucb1a = {}
                ucb1c = {}
                ucb1CTRRatio = {}
                ucb1_1CTRRatio = {}
                ucb1AlphaCTRRatio = {}
                tim = {}
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i], ucb1a[i], ucb1c[i], ucb1CTRRatio[i], ucb1_1CTRRatio[i],ucb1AlphaCTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1]) 
                #plt.plot(tim.values(),ucb1CTRRatio.values(), label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1_1CTRRatio.values(), label = 'UCB1_0.3SingleDay')
                #plt.plot(tim.values(), ucb1AlphaCTRRatio.values(), 'o')
                plt.annotate('Exp3', xy=(1.24e+09, 1.04479), xytext=(1.242e+09, 0.94), arrowprops=dict(facecolor='black', shrink=0.05),)
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
                plt.title('Greedy_Multiple with AgeQueue20')
                plt.annotate('Exp3', xy=(1.24e+09, 1.04479), xytext=(1.242e+09, 0.94), arrowprops=dict(facecolor='black', shrink=0.05),)
                
                
        if 'Hour'in x:
            with open(filename, 'r')as f:
                randa = {}
                randc = {}
                ucb1a = {}
                ucb1c = {}
                ucb1CTRRatio = {}
                ucb1_1CTRRatio = {}
                ucb1AlphaCTRRatio = {}
                tim = {}
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i], ucb1a[i], ucb1c[i], ucb1CTRRatio[i], ucb1_1CTRRatio[i],ucb1AlphaCTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1]) 
                #plt.plot(tim.values(),ucb1CTRRatio.values(), linestyle = "--", label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1_1CTRRatio.values(), label = 'UCB1_0.3SingleDay')
                #plt.plot(tim.values(), ucb1AlphaCTRRatio.values(), 'o')
                plt.annotate('Exp3', xy=(1.24e+09, 1.04479), xytext=(1.242e+09, 0.94), arrowprops=dict(facecolor='black', shrink=0.05),)
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
                plt.title('UCB1 and UCB1 timedecay')
                plt.annotate('Exp3', xy=(1.24e+09, 1.04479), xytext=(1.242e+09, 0.94), arrowprops=dict(facecolor='black', shrink=0.05),)
                
                
    