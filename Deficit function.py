#!/usr/bin/env python
# coding: utf-8

# In[159]:


import numpy as np
import pandas as pd


# In[247]:


#replace terminal names by indexes. done
#define terminals and routes. 
#find trips from and to a terminal.
#find its df, max intervals.
#apply shifting in tolerance(take tolerance +- 3min).
#find DHs.
#make the schedule using fifo.


terminals = pd.read_csv("../PMPML/terminalArray.csv")
timetable = pd.read_csv("final timetable.csv")
get_ipython().run_line_magic('matplotlib', 'inline')

termObjArr = [] #array of terminal objects
dfs = pd.DataFrame() #deficit functions of all terminals

termArray = terminals["term"].array
termCount = terminals.shape[0]
tripsCount = timetable["From"].shape[0] #number of trips in timetable


class Terminal:
    def __init__(this, index, name):
        this.id = index; #index in terminal array
        this.name = name;       #name at that index
        this.df = np.zeros(1440);
        this.dfMaxPos = [];
        this.tripsToTerm = [[] * 1 for row in range(1440)];
        
        
    def showDF(this, t1 = 0, t2 = 1440): 
        dfGraph = pd.DataFrame({str(this.id)+": "+this.name: this.df[t1:t2]})
        dfGraph.plot()
    
    def maxima(this):
        maxAt = dfs[this.id][dfs[this.id] == dfs[this.id].max()].index
        maxEnds = []
        maxEnds.append(maxAt[0])
        for i in range(1,len(maxAt)):
            if maxAt[i-1] + 1 == maxAt[i]:
                continue
            else:
                maxEnds.append(maxAt[i-1])
                maxEnds.append(maxAt[i])

        maxEnds.append(maxAt[i])
        this.dfMaxPos = maxEnds  
        return this.dfMaxPos


# In[248]:


termObjArr = []
for i in range(termCount):
    term = Terminal(i, termArray[i])
    termObjArr.append(term)
    


# In[249]:


#from timetable to deficit
def deficitFunction():
    #for each trip, +1 to the df of 'from' terminal and -1 to the df of 'to' terminal
    #try:
    for i in range(tripsCount):
        fromTerm = int(timetable['From'][i])
        toTerm = int(timetable['To'][i])
        start = int(timetable['start'][i])
        end = int(timetable['end'][i])

        termObjArr[fromTerm].df[start:] += 1        
        termObjArr[toTerm].df[end:] -= 1
        
        termObjArr[fromTerm].tripsFromTerm[start].append(i)
        termObjArr[toTerm].tripsToTerm[end -1].append(i)
            
#     except: 
#         print("error at " + str(i) + ", "+ str(fromTerm) + ", "+str(toTerm) + ", "+ str(start) + ", "+ str(end) )
#    #error at 2980, 50, 334, 370, 450
        
    for i in range(termCount):
        #insert df arrays in dataframe
        dfs.insert(i, i, termObjArr[i].df, allow_duplicates = True)
        #calculate each terminals max intervals
        termObjArr[i].maxima()
        
        
        
deficitFunction()


# In[267]:


def late(time):
    #return late threshold depending on the time of day
    return (3)
def early(time):
    return (3)


# In[242]:


termObjArr[26].showDF(1280,1350)


# In[243]:


#find minimum fleet size
def minFleet():
    fleet = 0
    for i in range(termCount):
        fleet += termObjArr[i].df.max()
    return fleet


# In[271]:


############################
# shift in tolerable range #: early departure corresponds to start time, late arrival -> end time
############################

#condition 3: If M <= early(n) + late, then start time and end time can be shifted in opposite directions
#condition 2: If M <= early, then start time can be shifted in right direction
#condition 1: If M <= late, then end time can be shifted in left directions


for term in termObjArr:    
    #if maxima != 0 get maxima of terminal
    if term.df.max() != 0:
        for maxCount in range(0,len(term.dfMaxPos),2): 

            s = term.dfMaxPos[maxCount]            #start time of maxima
            e = term.dfMaxPos[maxCount + 1]        #end time of maxima
            length = e - s                         #length of maxima
            
            tripStart = term.tripsFromTerm[s]      #trips causing start of maxima
            tripEnd = term.tripsToTerm[e]          #trips causing end of maxima
            
            #find early and late of each trip
            ## // ## if late and early of each trip satisfy condition, then take action accordingly
            #calculate for condition 1,2,3
            #update start and end of the trips accordingly in timetable
            #update the dfs and maxima  

            if length <= late(s):                          #condition 1
                print(term.id, length, s, e, "condition 1")
                #timetable ke trips ka end time -= 
            elif length <= early(e):                       #condition 2
                print(term.id, length, s, e, "condition 2")
            elif length < late(s) + early(e):              #condition  
                print(term.id, length, s, e, "condition 3")
            
            


# In[274]:


# timetable


# In[11]:





# In[57]:





# In[ ]:




