
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
    print save_addressCTR

    filenamesCTR = [x for x in os.listdir(save_addressCTR) if 'csv' in x]

    for x in filenamesCTR:
        filename = os.path.join(save_addressCTR, x)
                
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
                
        if 'Exp3CTR_03'in x:
            print 'in'
            with open(filename, 'r')as f:
                print "plot"
                logCTR1 =[]
                logCTR2 = []
                logCTR3 = []
                logCTR4 = []
                
                logCTR5 = []
                logCTR6= []
                logCTR7 = []
                logCTR8 = []
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
                    
                    logCTR5.append(words[205])   # Article 109476  (2,3,4,5)
                    logCTR6.append(words[45])
                    logCTR7.append(words[46])
                    logCTR8.append(words[47])
                '''
                f, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(8, sharex = True, sharey = True)
                
                ax1.plot(tim, logCTR2 )
                ax1.set_title("Exp3_Hour_109524")             
                ax2.plot(tim, logCTR4)
                ax2.set_title('Exp3_Hour_109541')
                
                ax3.plot(tim, logCTR1)
                ax3.set_title('Exp3_Hour_109517')
                ax4.plot(tim, logCTR3)
                ax4.set_title('Exp3_Hour_109626')
                
                ax5.plot(tim, logCTR5 )
                ax5.set_title("Exp3_Hour_109476 ")             
                ax6.plot(tim, logCTR6)
                ax6.set_title('Exp3_Hour_109541')
                
                ax7.plot(tim, logCTR7)
                ax7.set_title('Exp3_Hour_109517')
                ax8.plot(tim, logCTR8)
                ax8.set_title('Exp3_Hour_109626')
                #plt.plot(time1, cc)
                plt.xlabel('time')
                plt.ylabel('CTR')
                plt.legend()
                '''
                
        if 'UCB1CTR_Multi'in x:
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
                plt.plot(tim, logCTR1, label = "UCB1_Hour_109517")
                plt.plot(tim, logCTR3, linestyle = ':', label = "UCB1_Hour_109626")
                plt.plot(tim, logCTR2, label = "UCB1_Hour_109524")
                plt.plot(tim, logCTR4, label = "UCB1_Hour_109541")
                plt.xlabel('Time')
                plt.ylabel('CTR')
                plt.legend()
                #title('ArticleID: 109568')
                '''
#==========================Show All the Long Lasting Articles' CTR =======================
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
                
        if 'Exp3CTR_03'in x:
            print 'in'
            with open(filename, 'r')as f:
                print "plot"
                logCTR1 =[]
                logCTR2 = []
                logCTR3 = []
                logCTR4 = []
                logCTR5 = []
                logCTR6= []
               

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
                    logCTR1.append(words[243])
                    logCTR2.append(words[231])
                    logCTR3.append(words[205])
                    logCTR4.append(words[67])                    
                    logCTR5.append(words[94])   # Article 109476  (2,3,4,5)
                    logCTR6.append(words[122])
                '''

              
                f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, sharex = True, sharey = True)
                
                ax1.plot(tim, logCTR1 )
                ax1.set_title("Exp3_109536")             
                ax2.plot(tim, logCTR2)
                ax2.set_title('Exp3_109524')
                
                ax3.plot(tim, logCTR3)
                ax3.set_title('Exp3_109476')
                ax4.plot(tim, logCTR4)
                ax4.set_title('Exp3_109635')
                
                ax5.plot(tim, logCTR5 )
                ax5.set_title("Exp3_109667 ")             
                ax6.plot(tim, logCTR6)
                ax6.set_title('Exp3_109697')
                
                plt.xlabel('time')
                plt.ylabel('CTR')
                plt.legend()
                '''
                
                
                
        if 'UCB1CTR_Multi'in x:
            with open(filename, 'r')as f:
                print "plot"
                logCTR1 =[]
                logCTR2 = []
                logCTR3 = []
                logCTR4 = []
                logCTR5=[]
                logCTR6 = []
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
                    logCTR1.append(words[243])
                    logCTR2.append(words[231])
                    logCTR3.append(words[205])
                    logCTR4.append(words[67])                    
                    logCTR5.append(words[94])   # Article 109476  (2,3,4,5)
                    logCTR6.append(words[122])
                '''
              
                f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, sharex = True, sharey = True)
                
                ax1.plot(tim, logCTR1 )
                ax1.set_title("UCB1_109536")             
                ax2.plot(tim, logCTR2)
                ax2.set_title('UCB1_109524')
                
                ax3.plot(tim, logCTR3)
                ax3.set_title('UCB1_109476')
                ax4.plot(tim, logCTR4)
                ax4.set_title('UCB1_109635')
                
                ax5.plot(tim, logCTR5 )
                ax5.set_title("UCB1_109667 ")             
                ax6.plot(tim, logCTR6)
                ax6.set_title('UCB1_109697')
                
                plt.xlabel('time')
                plt.ylabel('CTR')
                plt.legend()
                '''
        
#===============================Test All the others=================================

        if 'Exp3CTR_03'in x:
            print 'in'
            with open(filename, 'r')as f:
                print "plot"
                logCTR1 =[]
                logCTR2 = []
                logCTR3 = []
                logCTR4 = []
                logCTR5 = []
                logCTR6= []
               

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
                    logCTR1.append(words[273])
                    logCTR2.append(words[274])
                    logCTR3.append(words[275])
                    logCTR4.append(words[276])                    
                    logCTR5.append(words[277])   # Article 109476  (2,3,4,5)
                    logCTR6.append(words[278])
                

              
                f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, sharex = True, sharey = True)
                
                ax1.plot(tim, logCTR1 )
                ax1.set_title("Exp3_109536")             
                ax2.plot(tim, logCTR2)
                ax2.set_title('Exp3_109524')
                
                ax3.plot(tim, logCTR3)
                ax3.set_title('Exp3_109476')
                ax4.plot(tim, logCTR4)
                ax4.set_title('Exp3_109635')
                
                ax5.plot(tim, logCTR5 )
                ax5.set_title("Exp3_109667 ")             
                ax6.plot(tim, logCTR6)
                ax6.set_title('Exp3_109697')
                
                plt.xlabel('time')
                plt.ylabel('CTR')
                plt.legend()
                