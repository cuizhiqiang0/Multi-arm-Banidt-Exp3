# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 22:40:42 2015

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

class exp3Struct:
    def __init__(self, gamma):
        self.gamma = gamma
        self.weights = 1.0
        self.pta = 0.0
        self.stats = articleAccess()
        
    def reInitilize(self):
        self.weights = 1.0
        self.pta=0.0
          
    def updatePta(self, n_arms, total_weight):
        #n_arms = n_arms
        self.pta= (1-self.gamma) * (self.weights / total_weight)
        self.pta= self.pta + (self.gamma) * (1.0 / float(n_arms))
 
    def updateWeight(self, n_arms, reward):
        #n_arms = n_arms
        X=reward/self.pta
        growth_factor = math.exp((self.gamma/n_arms)*X)
        self.weights = self.weights * growth_factor
        
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
        recordedStats = [articles_exp3[AllArticleIDpool[x]].stats.accesses for x in range(0, len(AllArticleIDpool))]
        # write to file
        save_to_file(fileNameWriteCTR, recordedStats, tim)
    
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

    #articles_logged = {}
    modes = {0:'multiple', 1:'single'} 	# the possible modes that this code can be run in; 'multiple' means multiple days or all days so theta dont change; single means it is reset every day; hours is reset after some hours depending on the reInitPerDay. 
    mode = 'multiple' 
    articles_exp3 = {}
    fileSig = 'Exp3Access_AvoidOld'
    gamma = 0.3     
    totalArticles = 0 		# total articles seen whether part of evaluation strategy or not
    countLine = 0 			# number of articles in this batch. should be same as batch size; not so usefull
    timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M') 	# the current data time
    dataDays = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'] # the files from Yahoo that the algorithms will be run on; these files are indexed by days starting from May 1, 2009. this array starts from day 3 as also in the test data in the paper
    fileNameWriteCTR = os.path.join(save_address,  fileSig + '_' + timeRun + '.csv')  
    
    #articleIDfilename = '/Users/Summer/Documents/Multi-arm-Banidt-Exp3/result/temp.txt'
    # Read all articleIDs from file
    with open(articleIDfilename, 'r') as f:
        for line in f:
            line = line.rstrip('\n').split('\t')
            AllArticleIDpool = copy.copy(line)
    # Initialize         
    for x in range(0,len(AllArticleIDpool)):
        #articles_logged[AllArticleIDpool[x]] = loggedStruct()
        articles_exp3[AllArticleIDpool[x]] = exp3Struct(gamma)
        #print AllArticleIDpool[x]
            
    #save all articleID into a file for later use
    with open(fileNameWriteCTR, 'a+') as f:
        f.write('\nExp3Accesses, New Run at  ' + datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
        f.write('\n, Time'+',' + ','.join([str(AllArticleIDpool[x]) for x in range(0, len(AllArticleIDpool))]))
        f.write('\n')
       
    for dataDay in dataDays:
        print "Processing", dataDay
        start_time = time.time()
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay
        if mode == 'single':
            re_initialize_article_exp3Structs()
        
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
                    if dataDay == '01' or dataDay == '02' or dataDay == '06':
                        currentArticles.append(article_id)
                    if dataDay == '03':
                        if article_id != '109536':
                            currentArticles.append(article_id)
    
                        if article_id != '109524':
                            currentArticles.append(article_id)       
                            
                    if dataDay == '04':
                        if article_id !='109536':
                            currentArticles.append(article_id)
    
                        if article_id !='109524':
                            currentArticles.append(article_id)
                            
                    if dataDay == '05':
                        if article_id !='109476':
                            currentArticles.append(article_id)
                            
                    if dataDay == '07':
                        if article_id !='109635':
                            currentArticles.append(article_id)
                            print 'delete 109635 from', dataDay
                            
                    if dataDay == '08':
                        if article_id !='109635':
                            currentArticles.append(article_id)
                            
                    if dataDay == '09':
                        if article_id !='109667':
                            currentArticles.append(article_id)
                            
                        if article_id !='109697':
                            currentArticles.append(article_id)
                            
                    if dataDay == '10':
                        if article_id !='109697':
                            currentArticles.append(article_id)
                            
                    if currentArticles.__contains__(article_id):     
                        total_weight = total_weight + articles_exp3[article_id].weights
                    
                   
                    
                pool_articleNum = len(currentArticles)
           
                for article in currentArticles:
                    articles_exp3[article].updatePta(pool_articleNum, total_weight)
                #LogCTR    
                #articles_logged[article_chosen].stats.accesses += 1
                #articles_logged[article_chosen].stats.clicks = click
                
                # Exp3 Chose article
                exp3Article = categorical_draw(currentArticles)
                
                # If the article chosen by Exp matches with log article
                if exp3Article == article_chosen:
                    article_chosen = str(article_chosen)
                    articles_exp3[article_chosen].stats.clicks +=click
                    articles_exp3[article_chosen].stats.accesses += 1
                    if click:
                        articles_exp3[article_chosen].updateWeight(pool_articleNum, click)
           
                if totalArticles%20000 ==0:
                    printWrite()
                    for x in range(0,len(AllArticleIDpool)):
                        try:
                            articles_exp3[AllArticleIDpool[x]].stats.CTR = articles_exp3[AllArticleIDpool[x]].stats.clicks / articles_exp3[AllArticleIDpool[x]].stats.accesses
                        except ZeroDivisionError:
                            articles_exp3[AllArticleIDpool[x]].stats.CTR = -0.02 # negative CTR means this article didn't appear in the time interval
          
                        articles_exp3[AllArticleIDpool[x]].stats.accesses = 0.0
                        articles_exp3[AllArticleIDpool[x]].stats.clicks = 0.0                       
                    
                    
                      
            # print stuff to screen and save parameters to file when the Yahoo! dataset file endd
            printWrite()
            print "Done in ", time.time()-start_time, dataDay
            
            






  
    

