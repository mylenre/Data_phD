# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 08:02:15 2020

@author: s1995204
"""

import os
import numpy as np

os.chdir(r'R:\GitHub\Data_phD\Scripts\Input_OGS')

process= []
variable= []
name=input("Enter name project : ")

listfile = ["INITIAL_CONDITION", "SOURCE_TERM", "BOUNDARY_CONDITION", "SOLID_PROPERTIES", "MEDIUM_PROPERTIES", "FLUID_PROPERTIES", "TIME_STEPPING", "NUMERICS", "OUTPUT"]
extension = ["IC", "ST", "BC", "MSP", "MMP", "MFP", "TIM", "NUM", "OUT"]

T = input("HEAT_TRANSPORT ? (Y/N)? \n") 
if T == 'Y':
  process.append(' HEAT_TRANSPORT')
  variable.append(' TEMPERATURE1')
H = input("GROUNDWATER_FLOW ? (Y/N)? \n") 
if H == 'Y':
  process.append(' GROUNDWATER_FLOW')
  variable.append(' HEAD')

print('-------------------------------------------\n')
print('Preparing PROCESS file \n')  
f = open(name +'.PCS', 'a')
for j in range(np.size(process)):
    f.write('#PROCESS\n $PCS_TYPE\n' + process[j] + '\n')
    print(process[j] + ': ')
    steady=input("Steady state ? (Y/N)")
    if steady == 'Y':
        f.write('$TIM_TYPE\n STEADY\n')
    reload=input("Initiation file ? ([Enter] for none; [1 1] for write every time step; [2] for reload; [3 1] for reload and write every time step) :  ")
    if reload != "":
        f.write('$RELOAD \n' + reload + '\n')
    del reload
f.write('#STOP \n')
f.close()

for i in range(np.size(listfile)):
   print('-------------------------------------------\n')
   print('Preparing ' + str(listfile[i]))
   f = open(name +'.'+ extension[i], 'a')  
   if i < 3:
     for j in range(np.size(process)):
         nb = input('Number of ' + listfile[i] + ' in ' + process[j] + ': ') 
         nb=eval(nb)
         for k in range(nb):
              var1 = input("GEO_TYPE " + str(k+1) + " (DOMAIN / POINT / POLYLINE) + Name : ") 
              var2 = input("DIS_TYPE " + str(k+1) + "(CONSTANT / CONSTANT_NEUMANN / CONSTANT_GEO / GRADIENT) + Value (i.e GRADIENT Depth Val Grad): ") 
              f.write('#' + listfile[i] + "\n $PCS_TYPE\n" + process[j] + "\n $PRIMARY_VARIABLE\n" + variable[j] + "\n")
              f.write(' $GEO_TYPE\n %s \n $DIS_TYPE\n %s\n' % (var1, var2))
   if i == 3:
    m=input("Enter number of material properties : ")
    m=eval(m)
    for k in range(m):
        print('\nMaterial number ' + str(k+1))
        var1 = input("DENSITY: " ) 
        var2 = input("THERMAL EXPANSION: ") 
        var3 = input("THERMAL CAPACITY: ") 
        var4 = input("THERMAL CONDUCTIVITY: ") 
        f.write('#' + listfile[i] + '\n $DENSITY\n 1 %s\n $THERMAL\n  EXPANSION\n  1 %s\n  CAPACITY\n  1 %s\n  CONDUCTIVITY\n  1 %s\n' % (var1, var2, var3, var4))
   if i ==4:
    for k in range(m):
        print('\nMaterial number ' + str(k+1))
        #var1 = input("GEO_TYPE " + str(k+1) + " (DOMAIN / POINT / POLYLINE): ") 
        var2 = input("GEOMETRY_DIMENSION (1/2/3): ") 
        var3 = input("GEOMETRY_AREA: ") 
        var4 = input("POROSITY: ") 
        var5 = input("TORTUOSITY: ") 
        var6 = input("HEAT_DISPERSION (i.e 1 0.5 0.5): ") 
        var7 = input("MASS_DISPERSION (i.e. 1 0.5 0.5): ") 
        var8 = input("STORAGE: ") 
        var9 = input("PERMEABILITY_TENSOR (ISOTROPIC/ANISOTROPIC + val): ") 
        f.write('#' + listfile[i] + '\n $NAME\n  DEFAULT\n $GEO_TYPE\n  DOMAIN\n $GEOMETRY_DIMENSION\n  %s\n $GEOMETRY_AREA\n  %s\n $POROSITY\n  1 %s\n $TORTUOSITY\n  1 %s\n $HEAT_DISPERSION\n  %s\n $MASS_DISPERSION\n  %s\n $STORAGE\n  1 %s\n $PERMEABILITY_TENSOR\n  %s\n' % (var2, var3, var4, var5, var6, var7, var8, var9))                   
   if i ==5:
        var1 = input("DENSITY : ") 
        var2 = input("VISCOSITY: ") 
        var3 = input("SPECIFIC_HEAT_CAPACITY: ") 
        var4 = input("HEAT_CONDUCTIVITY: ") 
        f.write('#' + listfile[i] + '\n $FLUID_TYPE\n  WATER\n $PCS_TYPE\n  HEAD\n $DENSITY\n  %s\n $VISCOSITY\n  1 %s\n $SPECIFIC_HEAT_CAPACITY\n  1 %s\n $HEAT_CONDUCTIVITY\n  1 %s\n' % (var1, var2, var3, var4))                    
   if i ==6:
    for j in range(np.size(process)):
        print('\n' + process[j] + ': ')
        var1 = input("TIME_STEPS ([nb duration(s)]): ") 
        var2 = input("TIME_END: ") 
        var3 = input("TIME_START: ") 
        f.write('#' + listfile[i] + '\n $PCS_TYPE\n ' + process[j] + '\n $TIME_STEPS\n  %s\n $TIME_END\n  %s\n $TIME_START\n  %s\n' % (var1, var2, var3))                    
   if i ==7:
    for j in range(np.size(process)):
        f.write('#' + listfile[i] + '\n $PCS_TYPE\n ' + process[j] + '\n $LINEAR_SOLVER\n  ; method error_tolerance max_iterations theta precond storage\n  2 6 1e-010 3000 1.0 1 4\n')                    
   if i ==8:
    for j in range(np.size(process)):
        print(process[j] + ': ')
        out = input("Enter number of output : ")
        out = eval(out)
        for o in range(out): 
          var1 = input("select GEO_TYPE " + str(k+1) + " (DOMAIN / POINT / POLYLINE) + Name : ") 
          var2 = input("STEPS: ") 
          f.write('#' + listfile[i] + '\n $PCS_TYPE\n ' + process[j] + '\n $NOD_VALUES\n '+ variable[j] + ' \n $GEO_TYPE\n  %s\n $DAT_TYPE\n  TECPLOT\n $TIM_TYPE\n  STEPS  %s\n' % (var1, var2))                         
   f.write('#STOP\n')           
   f.close()
   
        