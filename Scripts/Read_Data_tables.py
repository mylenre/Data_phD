# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 17:39:26 2019

@author: s1995204
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

AT={}
os.chdir(r'R:\GitHub\Data_phD\Data\Averages')
data = pd.read_csv('MeanT_Scotland_E.txt', delimiter=',', header=6)