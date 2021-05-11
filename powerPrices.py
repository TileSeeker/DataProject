# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 10:46:46 2021

@author: peter
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

"""
url = "https://www.nordpoolgroup.com/historical-market-data/"
absXpath = "/html/body/div[4]/div/div/div[2]/div/div/div[1]/div/table/tbody/tr[6]/td[1]/a"

driver = webdriver.Firefox(executable_path="C:\Program Files\Mozilla Firefox\geckodriver.exe")
driver.get(url)
driver.find_element_by_xpath(absXpath).click()

"""




class powerPrices():
    def __init__(self):
        self.historic_weather = self.getWeatherDataFromFile()
        
        #Constants
        self.dataUrl = "https://www.nordpoolgroup.com/globalassets/marketdata-excel-files/elspot-prices_2021_hourly_nok.xls"
        
        
        
    def getPowerPricesFromServer(self):
        r = requests.get(self.dataUrl, stream=True)
        r2 = r.content.decode('utf-8')
        r3 = r2.replace(",", ".")

        with open("powerPricesRaw.xls", "w") as f:
            #for chunk in r.iter_content(chunk_size=16*1024):
            print("Saving xls... ", end="")
            f.write(r3)
            print("Done")
        
        #Converting tha data to DataFrame
        df = pd.read_html("powerPricesRaw.xls")[0]
        
        #Changing column Name
        l = []
        for i in df.columns:
            l.append(i[2])
        df.columns = l
        
        #Changing timestamp
        df["dt"] = df["Unnamed: 0_level_2"] +" "+ df["Hours"].str[:2]
        df["dt"] = pd.to_datetime(df["dt"], format="%d-%m-%Y %H")
        df["dt"] = df[['dt']].apply(lambda x: x[0].timestamp(), axis=1).astype(int)
        
        
        return df
    
        #df.to_csv("excel_to_csv.csv", index=False)
        
    def getWeatherDataFromFile(self):
        data = pd.read_csv("newWeatherData.csv", na_filter=False, dtype={"dt": "int64", "clouds_all":"int64", "temp":"float64"}, parse_dates=["dt_iso"]).drop_duplicates(subset=["dt"]).reset_index(drop=True)
        #data = pd.read_csv("newWeatherData.csv",  na_filter=False, skip_blank_lines=True)
        return data
        
    def updateHistoricData(self):
        data = self.getPowerPricesFromServer().drop_duplicates(subset=["dt"]).reset_index(drop=True)
        dataMin = data["dt"][0]
        dataMax = data["dt"][len(data["dt"])-1]
        
        weatherData = self.getWeatherDataFromFile()
        weatherDataMin = weatherData["dt"][0]
        weatherDataMax = weatherData["dt"][len(weatherData["dt"])-1]
        weatherData["test"] = 100.0
        
        a = (weatherData["dt"] > dataMin) & (weatherData["dt"] < dataMax)
        b = (data["dt"] > weatherDataMin) & (data["dt"] < weatherDataMax)
        c = data.loc[b, "Tr.heim"] 
        d = weatherData.loc[a, "test"]
        print(c)
        print(type(c))
        df = weatherData
        #df.loc[a, ["test"]] = #data.loc[b, ["Tr.heim"]]

        return [df, a, b, c, d]
        

if __name__ == "__main__":
    p = powerPrices()
    data = p.historic_weather
    
    #r2 = p.getPowerPricesFromServer()
    #ppData = p.getPowerPricesFromServer()
    newData, a, b, c, d = p.updateHistoricData()