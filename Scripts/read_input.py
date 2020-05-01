# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import itertools
import os
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\2D_Mine_Models\Benchmark\TH\Layers\LM4\SANDWICH_v2_tri')

variables = []
file_name = input("Enter name : ") 

print(file_name)
with open(file_name+'.bc', 'r') as bcfile: 
  next(bcfile)
  for line in bcfile:
    if("#STOP" in line):
      break
    if(len(line)<=1):
      continue
    if('#BOUNDARY_CONDITION' in line):
       var = []
       continue
    if("$" in line):
       continue
    else:
       data=line.split(' ')
       data = list(filter(None, data))
       if np.size(data) == 1:
           var.append(data[0].rstrip())
       if np.size(data) == 2:
           var.append(data[1].rstrip())   
       variables.append(var)

variables.sort()
boundaryCondition = list(variables for variables,_ in itertools.groupby(variables))

variables = []
with open(file_name+'.st', 'r') as stfile: 
  next(stfile)
  for line in stfile:
    if("#STOP" in line):
      break
    if(len(line)<=1):
      continue
    if('#SOURCE_TERM' in line):
       var = []
       continue
    if("$" in line):
       continue
    else:
       data=line.split(' ')
       data = list(filter(None, data))
       if np.size(data) == 1:
           var.append(data[0].rstrip())
       if np.size(data) == 2:
           var.append(data[1].rstrip())   
       variables.append(var)

variables.sort()
sourceTerm = list(variables for variables,_ in itertools.groupby(variables))


variables = []
with open(file_name+'.ic', 'r') as icfile: 
  next(icfile)
  for line in icfile:
    if("#STOP" in line):
      break
    if(len(line)<=1):
      continue
    if('#INITIAL_CONDITION' in line):
       var = []
       continue
    if("$" in line):
       continue
    else:
       data=line.split(' ')
       data = list(filter(None, data))
       if np.size(data) == 1:
           var.append(data[0].rstrip())
       if np.size(data) >= 2:
           data[-1]=data[-1].rstrip()
           var.append(data[1:])   
       variables.append(var)

variables.sort()
initialCondition = list(variables for variables,_ in itertools.groupby(variables))

var = []
elem = []
name_medProp = [] 
i=0
j=0
with open(file_name+'.mmp', 'r') as icfile: 
  next(icfile)
  for line in icfile:
    if("#STOP" in line):
      break
    if(len(line)<=1):
      continue
    if('#MEDIUM_PROPERTIES' in line):
       i += 1
       continue
    if("Group" in line):
       continue
    if("$" in line):
       j += 1
       this_line = line.replace(" $","").replace("_"," ")
       name_medProp.append(this_line)
    else:
       data=line.split(' ')
       data = list(filter(None, data))
       if np.size(data) == 1:
           var.append(data[0].rstrip())
       if np.size(data) >= 2:
           data[-1]=data[-1].rstrip()
           var.append(data[-1])
j= int(j/i)
for item in var:  
    elem.append(float(''.join(item)))
a = np.asarray(elem) 
mediumProperties = a.reshape(i,j)  
name_medProp = name_medProp[:j]        

previous_line = ''
with open(file_name+'.msh', 'r') as mshfile: 
    for line in mshfile:
       if("#STOP" in line):
           break
       if previous_line.startswith(" $NODES"):
           nbnode = int(line)
       if previous_line.startswith(" $ELEMENTS"):
          nbelemt = int(line)
       previous_line = line
       
previous_line = []
density = []
thExpansion = []
thCapacity = []
thConductivity = []
materialProperties=[]
i=0
j=0
name_matProp = ['DENSITY','THERMAL EXPANSION','THERMAL CAPACITY','THERMAL CONDUCTIVITY']
with open(file_name+'.msp', 'r') as mspfile: 
    next(mspfile)
    for line in mspfile:
      if("#STOP" in line):
         break
      if(len(line)<=1):
         continue
      if('#SOLID_PROPERTIES' in line):
         i += 1
         continue 
      if('DENSITY' in previous_line):
         j += 1
         data=line.split(' ')
         data = list(filter(None, data))
         data[-1]=data[-1].rstrip()
         density.append(data[-1])   
      if('THERMAL' in line):
         continue
      if('EXPANSION' in previous_line):
         j += 1
         data=line.split(' ')
         data = list(filter(None, data))
         data[-1]=data[-1].rstrip()
         thExpansion.append(data[-1])        
      if('CAPACITY' in previous_line):
         j += 1
         data=line.split(' ')
         data = list(filter(None, data))
         data[-1]=data[-1].rstrip()
         thCapacity.append(data[-1])      
      if('CONDUCTIVITY' in previous_line):
         j += 1
         data=line.split(' ')
         data = list(filter(None, data))
         data[-1]=data[-1].rstrip()
         thConductivity.append(data[-1])   
      previous_line = line 

#materialProperties= [density,thExpansion,thCapacity,thConductivity]    
#materialProperties=list(map(list, zip(*materialProperties)))  
elem= [density,thExpansion,thCapacity,thConductivity]    
elem=list(map(list, zip(*elem)))  
for item in elem:
    materialProperties.append(list(np.float_(item)))    

previous_line = []
variables = []
i=0
name_timeProp = ['PCS_TYPE','TIME_STEPS','TIME_END','TIME_START']
with open(file_name+'.tim', 'r') as timfile: 
    next(timfile)
    for line in timfile:
      if("#STOP" in line):
         break
      if(len(line)<=1):
         continue
      if('#TIME_STEPPING' in line):
         i += 1
         var = []
         continue
      if("$" in line):
         continue
      else:
         data=line.split(' ')
         data = list(filter(None, data))
         if np.size(data) == 1:
             var.append(data[0].rstrip())
         if np.size(data) >= 2:
             data[-1]=data[-1].rstrip()
             var.append(data[0:])   
      variables.append(var)
variables.sort()
timeSteps = list(variables for variables,_ in itertools.groupby(variables))

print(nbelemt)
print(nbnode)
print(boundaryCondition)
print(initialCondition)
print(sourceTerm)
print(name_matProp)
print(materialProperties)
print(name_medProp)
print(mediumProperties)
print(name_timeProp)
print(timeSteps)

np.savetxt('file_test.txt', [nbelemt, nbnode])