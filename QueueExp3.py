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
        
    def reInitilize(self):
        self.weights = 1.0
        self.pta=0.0
          
    def updatePta(self, n_arms, total_weight):
        n_arms = n_arms
        self.pta= (1-self.gamma) * (self.weights / total_weight)
        self.pta= self.pta + (self.gamma) * (1.0 / float(n_arms))
 
    def updateWeight(self, n_arms, reward):
        n_arms = n_arms
        X=reward/self.pta
        growth_factor = math.exp((self.gamma/n_arms)*X)
        self.weights = self.weights * growth_factor

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

class myQueue:
    def __init__(self):
        self.dic = {}
        self.QueueLength = len(self.dic)
    def push(self, articleID):
        if articleID in self.dic:
            self.dic[articleID] += 1
        else:
            self.dic[articleID] = 0
    def pop(self):
        removed = min(self.dic, key=self.dic.get)
        a = copy.copy(removed)
        del self.dic[removed]
        return a
    def decreaseAll(self):
        for article in self.dic:
            self.dic[article] = self.dic[article] - 0.05
    def initialize(self):
        self.dic = {}
        
        
        

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
        
        exp3LA = sum([articles_exp3[x].learn_stats.accesses for x in articles_exp3])
        exp3C = sum([articles_exp3[x].learn_stats.clicks for x in articles_exp3]) 
        exp3CTR = sum([articles_exp3[x].learn_stats.clicks for x in articles_exp3]) / sum([articles_exp3[x].learn_stats.accesses for x in articles_exp3])
        
        ucb1LA = sum([articles_ucb1[x].learn_stats.accesses for x in articles_ucb1])
        ucb1C = sum([articles_ucb1[x].learn_stats.clicks for x in articles_ucb1])
        ucb1CTR = sum([articles_ucb1[x].learn_stats.clicks for x in articles_ucb1]) / sum([articles_ucb1[x].learn_stats.accesses for x in articles_ucb1])
        
        greedyLA = sum([articles_greedy[x].learn_stats.accesses for x in articles_greedy])
        greedyC = sum([articles_greedy[x].learn_stats.clicks for x in articles_greedy])
        greedyCTR = sum([articles_greedy[x].learn_stats.clicks for x in articles_greedy]) / sum([articles_greedy[x].learn_stats.accesses for x in articles_greedy])  
        
        print totalArticles,
        print 'Exp3Lrn', exp3CTR / randomCTR,
        print 'UCB1', ucb1CTR / randomCTR,
        print 'Greedy', greedyCTR / randomCTR,
    
        print ' '
        
        recordedStats = [randomLA, randomC, exp3LA, exp3C, ucb1LA, ucb1C, greedyLA, greedyC, exp3CTR / randomCTR, ucb1CTR / randomCTR, greedyCTR / randomCTR]
        # write to file
        save_to_file(fileNameWrite, articles_exp3, recordedStats, epochArticles, epochSelectedArticles, tim)
    
            
    # this function reset weight for all exp3
    def re_initialize_article_exp3Structs():
        for x in articles_exp3:
            articles_exp3[x].reInitilize()
            
    def re_initialize_article_ucb1Structs():
        for x in articles_ucb1:
            articles_ucb1[x].reInitilize()
    
    def re_initialize_article_greedyStructs():
        for x in articles_greedy:
            articles_greedy[x].reInitilize()
            
    def categorical_draw(articles):
        z = random.random()
        cum_pta = 0.0
        #flag = 0
        for x in articles:
            cum_pta = cum_pta + articles_exp3[x].pta
            if cum_pta > z:
                return x
    def ucb1SelectArm(articles):
        flag = 0
        for x in articles:
            if articles_ucb1[x].numPlayed ==0:
                flag = 1
                return x
        if flag == 0:
            return max(np.random.permutation([(x, articles_ucb1[x].pta) for x in articles]), key = itemgetter(1))[0]
    
    def greedySelectArm(epsilon, articles):
        '''
        if n == 0:
            epsilon = 1
        else:
            epsilon = min([1, (cd * K) / n ])
        '''
        if random.random() < epsilon:
            return choice(articles)
        else:
            return max(np.random.permutation([(x, articles_greedy[x].averageReward) for x in articles]), key = itemgetter(1))[0]
            
    def extremeGreedySelectArm(articles):
        return max(np.random.permutation([(x, articles_extremeGreedy[x].averageReward) for x in articles]), key = itemgetter(1))[0]
        
            
    modes = {0:'multiple', 1:'single', 2:'hours'} 	# the possible modes that this code can be run in; 'multiple' means multiple days or all days so theta dont change; single means it is reset every day; hours is reset after some hours depending on the reInitPerDay. 
    mode = 'multiple' 									# the selected mode
    fileSig = 'Modified_Q15_Multi'								# depending on further environment parameters a file signature to remember those. for example if theta is set every two hours i can have it '2hours'; for 
    reInitPerDay = 12								# how many times theta is re-initialized per day

    gamma = 0.3                                                  # parameter in exp3
    epsilon = 0.2                                               # parameter in e-greedy
 
    # relative dictionaries for algorithms
    articles_exp3 = {}
    articles_ucb1 = {}
    articles_greedy = {}
    articles_random = {}
    articlesPlayedByUCB1 = {}
    MyQExp3 = myQueue()
    MyQUCB1 = myQueue()
    MyQGreedy = myQueue()
    
    QueueSize = 15
    
    
    UCB1ChosenNum = 0
    Exp3ChosenNum = 0
    GreedyChosenNum = 0
    RandomChosenNum = 0
    
    
    ctr = 1 				# overall ctr
    totalArticles = 0 		# total articles seen whether part of evaluation strategy or not
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
            fileNameWrite = os.path.join(save_address, fileSig + dataDay + timeRun + '.csv')
            re_initialize_article_exp3Structs()
            re_initialize_article_ucb1Structs()
            re_initialize_article_greedyStructs()
            MyQ.initialize()
            
            Exp3ChosenNum = 0
            UCB1ChosenNum = 0
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
            f.write('\n, Time, randomAccesses; randomClicks; exp3Access; exp3Clicks; ucb1Accesses; ucb1Clicks; greedyAccesses; greedyClicks; exp3CTRRatio; ucb1CTRRatio; greedyCTRRatio, Article Access; Clicks; ID; Theta, ID; epochArticles, ID ;epochSelectedArticles \n')
            print fileName, fileNameWrite, dataDay, resetInterval
      
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
                    Exp3ChosenNum = 0
                    UCB1ChosenNum = 0
                    GreedyChosenNum = 0
                    RandomChosenNum = 0
                    
                    re_initialize_article_exp3Structs()     #Not sure whether to re-initialize exp3Struct
                    re_initialize_article_ucb1Structs()
                    re_initialize_article_greedyStructs()
                    MyQ.initialize()
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
                time_firstLoop = time.time()
                '''
                if countLine%10 == 0:
                    MyQ.decreaseAll() # every time when you need to choose one article from the pool
                '''
                
                for article in pool_articles:                    
                    article_id = article[0]
                    currentArticles.append(article_id)
                    
                    
                    
                    if article_id not in articles_exp3: #if its a new article; add it to dictionaries
                        articles_random[article_id] = randomStruct()
                        articles_exp3[article_id] = exp3Struct(gamma)
                        articles_ucb1[article_id] = ucb1Struct()
                        articles_greedy[article_id] = greedyStruct()
                    '''     
                    if MyQ.QueueLength < QueueSize:
                        MyQ.push(article_id)
                    elif article_id in MyQ.dic:
                        MyQ.dic[article_id] += 1
                    else:
                        a=MyQ.pop()
                        articles_exp3[a].reInitilize()
                        articles_ucb1[a].reInitilize()
                        articles_greedy[a].reInitilize()                      
                        MyQ.push(article_id)
                    '''   
                        
                    if article_id not in epochArticles:
                        epochArticles[article_id] = 1
                    else:
                        # we also count the times article appeared in selection pool in this batch
                        epochArticles[article_id] = epochArticles[article_id] + 1
                    
                    #total_weight = sum([articles_exp3[x].weights for x in pool_articles[:0]])
                    total_weight = total_weight + articles_exp3[article_id].weights
                    
                pool_articleNum = len(currentArticles)
                
                time_secondeLoop = time.time()
                
                for article in pool_articles:
                    article_id = article[0]
                    articles_exp3[article_id].updatePta(pool_articleNum, total_weight)
                    articles_ucb1[article_id].updatePta(UCB1ChosenNum)
                    articles_greedy[article_id].updateReward()
                
                time_selection = time.time()
                if article_chosen not in epochSelectedArticles:
                    epochSelectedArticles[article_chosen] = 1
                else:
                    epochSelectedArticles[article_chosen] = epochSelectedArticles[article_chosen] + 1					
                    # if articles_LinUCB[article_id].pta < 0: print 'PTA', articles_LinUCB[article_id].pta,
                
                # article picked by random strategy
                randomArticle = choice(currentArticles)                  
                # article picked by exp3
                exp3Article = categorical_draw(currentArticles)
                # article picked by ucb1
                ucb1Article = ucb1SelectArm(currentArticles)
                #articles_ucb1[ucb1Article].numPlayed = articles_ucb1[ucb1Article].numPlayed + 1
                
                greedyArticle = greedySelectArm(epsilon, currentArticles)
                #articles_greedy[greedyArticle].numPlayed = articles_greedy[greedyArticle].numPlayed + 1
                
                time_chose = time.time()
                # if random strategy article Picked by evaluation srategy
                if randomArticle == article_chosen:
                    RandomChosenNum = RandomChosenNum + 1
                    articles_random[randomArticle].learn_stats.clicks = articles_random[randomArticle].learn_stats.clicks + click
                    articles_random[randomArticle].learn_stats.accesses = articles_random[randomArticle].learn_stats.accesses + 1   
               
                # if exp3 article is chosen by evalution strategy
                if exp3Article == article_chosen:
                    Exp3ChosenNum = Exp3ChosenNum + 1
                    articles_exp3[article_chosen].learn_stats.clicks = articles_exp3[article_chosen].learn_stats.clicks + click
                    articles_exp3[article_chosen].learn_stats.accesses = articles_exp3[article_chosen].learn_stats.accesses + 1
                    if click:
                        articles_exp3[article_chosen].updateWeight(pool_articleNum, click)
                        
                    MyQExp3.decreaseAll() 
                    for article in pool_articles: 
                        article_id = article[0]
                        if MyQExp3.QueueLength < QueueSize:
                            MyQExp3.push(article_id)
                        elif article_id in MyQExp3.dic:
                            MyQExp3.dic[article_id] += 1
                        else:
                            a=MyQExp3.pop()
                            articles_exp3[a].reInitilize()
                            MyQExp3.push(article_id)
                
                if ucb1Article == article_chosen:
                    UCB1ChosenNum = UCB1ChosenNum + 1
                    articles_ucb1[article_chosen].learn_stats.clicks = articles_ucb1[article_chosen].learn_stats.clicks + click
                    articles_ucb1[article_chosen].learn_stats.accesses = articles_ucb1[article_chosen].learn_stats.accesses + 1
                    articles_ucb1[article_chosen].totalReward = articles_ucb1[article_chosen].totalReward + click
                    articles_ucb1[ucb1Article].numPlayed = articles_ucb1[ucb1Article].numPlayed + 1
                    
                    MyQUCB1.decreaseAll() 
                    for article in pool_articles: 
                        article_id = article[0]
                        if MyQUCB1.QueueLength < QueueSize:
                            MyQUCB1.push(article_id)
                        elif article_id in MyQ.dic:
                            MyQUCB1.dic[article_id] += 1
                        else:
                            a=MyQUCB1.pop()
                            articles_ucb1[a].reInitilize()
                            MyQUCB1.push(article_id)
 
                if greedyArticle == article_chosen:
                    GreedyChosenNum = GreedyChosenNum + 1
                    articles_greedy[article_chosen].learn_stats.clicks = articles_greedy[article_chosen].learn_stats.clicks + click
                    articles_greedy[article_chosen].learn_stats.accesses = articles_greedy[article_chosen].learn_stats.accesses + 1
                    articles_greedy[article_chosen].totalReward = articles_greedy[article_chosen].totalReward + click
                    articles_greedy[greedyArticle].numPlayed = articles_greedy[greedyArticle].numPlayed + 1
                    
                    MyQGreedy.decreaseAll() 
                    for article in pool_articles: 
                        article_id = article[0]
                        if MyQGreedy.QueueLength < QueueSize:
                            MyQGreedy.push(article_id)
                        elif article_id in MyQ.dic:
                            MyQGreedy.dic[article_id] += 1
                        else:
                            a=MyQGreedy.pop()
                            articles_greedy[a].reInitilize()
                            MyQGreedy.push(article_id)
                
               
                if totalArticles%20000 ==0:
                    # write observations for this batch
                    write_time = time.time()
                    printWrite()
                    batchStartTime = tim
                    epochArticles = {}
                    epochSelectedArticles = {}

            # print stuff to screen and save parameters to file when the Yahoo! dataset file endd
            printWrite()
            






  
    

