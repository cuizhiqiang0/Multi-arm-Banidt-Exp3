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
        recordedStats = [articles_logged[AllArticleIDpool[x]].stats.CTR for x in range(0, len(AllArticleIDpool))]
        # write to file
        save_to_file(fileNameWrite, recordedStats, tim)
    


    articles_logged = {}
    fileSig = 'LogCT_Accumlate'
          
    totalArticles = 0 		# total articles seen whether part of evaluation strategy or not
    countLine = 0 			# number of articles in this batch. should be same as batch size; not so usefull
    timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M') 	# the current data time
    dataDays = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'] # the files from Yahoo that the
    articleIDfilename = '/Users/Summer/Documents/Multi-arm-Banidt-Exp3/result/temp.txt'
    # Read all articleIDs from file
    with open(articleIDfilename, 'r') as f:
        for line in f:
            line = line.rstrip('\n').split('\t')
            AllArticleIDpool = copy.copy(line)
    # Initialize         
    for x in range(0,len(AllArticleIDpool)):
        articles_logged[AllArticleIDpool[x]] = loggedStruct()
            
    #save all articleID into a file for later use

       
    for dataDay in dataDays:
        print "Processing", dataDay
        
        start_time = time.time()
        #print "Done in ", time.time()-start_time, dataDay
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay
        fileNameWrite = os.path.join(save_address, fileSig + dataDay + timeRun + '.csv')
        
        with open(fileNameWrite, 'a+') as f:
            f.write('\nLogAccumutiveCTR, New Run at  ' + datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
            f.write('\n, Time'+',' + ','.join([str(AllArticleIDpool[x]) for x in range(0, len(AllArticleIDpool))]))
            f.write('\n')
        
        with open(fileName, 'r') as f:
            # reading file line ie observations running one at a time
            for line in f:  
                # read the observation
                tim, article_chosen, click, pool_articles = parseLine(line)
                article_chosen = str(article_chosen)
                #print "article_chosen", article_chosen
                articles_logged[article_chosen].stats.accesses += 1
                articles_logged[article_chosen].stats.clicks += click
                    
               
                # number of observations seen in this batch; reset after start of new batch
                countLine = countLine + 1
                totalArticles = totalArticles + 1              
            
                if totalArticles%20000 ==0:
                    for x in range(0,len(AllArticleIDpool)):
                        #AllArticleIDpool[x] = str(AllArticleIDpool[x])
                        #print AllArticleIDpool[x]
                        #print articles_logged[AllArticleIDpool[x]].stats.accesses
                        #print articles_logged[AllArticleIDpool[x]].stats.clicks
                        #print articles_logged[AllArticleIDpool[x]].stats.CTR
                        #articles_logged[AllArticleIDpool[x]].stats.updateCTR
                        #print articles_logged[AllArticleIDpool[x]].stats.CTR
                        
                        try:
                            articles_logged[AllArticleIDpool[x]].stats.CTR = articles_logged[AllArticleIDpool[x]].stats.clicks / articles_logged[AllArticleIDpool[x]].stats.accesses
                        except ZeroDivisionError:
                            articles_logged[AllArticleIDpool[x]].stats.CTR = -0.5
                        #print "CTR", articles_logged[AllArticleIDpool[x]].stats.CTR
                        # reset CTR
                    printWrite()
                        
                      
            # print stuff to screen and save parameters to file when the Yahoo! dataset file endd
            printWrite()
            
            print "Done in ", time.time()-start_time, dataDay
            
            






  
    

