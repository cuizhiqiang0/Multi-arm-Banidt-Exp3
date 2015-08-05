import re
from random import random, choice
from operator import itemgetter
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

# -----------------------Non-contextual Algorithms--------------------------------
# structure to save data from random strategy
class randomStruct:
    def __init__(self):
        self.learn_stats = articleAccess()
        self.deploy_stats = articleAccess()


# structure for epsilon-greedy algorithm
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

# this structure saves for the exp3 algorithm
class exp3Struct:
    def __init__(self, gamma):
        self.gamma = gamma
        self.weights = 1.0
        self.pta = 0.0
        self.learn_stats = articleAccess()
        
    def reInitilize(self):
        self.weights = 1.0
          
    def updateParameters(self, n_arms, reward):
        #n_arms = n_arms
        X=reward/self.pta
        growth_factor = math.exp((self.gamma/n_arms)*X)
        self.weights = self.weights * growth_factor
    def getProb(self, n_arms, total_weight):
        #n_arms = n_arms
        self.pta= (1-self.gamma) * (self.weights / total_weight)
        self.pta= self.pta + (self.gamma) * (1.0 / float(n_arms))
 
# structure for UCB1 algorithm
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
    
    def updateParameters(self, click):
        self.totalReward += click
        self.numPlayed +=1

    def getProb(self, allNumPlayed):
        try:
            self.pta = self.totalReward / self.numPlayed + np.sqrt(2*np.log(allNumPlayed) / self.numPlayed)
        except ZeroDivisionError:
            self.pta = 0.0
            
# -----------------------Contextual Algorithms--------------------------------   
# data structure for LinUCB for a single article; 
class LinUCBStruct(object):
    def __init__(self, d, articleID, alpha,tim = None):
        self.articleID = articleID
        self.A = np.identity(n=d)           # as given in the pseudo-code in the paper
                self.A_inv= np.linalg.inv(self.A)
        self.b = np.zeros(d)                # again the b vector from the paper 
        self.alpha = alpha
        
        self.theta = np.dot(self.A_inv, self.b)
        
        self.pta = 0                        # the probability of this article being chosen
        self.var = 0
        self.mean = 0

        self.identityMatrix = np.identity(n=d)

        self.learn_stats = articleAccess()  # in paper the evaluation is done on two buckets; so the stats are saved for both of them separately; In this code I am not doing deployment, so the code learns on all examples
        self.deploy_stats = articleAccess()
        
        self.last_access_time = tim
        

    def reInitilize(self):
        d = np.shape(self.A)[0]             # as theta is re-initialized some part of the structures are set to zero
        self.A = np.identity(n=d)
        self.b = np.zeros(d)
        self.A_inv = np.identity(n=d)
        self.theta = np.dot(self.A_inv, self.b)

    def updateParameters(self, featureVector, click):
        self.A += np.outer(featureVector, featureVector)
        self.b += featureVector*click
        self.A_inv = np.linalg.inv(self.A)

        self.theta = np.dot(self.A_inv, self.b)

    def getProb(self,featureVector):
        self.mean = np.dot(self.theta, featureVector)
        self.var =  np.sqrt(np.dot(np.dot(featureVector,self.A_inv ), featureVector))
        self.pta = self.mean + self.alpha * self.var

        
