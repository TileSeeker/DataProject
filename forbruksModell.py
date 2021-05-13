# -*- coding: utf-8 -*-
"""
Created on Wed May 12 15:48:02 2021

@author: peter
"""
import pandas as pd
import datetime
import heatingSimulation

defaultRooms = {
    "0" : {"roomName" : "outside", "maxCapacity" : 12000000000, "peopleInRoom" : 8000000000, "tempSV" : 0, "tempPV" : 0},
    "1" : {"roomName" : "toilet", "maxCapacity" : 1, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "2" : {"roomName" : "bathroom", "maxCapacity" : 1, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "3" : {"roomName" : "kitchen", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "4" : {"roomName" : "livingroom", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "5" : {"roomName" : "bedroom1", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "6" : {"roomName" : "bedroom2", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "7" : {"roomName" : "bedroom3", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "8" : {"roomName" : "bedroom4", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "9" : {"roomName" : "bedroom5", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "10" : {"roomName" : "bedroom6", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
        }

defaultUsers = {
    "1" : {"name": "User1", "location":"0", "guests":"0", "activity":"0", "bedroom":"5"},
    "2" : {"name": "User2", "location":"0", "guests":"0", "activity":"0", "bedroom":"6"},
    "3" : {"name": "User3", "location":"0", "guests":"0", "activity":"0", "bedroom":"7"},
    "4" : {"name": "User4", "location":"0", "guests":"0", "activity":"0", "bedroom":"8"},
    "5" : {"name": "User5", "location":"0", "guests":"0", "activity":"0", "bedroom":"9"},
    "6" : {"name": "User6", "location":"0", "guests":"0", "activity":"0", "bedroom":"10"}
    }

defaultActivityPowerConsumption = {
    "0":{"name":"TV", "power":150},
    "1":{"name":"Oven", "power":1800},
    "2":{"name":"Sleep", "power":0},
    "3":{"name":"GamingPC", "power":1000},
    "4":{"name":"El.Guitar", "power":300},
    "5":{"name":"Hair_blower", "power":2400},
    "6":{"name":"Disco_lights", "power":3},
    "7":{"name":"Music_system", "power":160},
    "8":{"name":"Phone_charge", "power":11},
    "9":{"name":"Shower", "power":1340},
    "10":{"name":"Arduino", "power":244},
    "11":{"name":"Coffee", "power":879},
    "12":{"name":"Water_heater", "power":784},
    "13":{"name":"No_Power", "power":0},
    "14":{"name":"laptop_charge", "power":230}
    }

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
    
    def curentPowerConsumption(self):
        now = datetime.datetime.now()
        hour = int(now.strftime("%H"))
        tt = self.getUserHabitsFromFile()

        userPower = 0
        for i in self.users:
            name = self.users[i]['name']
            userPower = userPower + self.PC[tt.loc[hour, f"{name}_activity"]]["power"]
        
        
        data = self.getWeatherDataFromFile()
        dataHourIndex = pd.to_datetime(data["dt"], unit='s').dt.strftime('%H').astype(int)
        
        
        
        timestamp = int(now.timestamp())
        roomPower = 0
        for i in self.rooms:
            if i == '0':
                continue
            
            print((i, timestamp))
            roomPower = heatingSimulation.heatingPowerSimulation().roomPowerCalc(i, timestamp)
            print(roomPower)
        power = userPower + roomPower
        return power
        
    
    def currentUserLocation(self):
        pass
    
    
if __name__ == "__main__":
    p = userPowerConsumption()
    
    curentPower = p.curentPowerConsumption()
    print(curentPower)
    #data, tt = p.updateHistoricUserConsumption(returnC=True)
