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
import MABAlgorithms   # Import Multi-armed bandits algorithms


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
                       
        print countLine,
        print 'Exp3', exp3CTR ,
        print 'UCB1', ucb1CTR ,
        print 'Greedy', greedyCTR
        
        recordedStats = [randomCTR, greedyCTR, exp3CTR, ucb1CTR, LinUCBCTR ]
        # write to file
        save_to_file(fileNameWrite, articles_exp3, recordedStats, tim)
    
    
    def exp3SelectArm(articles):
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
            return max([(x, articles_ucb1[x].pta) for x in articles], key = itemgetter(1))[0]
    
    def greedySelectArm(cd, K, n, articles):
        if n == 0:
            epsilon = 1
        else:
            epsilon = min([1, (cd * K) / n ])
        if random.random() < epsilon:
            return choice(articles)
        else:
            return max([(x, articles_greedy[x].averageReward for x in articles]), key = itemgetter(1))[0]
                
        
    fileSig = '1_MultipleDay'								# depending on further environment parameters a file signature to remember those. for example if theta is set every two hours i can have it '2hours'; for 
    reInitPerDay = 12								# how many times theta is re-initialized per day

    gamma = 0.3                                                  # parameter in exp3
    cd = 20                                               # parameter in e-greedy
 
    # relative dictionaries for algorithms
    articles_exp3 = {}
    articles_ucb1 = {}
    articles_greedy = {}
    articles_random = {}
        
    
    totalArticles = 0 		# total articles seen whether part of evaluation strategy or not
    countLine = 0 			# number of articles in this batch. should be same as batch size; not so usefull
    resetInterval = 0 		# initialize; value assigned later; determined when 
    timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M') 	# the current data time
    dataDays = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'] # the files from Yahoo that the algorithms will be run on; these files are indexed by days starting from May 1, 2009. this array starts from day 3 as also in the test data in the paper
    fileNameWriteCTR = os.path.join(save_address,'CTR.csv')
    
    for dataDay in dataDays:
        start_time = time.time()
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay
        hours = 0 					# times the theta was reset if the mode is 'hours'		
        batchStartTime = 0 			# time of first observation of the batch
        fileNameWrite = os.path.join(save_address,  fileSig +dataDay + timeRun + '.csv')

        time_open= time.time()    
        # put some new data in file for readability
        with open(fileNameWrite, 'a+') as f:
            f.write('\nNew Run at  ' + datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
            f.write('\n, Time, randomCTR; greedyCTR, exp3CTR; ucb1CTR; LinUCBCTR \n')
            print fileName, fileNameWrite, dataDay, resetInterval
        print 'opentime', time.time() - time_open
        
        with open(fileName, 'r') as f:
            # reading file line ie observations running one at a time
            
            for line in f:  
                line_time = time.time()
                # read the observation
                time_read = time.time()
                tim, article_chosen, click, pool_articles = parseLine(line)
                print "parse time", time.time() - time_read
                    
                # number of observations seen in this batch; reset after start of new batch
                countLine = countLine + 1
               
   
                # article ids for articles in the current pool for this observation
                currentArticles = []
                total_weight = 0
                time_firstLoop = time.time()
                for article in pool_articles:                    
                    article_id = article[0]
                    currentArticles.append(article_id)
                    
                    if article_id not in articles_exp3: #if its a new article; add it to dictionaries
                        articles_random[article_id] = randomStruct()
                        articles_exp3[article_id] = exp3Struct(gamma)
                        articles_ucb1[article_id] = ucb1Struct()
                        articles_greedy[article_id] = greedyStruct()
                        articles_extremeGreedy[article_id] = extremeGreedyStruct()
                        
                    #total_weight = sum([articles_exp3[x].weights for x in pool_articles[:0]])
                    total_weight = total_weight + articles_exp3[article_id].weights
                    
                pool_articleNum = len(currentArticles)
                print "firstLoop", time.time() - time_firstLoop
                
                time_secondeLoop = time.time()
                
                for article in pool_articles:
                    article_id = article[0]
                    articles_exp3[article_id].updatePta(pool_articleNum, total_weight)
                    articles_ucb1[article_id].updatePta(UCB1ChosenNum)
                    articles_greedy[article_id].updateReward()
                    articles_extremeGreedy[article_id].updateReward()
                print "secondLoop", time.time() - time_secondeLoop
                
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
                
                greedyArticle = greedySelectArm(cd, len(currentArticles), GreedyChosenNum, currentArticles)
                #articles_greedy[greedyArticle].numPlayed = articles_greedy[greedyArticle].numPlayed + 1
                
                extremeGreedyArticle = extremeGreedySelectArm(currentArticles)
                
                print "SelectionTIme", time.time() - time_selection
                
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
                
                if ucb1Article == article_chosen:
                    UCB1ChosenNum = UCB1ChosenNum + 1
                    articles_ucb1[article_chosen].learn_stats.clicks = articles_ucb1[article_chosen].learn_stats.clicks + click
                    articles_ucb1[article_chosen].learn_stats.accesses = articles_ucb1[article_chosen].learn_stats.accesses + 1
                    articles_ucb1[article_chosen].totalReward = articles_ucb1[article_chosen].totalReward + click
                    articles_ucb1[ucb1Article].numPlayed = articles_ucb1[ucb1Article].numPlayed + 1
 
                if greedyArticle == article_chosen:
                    GreedyChosenNum = GreedyChosenNum + 1
                    articles_greedy[article_chosen].learn_stats.clicks = articles_greedy[article_chosen].learn_stats.clicks + click
                    articles_greedy[article_chosen].learn_stats.accesses = articles_greedy[article_chosen].learn_stats.accesses + 1
                    articles_greedy[article_chosen].totalReward = articles_greedy[article_chosen].totalReward + click
                    articles_greedy[greedyArticle].numPlayed = articles_greedy[greedyArticle].numPlayed + 1
                
                if extremeGreedyArticle == article_chosen:
                    articles_extremeGreedy[article_chosen].learn_stats.clicks = articles_extremeGreedy[article_chosen].learn_stats.clicks + click
                    articles_extremeGreedy[article_chosen].learn_stats.accesses = articles_extremeGreedy[article_chosen].learn_stats.accesses + 1
                    articles_extremeGreedy[article_chosen].totalReward = articles_extremeGreedy[article_chosen].totalReward + click
                    articles_extremeGreedy[article_chosen].numPlayed = articles_extremeGreedy[article_chosen].numPlayed + 1
                print "chosen time", time.time() - time_chose            
                if countLine%20000 ==0:
                    # write observations for this batch
                    write_time = time.time()
                    printWrite()
                    print "write time", time.time() - write_time
                    batchStartTime = tim
                    epochArticles = {}
                    epochSelectedArticles = {}
                print 'oneLineTotalTime', time.time() - line_time

            print time.time() - time_oneFile
            # print stuff to screen and save parameters to file when the Yahoo! dataset file endd
            printWrite()
            print 'UCb1ChosenNum', UCB1ChosenNum
            print 'Exp3ChosenNum', Exp3ChosenNum
            print 'GreedyChosenNum', GreedyChosenNum
            print 'RandomChosenNum', RandomChosenNum
                
            






  
    

