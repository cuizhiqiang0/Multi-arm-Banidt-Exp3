import numpy as np
import os
from conf import *
from matplotlib.pylab import *
from operator import itemgetter

if __name__ == '__main__':
    
    filenames = [x for x in os.listdir(save_address) if '.csv' in x]
    '''
    articlesSingle = {}
    articlesMultiple = {}
    articlesHours = {}
    '''
    for x in filenames:
        print x
        filename = os.path.join(save_address, x)
        if 'Multiple' in x:
            with open(filename, 'r') as f:
                ucba = {}
                ucbc = {}
                randa = {}
                randc = {}
                greedya = {}
                greedyc = {}
                exp3a = {}
                exp3c = {}
                ucbCTR = {}
                randCTR = {}
                greedyCTR = {}
                exp3CTR = {}
                ucbCTRRatio = {}
                greedyCTRRatio = {}
                exp3CTRRatio={}
                tim = {}
                i = -1  
                for line in f:
                    i = i + 1
                    words = line.split(',')
                    if words[0].strip() != 'data':
                        continue
                    ucba[i], ucbc[i], randa[i], randc[i], greedya[i], greedyc[i], exp3a[i], exp3c[i]= [float(x) for x in words[2].split(';')]
                    '''
                    
                    if ucba[i] == 0 or rand[i] ==0 or greedya[i] ==0 or exp3a[i] == 0:
                        continue
                    '''
                    tim[i] = int(words[1])
                    randCTR[i]= randc[i]/randa[i]
                    ucbCTR[i] = ucbc[i]/ucba[i]
                    greedyCTR[i] = greedyc[i]/greedya[i]
                    exp3CTR[i] = exp3c[i]/exp3a[i]
                    
                    ucbCTRRatio[i] = ucbCTR[i] / randCTR[i]
                    greedyCTRRatio[i] = greedyCTR[i] / randCTR[i]
                    exp3CTRRatio[i] = exp3CTR[i] / randCTR[i]
            
                plt.plot(tim.values(), ucbCTRRatio.values(), label = 'ucbCTR Ratio')
                plt.plot(tim.values(), greedyCTRRatio.values(),  label = 'greedyCTR Ratio')
                plt.plot(tim.values(), exp3CTRRatio.values(),  label = 'greedyCTR Ratio')
            