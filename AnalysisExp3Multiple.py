import numpy as np
import os
from conf import *
from matplotlib.pylab import *
from operator import itemgetter

if __name__ == '__main__':
    filenames = [x for x in os.listdir(save_address) if 'csv' in x]
    for x in filenames:
        filename = os.path.join(save_address, x)
        if '0.3_MultipleDay'in x:
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
                plt.plot(tim.values(),exp3CTRRatio.values(),label = '0.3MultipleDay')
<<<<<<< HEAD

        if '0.7_MultipleDay'in x:
=======
        
        if '0.5_MultipleDay'in x:
>>>>>>> daa48e6f139dcdf215c4be0164ec45c09cd57f9f
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
                plt.plot(tim.values(),exp3CTRRatio.values(),label = '0.5MultipleDay')
        
        if '0.7_MultipleDay'in x:
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
                plt.plot(tim.values(),exp3CTRRatio.values(),label = '0.7_MultipleDay') 
<<<<<<< HEAD
        
=======
        '''
>>>>>>> daa48e6f139dcdf215c4be0164ec45c09cd57f9f
        if '1_MultipleDay'in x:
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
                plt.plot(tim.values(),exp3CTRRatio.values(),label = '1_MultipleDay')
        
<<<<<<< HEAD
        
=======
        '''
>>>>>>> daa48e6f139dcdf215c4be0164ec45c09cd57f9f
        '''
                
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
                plt.plot(tim.values(),exp3CTRRatio.values(),label = '0.5Single') 
        
        
  
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
                plt.plot(tim.values(),exp3CTRRatio.values(),label = '0.5Single')  
        '''
        
