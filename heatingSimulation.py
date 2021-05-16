# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:15:17 2021

@author: peter
"""
import pandas as pd
import datetime
import roomParameters
import Signals as s

class heatingPowerSimulation():
    def __init__(self):
        self.rooms = roomParameters.defaultRoomParameters
        self.conductivityTable = roomParameters.conductivityTable
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

            for j in self.rooms[room_ID]["areaOverlap"][i]:
                    
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
    
                energy =  energy + 5.7 * area * deltaT / conductivity

                    
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
        data = pd.read_csv("newWeatherData.csv", na_filter=False, 
                           dtype={"dt": "int64", "clouds_all":"int64", "temp":"float64"}, 
                           parse_dates=["dt_iso"])
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
                continue
            
            df[f"{roomName}_temp"] = roomTempTimetable[roomName].loc[df["hour"]].reset_index(drop=True)
        
        for i in rooms:
            """
            Tota Power in each room
            i = ["0", "1", "2" ...]
            """
            roomName = rooms[i]['roomName']            
            ceilingArea = floorArea = rooms[i]["area"]        
            floorConductivity = conductivityTable["floor"]
            ceilingConductivity = conductivityTable["ceiling"]
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
                    area = rooms[i]["areaOverlap"][j][k]
                    conductivity = conductivityTable[k]
                    deltaT = df[f"{roomName}_temp"] - df[f"{rooms[j]['roomName']}_temp"]
                    energy_raw = energy_raw + 5.7 * deltaT *  area / conductivity

            energyConCeiling = 5.7 * (df[f"{roomName}_temp"] - self.ceilingTemp) *ceilingArea / ceilingConductivity
            energyConFloor = 5.7 * (df[f"{roomName}_temp"] - self.groundTemp) * floorArea / floorConductivity
            energy_raw += energyConCeiling + energyConFloor
            
            #If the energy leaving the room is positive, use the rooms heating factor. If the energy is negative, use the cooling factor
            data.loc[energy_raw >= 0, f"{roomName}_heating_power [W/h]"] = energy_raw.loc[energy_raw>0] * rooms[i]["heatingFactor"]
            data.loc[energy_raw < 0, f"{roomName}_heating_power [W/h]"] = energy_raw.loc[energy_raw<0] * rooms[i]["coolingFactor"]            
            df.loc[:, f"{roomName}_heating_power [W/h]"] = data.loc[:, f"{roomName}_heating_power [W/h]"]
        
        #Save the new values to the weatherData file
        self.writeWeatherDataToFile(data, "newWeatherData.csv") 
        
        if returnC:    
            return [data, df]

    def updateRoomTempSP(self):
        hour = int(datetime.datetime.now().strftime("%H"))
        roomTempTable = self.getRoomTempTimetableFromFile()
    
        for i in self.rooms:
            if self.rooms[i]['roomName'] == 'outside':
                continue
            tempSV = int(roomTempTable.loc[hour, f"{self.rooms[i]['roomName']}"])
            roomParameters.defaultRoomParameters[i]["tempSV"] = tempSV
            
            
        rooms = roomParameters.defaultRoomParameters
        s.Signal("2543", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NDg2In0.tyfmG1iU9rh9WTSgQWSjeFRB4hv8XfEH166Oz2MvUlg").write(rooms["1"]["tempSV"])
        s.Signal("22010", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjcxIn0.tcPW357AsU-ZQP8XrlSmbXu9q0Sto27hpiVv5pnSbGA").write(rooms["2"]["tempSV"])
        s.Signal("14456", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NDg3In0.6MTURel9ZoJj50PN6aWAodakTv3k8rDjrF99Udk14nU").write(rooms["3"]["tempSV"])
        s.Signal("10733", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NDg4In0.nw7WrxngCNMhk7SgNnmuSI2Ht8_ESCDfdhJZqB-joJc").write(rooms["4"]["tempSV"])
        s.Signal("25901", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NDg5In0.BM73ysSfKKQDToNknonEI2KzO7oKwHQjLKUKIz9omyg").write(rooms["5"]["tempSV"])
        s.Signal("18399", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NDkwIn0.-KW0hqJRmbC1W61EJNkv1HjI47RGzg6G30KzhQlGYbw").write(rooms["6"]["tempSV"])
        s.Signal("19772", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NDkxIn0.aSusWa3j_LOPHIdmSh8vZ5GCzTTVaVOzoqqU_QfyCMw").write(rooms["7"]["tempSV"])
        s.Signal("19704", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NDkyIn0.Wv9KcGzlGCMTB0cXM9t0s0jX8g0dmyG1CCzmvYE5V4k").write(rooms["8"]["tempSV"])
        s.Signal("10205", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NDkzIn0.yQ3fNM61ecxH4U1f01kW9D8hUm5pbTlSNTPMMI9GKDc").write(rooms["9"]["tempSV"])
        print(s.Signal("22658", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NDk0In0.yFXNG1sNpLgb30l7jGx7XFwLgxchWOMOQpHcwjcAZQE").write(rooms["10"]["tempSV"]))
     
  
if __name__ == "__main__":
    sim = heatingPowerSimulation()
    
    data = sim.getWeatherDataFromFile()
    x = sim.roomPowerCalc("1", 1577836800)
    print(x)
    print(sim.getRoomTempByTime("1", 1577836800))

    y = sim.roomTempTimetable
    
    data, x = sim.updateHeatingSimulationData(returnC=True)
    print(x)
    
    sim.updateRoomTempSP()
    

    
