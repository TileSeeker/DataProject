# -*- coding: utf-8 -*-
"""
Created on Wed May 12 15:48:02 2021

@author: peter
"""
import pandas as pd
import datetime
import heatingSimulation
import roomParameters


#Room and user parameters are retrieved from the parameters file
defaultRooms = roomParameters.defaultRoomParameters
defaultUsers = roomParameters.defaultUsers
defaultActivityPowerConsumption = roomParameters.ActivityPowerConsumption


class userPowerConsumption():
    def __init__(self, rooms=defaultRooms, users=defaultUsers, activityPowerConsumption=defaultActivityPowerConsumption):
        self.rooms = rooms
        self.users = users
        self.PC = activityPowerConsumption

    def getWeatherDataFromFile(self):
        data = pd.read_csv("newWeatherData.csv", na_filter=False, dtype={"dt": "int64", "clouds_all":"int64"}, parse_dates=["dt_iso"]).drop_duplicates(subset=["dt"])
        data = data.drop_duplicates(subset=["dt"]).reset_index(drop=True)
        return data   
    
    def getUserHabitsFromFile(self):
        data = pd.read_csv("userTimetable.csv", dtype="str")
        return data
    
    def writeWeatherDataToFile(self, data, path="newWeatherData.csv"):
        data.to_csv(path, index=False)
        
    def updateHistoricUserConsumption(self, returnC=False):

        data = self.getWeatherDataFromFile()
        tt = self.getUserHabitsFromFile()

        c3 = "Total_user_power"
        c4 = "Total_user_NOK"
        
        
        #Creating the columns that are relevant
        tt[c3] = 0
        data[c3] = 0
        data[c4] = 0
        
        for i in self.users:
            name = self.users[i]["name"]
            c1 = f"{name}_power_consumption"
            c2 = f"{name}_NOK"
            data[c1] = 0
            data[c2] = 0
            tt[c1] = 0
            
            for j in range(len(tt["hours"])):
                tt.loc[j, c1] = self.PC[tt.loc[j,f"{name}_activity"]]["power"]
            
            # Calculating total User power su summing the power used by each user
            tt.loc[:, c3] = tt.loc[:, c3] + tt.loc[:, c1]
            
            dataHourIndex = pd.to_datetime(data["dt"], unit='s').dt.strftime('%H').astype(int)
            data.loc[:, c1] = tt.loc[dataHourIndex, c1].to_list() + data.loc[:, f"{self.rooms[self.users[i]['bedroom']]['roomName']}_heating_power [W/h]"]
            data.loc[:, c2] = data.loc[:, c1]*10**(-6)*data.loc[:, "power_prices[NOK/MWh]"]
            
            data.loc[:, c3] = data.loc[:, c3] + data.loc[:, c1]#tt.loc[dataHourIndex, c3].to_list()
        data.loc[:,c4] = data.loc[:, c3]*10**(-6)*data.loc[:, "power_prices[NOK/MWh]"]
        
        data.loc[:, "shared_power"] = 0
        data.loc[:, "shared_NOK"] = 0
        for i in self.rooms:
            if i < '5':
                data.loc[:, "shared_power"] = data.loc[:, "shared_power"] + data.loc[:, f"{self.rooms[i]['roomName']}_heating_power [W/h]"]
        data.loc[:, "shared_NOK"] = data.loc[:, "shared_power"]*10**(-6)*data.loc[:, "power_prices[NOK/MWh]"]      
        
        self.writeWeatherDataToFile(data)   
        if returnC:
            return [data, tt]
        
        
    def recentPowerPrice(self):
        # Returnerer den siste registrerte strømprisen i øre/kWh 
        data = self.getWeatherDataFromFile()
        
        lastPos = len(data["dt"])-1
        recentPowerPrice = round(data.loc[lastPos, "power_prices[NOK/MWh]"] * 10**(-1), 3)
        return recentPowerPrice

    
if __name__ == "__main__":
    p = userPowerConsumption()
    x = p.recentPowerPrice()
    print(x)

    data, tt = p.updateHistoricUserConsumption(returnC=True)
