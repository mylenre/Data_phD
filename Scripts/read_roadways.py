# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:52:01 2020

@author: s1995204
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
roadways = []

os.chdir(r'R:\Data\Data_GIS\seams')
with open('roadways.txt', 'r') as file:
  next(file)
  for line in file:
    if("((" in line):
      data = line.replace("((","").replace("(","").replace(",","").split('))')
      val =  data[0]
      split = val.split('	')   
      num = [float(x) for x in split ]
      l = int(np.size(split)/2)
      num2D = np.reshape(num,(l,2))
      avg = np.mean(num2D, axis=0)
      
      val2 = data[1]
      split2 = val2.split('	')  
      MI=split2[4]
      Depth=split2[3]
      
      stack = [avg[0],avg[1], Depth, MI]
      roadways.append(stack)
