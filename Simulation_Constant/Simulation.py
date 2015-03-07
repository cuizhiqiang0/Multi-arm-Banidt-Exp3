# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 12:24:59 2015

@author: Summer
"""

import math
import numpy as np
from MAB_algorithms import *
import datetime
from matplotlib.pylab import *
from random import sample

class batchStats():
    def __init__(self):
        self.stats = Stats()    # what's Stats()
        self.clickArray = []
        self.accessArray = []
        self.CTRArray = []
        self.time_ = []
        self.poolMSE = [] # What's this for
        self.articlesCTR = {}  #key: articleID, value: CTR
        
    def addRecord(self, iter_, poolArticles):
        self.clickArray.append(self.stats.clicks)
        self.accessArray.append(self.stats.accesses)
        self.CTRArray.append(self.stats.CTR)
        self.time_.append(iter_)
        #self.poolMSE.append(poolMSE)
        for x in poolArticles:  #poolArticles is a dictionary?
            if x in self.articlesCTR:
                self.articlesCTR[x].append(poolArticles[x])
            else:
                self.articlesCTR[x] = [poolArticles[x]]
    def plotArticle(self, article_id):
        plot(self.time_, self.articlesCTR[article_id])
        xlabel("Iterations")
        ylabel("CTR")
        title("")

class Article():
    def __init__(self, id, startTime, endTime, FV):
        self.id = id;
        self.startTime = startTime
        self.endTime = endTime
        self.initialTheta = None  #parameter in LinUCB?
        self.theta = None   #parameter in LinUCB?
        #self.featureVector = None
        self.deltaTheta = None
        self.absDiff = {}  # What's this for
        self.time_ ={}
    
    def setTheta(self, theta):
        self.initialTheta = theta
        self.theta = theta
        
    def setDeltaTheta(self, finalTheta, total_iterations):
        self.deltaTheta = (finalTheta - self.initialTheta) / total_iterations
        
    def evolveThetaWTime(self):
        self.theta +=self.deltaTheta
        
    def inPool(self, curr_time):
        return curr_time <=self.endTime and curr_time >=self.startTime
        
    def addRecord(self, time_,  alg_name):
        if alg_name in self.time_:
            self.time_[alg_name].append(time_)
        else:
            self.time_[alg_name] = [time_]
        '''    
        if alg_name in self.absDiff:
            self.absDiff[alg_name].append(absDiff)
        else:
            self.absDiff[alg_name] = [absDiff]
        '''    
    def plotAbsDiff(self):
        figure()
        for k in self.time_.keys():
            plot(self.time_[k], self.absDiff[k])
        legend(self.time_.keys(), loc =2)
        xlabel("iterations")
        ylabel("Abs Difference between Learnt and Ture parameters")
        title("Observing Learnt Parameter Difference")
class User():
    def __init__(self, id, featureVector):
        self.id = id
        self.featureVector = featureVector
        
class simulateOnlineData:
    def __init__(self, n_articles, n_users, dimension, iterations, type, environmentVars):
        self.dimension = dimension
        self.type = type
        self.articles = []
        self.articlePool = []
        self.users = []
        self.iterations = iterations
        self.alg_perf = {}
        self.iter_ = 0
        self.batchSize = 1000
        self.startTime = None
        self.environmentVars = environmentVars
        self.simulateArticlePool(n_articles)
        self.simulateUsers(n_users)
        
    def regulateEnvironment(self):
        if self.type =="abruptThetaChange":
            if self.iter_%self.environmentVars["reInitiate"] ==0:
                for x in self.articlePool:
                    x.theta = self.featureUniform()  # where is featureUniform
                print "Re-initiating parameters"
        elif self.type == "evolveTheta":
            pass
        
    def createIds(self, maxNum): # how it work??
        return map(
                lambda x:10**math.ceil(math.log(maxNum +1, 10)) + x, range(maxNum)
                )
    
    def featureUniform(self):
        feature = np.array([random() for _ in range(self.dimension)])
        return feature / self.dimension
        
    def simulateArticlePool(self, n_articles):
        def getEndTimes():
            pool = range(20)
            endTimes = [0 for i in startTimes]
            last = 20
            for i in range(1, self.iterations / article_life+1):
                chosen = sample(pool, 5)
                for c in chosen:
                    endTimes[c] = article_life*i
                pool = [x for x in pool if x not in chosen]
                pool += [x for x in range(last, last+5) if x < len(startTimes)]
                last +=5
                if last > len(startTimes):
                    break
            for p in pool:
                endTimes[p] = self.iterations
                
            return endTimes
        
        articles_id = self.createIds(n_articles)
        if n_articles >=20:
            article_life = int(self.iterations / ((n_articles - 20)*1.0/5))
            print article_life
            startTimes = [0 for x in range(20)] + [
                        (1+int(i/5)) * article_life for i in range(n_articles - 20)]
                        
            endTimes = getEndTimes()
            
        else:
            startTimes = [0 for x in range(n_articles)]
            endTimes = [self.iterations for x in range(n_articles)]
            
        print startTimes, endTimes
        for key, st, ed in zip(articles_id, startTimes, endTimes):
            self.articles.append(Article(key, st, ed, self.featureUniform()))
            self.articles[-1].theta = self.featureUniform()
            
    def simulateUsers(self, numUsers):
        """users of all context arriving uniformly"""
        userids = self.createIds(numUsers)
        for key in userids:
            self.users.append(User(key, self.featureUniform()))
            
    def evolveTheta(self):
        for x in self.articles:
            x.evolveTheta()
    
    def getUser(self):
        return choice(self.users)
        
    def updateArticlePool(self):
        self.articlePool = [x for x in self.articles if x.inPool(self.iter_)]
        
    def runAlgorithms(self, algorithms):
        self.startTime = datetime.datetime.now()
        for self.iter_ in range(self.iterations):
            self.regulateEnvironment()
            self.updateArticlePool()
            userArrived = self.getUser()
            for alg_name, alg in algorithms.items():
                pickedArticle = alg.decide(self.articlePool)
                clickExpectation = np.dot(pickedArticle.theta, userArrived.featureVector)
                click = np.random.binomial(1, clickExpectation)
                alg.updateWeight(pickedArticle, len(self.articlePool), click)
                
                self.iterationRecord(alg_name, userArrived.id, click, pickedArticle.id)
                
            if self.iter_%self.batchSize == 0 and self.iter_ >1:
                self.batchRecord(algorithms)
    def runAlgorithmsUCB1(self, algorithms):
        self.startTime = datetime.datetime.now()
        countLine = 0
        for self.iter_ in range(self.iterations):
            countLine += 1
            self.regulateEnvironment()
            self.updateArticlePool()
            userArrived = self.getUser()
            for alg_name, alg in algorithms.items():
                #print "CountLine", countLine
                pickedArticle = alg.decide(self.articlePool, countLine)
                #print "Picked", pickedArticle
                clickExpectation = np.dot(pickedArticle.theta, userArrived.featureVector)
                click = np.random.binomial(1, clickExpectation)
                alg.updateParameter(pickedArticle, click)
                
                self.iterationRecord(alg_name, userArrived.id, click, pickedArticle.id)
                
            if self.iter_%self.batchSize == 0 and self.iter_ >1:
                self.batchRecord(algorithms)
                
    def iterationRecord(self, alg_name, user_id, click, article_id):
        if alg_name not in self.alg_perf:
            self.alg_perf[alg_name] = batchStats()
        self.alg_perf[alg_name].stats.addrecord(click)
        
    def batchRecord(self, algorithms):
        for alg_name, alg in algorithms.items():
            poolArticlesCTR = dict([(x.id, alg.getarticleCTR(x.id)) for x in self.articlePool])
            if self.iter_%self.batchSize == 0:
                self.alg_perf[alg_name].addRecord(self.iter_, poolArticlesCTR)
                
            for article in self.articlePool:
                article.addRecord(self.iter_, alg_name)
                
        print "Iteration %d "%self.iter_, "Pool ", len(self.articlePool)," Elapsed time", datetime.datetime.now() - self.startTime
        
    def analyzeExperiment(self):
        "Plot vertical lines at specific events"
        def plotLines(xlocs):
            axes = plt.gca()
            for x in xlocs:
                xSet = [x for _ in range(31)]
                ymin, ymax = axes.get_ylim()
                ySet = ymin +(np.array(range(0, 31))*1.0/30) * (ymax - ymin)
                plot(xSet, ySet, "black")
                
        xlocs = list(set(map(lambda x: x.startTime, self.articles)))
        figure()
        for alg in self.alg_perf:
            plot(self.alg_perf[alg].time_, self.alg_perf[alg].CTRArray)
        legend(self.alg_perf.keys(), loc =4)
        xlabel("Iteration")
        ylabel("Cumulative CTR")
        title("CTR Performance")
        plotLines(xlocs)
        '''
        figure()
        for alg in self.alg_perf:
            plot(self.alg_perf[alg].time_, self.alg_perf[alg].poolMSE)
        legend(self.alg_perf.keys(), loc =3)
        xlabel("Iteratio")
        ylabe("MSE")
        title("Learning Error")
        plotLines(xlocs)
        '''
    def getPoolMSE(self, alg):
        diff = 0
        for article in self.articlePool:
            diff += self.getArticleAbsDiff(alg, article)**2
        diff = math.sqrt(diff)
        return diff
        
    def getArticleAbsDiff(self, alg, article):       
        return sum(map(abs, article.theta - alg.getLearntParams(article.id)))
        
if __name__ =='__main__':
    for i in range(1):
        simExperiment = simulateOnlineData(n_articles = 50,
                                           n_users = 1000,
                                           dimension = 5,
                                           iterations = 200000,
                                           type = "ConstantTheta",
                                           environmentVars = {"reInitiate":100000}
                                           )
        
        UCB1 = UCB1Algorithm()
        Exp3 = Exp3Algorithm(gamma = 0.3)
        decExp3 = Exp3Algorithm(gamma = 0.3, decay = 0.99)
        AgeQueueExp3 = Exp3QueueAlgorithm(gamma = 0.3)
        Random = RandomAlgorithm()
        
        simExperiment.runAlgorithmsUCB1({"UCB1": UCB1})
        #simExperiment.analyzeExperiment()
        #simExperiment.runAlgorithms({"Random": Random})
        #simExperiment.runAlgorithms({"Exp3":Exp3, "decExp3_0.99":decExp3, "Random":Random, "AgeQueueExp3_15": AgeQueueExp3})
        
        print "Done, begin analysis"
        simExperiment.analyzeExperiment()
                    
        