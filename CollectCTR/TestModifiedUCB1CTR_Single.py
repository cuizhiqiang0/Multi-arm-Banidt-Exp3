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

class ucb1Struct:
    def __init__(self):
        self.totalReward = 0.0
        self.numPlayed = 0
        self.pta = 0.0
        self.stats = articleAccess()

    def reInitilize(self): 
        self.totalReward = 0.0
        self.numPlayed = 0.0  
        self.pta=0.0
        
    def updatePta(self, allNumPlayed):
        try:
            self.pta = self.totalReward / self.numPlayed + np.sqrt(2*np.log(allNumPlayed) / self.numPlayed)
        except ZeroDivisionError:
            self.pta = 0.0
            
        
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
        recordedStats = [articles_ucb1[AllArticleIDpool[x]].stats.CTR for x in range(0, len(AllArticleIDpool))]
        # write to file
        save_to_file(fileNameWriteCTR, recordedStats, tim)
    
    def re_initialize_article_ucb1Structs():
        for x in articles_ucb1:
            articles_ucb1[x].reInitilize()
    
    def ucb1SelectArm(articles):
        flag = 0
        for x in articles:
            if articles_ucb1[x].numPlayed ==0:
                flag = 1
                return x
        if flag == 0:
            return max(np.random.permutation([(x, articles_ucb1[x].pta) for x in articles]), key = itemgetter(1))[0]
    
    modes = {0:'multiple', 1:'single'} 	# the possible modes that this code can be run in; 'multiple' means multiple days or all days so theta dont change; single means it is reset every day; hours is reset after some hours depending on the reInitPerDay. 
    mode = 'single'
    articles_ucb1 = {}
    gamma = 0.3 
    fileSig = 'UCB1CTR'
    UCB1ChosenNum = 0    
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
            #print AllArticleIDpool
    # Initialize         
    for x in range(0,len(AllArticleIDpool)):
        #articles_logged[AllArticleIDpool[x]] = loggedStruct()
        #articles_exp3[AllArticleIDpool[x]] = exp3Struct(gamma)
        articles_ucb1[AllArticleIDpool[x]] = ucb1Struct()
        #print AllArticleIDpool[x]
            
    #save all articleID into a file for later use
    with open(fileNameWriteCTR, 'a+') as f:
        f.write('\nUCB1CTR, New Run at  ' + datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
        f.write('\n, Time'+',' + ','.join([str(AllArticleIDpool[x]) for x in range(0, len(AllArticleIDpool))]))
        f.write('\n')
        
       
    for dataDay in dataDays:
        print "Processing", dataDay       
        start_time = time.time()
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay 
        if mode == 'single':
            re_initialize_article_ucb1Structs()
            UCB1ChosenNum = 0
            
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
                
                allNumPlayed = 0
                for article in pool_articles:
                    article_id = int(article[0])
                    article_id = str(article_id)
                    currentArticles.append(article_id)  
                    allNumPlayed += articles_ucb1[article_id].numPlayed
                    articles_ucb1[article_id].updatePta(allNumPlayed)
                for article in pool_articles:
                    article_id = int(article[0])
                    article_id = str(article_id)
                    currentArticles.append(article_id)  

                    articles_ucb1[article_id].updatePta(allNumPlayed)
                    
                pool_articleNum = len(currentArticles)

                #LogCTR    
                #articles_logged[article_chosen].stats.accesses += 1
                #articles_logged[article_chosen].stats.clicks = click
                
                
                #UCB1 choose article
                ucb1Article = ucb1SelectArm(currentArticles)
                ucb1Article = str(ucb1Article)
                # If the article chosen by Exp matches with log article
                if ucb1Article == article_chosen:
                    #print article_chosen
                    UCB1ChosenNum = UCB1ChosenNum + 1
                    articles_ucb1[article_chosen].stats.clicks += click
                    articles_ucb1[article_chosen].stats.accesses += 1
                    articles_ucb1[article_chosen].totalReward = articles_ucb1[article_chosen].totalReward + click
                    articles_ucb1[ucb1Article].numPlayed = articles_ucb1[ucb1Article].numPlayed + 1
            
                if totalArticles%20000 ==0:
                    for x in range(0,len(AllArticleIDpool)):
                        articles_ucb1[AllArticleIDpool[x]].stats.updateCTR
                        try:
                            articles_ucb1[AllArticleIDpool[x]].stats.CTR = articles_ucb1[AllArticleIDpool[x]].stats.clicks / articles_ucb1[AllArticleIDpool[x]].stats.accesses
                        except ZeroDivisionError:
                            articles_ucb1[AllArticleIDpool[x]].stats.CTR = -0.01 # negative CTR means this article didn't appear in the time interval
                            
                        articles_ucb1[AllArticleIDpool[x]].stats.accesses = 0.0
                        articles_ucb1[AllArticleIDpool[x]].stats.clicks = 0.0
                    printWrite()  
            # print stuff to screen and save parameters to file when the Yahoo! dataset file endd
            printWrite()
            print "Done in ", time.time()-start_time, dataDay
            
            






  
    

