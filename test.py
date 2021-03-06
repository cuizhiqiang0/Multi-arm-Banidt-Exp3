# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 13:08:04 2015

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
import Queue
from sets import Set

def articleAppear():
    def __init__(self):
        self.appearDate = Set()

def parseLine(line):
	line = line.split("|")

	tim, articleID, click = line[0].strip().split(" ")
	tim, articleID, click = int(tim), int(articleID), int(click)
 
	pool_articles = [l.strip().split(" ") for l in line[2:]]
	pool_articles = np.array([[int(l[0])] + [float(x.split(':')[1]) for x in l[1:]] for l in pool_articles])
	return tim, articleID, click, pool_articles


def save_to_file(fileNameWrite, dicts):
	with open(fileNameWrite, 'a+') as f:
         '''
         f.write(';'.join([str(x) for x in dicts]))
         f.write('\n')
         f.write(';'.join([str(dicts[x]) for x in dicts]))
         '''
         
         for x in dicts:
             f.write(str(x))
             f.write(','+str(dicts[x]))
             f.write('\n')


if __name__ == "__main__":
    
    totalArticles = {}
    AllArticleArray ={}
    timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M') 
    dataDays = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
    #dataDays = ['09', '10']
    #dataDays = ['01', '02']
    
    start_time = time.time()
    
    fileNameWrite = os.path.join(save_address, 'AllArticleIDAppearDate.csv')
    
    for dataDay in dataDays:
        start_time = time.time()        
        hours = 0 					# times the theta was reset if the mode is 'hours'		      
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay
        print "readFile", dataDay
        with open(fileName, 'r') as f:
            for line in f:
                tim, article_chosen, click, pool_articles = parseLine(line)
                
                for article in pool_articles:
                    article_id = int(article[0])
                    #article_id = article[0]
                    #print 'article_id', article_id
                    if article_id not in AllArticleArray:
                        AllArticleArray[article_id] = Set()
                        #print  AllArticleArray[article_id]
                        
                    AllArticleArray[article_id].add(dataDay)
                    #save_to_file(fileNameWrite, AllArticleArray)
                    #print  AllArticleArray[article_id]
        
        
                '''
                if article_chosen not in totalArticles:
                    totalArticles[article_chosen] = 1
                else:
                    totalArticles[article_chosen] = totalArticles[article_chosen] + 1

                for article in pool_articles:
                    article_id = article[0]
                    if article_id not in totalArticles:
                        totalArticles[article_id] = 1
                    else:
                        totalArticles[article_id] = totalArticles[article_id] + 1
                '''
        print "readFile", dataDay, "Time", time.time() - start_time
        #print time.time() - start_time
    print len(AllArticleArray)
    #print len(totalArticles)                       
    save_to_file(fileNameWrite, AllArticleArray)
    
    '''
    for dataDay in dataDays:
        start_time = time.time()
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay
        fileNameWrite = os.path.join(save_address,'Num'+ dataDay + timeRun + '.csv')
        with open(fileName, 'r') as f:
            for line in f:
                tim, article_chosen, click, pool_articles = parseLine(line)
                for article in pool_articles:
                    article_id = article[0]
                    if article_id not in totalArticles:
                        totalArticles[article_id] = 1
                    else:
                        totalArticles[article_id] = totalArticles[article_id] + 1
        print time.time() - start_time
    print totalArticles
    print len(totalArticles)                       
    save_to_file(fileNameWrite, totalArticles)
    '''
                    
                    
                
    
    
    
    '''
    recent = Queue.Queue(maxsize = 20)
    for i in range(50):
        recent.put(i)
        
        if recent.full():
            print recent.get()
    ID = np.array(range(50))
    print ID
    
    for i in ID:
        if i not in recent.queue:
            print i
        
        
        
    a = recent.get()
    print a
    b = recent.get()
    print a
    print b
    recent.put(32)
    recent.put(20)
    
    for i in range(19):
        print recent.get()
    '''
