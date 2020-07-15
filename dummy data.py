#!/usr/bin/env python
# coding: utf-8

# In[51]:


import pandas as pd
import numpy as np
import math, random
import os


# - Extract demand patterns from json file. 
# - Convert them to csv 

# - daily total load variation from 15 feb to 24 june

# In[54]:


daily = [-3,2,-11,-1,0,-6,-6,0,2,10,0,2,-1,1,0,1,1,-2,-2,-4,-4,-3,-5,-2,-9,-11,-16,-25,-30,-30,-46,-56,-60,-63,-65,-64,-64,-71,-70,-74,-74,-73,-73,-70,-71,-74,-74,-75,-75,-74,-72,-73,-76,-76,-76,-76,-74,-73,-76,-76,-77,-77,-75,-75,-73,-73,-77,-77,-77,-76,-74,-73,-74,-76,-75,-77,-76,-73,-70,-73,-75,-75,-75,-76,-74,-70,-72,-74,-74,-74,-73,-70,-68,-69,-72,-72,-72,-72,-70,-67,-69,-68,-69,-70,-70,-65,-64,-63,-67,-67,-66,-68,-63,-60,-63,-64,-65,-66,-64,-60,-58,-61,-62,-64,-63,-61,-57,-56,-56,-59,-60]
days = ["2020-02-15","2020-02-16","2020-02-17","2020-02-18","2020-02-19","2020-02-20","2020-02-21","2020-02-22","2020-02-23","2020-02-24","2020-02-25","2020-02-26","2020-02-27","2020-02-28","2020-02-29","2020-03-01","2020-03-02","2020-03-03","2020-03-04","2020-03-05","2020-03-06","2020-03-07","2020-03-08","2020-03-09","2020-03-10","2020-03-11","2020-03-12","2020-03-13","2020-03-14","2020-03-15","2020-03-16","2020-03-17","2020-03-18","2020-03-19","2020-03-20","2020-03-21","2020-03-22","2020-03-23","2020-03-24","2020-03-25","2020-03-26","2020-03-27","2020-03-28","2020-03-29","2020-03-30","2020-03-31","2020-04-01","2020-04-02","2020-04-03","2020-04-04","2020-04-05","2020-04-06","2020-04-07","2020-04-08","2020-04-09","2020-04-10","2020-04-11","2020-04-12","2020-04-13","2020-04-14","2020-04-15","2020-04-16","2020-04-17","2020-04-18","2020-04-19","2020-04-20","2020-04-21","2020-04-22","2020-04-23","2020-04-24","2020-04-25","2020-04-26","2020-04-27","2020-04-28","2020-04-29","2020-04-30","2020-05-01","2020-05-02","2020-05-03","2020-05-04","2020-05-05","2020-05-06","2020-05-07","2020-05-08","2020-05-09","2020-05-10","2020-05-11","2020-05-12","2020-05-13","2020-05-14","2020-05-15","2020-05-16","2020-05-17","2020-05-18","2020-05-19","2020-05-20","2020-05-21","2020-05-22","2020-05-23","2020-05-24","2020-05-25","2020-05-26","2020-05-27","2020-05-28","2020-05-29","2020-05-30","2020-05-31","2020-06-01","2020-06-02","2020-06-03","2020-06-04","2020-06-05","2020-06-06","2020-06-07","2020-06-08","2020-06-09","2020-06-10","2020-06-11","2020-06-12","2020-06-13","2020-06-14","2020-06-15","2020-06-16","2020-06-17","2020-06-18","2020-06-19","2020-06-20","2020-06-21","2020-06-22","2020-06-23","2020-06-24"]

daily = pd.Series(daily)
# daily.plot()
# daily.to_csv("dummy/3monthGraph.csv")


# - since load data is tickets collected by existing system, the current timetable plays major role in interpreting load data
#   

# In[58]:


timetable = pd.read_csv("final timetable.csv")
actual = pd.read_csv("dummy/actualGraph.csv")
weekAgo = pd.read_csv("dummy/weekAgoGraph.csv")
normal = pd.read_csv("dummy/normalGraph.csv")

routeCount = timetable["routeCode"].max()
# stopCounts = np.random.randint(20,31, routeCount)
# stopCounts = pd.Series(stopCounts)
# stopCounts.to_csv("stopCounts.csv")
routesCSV = pd.read_csv("routes.csv")

#stopCounts["stops"].sum()


# In[65]:


startDay = 129
endDay = 131
routesCount = routesCSV.shape[0]
normalDayLoad = 1200000
path = "dummy4/"


# In[66]:


############################################### LOOP ######################

RLdataframes = []
for dayNo in range(startDay,endDay): 
    day = days[dayNo]
    dailyLF = daily[dayNo]
    dailyLoad = normalDayLoad*(100 + dailyLF)/100 #80000 tickets on an avg per day
    print("daily total load: ",dailyLoad)
    os.makedirs(path + day)
    rlt = 0
    
    for route in range(routesCount):
#     route = 3
#     while route == 3:
        stopCount = routesCSV["stops"][route]

#     Load contributed by route is proportional to the number of trips happening
        routeLF = timetable[timetable["routeCode"] == route].shape[0]/timetable.shape[0]

        routeLoad = routeLF*dailyLoad
#         print(routeLoad, route)
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
#         print(stopLF)
        stopLoads = [] #hourly loads of the day

        for stopNo in range(stopCount):
            graph = normal.iloc[stopNo%normal.shape[0]][1:] #selection of graphs
            stopTotalL = stopLF[stopNo]*routeLoad           #routeLoad*% stop's contribution = stops contribution
            stopLoad = np.array(0) #array of hourly loads 
            stl = 0
            daymax = 0
             #increase the 100% load bu one till sum of load matches stopTotalLoad
            while(stl <= stopTotalL):
                stopLoad = daymax*stopLF[stopNo]*graph
                stl = stopLoad.sum() 
                daymax += 0.1
                
            #stop total load = sum(graph*stopMax * stopLF) 
            #load per hour at each stop
            stopLoads.append(stopLoad)
#             print(dayNo, route, stopNo) 
#             print(daymax,stopLF[stopNo],graph,stopLoad)
    
    
        routeLoads = pd.DataFrame(stopLoads) #hourly loads of all stops of a route 
        routeLoads = routeLoads.transpose()
        
        #############################################

        loads = []
        for stopNo in range(stopCount):
#             stopNo = str(stopNo)
            stopT = routeLoads[stopNo].sum().round()
            # print(routeLoad[stopNo])
            maxes = []
            # print(value)
            for j in range(len(routeLoads[stopNo])):
                maxI = routeLoads[stopNo][routeLoads[stopNo] == routeLoads[stopNo].min()].index[0]
                maxV = routeLoads[stopNo][maxI]

                for i in range(len(routeLoads[stopNo])):
                    if i in maxes:
                        continue;
            #         print(i, routeLoad[stopNo][i])
                    if routeLoads[stopNo][i] > maxV:
                        maxV = routeLoads[stopNo][i]
                        maxI = i
                if maxI not in maxes:
                    maxes.append(maxI)
            #     print(maxes)

            load = np.zeros(24)
            add = True;
            for i in range(len(maxes)):
                for j in range(i):
                    if(load.sum() != stopT):
                        load[maxes[j]] += 1;
                    else:
                        add = False;
                        break;
                if not add:
                    break;

            loads.append(load)
        intRouteLoads = pd.DataFrame(loads)
        
   #################################     
#         routeLoads.plot()
        intRouteLoads.to_csv(path + day + "/" + str(route) + ".csv")
#         route += 5

#         rlt += routeLoad
#     print(rlt)
print("khatam")

