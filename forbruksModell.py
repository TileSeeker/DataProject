# -*- coding: utf-8 -*-
"""
Created on Wed May 12 15:48:02 2021

@author: peter
"""
import pandas as pd
import datetime
import heatingSimulation
import roomParameters
import Signals as s






class userPowerConsumption():
    def __init__(self):
        
        #Room and user parameters are retrieved from the parameters file
        self.rooms = roomParameters.defaultRoomParameters
        self.users = roomParameters.defaultUsers
        self.PC = roomParameters.ActivityPowerConsumption

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
            if self.rooms[i]["powerBilling"] == 'public':
                data.loc[:, "shared_power"] = data.loc[:, "shared_power"] + pd.to_numeric(data.loc[:, f"{self.rooms[i]['roomName']}_heating_power [W/h]"], errors='coerce')
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
    
    def updateUserLocation(self):
        """
        Henter henter lokasjon til brukerne fra timeplanen, og oppdaterer den på CoT
        """
        hour = int(datetime.datetime.now().strftime("%H"))
        tt = self.getUserHabitsFromFile()
        
        for i in self.users:
            location = str(tt.loc[hour, f"{self.users[i]['name']}_location"])
            roomParameters.defaultUsers[i]["location"] = location
            
        users = roomParameters.defaultUsers
        s.Signal("19808", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk1In0.9bD-g6Gi40yjEiEYGOY1eoWl0wEuAZZN67yzS5gYOQs").write(users["1"]["location"])
        s.Signal("24769", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk2In0.zADZlTeWjpJpbEmG_d1mcw07mDtT9ZJ30sMDtU1ex80").write(users["2"]["location"])
        s.Signal("20536", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk3In0.es9iHyTEfrYM3ksN0QWtiULhRlQEcwatXWHFc5_fscc").write(users["3"]["location"])
        s.Signal("3430", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk4In0.WP5pJqMaPL8AwEEii2TMFys9kQUabpl2iztyxBRdLuc").write(users["4"]["location"])
        s.Signal("2105", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk5In0.fbZfuVuDshnMdUMW6EXrB6fSYhtdq0l2-j92h6AtlbM").write(users["5"]["location"])
        s.Signal("10015", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjAwIn0.nGZXNRU34wVFtzex9tS-0gVky_ppn3Gjmj_riA4oLZY").write(users["6"]["location"])

    
if __name__ == "__main__":
    p = userPowerConsumption()
    x = p.recentPowerPrice()
    print(x)
    data, tt = p.updateHistoricUserConsumption(returnC=True)

    p.updateUserLocation()