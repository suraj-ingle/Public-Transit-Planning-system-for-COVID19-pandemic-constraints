#!/usr/bin/env python
# coding: utf-8

# In[20]:


# importing libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# for calculating mean_squared error
from sklearn.metrics import mean_squared_error

# creating a dataset with curvilinear relationship

startDay  = 37

y = np.array([-71,-70,-74,-74,-73,-73,-70,-71,-74,-74,-75,-75,-74,-72,-73,-76,-76,-76,-76,-74,-73,-76,-76,-77,-77,-75,-75,-73,-73,-77,-77,-77,-76,-74,-73,-74,-76,-75,-77,-76,-73,-70,-73,-75,-75,-75,-76,-74,-70,-72,-74,-74,-74,-73,-70,-68,-69,-72,-72,-72,-72,-70,-67,-69,-68,-69,-70,-70,-65,-64,-63,-67,-67,-66,-68,-63,-60,-63,-64,-65,-66,-64,-60,-58,-61,-62,-64,-63,-61,-57,-56,-56,-59,-60])

endDay = startDay + len(y)

x= np.arange(len(y))

# plotting dataset


# In[74]:


model = np.poly1d(np.polyfit(x,y,2))
myLine = np.linspace(1,endDay + 50, len(y) + 50)
modelVal = model(myLine)

plt.figure(figsize=(10,5))
plt.scatter(x,y,s=15)
plt.plot(myLine, model(myLine))
plt.xlabel('Predictor',fontsize=16)
    plt.ylabel('Target',fontsize=16)
plt.show()


# In[75]:



# yNormal = []
# for i in range(len(y)):
#     yNormal.append(y[i] - model(myLine).min() +  model(myLine)[i])
# #     print(float(model(myLine)[i]), y[i] , )

# plt.plot(modelVal)
# plt.plot(y)


# In[48]:


# len(model(myLine))
# len(y) + 50


# In[ ]:




