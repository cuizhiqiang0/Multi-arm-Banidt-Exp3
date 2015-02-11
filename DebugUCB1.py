# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 15:12:00 2015

@author: Qingyun Wu
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
import Queue

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

class ucb1Struct:
    def __init__(self):
        self.totalReward = 0.0
        self.numPlayed = 0
        self.pta = 0.0
        self.learn_stats = articleAccess()
        self.deploy_stats = articleAccess()
        
    def reInitilize(self): 
        self.totalReward = 0.0
        self.numPlayed = 0.0  
        self.pta=0.0
        
    def updatePta(self, allNumPlayed):
        try:
            self.pta = self.totalReward / self.numPlayed + np.sqrt(2*np.log(allNumPlayed) / self.numPlayed)
        except ZeroDivisionError:
            self.pta = 0.0

class ucb1AlphaStruct:
    def __init__(self):
        self.totalReward = 0.0
        self.numPlayed = 0
        self.pta = 0.0
        self.learn_stats = articleAccess()
        self.deploy_stats = articleAccess()
        
    def reInitilize(self): 
        self.totalReward = 0.0
        self.numPlayed = 0.0  
        self.pta=0.0
        
    def updatePta(self, allNumPlayed, alpha):
        try:
            self.pta = self.totalReward / self.numPlayed + alpha / np.sqrt(self.numPlayed)
        except ZeroDivisionError:
            self.pta = 0.0
    
        
class randomStruct:
	def __init__(self):
		self.learn_stats = articleAccess()
		#self.deploy_stats = articleAccess()

'''
class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0
    def put(self, item):
        PriorityQueue.put(self, ())
'''
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
def save_to_file(fileNameWrite, dicts, recordedStats, epochArticles, epochSelectedArticles, tim):
	with open(fileNameWrite, 'a+') as f:
		f.write('data') # the observation line starts with data;
		f.write(',' + str(tim))
		f.write(',' + ';'.join([str(x) for x in recordedStats]))
		f.write(',' + ';'.join([str(dicts[x].learn_stats.accesses) + ' ' + str(dicts[x].learn_stats.clicks) + ' ' + str(x)  for x in epochSelectedArticles]))
		f.write(',' + ';'.join(str(x)+' ' + str(epochArticles[x]) for x in epochArticles))
		f.write(',' + ';'.join(str(x)+' ' + str(epochSelectedArticles[x]) for x in epochSelectedArticles))

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
        
        ucb1LA = sum([articles_ucb1[x].learn_stats.accesses for x in articles_ucb1])
        ucb1C = sum([articles_ucb1[x].learn_stats.clicks for x in articles_ucb1])
        ucb1CTR = sum([articles_ucb1[x].learn_stats.clicks for x in articles_ucb1]) / sum([articles_ucb1[x].learn_stats.accesses for x in articles_ucb1])
            
        ucb1_1LA = sum([articles_ucb1_1[x].learn_stats.accesses for x in articles_ucb1_1])
        ucb1_1C = sum([articles_ucb1_1[x].learn_stats.clicks for x in articles_ucb1_1])
        ucb1_1CTR = sum([articles_ucb1_1[x].learn_stats.clicks for x in articles_ucb1_1]) / sum([articles_ucb1_1[x].learn_stats.accesses for x in articles_ucb1_1])
            
        ucb1AlphaLA = sum([articles_ucb1Alpha[x].learn_stats.accesses for x in articles_ucb1Alpha])
        ucb1AlphaC = sum([articles_ucb1Alpha[x].learn_stats.clicks for x in articles_ucb1Alpha])
        ucb1AlphaCTR = sum([articles_ucb1Alpha[x].learn_stats.clicks for x in articles_ucb1Alpha]) / sum([articles_ucb1Alpha[x].learn_stats.accesses for x in articles_ucb1Alpha])
            
        print totalArticles,
        print 'UCB1', ucb1CTR / randomCTR,
        print 'UCB1_1', ucb1_1CTR / randomCTR,
        print 'UCB1Alpha', ucb1AlphaCTR / randomCTR,
        
        print ' '
        
        recordedStats = [randomLA, randomC, ucb1LA, ucb1C,  ucb1CTR / randomCTR, ucb1_1CTR / randomCTR, ucb1AlphaCTR / randomCTR ]
        # write to file
        save_to_file(fileNameWrite, articles_ucb1, recordedStats, epochArticles, epochSelectedArticles, tim)
    
            
    def re_initialize_article_ucb1Structs():
        for x in articles_ucb1:
            articles_ucb1[x].reInitilize()
             
    def re_initialize_article_ucb1_1Structs():
        for x in articles_ucb1_1:
            articles_ucb1_1[x].reInitilize()
             
    def re_initialize_article_ucb1AlphaStructs():
        for x in articles_ucb1Alpha:
            articles_ucb1Alpha[x].reInitilize()

    def ucb1SelectArm(articles):
        flag = 0
        for x in articles:
            if articles_ucb1[x].numPlayed ==0:
                flag = 1
                return x
        if flag == 0:
            return max(np.random.permutation([(x, articles_ucb1[x].pta) for x in articles]), key = itemgetter(1))[0]
        
    def ucb1SelectArm_1(articles):
        flag = 0
        for x in articles:
            if articles_ucb1_1[x].numPlayed ==0:
                flag = 1
                return x
        if flag == 0:
            return max(np.random.permutation([(x, articles_ucb1_1[x].pta) for x in articles]), key = itemgetter(1))[0]
            
    def ucb1AlphaSelectArm(articles):
        flag = 0
        for x in articles:
            if articles_ucb1Alpha[x].numPlayed ==0:
                flag = 1
                return x
        if flag == 0:
            return max(np.random.permutation([(x, articles_ucb1Alpha[x].pta) for x in articles]), key = itemgetter(1))[0]
        
        
            
    modes = {0:'multiple', 1:'single', 2:'hours'} 	# the possible modes that this code can be run in; 'multiple' means multiple days or all days so theta dont change; single means it is reset every day; hours is reset after some hours depending on the reInitPerDay. 
    mode = 'hours' 									# the selected mode
    fileSig = 'DebugUCB1_Hour'								# depending on further environment parameters a file signature to remember those. for example if theta is set every two hours i can have it '2hours'; for 
    reInitPerDay = 12								# how many times theta is re-initialized per day
    
    alpha = 20
    #gamma = 0.3                                                  # parameter in exp3
    #
    # relative dictionaries for algorithms
    #recentArticles = Queue.Queue(maxsize = 200)
    articles_ucb1 = {}
    articles_ucb1_1 ={}
    articles_ucb1Alpha = {}
    articles_random = {}
    articlesPlayedByUCB1 = []
    articlesPlayedByExp3 = []
    UCB1ChosenNum = 0
    UCB1_1ChosenNum =0
    UCB1AlphaChosenNum = 0
    
    UCB1ClickNum = 0
    Exp3ClickNum = 0
    
    
    ctr = 1 				# overall ctr
    numArticlesChosen = 1 	# overall the articles that are same as for LinUCB and the random strategy that created Yahoo! dataset. I will call it evaluation strategy
    totalArticles = 0 		# total articles seen whether part of evaluation strategy or not
    totalClicks = 0 		# total clicks 
    countNoArticle = 0 		# total articles in the pool 
    countLine = 0 			# number of articles in this batch. should be same as batch size; not so usefull
    resetInterval = 0 		# initialize; value assigned later; determined when 
    timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M') 	# the current data time
    dataDays = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'] # the files from Yahoo that the algorithms will be run on; these files are indexed by days starting from May 1, 2009. this array starts from day 3 as also in the test data in the paper
    fileNameWriteCTR = os.path.join(save_address,'CTR.csv')
    
    for dataDay in dataDays:
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay
        epochArticles = {} 			# the articles that are present in this batch or epoch
        epochSelectedArticles = {} 	# the articles selected in this epoch
        hours = 0 					# times the theta was reset if the mode is 'hours'		
        batchStartTime = 0 			# time of first observation of the batch

        # should be self explaining
        if mode == 'single':
            fileNameWrite = os.path.join(save_address, fileSig + dataDay + timeRun + '.csv')
            re_initialize_article_ucb1Structs()
            re_initialize_article_ucb1_1Structs()
            re_initialize_article_ucb1AlphaStructs()
            UCB1ChosenNum = 0
            UCB1_1ChosenNum =0
            UCB1AlphaChosenNum = 0
            
            countNoArticle = 0
            countLine = 0
        elif mode == 'multiple':
            fileNameWrite = os.path.join(save_address,  fileSig +dataDay + timeRun + '.csv')
        
        elif mode == 'hours':
            numObs = file_len(fileName)
            # resetInterval calcualtes after how many observations the count should be reset?
            resetInterval = int(numObs / reInitPerDay) + 1
            fileNameWrite = os.path.join(save_address,  fileSig + dataDay + '_' + str(hours) + timeRun + '.csv')
            
        # put some new data in file for readability
        with open(fileNameWrite, 'a+') as f:
            f.write('\nNew Run at  ' + datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
            f.write('\n, Time, randomAccesses; randomClicks; ucb1Accesses; ucb1Clicks; ucb1CTRRatio; ucb1_1CTRRatio; ucb1AlphaCTRRatio, Article Access; Clicks; ID; Theta, ID; epochArticles, ID ;epochSelectedArticles \n')
            print fileName, fileNameWrite, dataDay, resetInterval
        
        with open(fileName, 'r') as f:
            # reading file line ie observations running one at a time
                            
            for line in f:
                # read the observation
                tim, article_chosen, click, pool_articles = parseLine(line)
                if mode=='hours' and countLine > resetInterval:
                    hours = hours + 1
                    # each time theta is reset, a new file is started.
                    fileNameWrite = os.path.join(save_address, fileSig + dataDay + '_' + str(hours) + timeRun + '.csv')
                    # re-initialize
                    countLine = 0
                    re_initialize_article_ucb1Structs()
                    re_initialize_article_ucb1_1Structs()
                    re_initialize_article_ucb1AlphaStructs()
                    UCB1ChosenNum = 0
                    UCB1_1ChosenNum =0
                    UCB1AlphaChosenNum = 0
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
                total_weight = 0
                for article in pool_articles:
                    article_id = article[0]
                    currentArticles.append(article_id)
                    
                    '''
                    
                    if article_id not in recentArticles.queue:
                        #print "good"
                        articles_random[article_id] = randomStruct()
                        articles_exp3[article_id] = exp3Struct(gamma)
                        articles_ucb1[article_id] = ucb1Struct()
                    #print 'second'
                    if recentArticles.full():
                        recentArticles.get()
                        
                    recentArticles.put(article_id)
                    
                    '''
                    
                    #print "yyyyy"
                        
                    
                    if article_id not in articles_ucb1: #if its a new article; add it to dictionaries
                        articles_random[article_id] = randomStruct()
                        articles_ucb1[article_id] = ucb1Struct()
                        articles_ucb1_1[article_id] = ucb1Struct()
                        articles_ucb1Alpha[article_id] = ucb1AlphaStruct()
                        
                    articles_ucb1[article_id].updatePta(UCB1ChosenNum)
                    articles_ucb1_1[article_id].updatePta(UCB1ChosenNum)
                    articles_ucb1Alpha[article_id].updatePta(UCB1ChosenNum, alpha)
                                                                                         
                pool_articleNum = len(currentArticles)
                                     
                # article picked by random strategy
                randomArticle = choice(currentArticles)                  
                
                ucb1Article = ucb1SelectArm(currentArticles)
                articlesPlayedByUCB1.append(ucb1Article)
                
                ucb1_1Article = ucb1SelectArm_1(currentArticles)
                ucb1AlphaArticle = ucb1AlphaSelectArm(currentArticles)
                #print 'chosenArticle:',  article_chosen, "UCB1ChosenArticle:", ucb1Article,
                #print " "
                #articles_ucb1[ucb1Article].numPlayed = articles_ucb1[ucb1Article].numPlayed + 1
                             
                # if random strategy article Picked by evaluation srategy
                if randomArticle == article_chosen:
                    
                    articles_random[randomArticle].learn_stats.clicks = articles_random[randomArticle].learn_stats.clicks + click
                    articles_random[randomArticle].learn_stats.accesses = articles_random[randomArticle].learn_stats.accesses + 1   
                                
                
                if ucb1Article == article_chosen:
                    UCB1ChosenNum = UCB1ChosenNum + 1
                    #print "UCB1nArticle: ", ucb1Article, "Click", clickChose
                    #print " "
                    articles_ucb1[article_chosen].learn_stats.clicks = articles_ucb1[article_chosen].learn_stats.clicks + click
                    articles_ucb1[article_chosen].learn_stats.accesses = articles_ucb1[article_chosen].learn_stats.accesses + 1
                    articles_ucb1[article_chosen].totalReward = articles_ucb1[article_chosen].totalReward + click
                    articles_ucb1[ucb1Article].numPlayed = articles_ucb1[ucb1Article].numPlayed + 1
  
                    '''                    
                    if click:
                        UCB1ClickNum = UCB1ClickNum + 1
                        print "UCB1nArticle: ", ucb1Article, "Click", click
                        print "UCB1ClickNum", UCB1ClickNum,
                        print " "
                     '''   
                if ucb1_1Article == article_chosen:
                    UCB1_1ChosenNum = UCB1_1ChosenNum + 1
                    #print "UCB1nArticle: ", ucb1Article, "Click", clickChose
                    #print " "
                    articles_ucb1_1[article_chosen].learn_stats.clicks = articles_ucb1_1[article_chosen].learn_stats.clicks + click
                    articles_ucb1_1[article_chosen].learn_stats.accesses = articles_ucb1_1[article_chosen].learn_stats.accesses + 1
                    articles_ucb1_1[article_chosen].totalReward = articles_ucb1_1[article_chosen].totalReward + click
                    articles_ucb1_1[ucb1Article].numPlayed = articles_ucb1_1[ucb1Article].numPlayed + 1
                    '''                    
                    if click:
                        UCB1ClickNum = UCB1ClickNum + 1
                        print "UCB1nArticle: ", ucb1Article, "Click", click
                        print "UCB1ClickNum", UCB1ClickNum,
                        print " "
                    '''
                if ucb1AlphaArticle == article_chosen:
                    UCB1AlphaChosenNum = UCB1AlphaChosenNum + 1
                    #print "UCB1nArticle: ", ucb1Article, "Click", clickChose
                    #print " "
                    articles_ucb1Alpha[article_chosen].learn_stats.clicks = articles_ucb1Alpha[article_chosen].learn_stats.clicks + click
                    articles_ucb1Alpha[article_chosen].learn_stats.accesses = articles_ucb1Alpha[article_chosen].learn_stats.accesses + 1
                    articles_ucb1Alpha[article_chosen].totalReward = articles_ucb1Alpha[article_chosen].totalReward + click
                    articles_ucb1Alpha[ucb1Article].numPlayed = articles_ucb1Alpha[ucb1Article].numPlayed + 1
                    '''                    
                    if click:
                        UCB1ClickNum = UCB1ClickNum + 1
                        print "UCB1nArticle: ", ucb1Article, "Click", click
                        print "UCB1ClickNum", UCB1ClickNum,
                        print " "
                    '''

                if (totalArticles % 20000) == 0:
                    # write observations for this batch
                    print "Yes"
                    printWrite()
                    print "NO"
                    batchStartTime = tim
                    epochArticles = {}
                    epochSelectedArticles = {}
                    #print "zzzz"
                    totalClicks = totalClicks + click
            # print stuff to screen and save parameters to file when the Yahoo! dataset file endd
            printWrite()
            #print "zzzz"
                
                
            






  
    

