
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
                logCTR =[]
                logCTR2 = []
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
                    logCTR.append(words[2])
                    logCTR2.append(words[3])
                #plt.plot(tim, logCTR, label = "log")
                #plt.plot(tim, logCTR2, label = "log")
                plt.xlabel('CTR')
                plt.ylabel('Time')
                plt.legend()
                title('ArticleID: 109568')
        if 'Exp3CTR'in x:
            with open(filename, 'r')as f:
                print "plot"
                logCTR =[]
                logCTR2 = []
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
                    logCTR.append(words[2])
                    logCTR2.append(words[3])
                plt.plot(tim, logCTR, label = "Exp3")
                plt.plot(tim, logCTR2, label = "Exp3")
                plt.xlabel('CTR')
                plt.ylabel('Time')
                plt.legend()
                title('ArticleID: 109568')

        

