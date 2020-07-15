#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd 
import numpy as np 
import math, random, os
# timetable = pd.read_csv("final timetable.csv")

routesCSV = pd.read_csv("routes.csv")
path = "dummy4/2020-06-23/"

routesCount = routesCSV.shape[0]
# routesCount = 45 
busOcc = np.ones(24)*30 #array of max occupancy each hour

occUpperT = np.ones(24)*5 #tolerable increase in bus occupancy
occLowerT = np.ones(24)*10 #tolerable decrease in bus occupancy
dosLoad = 5 #denial of service for loads below certain value

minHeadway = 3 #max time the passenger can wait before giving up 

serviceStartHr = 0
serviceEndHr = 23


# In[15]:


#redistribute passengers in integer values

intRouteLoad = [] #route day Loads
for routeNo in range(routesCount): 

    routeLoad = pd.read_csv(path + str(routeNo) +".csv")
    routeLoad = routeLoad.drop("Unnamed: 0", axis = 1)
    routeLoad = routeLoad.transpose()
    intRouteLoad.append(routeLoad)
#     print(routeNo)

 


# In[16]:


#load accumalation as per min headway.
allHeadwayRL = []
for routeNo in range(len(intRouteLoad)):
    route = intRouteLoad[routeNo]
    headwayRL = pd.DataFrame()
    for stopNo in range(route.shape[1]):
        stopNo = stopNo
        stopLoad = []
        for hours in range(0,route.shape[0],minHeadway):
            load = 0
            for hour in range(hours, hours+minHeadway):
#                 print(routeNo, stopNo, hour)
                load += route[stopNo][hour]
                
            stopLoad.append(load)
        headwayRL[stopNo] = stopLoad
    allHeadwayRL.append(headwayRL)
# allHeadwayRL


# ## frequency calculation
# 1. if route is among lowFreqRoute - calc assign busses as per load
# 2. else use freq formula. 
#     a. if  dosLoad < load bw headway < 30 - give one bus at the end of 3hrs
#     b. if load bw headway < dosLoad - deny service.
#     c. if load by headway > 30 - calc slope of load increase and send buses when load = 30 
#         if some ppl remain after busses, add them to next hr load and calculate the freq for 

# In[17]:


# allHeadwayRL[lowFreqRoute[3]].plot()
len(allHeadwayRL)


# In[18]:


# method 1 

# find the stop where max total load is observed
def freq1(hourLoad, headLoad):
    freqOP = []
    for routeNo in range(routesCount):

        dailyMP = 0 # daily max point
        temp = 0
        for stopNo in range(hourLoad[routeNo].shape[1]):
            hrLoad = hourLoad[routeNo][stopNo].sum()
            if hrLoad > temp:
                temp = hourLoad[routeNo][stopNo].sum()
                dailyMP = stopNo
                
            

        #freq = bus/hour
        freq = []
#         if routeNo not in lowFreqRoute:
        hr = 0
        for hr in range(int(24/minHeadway)):
#             headHr = int(hr/minHeadway)
            headHrLoad = headLoad[routeNo][dailyMP][hr]
            
            if headHrLoad <= dosLoad:                  # f = 0
                f = headHrLoad/busOcc[hr]
                freq.append(0)
            elif headHrLoad <= busOcc[hr]:             # f = 1
                
                freq.append(1)
                
            elif headHrLoad > busOcc[hr]:         #more buses  than minHeadway ie more ppl than 30
                
                
                f = headHrLoad/busOcc[hr]
                freq.append(f)
                
#             print(routeNo, hr, headLoad)
             
        freqOP.append(freq)
#         else:
# #             calc the busses required. assign to 2 peak hours first. then to rest.
#             intRouteLoad[routeNo].sum().plot()
    print("khatam")        
    return freqOP
freq1 = freq1(intRouteLoad,allHeadwayRL)
freq1 = pd.DataFrame(freq1)
freq1 = freq1.transpose()


# In[19]:


#method 2
def freq2(hourLoad, headLoad):
    freqOP = []
    for routeNo in range(routesCount):
        maxL = []
        for hour in range(int(24/minHeadway)):
#             print(routeNo, hour , headLoad[routeNo])
            maxL.append(headLoad[routeNo].iloc[hour].max())

        freq = []
#         if routeNo not in lowFreqRoute:
        for hr in range(int(24/minHeadway)):
#             headHr = int(hr/minHeadway)
            headHrLoad = maxL[hr]
            
            if headHrLoad <= dosLoad:                  # f < 1
                f = headHrLoad/busOcc[hr]
                freq.append(0)
            elif headHrLoad <= busOcc[hr]:             # f = 1
                
                freq.append(1)
                
            elif headHrLoad > busOcc[hr]:         # f > 1
                
                
                f = headHrLoad/busOcc[hr]
                freq.append(f)
                
#             print(routeNo, hr, headLoad)
            
        freqOP.append(freq)
#         else:
# #             calc the busses required. assign to 2 peak hours first. then to rest.
#             intRouteLoad[routeNo].sum().plot()
    print("khatam")
    return freqOP
freq2 = freq2(intRouteLoad,allHeadwayRL)
freq2 = pd.DataFrame(freq2)
freq2 = freq2.transpose()


# - timetable for one month 
# - take average of one month.
# - different avg of weekends and normal days

# In[60]:


def arrivals(freq):
    routeArrivals = []
    for routeNo in range(routesCount):
        arrivalTimes = []
        hr = 0
        while hr < 24:
            headFreq = freq[routeNo][hr//minHeadway]
            if headFreq ==0:
                hr+=minHeadway
                continue
                
            time = hr*60
            headway = minHeadway*60/headFreq
            while time < (hr+minHeadway)*60:
                time += headway
                if time <= (hr+minHeadway)*60:
#                     print(hr*60, headFreq, time)
#                     print(routeNo , int(time))
                    arrivalTimes.append(time)
#                 print(routeNo , time,hr, hrHeadway)
            hr += minHeadway
        routeArrivals.append(arrivalTimes)
    return routeArrivals


# In[ ]:





# In[61]:


# Headway to timetable
arrivalTimes1 = arrivals(freq1)
arrivalTimes1 = pd.DataFrame(arrivalTimes1)
arrivalTimes1 = arrivalTimes1.transpose()

arrivalTimes2 = arrivals(freq2)
arrivalTimes2 = pd.DataFrame(arrivalTimes2)
arrivalTimes2 = arrivalTimes2.transpose()

# allHeadwayRL[6][6].sum()


# In[ ]:





# In[74]:





# In[83]:


def formTimetable(arrivalTimes):
    timetable = pd.DataFrame(columns=["routeCode","From","To","direction","startTime","duration","endTime"])
    rowNo = 0
    for routeNo in range(routesCount):
        routeInfo = routesCSV[routesCSV["routeCode"] == routeNo].iloc[0]
        
        fromTerm = routeInfo.From
        toTerm = routeInfo.To
        dur = routeInfo.duration
        routeName = routeInfo.routeName
        direction = routeInfo.direction 
#         print(arrivalTimes[routeNo])
        tripsCount = len(arrivalTimes[routeNo])
#         print(arrivalTimes[routeNo])
        for trip in range(tripsCount):
            
            startTime = arrivalTimes[routeNo][trip]
#             print(startTime)
            if not arrivalTimes[routeNo].isnull()[trip]: 
                endTime = startTime + dur
                startTime = startTime/60
                endTime = endTime/60

#                 print(routeNo , startTime, endTime)
                startTime2 = str(int(startTime)) + ":" + str(int((startTime - int(startTime))*60))

                endTime2 = str(int(endTime)) + ":" + str(int((endTime - int(endTime))*60))
#                 print(startTime2, endTime2)                       
                row = [routeName, fromTerm, toTerm, direction, startTime, dur, endTime]
                timetable.loc[rowNo] = row
                rowNo += 1
    print("khatam")
    return timetable


# In[84]:


# formTimetable(arrivalTimes1)
# formTimetable(arrivalTimes2)


# In[87]:


newTimetable1 = formTimetable(arrivalTimes1)
newTimetable1.to_csv("newTT1.csv")


# In[88]:


newTimetable2 = formTimetable(arrivalTimes2)
newTimetable2.to_csv("newTT2.csv")


# In[ ]:




