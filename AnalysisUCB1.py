# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 13:05:41 2015

@author: Summer
"""


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
    filenamesDebugExp3 = [x for x in os.listdir(save_addressDebugExp3) if 'csv' in x]
    filenamesUCB1 = [x for x in os.listdir(save_addressUCB1) if 'csv' in x]  
    filenamesExp3Greedy = [x for x in os.listdir(save_addressExp3Greedy) if 'csv' in x]
    filenamesQueue = [x for x in os.listdir(save_addressQueue) if 'csv' in x]
    filenamesTimeDecay = [x for x in os.listdir(save_addressTimeDecay) if 'csv' in x]
    filenamesDebugUCB1 = [x for x in os.listdir(save_addressDebugUCB1) if 'csv' in x]
    filenamesModifiedAgeQueue = [x for x in os.listdir(save_addressModifiedAgeQueue) if 'csv' in x]
    filenamesModifiedAllAge = [x for x in os.listdir(save_addressModifiedAllAge) if 'csv' in x]
    filenamesMyQueue = [x for x in os.listdir(save_addressMyQueue) if 'csv' in x]
    filenamesModifiedUCB1 =  [x for x in os.listdir(save_addressModifiedUCB1) if 'csv' in x]
    
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
                #plt.plot(tim.values(),exp3CTRRatio.values(),label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'UCB1_0.3SingleDay')
                #plt.plot(tim.values(), greedyCTRRatio.values(), label = 'greedy_0.3MultipleDay')
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
           
    for x in filenamesTimeDecay:
        filename = os.path.join(save_addressTimeDecay, x)
        if '0.7Multiple' in x:
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
                plt.xlabel('Time')
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
                #plt.plot(tim.values(),ucb1CTRRatio.values(), label = 'UCB1_Mult')
                #plt.plot(tim.values(), ucb1_1CTRRatio.values(), label = 'UCB1_0.3SingleDay')
                #plt.plot(tim.values(), ucb1AlphaCTRRatio.values(), 'o')
                plt.annotate('Exp3', xy=(1.24e+09, 1.04479), xytext=(1.242e+09, 0.94), arrowprops=dict(facecolor='black', shrink=0.05),)
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
                plt.title('Greedy with TimeDecay0.99')
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
                
    for x in filenamesModifiedAllAge:
        filename = os.path.join(save_addressModifiedAllAge, x)
        if 'Modi'in x:
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
                #plt.plot(tim.values(), ucb1CTRRatio.values(), linestyle = "--",  label = 'UCB1_0.3SingleDay')
                #plt.plot(tim.values(), greedyCTRRatio.values(), linestyle = "--")
                #plt.plot(tim.values(), extremeGreedyCTRRatio.values(), label = 'MultipleDay')
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
    
    for x in filenamesModifiedAgeQueue:
        filename = os.path.join(save_addressModifiedAgeQueue, x)
        if 'Modified'in x:
            with open(filename, 'r')as f:
                randa = {}
                randc = {}
                exp3a = {}
                exp3c = {}
                exp3CTRRatio = {}
                tim = {}
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i],exp3a[i],exp3c[i], exp3CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])                
                #plt.plot(tim.values(),exp3CTRRatio.values(), linestyle = "--", label = 'Exp31_0.3SingleDay')
    
    
    for x in filenamesMyQueue:
        filename = os.path.join(save_addressMyQueue, x)
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
                    randa[i],randc[i],exp3a[i],exp3c[i], ucb1a[i], ucb1c[i], greedya[i], greedyc[i], exp3CTRRatio[i], ucb1CTRRatio[i], greedyCTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1]) 
                #plt.plot(tim.values(),exp3CTRRatio.values(), linestyle = "--", label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1CTRRatio.values(), linestyle = "--", label = 'UCB1_0.3SingleDay')
                #plt.plot(tim.values(), greedyCTRRatio.values(),  linestyle = "--")
                plt.annotate('Exp3', xy=(1.24e+09, 1.04479), xytext=(1.242e+09, 0.94), arrowprops=dict(facecolor='black', shrink=0.05),)
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
                plt.title('Start Exp3 at different time')
                plt.annotate('Exp3', xy=(1.24e+09, 1.04479), xytext=(1.242e+09, 0.94), arrowprops=dict(facecolor='black', shrink=0.05),)
    
    for x in filenamesDebugExp3:
        filename = os.path.join(save_addressDebugExp3, x)
        if 'Multip'in x:
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
    
    for x in filenamesModifiedUCB1:
        filename = os.path.join(save_addressModifiedUCB1, x)
        if 'Multi'in x:
            with open(filename, 'r')as f:
                randa = {}
                randc = {}
                ucb1a = {}
                ucb1c = {}
                ucb1CTRRatio = {}
                tim = {}
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i], ucb1a[i], ucb1c[i], ucb1CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1]) 
                print len(tim)
                print len(ucb1CTRRatio)
                #plt.plot(tim.values(),ucb1CTRRatio.values(), label = 'Exp31_0.3SingleDay')
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
                plt.title('Modified_UCB1')
                plt.annotate('Exp3', xy=(1.24e+09, 1.04479), xytext=(1.242e+09, 0.94), arrowprops=dict(facecolor='black', shrink=0.05),)
                
                
        if 'Hour'in x:
            with open(filename, 'r')as f:
                randa = {}
                randc = {}
                ucb1a = {}
                ucb1c = {}
                ucb1CTRRatio = {}
 
                tim = {}
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i], ucb1a[i], ucb1c[i], ucb1CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1]) 
                    print ucb1CTRRatio[i]
                #plt.plot(tim.values(),ucb1CTRRatio.values(), linestyle = "--", label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1_1CTRRatio.values(), label = 'UCB1_0.3SingleDay')
                #plt.plot(tim.values(), ucb1AlphaCTRRatio.values(), 'o')
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
                plt.title('Modified UCB1')
                plt.annotate('Exp3', xy=(1.24e+09, 1.04479), xytext=(1.242e+09, 0.94), arrowprops=dict(facecolor='black', shrink=0.05),)
                
#------------------------------Modified UCB1---------------------------------------------------------------    

#------Multiple------          
    randa = {}
    randc = {}
    ucb1a = {}
    tim = {}
    ucb1CTRRatio = {}
    i = -1
    for x in filenamesModifiedUCB1:
        filename = os.path.join(save_addressModifiedUCB1, x)        
        if 'Multi'in x:
            with open(filename, 'r')as f: 
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i], ucb1a[i], ucb1c[i], ucb1CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1]) 
                
    plt.plot(tim.values(),ucb1CTRRatio.values(), label = 'MultipleDays')
    plt.xlabel('Time')
    plt.ylabel('CTR-Ratio')
    #plt.legend()
    plt.title('Modified_UCB1')
#------------Single--------
    
    randa = {}
    randc = {}
    ucb1a = {}
    tim = {}
    ucb1CTRRatio = {}
    i = -1
    for x in filenamesModifiedUCB1:
        filename = os.path.join(save_addressModifiedUCB1, x)        
        if 'Single'in x:
            with open(filename, 'r')as f: 
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i], ucb1a[i], ucb1c[i], ucb1CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1]) 
                
    plt.plot(tim.values(),ucb1CTRRatio.values(), label = 'SingleDay')
    plt.xlabel('Time')
    plt.ylabel('CTR-Ratio')
    #plt.legend()
    plt.title('Modified_UCB1')


#------------Hour--------
      
    randa = {}
    randc = {}
    ucb1a = {}
    tim = {}
    ucb1CTRRatio = {}
    i = -1
    for x in filenamesModifiedUCB1:
        filename = os.path.join(save_addressModifiedUCB1, x)        
        if 'Hour' in x:
            with open(filename, 'r')as f: 
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i], randc[i], ucb1a[i], ucb1c[i], ucb1CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1]) 
                
    plt.plot(tim.values(),ucb1CTRRatio.values(), label = 'Hours')
    plt.xlabel('Time')
    plt.ylabel('CTR-Ratio')
    plt.legend(loc='lower right')
    plt.title('Modified_UCB1')


               
            

                