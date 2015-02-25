# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 12:55:00 2015

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

class Stats():
    def __init__(self):
        self.accesses = 0.0
        self.clicks = 0.0
        self.CTR = 0.0
    def updateCTR(self):
        try:
            self.CTR = self.clicks / self.accesses
        except ZeroDivisionError:
            self.CTR = 0
        return self.CTR
        
    def addrecord(self, click):
        self.clicks += click
        self.accesses +=1
        self.updateCTR()


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
            self.dic[article] = self.dic[article] - 1
    def initialize(self):
        self.dic = {}

class RandomStruct:
    def __init__(self, id):
        self.stats = Stats()
        self.id = id
        
class Exp3Struct:
    def __init__(self, gamma, id):
        self.id = id
        self.gamma = gamma
        self.weights = 1.0
        self.pta = 0.0
        self.stats = Stats()
    def reInitilize(self):
        self.weights = 1.0
        self.pta = 0.0        
    def updateWeight(self, n_arms, reward):
        X = reward / self.pta
        growth_factor = math.exp((self.gamma / n_arms)*X)
        self.weights = self.weights * growth_factor
    def updatePta(self, n_arms, total_weight):
        self.pta = (1-self.gamma) * (self.weights / total_weight)
        self.pta +=(self.gamma)*(1.0/float(n_arms))
    def applyDecay(self, decay, duration):
        self.weights *= (decay**duration)
        
class UCB1Struct:
    def __init__(self, id):
        self.id = id
        self.totalReward = 0
        self.numPlayed = 0
        self.pta = 0.0
        self.stats = Stats()
    def reInitilize(self):
        self.totalReward = 0.0
        self.numPlayed = 0.0
        self.pta = 0.0  
    def updateParameter(self, click):
        self.totalReward += click
        self.numPlayed +=1
        
    def updatePta(self, allNumPlayed):
        try:
            self.pta = self.totalReward / self.numPlayed + np.sqrt(2*np.log(allNumPlayed) / self.numPlayed)
        except ZeroDivisionError:
            self.pta = 0.0
    def applyDecay(self, decay, duration):  # where to add decay
        self.totalReward *=(decay**duration)
    
        

class RandomAlgorithm:
    def __init__(self):
        self.articles = {}
    def decide(self, pool_articles):
        for x in pool_articles:
            if x.id not in pool_articles:
                self.articles[x.id] = RandomStruct(x.id)
        return choice(pool_articles)
    def updateWeight(self, pickedArticle, ArticleNum, click):
        a = 1        
    def getarticleCTR(self, article_id):
        return self.articles[article_id].stats.CTR
        
class Exp3Algorithm:
    def __init__(self, gamma, decay = None):
        self.articles = {}
        self.gamma = gamma
        self.decay = decay
    
    def decide(self, pool_articles):
        r = random.random()
        cum_pta = 0.0        
        total_Weights = 0.0
        for x in pool_articles:
            if x.id not in self.articles:
                self.articles[x.id] = Exp3Struct(self.gamma, x.id)
            total_Weights += self.articles[x.id].weights
        for x in pool_articles:
            self.articles[x.id].updatePta(len(pool_articles), total_Weights)
            cum_pta += self.articles[x.id].pta
            if cum_pta >r:
                return x
    def updateWeight(self, pickedArticle, ArticleNum, click):
        self.articles[pickedArticle.id].updateWeight(ArticleNum, click)
        if self.decay:
            self.applyDecayToAll(1)
    
    def applyDecayToAll(self, duration):
        for key in self.articles:
            self.articles[key].applyDecay(self.decay, duration)
    
    def getarticleCTR(self, article_id):
        return self.articles[article_id].stats.CTR

class Exp3QueueAlgorithm:
    def __init__(self, gamma, decay = None):
        self.articles = {}
        self.gamma = gamma
        self.decay = decay
    
    def decide(self, pool_articles):
        MyQ = myQueue()
        QueueSize = 15
        MyQ.decreaseAll()
        
        r = random.random()
        cum_pta = 0.0        
        total_Weights = 0.0
        for x in pool_articles:
            if x.id not in self.articles:
                self.articles[x.id] = Exp3Struct(self.gamma, x.id)
            
            if MyQ.QueueLength < QueueSize:
                MyQ.push(x)
            elif x.id in MyQ.dic:
                MyQ.dic[x.id] += 1
            else:
                a=MyQ.pop()
                articles_exp3[a].reInitilize()
                MyQ.push(x_id)
                
            total_Weights += self.articles[x.id].weights
        for x in pool_articles:
            self.articles[x.id].updatePta(len(pool_articles), total_Weights)
            cum_pta += self.articles[x.id].pta
            if cum_pta >r:
                return x
    def updateWeight(self, pickedArticle, ArticleNum, click):
        self.articles[pickedArticle.id].updateWeight(ArticleNum, click)
        if self.decay:
            self.applyDecayToAll(1)
    
    def applyDecayToAll(self, duration):
        for key in self.articles:
            self.articles[key].applyDecay(self.decay, duration)
    
    def getarticleCTR(self, article_id):
        return self.articles[article_id].stats.CTR

class UCB1Algorithm:
    def __init__(self, decay = None):
        self.articles = {}
        self.decay = decay
    def decide(self, pool_articles, allNumPlayed):
        minPta = 0.0
        articlePicked = None
        for x in pool_articles:
            if x.id not in self.articles:
                self.articles[x.id] = UCB1Struct(x.id)
            x_pta = self.articles[x.id].updatePta(allNumPlayed)
            
            if minPta < x_pta:
                articlePicked = x
                minPta = x_pta
        return articlePicked
    def updateParameter(self, pickedArticle, allNumPlayed, click):
        self.articles[pickedArticle.id].updateParameter(allNumPlayed, click)
        if self.decay:
            self.applyDecayToAll(1)
    def applyDecayToAll(self, duration):
        for key in self.articles:
            self.articles[key].applyDecay(self.decay, duration)
    def getarticleCTR(self, article_id):
        return self.articles[article_id].stats.CTR
        
        
        
    
                
            
        
        
