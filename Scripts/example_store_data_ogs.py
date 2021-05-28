# script Mylene to store data from OGS 1D polyline output for each time step

import numpy as np
import os
import glob

os.chdir(r' xxx ')# the full link to directory

filename='xxx' # the file name without the extension
filelist=glob.glob('*\*'+filename+'.tec')
N = np.size(filelist)

# Initialize variables
time_all = []
scenario = {}

for i in range(N):
    data={}
    with open(filelist[i]) as file:
       name = filelist[i]
       print('processing ' + name)
       for line in file:
           if("TITLE" in line):
               continue
           if("VARIABLES" in line):
               continue
           if(' ZONE T' in line):
               this_line = line.replace('"','').replace('e+','e').split("=")
               time = this_line[2].rstrip()
               time_all.append(time)
               
               # initialize your temporary variables
               x = []
               Tx= []
               continue
           else:
               this_line=line.replace('e+','e').split(' ')
               x.append(float(this_line[0].rstrip()))
               Tx.append(float(this_line[1].rstrip()))
           data[float(time)] = [x,Tx]
    subdir = filelist[i].split('\\')[0].split('_')[1]
    scenario[subdir] = [data]  


#%% Get data 
colormap = np.array([ 'palevioletred',  'royalblue', 'tan', 'teal', 'forestgreen', 'magenta', 'green', 'black']) # just to select the color of the profiles
fts=11 # to define the size of the text in the plots

j=0
# find unique values of time
res=list(set.intersection(*map(set,[scenario[i][0].keys() for i in scenario])))
res = pd.DataFrame(np.array(res)/86400)
print('Available time to plots: ', res)

timeplot=input("Enter index of time steps to plot (i.e. [30, 52]) : ") 
timeplot=eval(timeplot)
plt.figure(figsize=(5,5.5))
for i in timeplot:
    for key in scenario:
        print(str(key))
        n = int(res.iloc[30]) * 86400
        tf= scenario[key][0][n]
        plt.plot(tf[1],tf[0],lw=1.5, label = str(key), color = colormap[j])       
        plt.xlabel('Temperature (°C)', fontsize = fts)
        plt.ylabel('Depth (m)', fontsize = fts)
        plt.xticks(fontsize = fts)
        plt.yticks(fontsize = fts)
        plt.xlim(4,20)
        plt.ylim(max(tf[0]), min(tf[0]))
        plt.legend(loc = 'best')
        j += 1 
plt.tight_layout() #pad=0.2, w_pad=0.2, h_pad=0.2

#plt.savefig('Temperature_profile.png', facecolor='w',frameon=None, metadata=None)