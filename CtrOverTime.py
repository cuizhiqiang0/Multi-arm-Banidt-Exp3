# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 23:30:57 2015

@author: Summer
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 15:12:00 2015

@author: Summer
"""

from conf import *
import time
import re
from random import random, choice
from operator import itemgetter
import datetime
import numpy as np
import math
import random

class articleAccess():
    def __init__(self):
        self.accesses = 0.0
        self.clicks = 0.0
        self.CTR = 0.0
    def updateCTR(self):
        try:
            self.CTR = self.clicks / self.accesses
        except ZeroDivisionError:
            return self.CTR


# this structure saves for the exp3 algorithm
class exp3Struct:
    def __init__(self):
        self.weights = 1.0
        self.pta = 0.0
        self.learn_stats = articleAccess()
        
    def reInitilize(self):
        self.weights = 1.0
        self.pta=0.0
          
    def updatePta(self, gamma, n_arms, total_weight):
        n_arms = n_arms
        self.pta= (1-gamma) * (self.weights / total_weight)
        self.pta= self.pta + (gamma) * (1.0 / float(n_arms))
 
    def updateWeight(self, gamma, n_arms, reward):
        n_arms = n_arms
        X=reward/self.pta
        growth_factor = math.exp((gamma/n_arms)*X)
        self.weights = self.weights * growth_factor

            
class greedyStruct:
    def __init__(self):
        self.learn_stats = articleAccess()
        self.deploy_stats = articleAccess()
        self.totalReward = 0.0
        self.numPlayed = 0.0
        self.averageReward = 0.0

    def reInitilize(self):
        self.totalReward = 0.0
        self.numPlayed = 0.0
        self.averageReward = 0.0

    def updateReward(self):
        try:
            self.averageReward = self.totalReward / self.numPlayed
        except ZeroDivisionError:
            self.averageReward = 0.0
        

# structure to save data from random strategy as mentioned in LiHongs paper
class randomStruct:
	def __init__(self):
		self.learn_stats = articleAccess()
		#self.deploy_stats = articleAccess()

# This code simply reads one line from the source files of Yahoo!. Please see the yahoo info file to understand the format. I tested this part; so should be good but second pair of eyes could help
def parseLine(line):
	line = line.split("|")

	tim, articleID, click = line[0].strip().split(" ")
	tim, articleID, click = int(tim), int(articleID), int(click)
 
	pool_articles = [l.strip().split(" ") for l in line[2:]]
	pool_articles = np.array([[int(l[0])] + [float(x.split(':')[1]) for x in l[1:]] for l in pool_articles])
	return tim, articleID, click, pool_articles
	# returns time, id of selected article, if clicked i.e. the response, 

# this code saves different parameters in the file for one batch; this code is written to meet special needs since we need to see statistics as they evolve; I record accumulative stats from which batch stats can be extracted easily
# dicts: is a dictionary of articles UCB structures indexed by 'article-id' key. to reference an article we do dicts[article-id]
# recored_stats: are interesting statistics we want to save; i save accesses and clicks for UCB, random and greedy strategy for all articles in this batch
# epochArticles: are articles that were availabe to be chosen in this epoch or interval or batch.
# epochSelectedArticles: are articles that were selected by any algorithm in this batch.
# tim: is time of the last observation in the batch
def save_to_file(fileNameWrite, recordedStats, tim):
	with open(fileNameWrite, 'a+') as f:
		f.write('data') # the observation line starts with data;
		f.write(',' + str(tim))
		f.write(',' + ';'.join([str(x) for x in recordedStats]))
		f.write('\n')

# this code counts the line in a file; we need to divide data if we are re-setting theta multiple times a day. Could have been done based on time; i guess little harder to implement
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
if __name__ == '__main__':
    def printWrite():
        randomLA = sum([articles_random[x].learn_stats.accesses for x in articles_random])
        randomC = sum([articles_random[x].learn_stats.clicks for x in articles_random]) 
        randomCTR = sum([articles_random[x].learn_stats.clicks for x in articles_random]) / sum([articles_random[x].learn_stats.accesses for x in articles_random])
        
        exp3LA_1 = sum([articles_exp3_1[x].learn_stats.accesses for x in articles_exp3_1])
        exp3C_1 = sum([articles_exp3_1[x].learn_stats.clicks for x in articles_exp3_1]) 
        exp3CTR_1 = sum([articles_exp3_1[x].learn_stats.clicks for x in articles_exp3_1]) / sum([articles_exp3_1[x].learn_stats.accesses for x in articles_exp3_1])
        
        exp3LA_2 = sum([articles_exp3_2[x].learn_stats.accesses for x in articles_exp3_2])
        exp3C_2 = sum([articles_exp3_2[x].learn_stats.clicks for x in articles_exp3_2]) 
        exp3CTR_2 = sum([articles_exp3_2[x].learn_stats.clicks for x in articles_exp3_2]) / sum([articles_exp3_2[x].learn_stats.accesses for x in articles_exp3_2])
        
        exp3LA_3 = sum([articles_exp3_3[x].learn_stats.accesses for x in articles_exp3_3])
        exp3C_3 = sum([articles_exp3_3[x].learn_stats.clicks for x in articles_exp3_3]) 
        exp3CTR_3 = sum([articles_exp3_3[x].learn_stats.clicks for x in articles_exp3_3]) / sum([articles_exp3_3[x].learn_stats.accesses for x in articles_exp3_3])
        
        exp3LA_4 = sum([articles_exp3_4[x].learn_stats.accesses for x in articles_exp3_4])
        exp3C_4 = sum([articles_exp3_4[x].learn_stats.clicks for x in articles_exp3_4]) 
        exp3CTR_4 = sum([articles_exp3_4[x].learn_stats.clicks for x in articles_exp3_4]) / sum([articles_exp3_4[x].learn_stats.accesses for x in articles_exp3_4])
        
        exp3LA_5 = sum([articles_exp3_5[x].learn_stats.accesses for x in articles_exp3_5])
        exp3C_5 = sum([articles_exp3_5[x].learn_stats.clicks for x in articles_exp3_5]) 
        exp3CTR_5 = sum([articles_exp3_5[x].learn_stats.clicks for x in articles_exp3_5]) / sum([articles_exp3_5[x].learn_stats.accesses for x in articles_exp3_5])
        
        exp3LA_6 = sum([articles_exp3_6[x].learn_stats.accesses for x in articles_exp3_6])
        exp3C_6 = sum([articles_exp3_6[x].learn_stats.clicks for x in articles_exp3_6]) 
        exp3CTR_6 = sum([articles_exp3_7[x].learn_stats.clicks for x in articles_exp3_6]) / sum([articles_exp3_6[x].learn_stats.accesses for x in articles_exp3_6])
        
        exp3LA_7 = sum([articles_exp3_7[x].learn_stats.accesses for x in articles_exp3_7])
        exp3C_7 = sum([articles_exp3_7[x].learn_stats.clicks for x in articles_exp3_7]) 
        exp3CTR_7 = sum([articles_exp3_7[x].learn_stats.clicks for x in articles_exp3_7]) / sum([articles_exp3_7[x].learn_stats.accesses for x in articles_exp3_7])
        
        exp3LA_8 = sum([articles_exp3_8[x].learn_stats.accesses for x in articles_exp3_8])
        exp3C_8 = sum([articles_exp3_8[x].learn_stats.clicks for x in articles_exp3_8]) 
        exp3CTR_8 = sum([articles_exp3_8[x].learn_stats.clicks for x in articles_exp3_8]) / sum([articles_exp3_8[x].learn_stats.accesses for x in articles_exp3_8])
        
        exp3LA_9 = sum([articles_exp3_9[x].learn_stats.accesses for x in articles_exp3_9])
        exp3C_9 = sum([articles_exp3_9[x].learn_stats.clicks for x in articles_exp3_9]) 
        exp3CTR_9 = sum([articles_exp3_9[x].learn_stats.clicks for x in articles_exp3_9]) / sum([articles_exp3_9[x].learn_stats.accesses for x in articles_exp3_9])
               
        greedyLA_1 = sum([articles_greedy_1[x].learn_stats.accesses for x in articles_greedy_1])
        greedyC_1 = sum([articles_greedy_1[x].learn_stats.clicks for x in articles_greedy_1])
        greedyCTR_1 = sum([articles_greedy_1[x].learn_stats.clicks for x in articles_greedy_1]) / sum([articles_greedy_1[x].learn_stats.accesses for x in articles_greedy_1])
        
        greedyLA_2 = sum([articles_greedy_2[x].learn_stats.accesses for x in articles_greedy_2])
        greedyC_2 = sum([articles_greedy_2[x].learn_stats.clicks for x in articles_greedy_2])
        greedyCTR_2 = sum([articles_greedy_2[x].learn_stats.clicks for x in articles_greedy_2]) / sum([articles_greedy_2[x].learn_stats.accesses for x in articles_greedy_2])
        
        greedyLA_3 = sum([articles_greedy_3[x].learn_stats.accesses for x in articles_greedy_3])
        greedyC_3 = sum([articles_greedy_3[x].learn_stats.clicks for x in articles_greedy_3])
        greedyCTR_3 = sum([articles_greedy_3[x].learn_stats.clicks for x in articles_greedy_3]) / sum([articles_greedy_3[x].learn_stats.accesses for x in articles_greedy_3])
        
        greedyLA_4 = sum([articles_greedy_4[x].learn_stats.accesses for x in articles_greedy_4])
        greedyC_4 = sum([articles_greedy_4[x].learn_stats.clicks for x in articles_greedy_4])
        greedyCTR_4 = sum([articles_greedy_4[x].learn_stats.clicks for x in articles_greedy_4]) / sum([articles_greedy_4[x].learn_stats.accesses for x in articles_greedy_4])
        
        greedyLA_5 = sum([articles_greedy_5[x].learn_stats.accesses for x in articles_greedy_5])
        greedyC_5 = sum([articles_greedy_5[x].learn_stats.clicks for x in articles_greedy_5])
        greedyCTR_5 = sum([articles_greedy_5[x].learn_stats.clicks for x in articles_greedy_5]) / sum([articles_greedy_5[x].learn_stats.accesses for x in articles_greedy_5])
        
        greedyLA_6 = sum([articles_greedy_6[x].learn_stats.accesses for x in articles_greedy_6])
        greedyC_6 = sum([articles_greedy_6[x].learn_stats.clicks for x in articles_greedy_6])
        greedyCTR_6 = sum([articles_greedy_6[x].learn_stats.clicks for x in articles_greedy_6]) / sum([articles_greedy_6[x].learn_stats.accesses for x in articles_greedy_6])
        
        greedyLA_7 = sum([articles_greedy_7[x].learn_stats.accesses for x in articles_greedy_7])
        greedyC_7 = sum([articles_greedy_7[x].learn_stats.clicks for x in articles_greedy_7])
        greedyCTR_7 = sum([articles_greedy_7[x].learn_stats.clicks for x in articles_greedy_7]) / sum([articles_greedy_7[x].learn_stats.accesses for x in articles_greedy_7])
        
        greedyLA_8 = sum([articles_greedy_8[x].learn_stats.accesses for x in articles_greedy_8])
        greedyC_8 = sum([articles_greedy_8[x].learn_stats.clicks for x in articles_greedy_8])
        greedyCTR_8 = sum([articles_greedy_8[x].learn_stats.clicks for x in articles_greedy_8]) / sum([articles_greedy_8[x].learn_stats.accesses for x in articles_greedy_8])
        
        greedyLA_9 = sum([articles_greedy_9[x].learn_stats.accesses for x in articles_greedy_9])
        greedyC_9 = sum([articles_greedy_9[x].learn_stats.clicks for x in articles_greedy_9])
        greedyCTR_9 = sum([articles_greedy_9[x].learn_stats.clicks for x in articles_greedy_9]) / sum([articles_greedy_9[x].learn_stats.accesses for x in articles_greedy_9])
        
        print totalArticles,
        print 'Exp3Lrn_1', exp3CTR_1 / randomCTR,
        print 'Exp3Lrn_2', exp3CTR_2 / randomCTR,
        print 'Exp3Lrn_3', exp3CTR_3 / randomCTR,
        print 'Exp3Lrn_4', exp3CTR_4 / randomCTR,
        print 'Exp3Lrn_5', exp3CTR_5 / randomCTR,
        print 'Exp3Lrn_6', exp3CTR_6 / randomCTR,
        print 'Exp3Lrn_7', exp3CTR_7 / randomCTR,
        print 'Exp3Lrn_8', exp3CTR_8 / randomCTR,
        print 'Exp3Lrn_9', exp3CTR_9 / randomCTR,
        #print 'Greedy', greedyCTR_1 / randomCTR,

        print ' '
        
        recordedStats = [exp3CTR_1 / randomCTR, exp3CTR_2 / randomCTR, exp3CTR_3 / randomCTR, exp3CTR_4 / randomCTR, exp3CTR_5 / randomCTR, exp3CTR_6 / randomCTR, exp3CTR_7 / randomCTR, exp3CTR_8 / randomCTR, exp3CTR_9 / randomCTR,  greedyCTR_1 / randomCTR, greedyCTR_2 / randomCTR, greedyCTR_3 / randomCTR, greedyCTR_4 / randomCTR, greedyCTR_5 / randomCTR, greedyCTR_6 / randomCTR, greedyCTR_7 / randomCTR, greedyCTR_8 / randomCTR, greedyCTR_9 / randomCTR ]
        # write to file
        save_to_file(fileNameWrite, recordedStats,tim)
    
            
    # this function reset weight for all exp3
    def re_initialize_article_exp3Structs():
        for x in articles_exp3_1:
            articles_exp3_1[x].reInitilize()
            
        for x in articles_exp3_2:
            articles_exp3_2[x].reInitilize()
            
        for x in articles_exp3_3:
            articles_exp3_3[x].reInitilize()
            
        for x in articles_exp3_4:
            articles_exp3_4[x].reInitilize()
            
        for x in articles_exp3_5:
            articles_exp3_5[x].reInitilize()
            
        for x in articles_exp3_6:
            articles_exp3_6[x].reInitilize()
            
        for x in articles_exp3_7:
            articles_exp3_7[x].reInitilize()
            
        for x in articles_exp3_8:
            articles_exp3_8[x].reInitilize()
            
        for x in articles_exp3_9:
            articles_exp3_9[x].reInitilize()
    
    
    def re_initialize_article_greedyStructs():
        for x in articles_greedy_1:
            articles_greedy_1[x].reInitilize()
            
        for x in articles_greedy_2:
            articles_greedy_2[x].reInitilize()
            
        for x in articles_greedy_3:
            articles_greedy_3[x].reInitilize()
            
        for x in articles_greedy_4:
            articles_greedy_4[x].reInitilize()
            
        for x in articles_greedy_5:
            articles_greedy_5[x].reInitilize()
            
        for x in articles_greedy_6:
            articles_greedy_6[x].reInitilize()
            
        for x in articles_greedy_7:
            articles_greedy_7[x].reInitilize()
            
        for x in articles_greedy_8:
            articles_greedy_8[x].reInitilize()
            
        for x in articles_greedy_9:
            articles_greedy_9[x].reInitilize()
    
    def categorical_draw_1(articles):
        z = random.random()
        cum_pta = 0.0
        #a = range(9)
        #flag = 0
        for x in articles:
            cum_pta = cum_pta + articles_exp3_1[x].pta
            if cum_pta > z:
                return x
    def categorical_draw_2(articles):
        z = random.random()
        cum_pta = 0.0
        #a = range(9)
        #flag = 0
        for x in articles:
            cum_pta = cum_pta + articles_exp3_2[x].pta
            if cum_pta > z:
                return x
    
    def categorical_draw_3(articles):
        z = random.random()
        cum_pta = 0.0
        #a = range(9)
        #flag = 0
        for x in articles:
            cum_pta = cum_pta + articles_exp3_3[x].pta
            if cum_pta > z:
                return x
                
    def categorical_draw_4(articles):
        z = random.random()
        cum_pta = 0.0
        #a = range(9)
        #flag = 0
        for x in articles:
            cum_pta = cum_pta + articles_exp3_1[x].pta
            if cum_pta > z:
                return x
    
    def categorical_draw_5(articles):
        z = random.random()
        cum_pta = 0.0
        #a = range(9)
        #flag = 0
        for x in articles:
            cum_pta = cum_pta + articles_exp3_5[x].pta
            if cum_pta > z:
                return x
    
    def categorical_draw_6(articles):
        z = random.random()
        cum_pta = 0.0
        #a = range(9)
        #flag = 0
        for x in articles:
            cum_pta = cum_pta + articles_exp3_6[x].pta
            if cum_pta > z:
                return x
    
    def categorical_draw_7(articles):
        z = random.random()
        cum_pta = 0.0
        #a = range(9)
        #flag = 0
        for x in articles:
            cum_pta = cum_pta + articles_exp3_7[x].pta
            if cum_pta > z:
                return x   
    
    def categorical_draw_8(articles):
        z = random.random()
        cum_pta = 0.0
        #a = range(9)
        #flag = 0
        for x in articles:
            cum_pta = cum_pta + articles_exp3_8[x].pta
            if cum_pta > z:
                return x
    
    def categorical_draw_9(articles):
        z = random.random()
        cum_pta = 0.0
        #a = range(9)
        #flag = 0
        for x in articles:
            cum_pta = cum_pta + articles_exp3_9[x].pta
            if cum_pta > z:
                return x
        
        
    def greedySelectArm_1(epsilon, articles):
        if random.random() < epsilon:
            return choice(articles)
        else:
            return max(np.random.permutation([(x, articles_greedy_1[x].averageReward) for x in articles]), key = itemgetter(1))[0]
    
    def greedySelectArm_2(epsilon, articles):

        if random.random() < epsilon:
            return choice(articles)
        else:
            return max(np.random.permutation([(x, articles_greedy_2[x].averageReward) for x in articles]), key = itemgetter(1))[0]
            
    def greedySelectArm_3(epsilon, articles):
        if random.random() < epsilon:
            return choice(articles)
        else:
            return max(np.random.permutation([(x, articles_greedy_3[x].averageReward) for x in articles]), key = itemgetter(1))[0]
            
    def greedySelectArm_4(epsilon, articles):
        if random.random() < epsilon:
            return choice(articles)
        else:
            return max(np.random.permutation([(x, articles_greedy_4[x].averageReward) for x in articles]), key = itemgetter(1))[0]
            
    def greedySelectArm_5(epsilon, articles):
        if random.random() < epsilon:
            return choice(articles)
        else:
            return max(np.random.permutation([(x, articles_greedy_5[x].averageReward) for x in articles]), key = itemgetter(1))[0]
            
    def greedySelectArm_6(epsilon, articles):
        if random.random() < epsilon:
            return choice(articles)
        else:
            return max(np.random.permutation([(x, articles_greedy_6[x].averageReward) for x in articles]), key = itemgetter(1))[0]
            
    def greedySelectArm_7(epsilon, articles):
        if random.random() < epsilon:
            return choice(articles)
        else:
            return max(np.random.permutation([(x, articles_greedy_7[x].averageReward) for x in articles]), key = itemgetter(1))[0]
            
    def greedySelectArm_8(epsilon, articles):
        if random.random() < epsilon:
            return choice(articles)
        else:
            return max(np.random.permutation([(x, articles_greedy_8[x].averageReward) for x in articles]), key = itemgetter(1))[0]
            
    def greedySelectArm_9(epsilon, articles):
        if random.random() < epsilon:
            return choice(articles)
        else:
            return max(np.random.permutation([(x, articles_greedy_9[x].averageReward) for x in articles]), key = itemgetter(1))[0]

            
    modes = {0:'multiple', 1:'single', 2:'hours'} 	# the possible modes that this code can be run in; 'multiple' means multiple days or all days so theta dont change; single means it is reset every day; hours is reset after some hours depending on the reInitPerDay. 
    mode = 'single' 									# the selected mode
    fileSig = 'CTROverTime_Single'								# depending on further environment parameters a file signature to remember those. for example if theta is set every two hours i can have it '2hours'; for 
    reInitPerDay = 12								# how many times theta is re-initialized per day
    
    
    
    #gamma = 0.3
    #cd = 10
    gamma = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]                                                # parameter in exp3
    epsilon = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]                                              # parameter in e-greedy
 
    # relative dictionaries for algorithms
    articles_exp3_1 = {}
    articles_exp3_2= {}
    articles_exp3_3 = {}
    articles_exp3_4 = {}
    articles_exp3_5 = {}
    articles_exp3_6 = {}
    articles_exp3_7 = {}
    articles_exp3_8 = {}
    articles_exp3_9 = {}   
    articles_greedy_1 = {}
    articles_greedy_2 = {}
    articles_greedy_3 = {}
    articles_greedy_4 = {}
    articles_greedy_5 = {}
    articles_greedy_6 = {}
    articles_greedy_7 = {}
    articles_greedy_8 = {}
    articles_greedy_9 = {}
    articles_random = {}
    
    
    
    ctr = 1 				# overall ctr
    totalArticles = 0 		# total articles seen whether part of evaluation strategy or not
    totalClicks = 0 		# total clicks 
    countLine = 0 			# number of articles in this batch. should be same as batch size; not so usefull
    resetInterval = 0 		# initialize; value assigned later; determined when 
    timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M') 	# the current data time
    dataDays = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'] # the files from Yahoo that the algorithms will be run on; these files are indexed by days starting from May 1, 2009. this array starts from day 3 as also in the test data in the paper
    fileNameWriteCTR = os.path.join(save_address,'CTR.csv')
    
    for dataDay in dataDays:
        start_time = time.time()
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay
        epochArticles = {} 			# the articles that are present in this batch or epoch
        epochSelectedArticles = {} 	# the articles selected in this epoch
        hours = 0 					# times the theta was reset if the mode is 'hours'		
        batchStartTime = 0 			# time of first observation of the batch

        # should be self explaining
        if mode == 'single':
            fileNameWrite = os.path.join(save_address, 'All'+ fileSig + dataDay + timeRun + '.csv')
            re_initialize_article_exp3Structs()
            re_initialize_article_greedyStructs()
            countNoArticle = 0
            countLine = 0
        elif mode == 'multiple':
            fileNameWrite = os.path.join(save_address,  'All'+fileSig +dataDay + timeRun + '.csv')
        
        elif mode == 'hours':
            numObs = file_len(fileName)
            # resetInterval calcualtes after how many observations the count should be reset?
            resetInterval = int(numObs / reInitPerDay) + 1
            fileNameWrite = os.path.join(save_address,  'All'+fileSig + dataDay + '_' + str(hours) + timeRun + '.csv')
            
        # put some new data in file for readability
        with open(fileNameWrite, 'a+') as f:
            f.write('\nNew Run at  ' + datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
            f.write('\n, Time,  exp3CTRRatio_1; exp3CTRRatio_2; exp3CTRRatio_3; exp3CTRRatio_4; exp3CTRRatio_5; exp3CTRRatio_6; exp3CTRRatio_7; exp3CTRRatio_8; exp3CTRRatio_9; greedyCTRRatio_1, greedyCTRRatio_2, greedyCTRRatio_3, greedyCTRRatio_4, greedyCTRRatio_5, greedyCTRRatio_6, greedyCTRRatio_7, greedyCTRRatio_8, greedyCTRRatio_9  \n')
            print fileName, fileNameWrite, dataDay, resetInterval
        
        with open(fileName, 'r') as f:
            # reading file line ie observations running one at a time
            time_oneFile = time.time()                
            for line in f:             
                # read the observation
                tim, article_chosen, click, pool_articles = parseLine(line)
                if mode=='hours' and countLine > resetInterval:
                    hours = hours + 1
                    # each time theta is reset, a new file is started.
                    fileNameWrite = os.path.join(save_address, fileSig + dataDay + '_' + str(hours) + timeRun + '.csv')
                    # re-initialize
                    countLine = 0
                    re_initialize_article_exp3Structs()     #Not sure whether to re-initialize exp3Struct
                    re_initialize_article_greedyStructs()
                    printWrite()
                    batchStartTime = tim
                    epochArticles = {}
                    epochSelectedArticles = {}
                    print "hours thing fired!!"
                    
                # number of observations seen in this batch; reset after start of new batch
                countLine = countLine + 1
                totalArticles = totalArticles + 1
   
                # article ids for articles in the current pool for this observation
                currentArticles = []
                total_weight_1 = 0
                total_weight_2 = 0
                total_weight_3 = 0
                total_weight_4 = 0
                total_weight_5 = 0
                total_weight_6 = 0
                total_weight_7 = 0
                total_weight_8 = 0
                total_weight_9 = 0
                
                for article in pool_articles:                    
                    article_id = article[0]
                    currentArticles.append(article_id)
                    
                    if article_id not in articles_exp3_1: #if its a new article; add it to dictionaries
                        articles_random[article_id] = randomStruct()

                        articles_greedy_1[article_id] = greedyStruct()
                        articles_greedy_2[article_id] = greedyStruct()
                        articles_greedy_3[article_id] = greedyStruct()
                        articles_greedy_4[article_id] = greedyStruct()
                        articles_greedy_5[article_id] = greedyStruct()
                        articles_greedy_6[article_id] = greedyStruct()
                        articles_greedy_7[article_id] = greedyStruct()
                        articles_greedy_8[article_id] = greedyStruct()
                        articles_greedy_9[article_id] = greedyStruct()
                        articles_exp3_1[article_id] = exp3Struct()
                        articles_exp3_2[article_id]= exp3Struct()
                        articles_exp3_3[article_id] = exp3Struct()
                        articles_exp3_4[article_id] = exp3Struct()
                        articles_exp3_5[article_id] = exp3Struct()
                        articles_exp3_6[article_id] = exp3Struct()
                        articles_exp3_7[article_id] = exp3Struct()
                        articles_exp3_8[article_id] = exp3Struct()
                        articles_exp3_9[article_id] = exp3Struct()

                    #total_weight = sum([articles_exp3[x].weights for x in pool_articles[:0]])
                    total_weight_1 = total_weight_1 + articles_exp3_1[article_id].weights
                    total_weight_2 = total_weight_2 + articles_exp3_2[article_id].weights
                    total_weight_3 = total_weight_3 + articles_exp3_3[article_id].weights
                    total_weight_4 = total_weight_4 + articles_exp3_4[article_id].weights
                    total_weight_5 = total_weight_5 + articles_exp3_5[article_id].weights
                    total_weight_6 = total_weight_6 + articles_exp3_6[article_id].weights
                    total_weight_7 = total_weight_7 + articles_exp3_7[article_id].weights
                    total_weight_8 = total_weight_8 + articles_exp3_8[article_id].weights
                    total_weight_9 = total_weight_9 + articles_exp3_9[article_id].weights
                    
                pool_articleNum = len(currentArticles)
                    
                for article in pool_articles:
                    article_id = article[0]
                    articles_greedy_1[article_id].updateReward()
                    articles_greedy_2[article_id].updateReward()
                    articles_greedy_3[article_id].updateReward()
                    articles_greedy_4[article_id].updateReward()
                    articles_greedy_5[article_id].updateReward()
                    articles_greedy_6[article_id].updateReward()
                    articles_greedy_7[article_id].updateReward()
                    articles_greedy_8[article_id].updateReward()
                    articles_greedy_9[article_id].updateReward()
                    #articles_exp3[article_id].updatePta(gamma, pool_articleNum, total_weight)
                    articles_exp3_1[article_id].updatePta(gamma[0], pool_articleNum, total_weight_1)
                    articles_exp3_2[article_id].updatePta(gamma[1], pool_articleNum, total_weight_2)
                    articles_exp3_3[article_id].updatePta(gamma[2], pool_articleNum, total_weight_3)
                    articles_exp3_4[article_id].updatePta(gamma[3], pool_articleNum, total_weight_4)
                    articles_exp3_5[article_id].updatePta(gamma[4], pool_articleNum, total_weight_5)
                    articles_exp3_6[article_id].updatePta(gamma[5], pool_articleNum, total_weight_6)
                    articles_exp3_7[article_id].updatePta(gamma[6], pool_articleNum, total_weight_7)
                    articles_exp3_8[article_id].updatePta(gamma[7], pool_articleNum, total_weight_8)
                    articles_exp3_9[article_id].updatePta(gamma[8], pool_articleNum, total_weight_9)


                # article picked by random strategy
                randomArticle = choice(currentArticles)                  
                # article picked by exp3
                exp3Article_1 = categorical_draw_1(currentArticles)
                exp3Article_2 = categorical_draw_2(currentArticles)
                exp3Article_3 = categorical_draw_3(currentArticles)
                exp3Article_4 = categorical_draw_4(currentArticles)
                exp3Article_5 = categorical_draw_5(currentArticles)
                exp3Article_6 = categorical_draw_6(currentArticles)
                exp3Article_7 = categorical_draw_7(currentArticles)
                exp3Article_8 = categorical_draw_8(currentArticles)
                exp3Article_9 = categorical_draw_9(currentArticles)
                
                greedyArticle_1 = greedySelectArm_1(epsilon[0], currentArticles)
                greedyArticle_2 = greedySelectArm_2(epsilon[1], currentArticles)
                greedyArticle_3 = greedySelectArm_3(epsilon[2], currentArticles)
                greedyArticle_4 = greedySelectArm_4(epsilon[3], currentArticles)
                greedyArticle_5 = greedySelectArm_5(epsilon[4], currentArticles)
                greedyArticle_6 = greedySelectArm_6(epsilon[5], currentArticles)
                greedyArticle_7 = greedySelectArm_7(epsilon[6], currentArticles)
                greedyArticle_8 = greedySelectArm_8(epsilon[7], currentArticles)
                greedyArticle_9 = greedySelectArm_9(epsilon[8], currentArticles)
                #articles_greedy[greedyArticle].numPlayed = articles_greedy[greedyArticle].numPlayed + 1
                 
                # if random strategy article Picked by evaluation srategy
                if randomArticle == article_chosen:
                    articles_random[randomArticle].learn_stats.clicks = articles_random[randomArticle].learn_stats.clicks + click
                    articles_random[randomArticle].learn_stats.accesses = articles_random[randomArticle].learn_stats.accesses + 1   
               
                # if exp3 article is chosen by evalution strategy
                if exp3Article_1 == article_chosen:
                    articles_exp3_1[article_chosen].learn_stats.clicks = articles_exp3_1[article_chosen].learn_stats.clicks + click
                    articles_exp3_1[article_chosen].learn_stats.accesses = articles_exp3_1[article_chosen].learn_stats.accesses + 1
                    if click:
                        articles_exp3_1[article_chosen].updateWeight(gamma[0], pool_articleNum, click)
                
                if exp3Article_2 == article_chosen:
                    articles_exp3_2[article_chosen].learn_stats.clicks = articles_exp3_2[article_chosen].learn_stats.clicks + click
                    articles_exp3_2[article_chosen].learn_stats.accesses = articles_exp3_2[article_chosen].learn_stats.accesses + 1
                    if click:
                        articles_exp3_2[article_chosen].updateWeight(gamma[1], pool_articleNum, click)
                        
                if exp3Article_3 == article_chosen:
                    articles_exp3_3[article_chosen].learn_stats.clicks = articles_exp3_3[article_chosen].learn_stats.clicks + click
                    articles_exp3_3[article_chosen].learn_stats.accesses = articles_exp3_3[article_chosen].learn_stats.accesses + 1
                    if click:
                        articles_exp3_3[article_chosen].updateWeight(gamma[2], pool_articleNum, click)
                
                if exp3Article_4 == article_chosen:
                    articles_exp3_4[article_chosen].learn_stats.clicks = articles_exp3_4[article_chosen].learn_stats.clicks + click
                    articles_exp3_4[article_chosen].learn_stats.accesses = articles_exp3_4[article_chosen].learn_stats.accesses + 1
                    if click:
                        articles_exp3_4[article_chosen].updateWeight(gamma[3], pool_articleNum, click)
                
                
                if exp3Article_5 == article_chosen:
                    articles_exp3_5[article_chosen].learn_stats.clicks = articles_exp3_5[article_chosen].learn_stats.clicks + click
                    articles_exp3_5[article_chosen].learn_stats.accesses = articles_exp3_5[article_chosen].learn_stats.accesses + 1
                    if click:
                        articles_exp3_5[article_chosen].updateWeight(gamma[4], pool_articleNum, click)
                        
                if exp3Article_6 == article_chosen:
                    articles_exp3_6[article_chosen].learn_stats.clicks = articles_exp3_6[article_chosen].learn_stats.clicks + click
                    articles_exp3_6[article_chosen].learn_stats.accesses = articles_exp3_6[article_chosen].learn_stats.accesses + 1
                    if click:
                        articles_exp3_6[article_chosen].updateWeight(gamma[5], pool_articleNum, click)
                
                if exp3Article_7 == article_chosen:
                    articles_exp3_7[article_chosen].learn_stats.clicks = articles_exp3_7[article_chosen].learn_stats.clicks + click
                    articles_exp3_7[article_chosen].learn_stats.accesses = articles_exp3_7[article_chosen].learn_stats.accesses + 1
                    if click:
                        articles_exp3_7[article_chosen].updateWeight(gamma[6], pool_articleNum, click)
                        
                if exp3Article_8 == article_chosen:
                    articles_exp3_8[article_chosen].learn_stats.clicks = articles_exp3_8[article_chosen].learn_stats.clicks + click
                    articles_exp3_8[article_chosen].learn_stats.accesses = articles_exp3_8[article_chosen].learn_stats.accesses + 1
                    if click:
                        articles_exp3_8[article_chosen].updateWeight(gamma[7], pool_articleNum, click)
                        
                if exp3Article_9 == article_chosen:
                    articles_exp3_9[article_chosen].learn_stats.clicks = articles_exp3_9[article_chosen].learn_stats.clicks + click
                    articles_exp3_9[article_chosen].learn_stats.accesses = articles_exp3_9[article_chosen].learn_stats.accesses + 1
                    if click:
                        articles_exp3_9[article_chosen].updateWeight(gamma[8], pool_articleNum, click)
                
                if greedyArticle_1 == article_chosen:
                    articles_greedy_1[article_chosen].learn_stats.clicks = articles_greedy_1[article_chosen].learn_stats.clicks + click
                    articles_greedy_1[article_chosen].learn_stats.accesses = articles_greedy_1[article_chosen].learn_stats.accesses + 1
                    articles_greedy_1[article_chosen].totalReward = articles_greedy_1[article_chosen].totalReward + click
                    articles_greedy_1[article_chosen].numPlayed = articles_greedy_1[article_chosen].numPlayed + 1
                if greedyArticle_2 == article_chosen:
                    articles_greedy_2[article_chosen].learn_stats.clicks = articles_greedy_2[article_chosen].learn_stats.clicks + click
                    articles_greedy_2[article_chosen].learn_stats.accesses = articles_greedy_2[article_chosen].learn_stats.accesses + 1
                    articles_greedy_2[article_chosen].totalReward = articles_greedy_2[article_chosen].totalReward + click
                    articles_greedy_2[article_chosen].numPlayed = articles_greedy_2[article_chosen].numPlayed + 1
                if greedyArticle_3 == article_chosen:
                    articles_greedy_3[article_chosen].learn_stats.clicks = articles_greedy_3[article_chosen].learn_stats.clicks + click
                    articles_greedy_3[article_chosen].learn_stats.accesses = articles_greedy_3[article_chosen].learn_stats.accesses + 1
                    articles_greedy_3[article_chosen].totalReward = articles_greedy_3[article_chosen].totalReward + click
                    articles_greedy_3[article_chosen].numPlayed = articles_greedy_3[article_chosen].numPlayed + 1
                if greedyArticle_4 == article_chosen:
                    articles_greedy_4[article_chosen].learn_stats.clicks = articles_greedy_4[article_chosen].learn_stats.clicks + click
                    articles_greedy_4[article_chosen].learn_stats.accesses = articles_greedy_4[article_chosen].learn_stats.accesses + 1
                    articles_greedy_4[article_chosen].totalReward = articles_greedy_4[article_chosen].totalReward + click
                    articles_greedy_4[article_chosen].numPlayed = articles_greedy_4[article_chosen].numPlayed + 1
                if greedyArticle_5 == article_chosen:
                    articles_greedy_5[article_chosen].learn_stats.clicks = articles_greedy_5[article_chosen].learn_stats.clicks + click
                    articles_greedy_5[article_chosen].learn_stats.accesses = articles_greedy_5[article_chosen].learn_stats.accesses + 1
                    articles_greedy_5[article_chosen].totalReward = articles_greedy_5[article_chosen].totalReward + click
                    articles_greedy_5[article_chosen].numPlayed = articles_greedy_5[article_chosen].numPlayed + 1
                if greedyArticle_6 == article_chosen:
                    articles_greedy_6[article_chosen].learn_stats.clicks = articles_greedy_6[article_chosen].learn_stats.clicks + click
                    articles_greedy_6[article_chosen].learn_stats.accesses = articles_greedy_6[article_chosen].learn_stats.accesses + 1
                    articles_greedy_6[article_chosen].totalReward = articles_greedy_6[article_chosen].totalReward + click
                    articles_greedy_6[article_chosen].numPlayed = articles_greedy_6[article_chosen].numPlayed + 1
                if greedyArticle_7 == article_chosen:
                    articles_greedy_7[article_chosen].learn_stats.clicks = articles_greedy_7[article_chosen].learn_stats.clicks + click
                    articles_greedy_7[article_chosen].learn_stats.accesses = articles_greedy_7[article_chosen].learn_stats.accesses + 1
                    articles_greedy_7[article_chosen].totalReward = articles_greedy_7[article_chosen].totalReward + click
                    articles_greedy_7[article_chosen].numPlayed = articles_greedy_7[article_chosen].numPlayed + 1
                if greedyArticle_8 == article_chosen:
                    articles_greedy_8[article_chosen].learn_stats.clicks = articles_greedy_8[article_chosen].learn_stats.clicks + click
                    articles_greedy_8[article_chosen].learn_stats.accesses = articles_greedy_8[article_chosen].learn_stats.accesses + 1
                    articles_greedy_8[article_chosen].totalReward = articles_greedy_8[article_chosen].totalReward + click
                    articles_greedy_8[article_chosen].numPlayed = articles_greedy_8[article_chosen].numPlayed + 1
                if greedyArticle_9 == article_chosen:
                    articles_greedy_9[article_chosen].learn_stats.clicks = articles_greedy_9[article_chosen].learn_stats.clicks + click
                    articles_greedy_9[article_chosen].learn_stats.accesses = articles_greedy_9[article_chosen].learn_stats.accesses + 1
                    articles_greedy_9[article_chosen].totalReward = articles_greedy_9[article_chosen].totalReward + click
                    articles_greedy_9[article_chosen].numPlayed = articles_greedy_9[article_chosen].numPlayed + 1
                                   
            print time.time() - time_oneFile
            printWrite()
                
                   
            






  
    

