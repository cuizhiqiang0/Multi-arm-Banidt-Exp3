# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 23:58:04 2015

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
import copy
import os

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

class loggedStruct():
    def __init__(self):
        self.stats = articleAccess()

class greedyStruct:
    def __init__(self):
        self.stats = articleAccess()
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
            
        
# This code simply reads one line from the source files of Yahoo!. Please see the yahoo info file to understand the format. I tested this part; so should be good but second pair of eyes could help
def parseLine(line):
	line = line.split("|")

	tim, articleID, click = line[0].strip().split(" ")
	tim, articleID, click = int(tim), int(articleID), int(click)
 
	pool_articles = [l.strip().split(" ") for l in line[2:]]
	pool_articles = np.array([[int(l[0])] + [float(x.split(':')[1]) for x in l[1:]] for l in pool_articles])
	return tim, articleID, click, pool_articles
	# returns time, id of selected article, if clicked i.e. the response, 


# tim: is time of the last observation in the batch
def save_to_file(fileNameWrite, recordedStats, tim):
	with open(fileNameWrite, 'a+') as f:
         f.write('data')
         f.write(',' + str(tim))
         f.write(',' + ','.join([str(x) for x in recordedStats]))
         f.write('\n')

# this code counts the line in a file; we need to divide data if we are re-setting theta multiple times a day. Could have been done based on time; i guess little harder to implement
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
    
if __name__ == '__main__':
    
    def printWrite():
        #recordedStats = [articles_logged[AllArticleIDpool[x]].stats.CTR for x in range(0, len(AllArticleIDpool))]
        recordedStats = [articles_greedy[AllArticleIDpool[x]].stats.CTR for x in range(0, len(AllArticleIDpool))]
        # write to file
        save_to_file(fileNameWriteCTR, recordedStats, tim)
    
    def re_initialize_article_greedyStructs():
        for x in articles_greedy:
            articles_greedy[x].reInitilize()
            
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
            
    #articles_logged = {}
    #articles_exp3 = {}
    #articles_ucb1 = {}
    articles_greedy = {}
    fileSig = 'GreedyCTR'
    gamma = 0.3 
    epsilon = 0.2
    UCB1ChosenNum = 0 
    GreedyChosenNum = 0
    totalArticles = 0 		# total articles seen whether part of evaluation strategy or not
    countLine = 0 			# number of articles in this batch. should be same as batch size; not so usefull
    timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M') 	# the current data time
    dataDays = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'] # the files from Yahoo that the algorithms will be run on; these files are indexed by days starting from May 1, 2009. this array starts from day 3 as also in the test data in the paper
    fileNameWriteCTR = os.path.join(save_address,  fileSig + '_' + timeRun + '.csv')   
    
    articleIDfilename = '/Users/Summer/Documents/Multi-arm-Banidt-Exp3/result/savedArticleID.txt'
    # Read all articleIDs from file
    with open(articleIDfilename, 'r') as f:
        for line in f:
            line = line.rstrip('\n').split('\t')
            AllArticleIDpool = copy.copy(line)
    # Initialize         
    for x in range(0,len(AllArticleIDpool)):
        #articles_logged[AllArticleIDpool[x]] = loggedStruct()
        #articles_exp3[AllArticleIDpool[x]] = exp3Struct(gamma)
        articles_greedy[AllArticleIDpool[x]] = greedyStruct()
            
    #save all articleID into a file for later use
    with open(fileNameWriteCTR, 'a+') as f:
        f.write('\nExp3CTR, New Run at  ' + datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
        f.write('\n, Time'+',' + ','.join([str(AllArticleIDpool[x]) for x in range(0, len(AllArticleIDpool))]))
        f.write('\n')
       
    for dataDay in dataDays:
        print "Processing", dataDay
        
        start_time = time.time()
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay 
        with open(fileName, 'r') as f:
            # reading file line ie observations running one at a time
            for line in f:  
                countLine = countLine + 1
                totalArticles = totalArticles + 1 
                
                # read the observation
                tim, article_chosen, click, pool_articles = parseLine(line)
                article_chosen = str(article_chosen)
                currentArticles = []
                total_weight = 0.0
                for article in pool_articles:
                    article_id = int(article[0])
                    article_id = str(article_id)
                    currentArticles.append(article_id)
                    articles_greedy[article_id].updateReward()
                    
                pool_articleNum = len(currentArticles)

                #LogCTR    
                #articles_logged[article_chosen].stats.accesses += 1
                #articles_logged[article_chosen].stats.clicks = click
                
                
                #UCB1 choose article
                greedyArticle = greedySelectArm(epsilon, currentArticles)
                greedyArticle = str(greedyArticle)
                
                # If the article chosen by Exp matches with log article
                if greedyArticle == article_chosen:
                    #print article_chosen
                    GreedyChosenNum = GreedyChosenNum + 1
                    articles_greedy[article_chosen].stats.clicks += click
                    articles_greedy[article_chosen].stats.accesses += 1
                    articles_greedy[article_chosen].totalReward = articles_greedy[article_chosen].totalReward + click
                    articles_greedy[greedyArticle].numPlayed = articles_greedy[greedyArticle].numPlayed + 1
                      
                if totalArticles%20000 ==0:
                    for x in range(0,len(AllArticleIDpool)):
                        articles_greedy[AllArticleIDpool[x]].stats.updateCTR
                        try:
                            articles_greedy[AllArticleIDpool[x]].stats.CTR = articles_greedy[AllArticleIDpool[x]].stats.clicks / articles_greedy[AllArticleIDpool[x]].stats.accesses
                        except ZeroDivisionError:
                            articles_greedy[AllArticleIDpool[x]].stats.CTR = -0.01
                        articles_greedy[AllArticleIDpool[x]].stats.accesses = 0.0
                        articles_greedy[AllArticleIDpool[x]].stats.clicks = 0.0
                    printWrite()  
            # print stuff to screen and save parameters to file when the Yahoo! dataset file endd
            printWrite()
            print "Done in ", time.time()-start_time, dataDay
            
            






  
    

