# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 10:46:46 2021

@author: peter
"""

import requests
import pandas as pd

class powerPrices():
    def __init__(self):
        self.historic_weather = self.getWeatherDataFromFile()
        
        #Constants
        self.dataUrl = "https://www.nordpoolgroup.com/globalassets/marketdata-excel-files/elspot-prices_2021_hourly_nok.xls"
        
        
        
    def getPowerPricesFromServer(self):
        
        # Download power prices xls-file from URL
        r = requests.get(self.dataUrl, stream=True)
        r2 = r.content.decode('utf-8')
        r3 = r2.replace(",", ".")

        with open("powerPricesRaw.xls", "w") as f:
            #for chunk in r.iter_content(chunk_size=16*1024):
            print("\t Saving xls... ", end="")
            f.write(r3)
            #print("Done")
        
        #Converting tha data to DataFrame
        df = pd.read_html("powerPricesRaw.xls")[0]
        #Changing column Name
        l = []
        for i in df.columns:
            l.append(i[3])

        df.columns = l
        #Changing timestamp
        df["dt"] = df["Unnamed: 0_level_3"] +" "+ df["Hours"].str[:2]
        df["dt"] = pd.to_datetime(df["dt"], format="%d-%m-%Y %H")
        df["dt"] = df[['dt']].apply(lambda x: x[0].timestamp(), axis=1).astype(int)
        
        
        return df
    
        #df.to_csv("excel_to_csv.csv", index=False)
        
    def getWeatherDataFromFile(self):
        data = pd.read_csv("newWeatherData.csv", na_filter=False, dtype={"dt": "int64", "clouds_all":"int64"}, parse_dates=["dt_iso"]).drop_duplicates(subset=["dt"]).reset_index(drop=True)
        #data = pd.read_csv("newWeatherData.csv",  na_filter=False, skip_blank_lines=True)
        return data
        
    def writeWeatherDataToFile(self, data, path="newWeatherData.csv"):
        data.to_csv(path, index=False)
    
    def updateHistoricData(self, returnC=False):
        data = self.getPowerPricesFromServer().drop_duplicates(subset=["dt"]).reset_index(drop=True)
        
        
        # Get 'weatherData' from file
        weatherData = self.getWeatherDataFromFile()
        # Repaces ',' with '.'. Allws for conversion from str to float 
        weatherData.loc[:, "power_prices[NOK/MWh]"] = weatherData.loc[:, "power_prices[NOK/MWh]"].astype(str).str.replace(',','.')
        
        #Create a bool array that indicates where the DFs will be combined. This is to ensure that the Series are of the same length
        dataMin = data["dt"][0]
        dataMax = data["dt"][len(data["dt"])-1]
        
        weatherDataMin = weatherData["dt"][0]
        weatherDataMax = weatherData["dt"][len(weatherData["dt"])-1]
        
        a = (weatherData["dt"] > dataMin) & (weatherData["dt"] < dataMax)
        #print(len(weatherData[a]))
        b = (data["dt"] > weatherDataMin) & (data["dt"] < weatherDataMax)
        #print(len(data[b]))
        
        #Add the power cost data from 'data' to 'weatherData'.
        c = data.loc[b, "Tr.heim"]
        weatherData.loc[a, "power_prices[NOK/MWh]"] = c.to_list() #Convert c to list. This prevents index conflicts
        
        #Converts all data in "power price" series to str. Then used 'to_numeric' to convert to float. All values that can't be convertet, are made into NaN values for easier detection.
        weatherData.loc[:, "power_prices[NOK/MWh]"] = weatherData.loc[:, "power_prices[NOK/MWh]"].astype(str)
        weatherData.loc[:, "power_prices[NOK/MWh]"] = pd.to_numeric(weatherData.loc[:, "power_prices[NOK/MWh]"], errors='coerce')
        
        # Find all indexes where NaN is located. Add the locations to the list 'nanLocation'
        nanLocation = weatherData.loc[weatherData["power_prices[NOK/MWh]"].isnull(),"power_prices[NOK/MWh]"].index
        
        #Replace all NaN values, with the value that comes before it
        for i in nanLocation:
            weatherData.loc[i, "power_prices[NOK/MWh]"] = (weatherData.loc[i-1,"power_prices[NOK/MWh]"] + weatherData.loc[i+1,"power_prices[NOK/MWh]"]) / 2
        
        self.writeWeatherDataToFile(weatherData)
        if returnC:
            return weatherData
        
    def powerPriceNow(self):
        data = self.getWeatherDataFromFile()
        powerPrice = data["power_prices[NOK/MWh]"][len(data["dt"])-1]
        return powerPrice
        

if __name__ == "__main__":
    p = powerPrices()
    data = p.historic_weather
    
    #r2 = p.getPowerPricesFromServer()
    ppData = p.getPowerPricesFromServer()
    newData= p.updateHistoricData(returnC=True)
    print(p.powerPriceNow())