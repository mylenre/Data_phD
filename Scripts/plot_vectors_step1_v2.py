# -*- coding: utf-8 -*-
"""
Created on Fri May  1 13:11:12 2020

@author: s1995204
"""

import numpy as np
import os
#tested for:
#os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\2D_Mine_Models\Benchmark\TH\Layers\LM4\V2\COMPLEX_v2')
#filename='LM4_domain_quad.tec'

os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\Heat_extraction_model_water\2_1Y\2_3D-SI_VO\366day')
filename='SI_BHE_sfc_surface_out_t1.tec'

time = []
x = []
y = []
z = []
T = []
#xn = []
#yn = []
#element = {}
node = {}
N= 5040
i=0

print(filename)
with open(filename, 'r') as file: 
  next(file)
  for line in file:
    if("TITLE" in line):
       continue
    if('STRANDID' in line):
       continue
    if("VARIABLES" in line):
       this_line = line.replace('"','').replace('=',',').split(",")
       variables = this_line[1:np.size(this_line)]
       continue
    if('ZONE T' in line):
       this_line = line.replace('"','').replace('e+','e').replace('s','').replace('=',',').split(",")
       time.append(float(this_line[2]))
       j=0
       x = []
       y = []
       z = []
       T = []
#       xn = []
#       yn = []
       i=i+1
       print("time step : " + str(i-1))
       continue   
    if j < N:
          this_line=line.replace('e+','e').split(' ')
          x.append(float(this_line[0].rstrip()))
          y.append(float(this_line[1].rstrip()))
          z.append(float(this_line[2].rstrip()))
          T.append(float(this_line[3].rstrip()))
          j=j+1
    node[time[i-1]] = [x,y,z,T]
   # else:
   #     this_line=line.split(' ')
   #     this_linec = [c for c in this_line if c != ""]
   #     xn.append(float(this_linec[0].rstrip()))
   #     yn.append(float(this_linec[1].rstrip())) 
   #     j=j+1
   # element[time[i-1]] = [xn,yn]