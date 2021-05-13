# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:15:17 2021

@author: peter
"""
import pandas as pd
import datetime
import roomParameters

defaultRoomParameters = roomParameters.defaultRoomParameters
defaultConductivityTable = roomParameters.conductivityTable

class heatingPowerSimulation():
    def __init__(self, rooms=defaultRoomParameters, areaOverlap=None, conductivityTable = defaultConductivityTable):
        self.rooms = defaultRoomParameters
        #self.areaOverlap = defaultAreaOverlap
        self.conductivityTable = conductivityTable
        self.roomTempTimetable = self.getRoomTempTimetableFromFile()
        self.historic_weather = self.getWeatherDataFromFile()
        
        #constants
        self.groundTemp = 4 # Celsius
        self.ceilingTemp = 21 # Celsius
        
    def roomPowerCalc(self, room_ID, timestamp):        
        
        roomTemp = self.rooms[room_ID]["tempSV"]
        ceilingArea = floorArea = self.rooms[room_ID]["area"]        
        floorConductivity = self.conductivityTable["floor"]
        ceilingConductivity = self.conductivityTable["ceiling"]
        energy = 0
        
        for i in self.rooms[room_ID]["areaOverlap"]:
            # i = rooms that are in direct connection with the main room
                #print("Room_ID: ", end="")
                #print(i)

            #if self.rooms[room_ID]["areaOverlap"][i]:
                for j in self.rooms[room_ID]["areaOverlap"][i]:
                    #print("Room Name:", end="")
                    #print(j)
                    
                    
                    """
                     j = the dict key. The key is named after the area type: 
                        "outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1, "door":0
                                               
                    The value stored in the  of the area type being calculated:                        
                   """
                    area = self.rooms[room_ID]["areaOverlap"][i][j]
                    conductivity = self.conductivityTable[j]

                    if i == "0":
                        otherRoomTemp = self.getOutsideTempByTime(timestamp)
                        
                    else:                    
                        otherRoomTemp = self.getRoomTempByTime(i, timestamp)
                        
                    deltaT = (roomTemp - otherRoomTemp)
                    #print(deltaT)
    
                    energy =  energy + 5.7 * area * deltaT / conductivity
                    #print(energy)
                    
        #Add energy loss through ceiling and floor
        energy = energy + 5.7 * ( (roomTemp - self.groundTemp) * floorArea / floorConductivity  + (roomTemp - self.ceilingTemp) * ceilingArea / ceilingConductivity)
        
        return energy[0]    
    
    def getRoomTempByTime(self, room_ID, timestamp):
        data = self.historic_weather
        roomName = self.rooms[room_ID]["roomName"] 
        hour = None
        if type(timestamp) == int:
            hour = datetime.datetime.utcfromtimestamp(timestamp).strftime("%H")
            hour = int(hour)
        else:
            hour = pd.to_datetime(data["dt"], unit='s').dt.strftime("%H").astype(int)
                
        temp = self.roomTempTimetable.loc[hour, roomName]
        #print(temp)
        return temp
        
    
    def getOutsideTempByTime(self, timestamp):
        historic_weather = self.historic_weather.drop_duplicates(subset=["dt"])
        
        if type(timestamp) == int:
            historicOutsideTemp = historic_weather[historic_weather["dt"] == timestamp]["temp"] -273.15 # in Celsius
        
        else:
            historicOutsideTemp = historic_weather["temp"] -273.15 # in Celsius
        
        return historicOutsideTemp
    
    def getRoomTempTimetableFromFile(self):
        roomTempTimetable = pd.read_csv("roomTempTimetable.csv", sep=",", index_col=0)
        return roomTempTimetable
    
    def getWeatherDataFromFile(self):
        data = pd.read_csv("newWeatherData.csv", na_filter=False, dtype={"dt": "int64", "clouds_all":"int64", "temp":"float64"}, parse_dates=["dt_iso"])
        #data = pd.read_csv("newWeatherData.csv",  na_filter=False, skip_blank_lines=True)
        return data
    def writeWeatherDataToFile(self, data, path="newWeatherData.csv"):
        data.to_csv(path, index=False)
    
    def updateHeatingSimulationData(self, returnC=False):
        data = self.getWeatherDataFromFile().drop_duplicates(subset=["dt"]).reset_index(drop=True)
        roomTempTimetable = self.roomTempTimetable
        conductivityTable = self.conductivityTable
        rooms = self.rooms
        
        #Temp datafram that will contain the data for the calculations.
        #All the data is contained here to make the opperation easier to troubleshoot.
        df = pd.DataFrame()
        
        #Timestamp coulumb
        df["dt"] = data["dt"]
        
        #Hour columb
        df["hour"] = pd.to_datetime(data["dt"], unit='s').dt.strftime("%H").astype(int)
        
        #Outside temp
        df["outside_temp"] = data["temp"] -273.15
        
        #Room temp
        for i in rooms:
            roomName = rooms[i]['roomName'] 
            if roomName == "outside":
                #print("outside -> skip")
                continue
            
            df[f"{roomName}_temp"] = roomTempTimetable[roomName].loc[df["hour"]].reset_index(drop=True)
            #df[f"{roomName}_temp"] = roomTempTimetable[roomName][df["hour"]].reset_index(drop=True)
            """
            #df[f"{roomName}_temp"] = 0
            
            for j in range(len(df["hour"])-1):
                print(j)
                df[f"{roomName}_temp"][j] = roomTempTimetable[roomName][df["hour"][j]]
            """
        
        for i in rooms:
            """
            Tota Power in each room
            i = ["0", "1", "2" ...]
            """
            roomName = rooms[i]['roomName']            
            ceilingArea = floorArea = rooms[i]["area"]        
            floorConductivity = conductivityTable["floor"]
            ceilingConductivity = conductivityTable["ceiling"]
            #print(f"i == {i}: {rooms[i]['roomName']}")
            energy = 0
            energy_raw = 0
            for j in rooms[i]["areaOverlap"]:
                """
                Adjecent rooms
                j = ["0", "2", "3"]
                """
                #print(f"j == {j}")
                
                for k in rooms[i]["areaOverlap"][j]:
                    """
                     j = the dict key. The key is named after the area type: 
                        "outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1, "door":0
                                               
                    The value stored in the  of the area type being calculated:
                    """
                    #print(f"\t k == {k}: ")
                    area = rooms[i]["areaOverlap"][j][k]
                    conductivity = conductivityTable[k]
                    deltaT = df[f"{roomName}_temp"] - df[f"{rooms[j]['roomName']}_temp"]
                    energy_raw = energy_raw + 5.7 * deltaT *  area / conductivity
                    """
                    print(f"\t\t conductivity = {conductivity}")
                    print(f"\t\t area = {area}")
                    print(f"\t\t deltaT = ")
                    df[f"deltaT_{roomName}_{rooms[j]['roomName']}"] = df[f"{roomName}_temp"] - df[f"{rooms[j]['roomName']}_temp"]
                    """
            energyConCeiling = 5.7 * (df[f"{roomName}_temp"] - self.ceilingTemp) *ceilingArea / ceilingConductivity
            energyConFloor = 5.7 * (df[f"{roomName}_temp"] - self.groundTemp) * floorArea / floorConductivity
            energy_raw += energyConCeiling + energyConFloor
            
            df[f"{roomName}_heating_power [W/h]"] = abs(energy_raw)
            data[f"{roomName}_heating_power [W/h]"] = abs(energy_raw)
        
        #self.historic_weather = data
        self.writeWeatherDataToFile(data, "newWeatherData.csv") 
        
        if returnC:    
            return [data, df]

    
  
if __name__ == "__main__":
    s = heatingPowerSimulation()
    
    data = s.getWeatherDataFromFile()
    x = s.roomPowerCalc("1", 1577836800)
    print(x)
    #print(s.getRoomTempByTime("1", 1577836800))
    
    #roomTempTimetable = s.getRoomTempTimetableFromFile()
    #s.getOutsideTempByTime(1577836800)
    #historic_weather = s.getWeatherDataFromFile()
    #x = historic_weather[historic_weather["dt"] == 1578258000]["temp"]
    
    
    #data2 = s.updateHeatingSimulationData()
    
    #df = s.roomPowerCalc("1", 1577836800)
    y = s.roomTempTimetable
    
    data, x = s.updateHeatingSimulationData(returnC=True)
    #print(x)
    

    
