import numpy as np
import os
from conf import *
from matplotlib.pylab import *
from operator import itemgetter

if __name__ == '__main__':
    filenamesExp3 = [x for x in os.listdir(save_addressExp3) if 'csv' in x]
    filenamesUCB1 = [x for x in os.listdir(save_addressUCB1) if 'csv' in x]
    
    for x in filenamesExp3:
        filename = os.path.join(save_addressExp3, x)

        if '0.3_Single'in x:
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
                    randa[i],randc[i],exp3a[i],exp3c[i],exp3CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])

                plt.plot(tim.values(),exp3CTRRatio.values(), linestyle = '--', label = '0.3Single')
                #plt.legend(loc='best')
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
                
        if '0.5_Single'in x:
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
                    randa[i],randc[i],exp3a[i],exp3c[i],exp3CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])
                plt.plot(tim.values(),exp3CTRRatio.values(),linestyle = ':', label = '0.5Single')
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
        
        if '0.3_Multiple'in x:
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
                    randa[i],randc[i],exp3a[i],exp3c[i],exp3CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])
                plt.plot(tim.values(),exp3CTRRatio.values(),label = '0.5Multiple')
        
        if '0.5_Multiple'in x:
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
                    randa[i],randc[i],exp3a[i],exp3c[i],exp3CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])
                plt.plot(tim.values(),exp3CTRRatio.values(),label = '0.5Multiple')                


    
    
    
    '''
    for x in filenamesUCB1:
        filename = os.path.join(save_addressUCB1, x)
        if 'UCB10.3_SingleDay'in x:
            with open(filename, 'r')as f:
                randa = {}
                randc = {}
                exp3a = {}
                exp3c = {}
                ucb1a = {}
                ucb1c = {}
                exp3CTRRatio = {}
                ucb1CTRRatio = {}
                tim = {}
                i = -1
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip()!='data':
                        continue
                    randa[i],randc[i],exp3a[i],exp3c[i], ucb1a[i], ucb1c[i], exp3CTRRatio[i], ucb1CTRRatio[i]= [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])
                #plt.plot(tim.values(),exp3CTRRatio.values(), marker = '+', label = 'Exp31_0.3SingleDay')
                plt.plot(tim.values(), ucb1CTRRatio.values(), label = 'UCB1_0.3SingleDay')
                #plt.legend(loc = 'best')
                plt.xlabel('Time')
                plt.ylabel('CTR-Ratio')
     
        if '0.7_Single'in x:
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
                    randa[i],randc[i],exp3a[i],exp3c[i],exp3CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])
                plt.plot(tim.values(),exp3CTRRatio.values(),label = '0.7_Single') 
    

        if '0.5_Hour'in x:
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
                    randa[i],randc[i],exp3a[i],exp3c[i],exp3CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])
                plt.plot(tim.values(),exp3CTRRatio.values(),label = '0.5Hour')   
        
        
        
        if '0.5_Multiple'in x:
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
                    randa[i],randc[i],exp3a[i],exp3c[i],exp3CTRRatio[i] = [float(x) for x in words[2].split(';')]
                    tim[i] = int(words[1])
                plt.plot(tim.values(),exp3CTRRatio.values(),label = '0.5Multiple')                

        '''
        

