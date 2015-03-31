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
        
        greedyLA = sum([articles_greedy[x].learn_stats.accesses for x in articles_greedy])
        greedyC = sum([articles_greedy[x].learn_stats.clicks for x in articles_greedy])
        greedyCTR = sum([articles_greedy[x].learn_stats.clicks for x in articles_greedy]) / sum([articles_greedy[x].learn_stats.accesses for x in articles_greedy])
                       
        print totalArticles,
        print 'Greedy', greedyCTR / randomCTR,
        print ' '
        
        recordedStats = [greedyLA, greedyC, greedyCTR / randomCTR]
        # write to file
        save_to_file(fileNameWrite, articles_greedy, recordedStats, tim)
    
    
    
    def re_initialize_article_greedyStructs():
        for x in articles_greedy:
            articles_greedy[x].reInitilize()

    
    def greedySelectArm(epsilon, articles):
        if random.random() < epsilon:
            return choice(articles)
        else:
            return max(np.random.permutation([(x, articles_greedy[x].averageReward) for x in articles]), key = itemgetter(1))[0]

    modes = {0:'multiple', 1:'single', 2:'hours'} 	# the possible modes that this code can be run in; 'multiple' means multiple days or all days so theta dont change; single means it is reset every day; hours is reset after some hours depending on the reInitPerDay. 
    mode = 'multiple' 									# the selected mode
    fileSig = 'epsilon0.5_Multi'								# depending on further environment parameters a file signature to remember those. for example if theta is set every two hours i can have it '2hours'; for
    reInitPerDay = 12								# how many times theta is re-initialized per day

    gamma = 0.3                                                  # parameter in exp3
    cd = 20                                               # parameter in e-greedy
    epsilon =0.5
 
    # relative dictionaries for algorithms
  
    articles_greedy = {}
    articles_random = {}
    
    GreedyChosenNum = 0
    RandomChosenNum = 0
    
    
    ctr = 1 				# overall ctr
    totalArticles = 0 		# total articles seen whether part of evaluation strategy or not
    countLine = 0 			# number of articles in this batch. should be same as batch size; not so usefull
    resetInterval = 0 		# initialize; value assigned later; determined when 
    timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M') 	# the current data time
    dataDays = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'] # the files from Yahoo that the algorithms will be run on; these files are indexed by days starting from May 1, 2009. this array starts from day 3 as also in the test data in the paper
    fileNameWriteCTR = os.path.join(save_address,  fileSig + '_' + timeRun + '.csv')
    
    for dataDay in dataDays:
        start_time = time.time()
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay
        hours = 0 					# times the theta was reset if the mode is 'hours'		
        
    
        if mode == 'single':
            fileNameWrite = os.path.join(save_address, fileSig + dataDay + timeRun + '.csv')
        
            re_initialize_article_greedyStructs()
            GreedyChosenNum = 0
            RandomChosenNum = 0
            
            countNoArticle = 0
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
            f.write('\n, Time, greedyAccesses; greedyClicks; greedyCTRRatio \n')
            print fileName, fileNameWrite, dataDay, resetInterval
        print 'opentime', time.time() - time_open
        
        with open(fileName, 'r') as f:
            # reading file line ie observations running one at a time
            
            for line in f:  
                line_time = time.time()
                # read the observation
                time_read = time.time()
                tim, article_chosen, click, pool_articles = parseLine(line)
                if mode=='hours' and countLine > resetInterval:
                    hours = hours + 1
                    # each time theta is reset, a new file is started.
                    fileNameWrite = os.path.join(save_address, fileSig + dataDay + '_' + str(hours) + timeRun + '.csv')
                    # re-initialize
                    countLine = 0
                    GreedyChosenNum = 0
                    RandomChosenNum = 0
                    re_initialize_article_greedyStructs()
                    printWrite()
                    print "hours thing fired!!"
                    
                # number of observations seen in this batch; reset after start of new batch
                countLine = countLine + 1
                totalArticles = totalArticles + 1
   
                # article ids for articles in the current pool for this observation
                currentArticles = []
                total_weight = 0
                time_firstLoop = time.time()
                for article in pool_articles:                    
                    article_id = article[0]
                    currentArticles.append(article_id)
                    
                    if article_id not in articles_greedy: #if its a new article; add it to dictionaries
                        articles_random[article_id] = randomStruct()
                        articles_greedy[article_id] = greedyStruct()
            
                    articles_greedy[article_id].updateReward()
            
                pool_articleNum = len(currentArticles)
                
                
                # article picked by random strategy
                randomArticle = choice(currentArticles)
                greedyArticle = greedySelectArm(epsilon, currentArticles)
                
                time_chose = time.time()
                # if random strategy article Picked by evaluation srategy
                if randomArticle == article_chosen:
                    RandomChosenNum = RandomChosenNum + 1
                    articles_random[randomArticle].learn_stats.clicks = articles_random[randomArticle].learn_stats.clicks + click
                    articles_random[randomArticle].learn_stats.accesses = articles_random[randomArticle].learn_stats.accesses + 1   
               
                if greedyArticle == article_chosen:
                    GreedyChosenNum = GreedyChosenNum + 1
                    articles_greedy[article_chosen].learn_stats.clicks = articles_greedy[article_chosen].learn_stats.clicks + click
                    articles_greedy[article_chosen].learn_stats.accesses = articles_greedy[article_chosen].learn_stats.accesses + 1
                    articles_greedy[article_chosen].totalReward = articles_greedy[article_chosen].totalReward + click
                    articles_greedy[greedyArticle].numPlayed = articles_greedy[greedyArticle].numPlayed + 1

                if totalArticles%20000 ==0:
                    printWrite()
                
            printWrite()
                
            






  
    

