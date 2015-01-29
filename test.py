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

if __name__ == "__main__":
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