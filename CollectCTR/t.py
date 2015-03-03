# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:18:09 2015

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

articleIDfilename = '/Users/Summer/Documents/Multi-arm-Banidt-Exp3/result/savedArticleID.txt'
with open(articleIDfilename, 'r') as f:
    for line in f:
        line = line.rstrip('\n').split('\t')
        AllArticleIDpool = copy.copy(line)
print AllArticleIDpool

for x in range(0,len(AllArticleIDpool)):
    print AllArticleIDpool[x], str(AllArticleIDpool[x])

fileNameWrite = os.path.join(save_address,  'test.csv')
aa = [1,2,3,4,6]       
        # put some new data in file for readability
with open(fileNameWrite, 'a+') as f:
    f.write('\nNew Run at')
    f.write(',' + ','.join([str(AllArticleIDpool[x]) for x in range(0, len(AllArticleIDpool))]))

a = {1:'a', 2:'b', 3:'c'}
cc = [1,2,3]
stats =[]
stats = [a[cc[x]] for x in range(0,len(cc))]
print "stat", stats