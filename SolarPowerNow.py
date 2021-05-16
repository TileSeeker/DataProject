# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 14:29:08 2021

@author: peter

Hensikten med dette programmet er å beregnet hvor mye energi blir generert NÅ

Henter Solopp-, Solnedgang og skydekke

Hvis sol_er_oppe:
    solenergi = panelstyrke * max_loss*(100 - skydekke)
"""
import pandas as pd
import requests
import json
import time
import datetime
from suntime import Sun, SunTimeException




class SolarPower:
    def __init__(self):
        #Solar Array Data
        self.itemCode = "ALTS-200W-24P"
        self.solarPanelEfficiency = 0.1572 #Prosent
        self.solarPanelMinTemp = -40 # Celsius
        self.solarPanelMaxTemp = 80 # Celsius
        self.solarPanelPower = 4864 # W
        self.solarPanelArea = 32 # m^2
        self.powersqm = 153 #W/m^2
        
        
        # Constants
        self.solarIridiationConstant = 1367 #W/m^2
        self.solarPanelMaxCloudLoss = 0.30# prosent
        self.lat = 63.42
        self.lon = 10.40
        self.city = "Trondheim"
        self.sun = Sun(self.lat, self.lon)
        
        #data
        self.weatherData = self.getWeatherDataFromFile()
        
        #Weather Data
        self.key = "8554bc4036b0ec568b136bbba124d344"
        self.url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.key}"
        
    def getWeatherDataFromFile(self):
        #data = pd.read_csv("weatherHistoryHourly.csv", dtype={"dt": "int64", "clouds_all":"int64"}, parse_dates=["dt_iso"])
        data = pd.read_csv("newWeatherData.csv", dtype={"dt": "int64", "clouds_all":"int64"}, parse_dates=["dt_iso"])
        return data
    
    def getIridiationDataFromFile(self):
        irridiationData = pd.read_csv("solarIridiation.csv", dtype={"P":"float64"})
        return irridiationData
        
    def weatherCoefficient(self, timestamp = None, date = None, row=None, data=None):
        
        if timestamp != None:
            cloud_coverage = row = data.loc[data["dt"] == timestamp, "clouds_all"]
            cloudCoefficient = 1-(self.solarPanelMaxCloudLoss*cloud_coverage/100)
            
            return cloudCoefficient
        
        elif date != None:
            pass
        
        elif row != None:
            cloud_coverage = data["clouds_all"][row]
            cloudCoefficient = 1-(self.solarPanelMaxCloudLoss*cloud_coverage/100)
            
            return cloudCoefficient
            
        else:
            return 1
            
        return 1
    
    
    
    def irradiationCoefficient(self, timestamp = None, data=None):
        return 1
    
    def powerCalculationHour(self, timestamp = None, row = None, data=None):
        
        timestamp = data["dt"][row]
        sunRise = self.sun.get_sunrise_time(datetime.datetime.utcfromtimestamp(timestamp)).replace(tzinfo=None)
        sunSet = self.sun.get_sunset_time(datetime.datetime.utcfromtimestamp(timestamp)).replace(tzinfo=None)
        dataTime = datetime.datetime.utcfromtimestamp(timestamp)
        
        if sunRise < dataTime < sunSet:
            return self.solarIridiationConstant * self.solarPanelEfficiency *self.weatherCoefficient(row=row, data=data) * self.irradiationCoefficient()
        
        else:
            return 0
    
    def updateHistoricSolarPowerGeneration(self):
       data = self.getWeatherDataFromFile()
       data.loc[:,"generated_solar_power[Wh]"] = 0.1
       iri = self.getIridiationDataFromFile()
       
       for i in range(len(data["dt"])-1):
           timeC = datetime.datetime.utcfromtimestamp(data["dt"][i]).strftime("%m%d%H%M")
           series = iri.loc[iri["dateC"] == int(timeC), "P"]

           try:
               power = series.to_list()[0]
           except:
               timeC = datetime.datetime.utcfromtimestamp(data["dt"][i-1]).strftime("%m%d%H%M")
               series = iri.loc[iri["dateC"] == int(timeC), "P"]
               power = series.to_list()[0]
           
           
           data.loc[i, "generated_solar_power[Wh]"] = power
       
       data.loc[:, "generated_solar_power[Wh]"].astype(float)
       """
       for i in range(len(data["dt"])):
           #data2["generated_solar_power[Wh]"][i] = self.powerCalculationHour(data["dt"][i])
           data.loc[:,"generated_solar_power[Wh]"].iloc[i] = self.powerCalculationHour(row = i, data=data)
           #print(f"{data['generated_solar_power[Wh]'][i]}  =   {self.powerCalculationHour(row = i)}")  
           
       """
       data.to_csv("newWeatherData.csv", index=False)
        
       return data

    def updateHistoricWeatherData(self):
    
        oldWeatherData = self.getWeatherDataFromFile() # Get data
        lastOldDataTimestamp = oldWeatherData.loc[:,"dt"].iloc[len(oldWeatherData["dt"])-1] + 86400 # Last Timestamp
        lastOldDataDate = datetime.datetime.utcfromtimestamp(lastOldDataTimestamp) # Last Timestamp in datetime format
        lastOldDataDay = lastOldDataDate.replace(hour = 0)  # Last timestamp day 
        
        currentDate = datetime.datetime.utcnow()
        currentDateTimestamp = int(currentDate.timestamp())
        
        deltatime = (currentDate - lastOldDataDay)
        
        df = df2 = pd.DataFrame(columns=oldWeatherData.columns)
        
        
        for days in range(deltatime.days):
            
            
            if (deltatime.days - days) < 5:
                timestamp = int((lastOldDataDay + datetime.timedelta(days=days)).timestamp()) + 7200
                data = self.getHistoricWeatherDataFromTimestamp(timestamp)
                df2 = pd.DataFrame(data["hourly"]).rename(columns={"clouds":"clouds_all"})
                
                df = df.append(df2).reset_index(drop=True)
                
            else:
                yesterdayTimestamp = int((lastOldDataDay + datetime.timedelta(days=deltatime.days) - datetime.timedelta(days=1)).timestamp())
                data = self.getHistoricWeatherDataFromTimestamp(yesterdayTimestamp)
                df2 = pd.DataFrame(data["hourly"]).rename(columns={"clouds":"clouds_all"})
                
                timestamp = int((lastOldDataDay + datetime.timedelta(days=days)).timestamp()+7200)
                #return lastOldDataDay
                for n in range(len(df2["dt"])):
                    df2["dt"][n] = timestamp + 3600*n
                    
                df = df.append(df2).reset_index(drop=True)
                
        
        df.loc[:,"dt"] = pd.to_numeric(df["dt"]).astype(int)
        
        for i in range(len(df["dt"])):
            
            df.loc[:,"dt_iso"].iloc[i] = str (datetime.datetime.utcfromtimestamp(df["dt"][i])) + " +0000 UTC"
        
        newWeatherData = oldWeatherData.append(df)
        newWeatherData.to_csv("newWeatherData.csv", index=False)
        
        return(df)
        
    
    def getHistoricWeatherDataFromTimestamp(self, timestamp):
        hUrl = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={self.lat}&lon={self.lon}&dt={timestamp}&appid={self.key}"
        get = requests.get(hUrl)
        hWeather = json.loads(get.content)

        return hWeather
        
        
    def getWeatherNow(self):
        
        get = requests.get(self.url)
        data = json.loads(get.content)
        
        return data    
    
    def getSolarPowerNow(self): 
        
        data = self.getWeatherNow()
        
        cloudFactor = data["clouds"]["all"] / 100
        sunRiseUnix = data["sys"]["sunrise"]
        sunSetUnix = data["sys"]["sunset"]
        
        systemSize = 6000 #W
        maxCloudLoss = 0.30 #prosent
        
        currentTimeUnix = time.time()
        if currentTimeUnix > sunRiseUnix and currentTimeUnix < sunSetUnix:
            return systemSize * (1 - maxCloudLoss *cloudFactor)
        
        else:
            return 0


# Test function 
# When the file is run as main, it wil automatically run several functions to make sure the program works
if __name__ == "__main__":

    sim = SolarPower()

    d = sim.updateHistoricWeatherData()
    data = sim.getWeatherDataFromFile() 
    powerData = sim.updateHistoricSolarPowerGeneration()
    e = sim.getWeatherNow()
    f = sim.getSolarPowerNow()   

    
    I = sim.getIridiationDataFromFile()

    
