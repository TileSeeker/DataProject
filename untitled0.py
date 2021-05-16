# -*- coding: utf-8 -*-
"""
Created on Sat May 15 20:25:11 2021

@author: peter
"""

import pandas as pd
import numpy as np
import datetime
import statistics

df = pd.read_csv("SolarPowerRaw.csv")
newColumns = df.loc[9, :].to_list()
df = df.loc[10:, :].reset_index(drop=True)
df.columns = newColumns
df["dt"] = pd.to_datetime(df["time"], format="%Y%m%d:%H%M")

df["P"] = df["P"].astype(float)

df["dt2"] = df["dt"].dt.strftime("%m%d%H%M")



startTimeStr = "20200101:0000"
endTimeStr =  "20201231:2300"

startTime = int(datetime.datetime.strptime(startTimeStr, "%Y%m%d:%H%M").timestamp())
endTime = int(datetime.datetime.strptime(endTimeStr, "%Y%m%d:%H%M").timestamp())
timeD = 3600


df2 = pd.DataFrame()
ts =[]
date = []
dateC = []
power = []
for i in range(startTime+1800, endTime+1800, timeD): 
    timestamp = i -1800
    data_in_datetime = datetime.datetime.utcfromtimestamp(i)
    timeCompare = data_in_datetime.strftime("%m%d%H%M")
    x = df.loc[df.loc[:,"dt2"]==timeCompare, "P"].to_list()
    y = np.mean(x)
    
    
    ts.append(timestamp)
    #date.append(data_in_datetime)
    dateC.append(timeCompare)
    power.append(y)
    
    
    
df2.loc[:,"ts"] = ts
#df2.loc[:,"date"] = date
df2.loc[:,"dateC"] = dateC
df2.loc[:, "P"] = power

df2.to_csv("solarIridiation.csv", index=False)

"""
df2.loc[:, "P"] = df.loc[df2.loc[:,"dateC"] == df.loc[:, "dt2"], "P"].to_list()
"""


"""
    x = statistics.mean(df.loc[df["dt2"]==timeS, "P"].to_list())
"""
    