# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:52:01 2020

@author: s1995204
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
workings = []

os.chdir(r'R:\Data\Data_GIS\seams')
with open('workings.txt', 'r') as file:
  next(file)
  for line in file:
    if("((" in line):
      data = line.replace("((","").replace("(","").replace(",","").split('))')
      val =  data[0]
      split = val.split('	')   
      num = [float(x) for x in split ]
      l = int(np.size(split)/3)
      num2D = np.reshape(num,(l,3))
      avg = np.mean(num2D, axis=0)
      
      val2 = data[1]
      split2 = val2.split('	')  
      SE_THKNS=split2[4]
      SE_CODE=split2[5]
      PHASED =split2[6]
      PANNEL =split2[7]
      DIP=split2[8]
      DIP_DRN= split2[9]
      COLLIERY = split2[10]
      
      stack = [PANNEL, COLLIERY, avg[0],avg[1],avg[2],  SE_CODE, SE_THKNS, DIP, DIP_DRN,]
      workings.append(stack)
