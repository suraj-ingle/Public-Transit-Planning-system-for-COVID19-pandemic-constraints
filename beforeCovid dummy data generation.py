#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import math, random
import os


# In[ ]:


startDay = 129
endDay = 131
routesCount = routesCSV.shape[0]
normalDayLoad = 1200000
path = "dummy4/"


# In[ ]:


daily = [-3,2,-11,-1,0,-6,-6,0,2,10,0,2,-1,1,0,1,1,-2,-2,-4,-4,-3,-5,-2,-9,-11,-16,-25,-30,-30,-46,-56,-60,-63,-65,-64,-64,-71,-70,-74,-74,-73,-73,-70,-71,-74,-74,-75,-75,-74,-72,-73,-76,-76,-76,-76,-74,-73,-76,-76,-77,-77,-75,-75,-73,-73,-77,-77,-77,-76,-74,-73,-74,-76,-75,-77,-76,-73,-70,-73,-75,-75,-75,-76,-74,-70,-72,-74,-74,-74,-73,-70,-68,-69,-72,-72,-72,-72,-70,-67,-69,-68,-69,-70,-70,-65,-64,-63,-67,-67,-66,-68,-63,-60,-63,-64,-65,-66,-64,-60,-58,-61,-62,-64,-63,-61,-57,-56,-56,-59,-60]
days = ["2020-02-15","2020-02-16","2020-02-17","2020-02-18","2020-02-19","2020-02-20","2020-02-21","2020-02-22","2020-02-23","2020-02-24","2020-02-25","2020-02-26","2020-02-27","2020-02-28","2020-02-29","2020-03-01","2020-03-02","2020-03-03","2020-03-04","2020-03-05","2020-03-06","2020-03-07","2020-03-08","2020-03-09","2020-03-10","2020-03-11","2020-03-12","2020-03-13","2020-03-14","2020-03-15","2020-03-16","2020-03-17","2020-03-18","2020-03-19","2020-03-20","2020-03-21","2020-03-22","2020-03-23","2020-03-24","2020-03-25","2020-03-26","2020-03-27","2020-03-28","2020-03-29","2020-03-30","2020-03-31","2020-04-01","2020-04-02","2020-04-03","2020-04-04","2020-04-05","2020-04-06","2020-04-07","2020-04-08","2020-04-09","2020-04-10","2020-04-11","2020-04-12","2020-04-13","2020-04-14","2020-04-15","2020-04-16","2020-04-17","2020-04-18","2020-04-19","2020-04-20","2020-04-21","2020-04-22","2020-04-23","2020-04-24","2020-04-25","2020-04-26","2020-04-27","2020-04-28","2020-04-29","2020-04-30","2020-05-01","2020-05-02","2020-05-03","2020-05-04","2020-05-05","2020-05-06","2020-05-07","2020-05-08","2020-05-09","2020-05-10","2020-05-11","2020-05-12","2020-05-13","2020-05-14","2020-05-15","2020-05-16","2020-05-17","2020-05-18","2020-05-19","2020-05-20","2020-05-21","2020-05-22","2020-05-23","2020-05-24","2020-05-25","2020-05-26","2020-05-27","2020-05-28","2020-05-29","2020-05-30","2020-05-31","2020-06-01","2020-06-02","2020-06-03","2020-06-04","2020-06-05","2020-06-06","2020-06-07","2020-06-08","2020-06-09","2020-06-10","2020-06-11","2020-06-12","2020-06-13","2020-06-14","2020-06-15","2020-06-16","2020-06-17","2020-06-18","2020-06-19","2020-06-20","2020-06-21","2020-06-22","2020-06-23","2020-06-24"]

daily = pd.Series(daily)
# daily.plot()
# daily.to_csv("dummy/3monthGraph.csv")


# In[ ]:


b4covid = []
b4covid = daily[76:]
l = len(b4covid)
h = 75 - 56
m = h/l
# b4covid = b4covid.to_numpy()
arr = np.ones(l)*(-77)

for i in range(l):
    arr[i] = arr[i] + m*i
    b4covid[i] -= arr[i]
#b4covid

b4covid = pd.DataFrame(data = [b4covid, arr])
b4covid = b4covid.transpose()
b4covid.plot()

b4covid = pd.read_csv("b4covid.csv")
b4covid["load"] *= 1.3 # amplified variation factor as the graph during covid is damped 
daily =  b4covid["load"]


# In[ ]:


for dayNo in range(startDay, endDay): 
    dailyLF = daily[dayNo]
    os.makedirs(path + "b4covid/day" + str(dayNo))
    
    for route in range(routesCount):
        
        stopCount = stopCounts["stops"][route]

        dailyLoad = normalDayLoad*(100 + dailyLF)
        routeLF = timetable[timetable["routeCode"] == route].shape[0]/timetable.shape[0]

        routeLoad = routeLF*dailyLoad

        stopLF = np.ones(stopCount) #% of load provided by each stop
        equalLF = 100/stopCount

        maxLF = 2*(equalLF - 1)
        halfL = math.ceil(stopCount/2)

        for i in range(halfL):    
            d = i*maxLF/halfL
            stopLF[i] += d
            stopLF[len(stopLF) - i -1] += d

        stopLF[6] += 100 - stopLF.sum()
        stopLF = stopLF/100
        stopLoads = [] #loads of the day

        for stopNo in range(stopCount): 
            graph = normal.iloc[stopNo%normal.shape[0]][1:]     #selection of graphs
            stopTotalL = stopLF[stopNo]*routeLoad               #routeLoad*% stop's contribution = stops contribution
            stl = 0
            daymax = 0
             #increase the 100% load bu one till sum of load matches stopTotalLoad
            while(stl <= stopTotalL):
                stopLoad = daymax*stopLF[stopNo]*graph   #load per hour at each stop
                stl = stopLoad.sum() 
                daymax += 0.1
                                            
            stopLoads.append(stopLoad)

        routeLoads = pd.DataFrame(stopLoads)
        routeLoads = routeLoads.transpose()
        #routeLoads.plot()
        routeLoads.to_csv(path + "b4covid/day"+ str(dayNo) +"/"+ str(route) + ".csv")

