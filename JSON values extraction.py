#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import math, random
import os


# In[ ]:


with open ("hour.txt", "r") as myfile:
    data=myfile.readlines()
    
names = ["All Cities","Boston","Calgray","Chicago","Denver","Halifax","Montreal","New Jersey","New York City","Ottawa","Philadelphia","Pittsburgh","Salt Lake City","San Diego","Toronto","Vancouver","Victoria","Washington D.C.","BART (SF Bay Area)","BC Transit (Victoria)","Bee-Line (NYC)","Brampton Transit","Busit (Hamilton","NZ)","CTA (Chicago)","Edmonton Transit","Fairfax Connector","Long Island Rail Road","MBTA (Boston)","MDOT MTA","MTA","NICE Bus (NYC)","NJ Transit","OC Transpo (Ottawa)","PAAC (Pittsburgh)","SEPTA - Bus","STM","STO","Canada","United States"]

actual = []
weekAgo= []
normal = []
act = 0
week= 0
norm= 0

for t in range(len(data)):
    required = 0
    if "name" in data[t]: #check "name" line 
         #name in required array, append its arrays
        for n in names: 
            if n in data[t]:
                required = 1
                break
        
        if required == 1:
            #print(data[t].split('"')[3], )
            act = data[t+1].split("actual")[1]
            act = act[act.index("[") + 1: act.index("]")].split(",")
            actual.append(act)

            week = data[t+2].split("week_ago")[1]
            week = week[week.index("[") + 1: week.index("]")].split(",")
            weekAgo.append(week)

            norm = data[t+3].split("normal")[1]
            norm = norm[norm.index("[") + 1: norm.index("]")].split(",")
            normal.append(norm)

for arr in weekAgo:
    for i in range(len(arr)):
        arr[i] = float(arr[i])      
for arr in normal:
    for i in range(len(arr)):
        arr[i] = float(arr[i])
for arr in actual:
    for i in range(len(arr)):
        arr[i] = float(arr[i])
        
actual = pd.DataFrame(data = actual, )
weekAgo = pd.DataFrame(data = weekAgo, )
normal = pd.DataFrame(data = normal, )

actual.to_csv("dummy/actualGraph.csv")
weekAgo.to_csv("dummy/weekAgoGraph.csv")
normal.to_csv("dummy/normalGraph.csv")

