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
        data = pd.read_csv("weatherHistoryHourly.csv", dtype={"dt": "int64", "clouds_all":"int64"}, parse_dates=["dt_iso"])
        return data
        
    def weatherCoefficient(self, timestamp = None, date = None, row=None, data=None):
        
        if timestamp != None:
            cloud_coverage = row = data.loc[data["dt"] == timestamp, "clouds_all"]
            #cloud_coverage = float(row["clouds_all"])
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
       data["generated_solar_power[Wh]"] = 0.1
       
       for i in range(len(data["dt"])):
           #data2["generated_solar_power[Wh]"][i] = self.powerCalculationHour(data["dt"][i])
           data["generated_solar_power[Wh]"][i] = self.powerCalculationHour(row = i, data=data)
           #print(f"{data['generated_solar_power[Wh]'][i]}  =   {self.powerCalculationHour(row = i)}")  
       data.to_csv("test.csv")
        
       return data

    def updateHistoricWeatherData(self):
        oldWeatherData = self.getWeatherDataFromFile()
        
        endOfOldData = oldWeatherData["dt"][len(oldWeatherData["dt"])-1]
        
        historicUrl = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={self.lat}&lon={self.lon}&dt={endOfOldData}&appid={self.key}"       
        
        get = requests.get(historicUrl)
        NewWeatherData = json.loads(get.content)
        
        
        #print(NewWeatherData)
        
        
        
        
        return NewWeatherData
    
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
    """
    w = Weather()
    
    print(w.getWeatherNow())
    print(w.getSolarPowerNow())
        

    s = SolarPower()
    data = s.getWeatherDataFromFile()
    timestamp = datetime.date.fromtimestamp(data["dt"][1])
    print(timestamp)
    
    data.duplicated("dt")
    
    data2 = s.updateHistoricSolarPowerGeneration()
    print(data2)
    
    lat = 63.42
    lon = 10.40
    
    sun = Sun(lat, lon)
    
    today_sr = sun.get_sunrise_time()
    today_ss = sun.get_sunset_time()
    
    print(today_sr)
    print(today_ss)
    
    abd_sr = sun.get_local_sunrise_time(datetime.date.fromtimestamp(1577840400)).replace(tzinfo=None)
    print(abd_sr)
    
    sbd_sr2 = sun.get_local_sunrise_time(datetime.date.fromtimestamp(1578513600)).replace(tzinfo=None)
    print(sbd_sr2)
    
    sr_test = sun.get_local_sunrise_time(datetime.date.fromtimestamp(data["dt"][0]))
    print(sr_test)
    print(type(sr_test))
"""

    s = SolarPower()
    d = s.updateHistoricWeatherData()
    data = s.getWeatherDataFromFile() 
    data2 = pd.DataFrame(columns=data.columns)
    #print(d)
    """
    for day in missing_days:
        for hour in day:
            for header in hour
                data[header] = hour[header]
    
    for hour in range(len(d["hourly"])):
        for header in data.columns:
            data
        print(d["hourly"][hour]["dt"])
    
    print(d["hourly"][0]["dt"])
    
    print(d["hourly"][0])
    
    """
    #d2 = pd.DataFrame(d["hourly"])
    newData = pd.read_csv("newWeatherData.csv", dtype={"dt": "int64", "clouds_all":"int64"}, parse_dates=["dt_iso"])
    
    t1 = datetime.datetime.utcfromtimestamp(data["dt"][len(data["dt"])-1]).replace(hour=0)
    print(t1)
    
    t4 = datetime.datetime.utcfromtimestamp(data["dt"][len(newData["dt"])-1]).replace(hour=0)
    print(t4)
    
    """
    print(t1)
    t2 = datetime.datetime.now()
    t3 = t2 - t1
    
    df3 = pd.DataFrame()
    for days in range(t3.days):
        timestamp = int((t1+datetime.timedelta(days=days)).timestamp())
        w = s.getHistoricWeatherDataFromTimestamp(timestamp)
        
        df2 = df.rename(columns={"clouds":"clouds_all"})
        for t in range(len(df2["dt"])):
            utc_str = str(datetime.datetime.utcfromtimestamp(int(df2["dt"][t]))) + " +0000 UTC"
                #print(utc_str)
                #df2["dt_iso"][t] = utc_str
        print(f"{days} is out of range")
        df3 = df3.append(df2).reset_index(drop=True)
    df3["dt_iso"]=0
    for t in range(len(df3["dt"])):
          utc_str = str(datetime.datetime.utcfromtimestamp(int(df3["dt"][t]))) + " +0000 UTC"
          
          df3["dt_iso"][t] = utc_str
    data3 = data.append(df3).reset_index(drop=True)
    data3.to_csv("newWeatherData2", index=False)
        
    
    
    #url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={s.lat}&lon={slon}&dt={timestamp}&appid={s.key}"
    
    """
    """
    for days in range(1, t3.days):
        date = t1 + datetime.timedelta(days=days)
        print(date)
        timestamp = int(date.timestamp())
        print(timestamp)
        url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={s.lat}&lon={s.lon}&dt={timestamp}&appid={s.key}"
        get = requests.get(url)
        NewWeatherData = json.loads(get.content)
        print(NewWeatherData)
        #df = pd.DataFrame(NewWeatherData["hourly"])
        #print(df)      

    """
    
