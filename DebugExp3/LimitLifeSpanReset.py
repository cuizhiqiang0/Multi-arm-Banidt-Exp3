# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 02:11:16 2015

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
    def __init__(self, gamma):
        self.gamma = gamma
        self.weights = 1.0
        self.pta = 0.0
        self.learn_stats = articleAccess()
        self.LifeSpanCounter = 0
        
    def reInitilize(self):
        self.weights = 1.0
        self.pta=0.0
        self.LifeSpanCounter = 0
          
    def updatePta(self, n_arms, total_weight):
        #n_arms = n_arms
        self.pta= (1-self.gamma) * (self.weights / total_weight)
        self.pta= self.pta + (self.gamma) * (1.0 / float(n_arms))
 
    def updateWeight(self, n_arms, reward):
        #n_arms = n_arms
        X=reward/self.pta
        growth_factor = math.exp((self.gamma/n_arms)*X)
        self.weights = self.weights * growth_factor


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
def save_to_file(fileNameWrite, dicts, recordedStats, tim):
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
        
        exp3LA = sum([articles_exp3[x].learn_stats.accesses for x in articles_exp3])
        exp3C = sum([articles_exp3[x].learn_stats.clicks for x in articles_exp3]) 
        exp3CTR = sum([articles_exp3[x].learn_stats.clicks for x in articles_exp3]) / sum([articles_exp3[x].learn_stats.accesses for x in articles_exp3])
                       
        print totalArticles,
        print 'Exp3Lrn', exp3CTR / randomCTR,
        print ' '
        
        recordedStats = [exp3LA, exp3C, exp3CTR / randomCTR]
        # write to file
        save_to_file(fileNameWrite, articles_exp3, recordedStats, tim)
    
            
    # this function reset weight for all exp3
    def re_initialize_article_exp3Structs():
        for x in articles_exp3:
            articles_exp3[x].reInitilize()
    
    def categorical_draw(articles):
        z = random.random()
        cum_pta = 0.0
        #flag = 0
        for x in articles:
            cum_pta = cum_pta + articles_exp3[x].pta
            if cum_pta > z:
                return x
                   
            
    modes = {0:'multiple', 1:'single', 2:'hours'} 	# the possible modes that this code can be run in; 'multiple' means multiple days or all days so theta dont change; single means it is reset every day; hours is reset after some hours depending on the reInitPerDay. 
    mode = 'multiple' 									# the selected mode
    fileSig = 'Exp3_ResetLifeSpan'								# depending on further environment parameters a file signature to remember those. for example if theta is set every two hours i can have it '2hours'; for 
    reInitPerDay = 12								# how many times theta is re-initialized per day

    gamma = 0.3                                                  # parameter in exp3
    LifeSpanThreshold = 4040000 

    # relative dictionaries for algorithms
    articles_exp3 = {}
    articles_random = {}

    totalArticles = 0 		# total articles seen whether part of evaluation strategy or not
    countLine = 0 			# number of articles in this batch. should be same as batch size; not so usefull
    resetInterval = 0 		# initialize; value assigned later; determined when 
    timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M') 	# the current data time
    dataDays = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'] # the files from Yahoo that the algorithms will be run on; these files are indexed by days starting from May 1, 2009. this array starts from day 3 as also in the test data in the paper
    #fileNameWriteCTR = os.path.join(save_address,  fileSig + '_' + timeRun + '.csv')
    
    for dataDay in dataDays:
        start_time = time.time()
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay
        epochArticles = {} 			# the articles that are present in this batch or epoch
        epochSelectedArticles = {} 	# the articles selected in this epoch
        hours = 0 					# times the theta was reset if the mode is 'hours'		
        batchStartTime = 0 			# time of first observation of the batch

        # should be self explaining
        if mode == 'single':
            fileNameWrite = os.path.join(save_address, fileSig + dataDay + timeRun + '.csv')
            re_initialize_article_exp3Structs()
            countLine = 0
        elif mode == 'multiple':
            fileNameWrite = os.path.join(save_address,  fileSig +dataDay + timeRun + '.csv')
        
        elif mode == 'hours':
            numObs = file_len(fileName)
            # resetInterval calcualtes after how many observations the count should be reset?
            resetInterval = int(numObs / reInitPerDay) + 1
            fileNameWrite = os.path.join(save_address,  fileSig + dataDay + '_' + str(hours) + timeRun + '.csv')
        time_open= time.time()    
        # put some new data in file for readability
        with open(fileNameWrite, 'a+') as f:
            f.write('\nNew Run at  ' + datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
            f.write('\n, Time, exp3Access; exp3Clicks; exp3CTRRatio \n')
            print fileName, fileNameWrite, dataDay, resetInterval
        print 'opentime', time.time() - time_open
        
        with open(fileName, 'r') as f:
            # reading file line ie observations running one at a time
            
            for line in f:
                # read the observation
                tim, article_chosen, click, pool_articles = parseLine(line)
                article_chosen = str(int(article_chosen))
                if mode=='hours' and countLine > resetInterval:
                    hours = hours + 1
                    # each time theta is reset, a new file is started.
                    fileNameWrite = os.path.join(save_address, fileSig + dataDay + '_' + str(hours) + timeRun + '.csv')
                    # re-initialize
                    re_initialize_article_exp3Structs()     #Not sure whether to re-initialize exp3Struct)
                    printWrite()
                    print "hours thing fired!!"
                    
                # number of observations seen in this batch; reset after start of new batch
                countLine = countLine + 1
                totalArticles = totalArticles + 1
   
                # article ids for articles in the current pool for this observation
                currentArticles = []
                total_weight = 0.0
                
                for article in pool_articles:                    
                    article_id = str(int(article[0]))
                    currentArticles.append(article_id)
                    
                    if article_id not in articles_exp3: #if its a new article; add it to dictionaries
                        articles_random[article_id] = randomStruct()
                        articles_exp3[article_id] = exp3Struct(gamma)
                    else:
                        articles_exp3[article_id].LifeSpanCounter += 1
                        
                    if articles_exp3[article_id].LifeSpanCounter > LifeSpanThreshold:
                        articles_exp3[article_id].reInitilize()
                        
                    total_weight = total_weight + articles_exp3[article_id].weights
                    
                pool_articleNum = len(currentArticles)
        
                for article in currentArticles:
                    #print article
                    articles_exp3[article].updatePta(pool_articleNum, total_weight)

                # article picked by random strategy
                randomArticle = choice(currentArticles)
                # article picked by exp3
                exp3Article = categorical_draw(currentArticles)
                
                time_chose = time.time()
                # if random strategy article Picked by evaluation srategy
                if randomArticle == article_chosen:
                    articles_random[randomArticle].learn_stats.clicks = articles_random[randomArticle].learn_stats.clicks + click
                    articles_random[randomArticle].learn_stats.accesses = articles_random[randomArticle].learn_stats.accesses + 1   
               
                # if exp3 article is chosen by evalution strategy
                if exp3Article == article_chosen:
                    articles_exp3[article_chosen].learn_stats.clicks = articles_exp3[article_chosen].learn_stats.clicks + click
                    articles_exp3[article_chosen].learn_stats.accesses = articles_exp3[article_chosen].learn_stats.accesses + 1
                    if click:
                        articles_exp3[article_chosen].updateWeight(pool_articleNum, click)
                 
                if totalArticles%20000 ==0:
                    # write observations for this batch
                    printWrite()
           
             
            # print stuff to screen and save parameters to file when the Yahoo! dataset file endd
            printWrite()
                
            






  
    

