# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 13:29:42 2015

@author: Summer
"""



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
    filenamesCTROverall = [x for x in os.listdir(save_addressCTROverall) if 'csv' in x]
    
    for x in filenamesCTROverall:
        filename = os.path.join(save_addressCTROverall, x)
        if 'Single01'in x:
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
                gamma = [0.1,0.2,0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    AllResults= [float(x) for x in words[2].split(';')]
                    print AllResults[0:8]
                    tim[i] = int(words[1])
                plt.plot(gamma, AllResults[0:9],'o', label = 'Single01')
                #plt.plot(tim.values(),exp3CTRRatio.values(), linestyle = ":", label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'Hour')
                #plt.plot(tim.values(), greedyCTRRatio.values(), linestyle = ":", label = 'greedy_Hour')
                plt.legend()
                plt.xlabel('gamma')
                plt.ylabel('CTR-Ratio')
        
        if 'Single02'in x:
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
                gamma = [0.1,0.2,0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    AllResults= [float(x) for x in words[2].split(';')]
                    print AllResults[0:8]
                    tim[i] = int(words[1])
                plt.plot(gamma, AllResults[0:9], 'o', label = 'Single02')
                #plt.plot(tim.values(),exp3CTRRatio.values(), linestyle = ":", label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'Hour')
                #plt.plot(tim.values(), greedyCTRRatio.values(), linestyle = ":", label = 'greedy_Hour')
                plt.legend()
                plt.xlabel('gamma')
                plt.ylabel('CTR-Ratio')
        
        if 'Single03'in x:
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
                gamma = [0.1,0.2,0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    AllResults= [float(x) for x in words[2].split(';')]
                    print AllResults[0:8]
                    tim[i] = int(words[1])
                plt.plot(gamma, AllResults[0:9], 'o', label = 'Single03')
                #plt.plot(tim.values(),exp3CTRRatio.values(), linestyle = ":", label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'Hour')
                #plt.plot(tim.values(), greedyCTRRatio.values(), linestyle = ":", label = 'greedy_Hour')
                plt.legend()
                plt.xlabel('gamma')
                plt.ylabel('CTR-Ratio')
                
        
        
        if 'Single04'in x:
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
                gamma = [0.1,0.2,0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    AllResults= [float(x) for x in words[2].split(';')]
                    print AllResults[0:8]
                    tim[i] = int(words[1])
                plt.plot(gamma, AllResults[0:9], 'o', label = 'Single04')
                #plt.plot(tim.values(),exp3CTRRatio.values(), linestyle = ":", label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'Hour')
                #plt.plot(tim.values(), greedyCTRRatio.values(), linestyle = ":", label = 'greedy_Hour')
                plt.legend()
                plt.xlabel('gamma')
                plt.ylabel('CTR-Ratio')
                
        if 'Multiple10'in x:
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
                gamma = [0.1,0.2,0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    AllResults= [float(x) for x in words[2].split(';')]
                    print AllResults[0:8]
                    tim[i] = int(words[1])
                plt.plot(gamma, AllResults[0:9], label = 'Multiple10')
                #plt.plot(tim.values(),exp3CTRRatio.values(), linestyle = ":", label = 'Exp31_0.3SingleDay')
                #plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'Hour')
                #plt.plot(tim.values(), greedyCTRRatio.values(), linestyle = ":", label = 'greedy_Hour')
                plt.legend()
                plt.xlabel('gamma')
                plt.ylabel('CTR-Ratio')
                
    