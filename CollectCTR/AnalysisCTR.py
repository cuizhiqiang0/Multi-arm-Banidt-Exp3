
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

    filenamesCTR = [x for x in os.listdir(save_addressCTR) if 'csv' in x]

    for x in filenamesCTR:
        filename = os.path.join(save_addressCTR, x)
        print filename
        '''
        if 'LogCTR'in x:
            with open(filename, 'r')as f:
                print "plot"
                logCTR =[]
                tim = []
                i = -1
                for line in f:
                    i = i+1
                    if i> 2:
                        #print line
                        words = line.split(',')
                        #print words 
                        tim.append(words[0])
                        #print words[0]
                        #print words[1]
                        logCTR.append(words[1])
                plt.plot(tim, logCTR, label = "log")
                plt.xlabel('CTR')
                plt.ylabel('Time')
                plt.legend()
                title('ArticleID: 109568')
        
        if 'Exp3CTR'in x:
            with open(filename, 'r')as f:
                print "plot"
                logCTR =[]
                tim = []
                i = -1
                for line in f:
                    i = i+1
                    if i> 2:
                        #print line
                        words = line.split(',')
                        #print words 
                        tim.append(words[0])
                        #print words[0]
                        #print words[1]
                        logCTR.append(words[1])
                plt.plot(tim, logCTR, label = "Exp3")
                plt.legend()
        
        if 'LogCTR'in x:
            with open(filename, 'r')as f:
                print "plot"
                logCTR =[]
                tim = []
                i = -1
                for line in f:
                    i = i+1
                    if i> 2:
                        #print line
                        words = line.split(',')
                        if float(words[1])>=0:
                            #print words 
                            tim.append(words[0])
                            #print words[0]
                            #print words[1]
                            logCTR.append(words[1])
                plt.plot(tim, logCTR, label = "log")
                plt.xlabel('CTR')
                plt.ylabel('Time')
                plt.legend()
                title('ArticleID: 109568')
        
        if 'Exp3CTR'in x:
            with open(filename, 'r')as f:
                print "plot"
                logCTR =[]
                tim = []
                i = -1
                for line in f:
                    i = i+1
                    if i> 2:
                        #print line
                        words = line.split(',')
                        if float(words[1]) >= 0:
                            #print words 
                            tim.append(words[0])
                            #print words[0]
                            #print words[1]
                            logCTR.append(words[1])
                plt.plot(tim, logCTR, label = "Exp3")
                plt.legend()
        '''
                
        if 'LogCTR'in x:
            with open(filename, 'r')as f:
                print "plot"
                logCTR1 =[]
                logCTR2 = []
                logCTR3 = []
                logCTR4 = []
                tim = []
                i = -1
                for line in f:
                    i = i+1
                    words = line.split(',')
                    if words[0].strip() != 'data':
                        continue
                    tim.append(words[1])
                    #print words[0]
                    #print words[1]
                    logCTR1.append(words[224])
                    logCTR2.append(words[231])
                    logCTR3.append(words[58])
                    logCTR4.append(words[247])
                
                '''    
                plt.plot(tim, logCTR1, label = "Log_109517")
                plt.plot(tim, logCTR3, label = "Log_109626")
                plt.plot(tim, logCTR2, label = "Log_109524")
                plt.plot(tim, logCTR4, label = "Log_109541")
                plt.xlabel('Time')
                plt.ylabel('CTR')
                plt.legend()
                #title('ArticleID: 109568')
                '''
                
        if 'Exp3CTR'in x:
            with open(filename, 'r')as f:
                print "plot"
                logCTR1 =[]
                logCTR2 = []
                logCTR3 = []
                logCTR4 = []
                tim = []
                i = -1
                for line in f:
                    i = i+1
                    words = line.split(',')
                    if words[0].strip() != 'data':
                        continue
                    tim.append(words[1])
                    #print words[0]
                    #print words[1]
                    logCTR1.append(words[224])
                    logCTR2.append(words[231])
                    logCTR3.append(words[58])
                    logCTR4.append(words[247])
                '''
                plt.plot(tim, logCTR1, label = "Exp3_109517")
                plt.plot(tim, logCTR3, linestyle = ':', label = "Exp3_109626")
                plt.plot(tim, logCTR2, label = "Exp3_109524")
                plt.plot(tim, logCTR4,  linestyle = ':',label = "Exp3_109541")
                plt.xlabel('time')
                plt.ylabel('CTR')
                plt.legend()
                #title('ArticleID: 109568')
                '''
                
        if 'UCB1CTR'in x:
            with open(filename, 'r')as f:
                print "plot"
                logCTR1 =[]
                logCTR2 = []
                logCTR3 = []
                logCTR4 = []
                tim = []
                i = -1
                for line in f:
                    i = i+1
                    words = line.split(',')
                    if words[0].strip() != 'data':
                        continue
                    tim.append(words[1])
                    #print words[0]
                    #print words[1]
                    logCTR1.append(words[224])
                    logCTR2.append(words[231])
                    logCTR3.append(words[58])
                    logCTR4.append(words[247])
                
                    
                plt.plot(tim, logCTR1, label = "UCB1_109517")
                plt.plot(tim, logCTR3, linestyle = ':', label = "UCB1_109626")
                plt.plot(tim, logCTR2, label = "UCB1_109524")
                plt.plot(tim, logCTR4, label = "UCB1_109541")
                plt.xlabel('Time')
                plt.ylabel('CTR')
                plt.legend()
                #title('ArticleID: 109568')
                
        

