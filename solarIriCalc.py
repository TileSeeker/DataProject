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
endTimeStr =  "20210101:0000"

startTime = int(datetime.datetime.strptime(startTimeStr, "%Y%m%d:%H%M").timestamp())
endTime = int(datetime.datetime.strptime(endTimeStr, "%Y%m%d:%H%M").timestamp())
timeD = 3600


df2 = pd.DataFrame()
dateC = []
power = []
for i in range(startTime+1800, endTime+1800, timeD): 
    
    #Getting data from raw Data file. Must compensate for the fact that the time is formatet as every half-hour: [0030, 0130, ... ] 
    data_in_datetime = datetime.datetime.fromtimestamp(i)
    timeCompare = data_in_datetime.strftime("%m%d%H%M")
    x = df.loc[df.loc[:,"dt2"]==timeCompare, "P"].to_list()
    y = np.mean(x)

    #Prepare for mergig with other main Data fromatet per whole hour [0000, 0100, ... ]
    data_in_datetime = datetime.datetime.fromtimestamp(i-1800)
    timeCompare = data_in_datetime.strftime("%m%d%H%M")
    

    dateC.append(timeCompare)
    power.append(y)
    

df2.loc[:,"dateC"] = dateC
df2.loc[:, "P"] = power

df2.to_csv("solarIridiation.csv", index=False)

    