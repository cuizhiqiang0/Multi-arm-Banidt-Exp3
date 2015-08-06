# -*- coding: utf-8 -*-
"""
Created on Wed May 20 09:39:52 2015

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
from numpy import array
from sets import Set
from collections import defaultdict
from scipy.cluster.vq import vq, kmeans, whiten, kmeans2

def articleAppear():
    def __init__(self):
        self.appearDate = Set()
# extract unique rows from matrix a
def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

def parseLine(line):
	line = line.split("|")

	#tim, articleID, click = line[0].strip().split(" ")
	#tim, articleID, click = int(tim), int(articleID), int(click)
	# user_features = np.array([x for ind,x in enumerate(re.split(r"[: ]", line[1])) if ind%2==0][1:])
	#user_features = np.array([float(x.strip().split(':')[1]) for x in line[1].strip().split(' ')[1:]])

	pool_articles = [l.strip().split(" ") for l in line[2:]]
	pool_articles = np.array([[int(l[0])] + [float(x.split(':')[1]) for x in l[1:]] for l in pool_articles])
	return pool_articles

def save_to_file(fileNameWrite, dicts):
	with open(fileNameWrite, 'a+') as f:     
         for x in dicts:
            f.write(str(x)+';')
            f.write('   '.join(str(dicts[x][i]) for i in range(len(dicts[x]))))
            f.write('\n')

if __name__ == "__main__":
    
    
   
    totalArticles = {}
    timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M') 
    dataDays = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
    #dataDays = ['01', '02']
    #dataDay = 'test'
    
    start_time = time.time()
    sig = 'test'
    fileNameWrite = os.path.join(save_address, 'AllArticles'+str(timeRun)+ '.txt')
    fileNameWrite1 = os.path.join(save_address, 'assignment' + sig+'.csv')
    fileNameWriteCluster =  '/Users/Summer/Dropbox/workspace/CoLinUCBRealData/data/kmeans_model.dat'
    fileNameRead = os.path.join(save_address, 'AllArticles.txt')
    i = 0
    
    for dataDay in dataDays:          
        fileName = yahoo_address + "/ydata-fp-td-clicks-v1_0.200905" + dataDay
        #fileName = yahoo_address + '/Test'
    
    
        with open(fileName, 'r') as f:       
            for line in f:
                pool_articles = parseLine(line)
                for article in pool_articles:
                    article_id = article[0]
                    article_featureVector = article[1:6]
                    if article_id not in totalArticles:
                        totalArticles[article_id] = np.asarray(article_featureVector) 
                    
    print 'finsih read'        
    save_to_file(fileNameWrite, totalArticles)

    '''
    #read from files
    with open(fileNameRead, 'r') as f:
        ArticleIDs = []
        ArticleFeatures = []
        for line in f:
            vec = []
            line = line.split(';')
            
            ArticleIDs.append(float(line[0]))
            #print line
    
            word = line[1].split('  ')
            for i in range(5):
                vec.append(float(word[i]))
            ArticleFeatures.append(np.asarray(vec))
        ArticleFeatures = np.asarray(ArticleFeatures)
    print  ArticleIDs[1], ArticleFeatures[1]
    '''

    
    
   
    

    
    
