# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 09:14:33 2020

@author: mylen
"""

import matplotlib.pyplot as plt
import numpy as np
import os

file = 'Mine_2D_Dawdon2bis.msh'
name= 'dawdonBis'

os.chdir(r'C:\Users\mylen\Downloads\OneDrive_1_14-08-2020')
k=[]
x=[]
y=[]
z=[]
p=[]
m=[]
n1=[]
n2=[]
n3=[]

fp = open(file)
for i, line in enumerate(fp):
    if i == 4:
        n=int(line)
        break
for i, line in enumerate(fp):
    if i == (n + 2):
        e=int(line)
        break
fp.close()  

f = open(name +'_p.msh', 'a')
f.write('#FEM_MSH\n  $PCS_TYPE\n   NO_PCS\n  $NODES\n' + str(n) + '\n')

fp = open(file)
for jn, line in enumerate(fp):
    if (jn > 4) & (jn < (n+5)):
        l = line.split(" ")
        k = int(l[0])-1
        x = float(l[1])
        y = float(l[2])
        z = float(l[3])      
        f.write('%s %s %s %s\n' % (k, x, y, z))
        # k.append(float(l[0])-1)
        # x.append(float(l[1]))
        # y.append(float(l[2]))
        # z.append(float(l[3]))
        # nodes= [k, x, y, z]
fp.close()
f.write(' $ELEMENTS\n'  + str(e) + '\n')

fp = open(file)
for je, line in enumerate(fp):
    if (je > (n+7)) & (je < (n+e+8)):
        l = line.split(" ")
        p = int(l[0])-1
        m = int(l[3])-1
        n1 = int(l[5])-1 
        n2 = int(l[6])-1
        n3 = int(l[7])-1
        f.write('%s %s %s %s %s\n' % (p, m, n1, n2, n3))
        # p.append(float(l[0])-1)
        # m.append(float(l[3])-1)
        # n1.append(float(l[5])-1) 
        # n2.append(float(l[6])-1)
        # n3.append(float(l[7])-1)
       # nodes= [p, m, 'tri', n1, n2, n3]        
fp.close()
f.write('#STOP\n')           
f.close()

