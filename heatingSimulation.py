# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:15:17 2021

@author: peter
"""
import pandas as pd
import datetime

defaultRoomParameters = {
    # Windows = 1m * 1.2m = 1.2m^2
    # Doors = 1.63m^2
    # Ceiling height = 2.3m
    
    
    
    "0" : {"roomName" : "outside", "maxCapacity" : 12000000000, "peopleInRoom" : 8000000000, "tempSV" : 0, "tempPV" : 0, "area":0, "areaOverlap":{}},
    "1" : {"roomName" : "toilet", "maxCapacity" : 1, "peopleInRoom" : 0, "tempSV" : 28, "tempPV" : 0, "area":2.5, 
           "areaOverlap":{
               "0":{"outside_wall":2.873}, 
               "2":{"inside_wall":4.4}, 
               "4":{"inside_wall":5.854, "door":1.63},
                         }
          },
    
    "2" : {"roomName" : "bathroom", "maxCapacity" : 1, "peopleInRoom" : 0, "tempSV" : 28, "tempPV" : 0, "area":3,
           "areaOverlap":{
               "0":{"outside_wall":6.8875}, 
               "1":{"inside_wall":4.4}, 
               "4":{"inside_wall":1.82, "door":1.63},
               "10":{"inside_wall":1.4375}
                         }
          },
    
    "3" : {"roomName" : "kitchen", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":8,
            "areaOverlap":{
               "0":{"outside_wall":10.0625}, 
               "4":{"inside_wall":4.6, "air":9.2}, 
               "11":{"inside_wall":4.6},
                        }
           },
    
    "4" : {"roomName" : "livingroom", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":28.5,
           "areaOverlap":{
               "0":{"outside_wall":8.045, "door":1.63, "window":2.4},
               "1":{"inside_wall":5.854, "door":1.63},
               "2":{"inside_wall":1.82, "door":1.63},
               "3":{"inside_wall":4.6, "air":9.2},
               "5":{"inside_wall":4.025, "door":1.63},
               "6":{"inside_wall":2.97, "door":1.63},
               "7":{"inside_wall":9.87, "door":1.63},
               "8":{"inside_wall":9.87, "door":1.63},
               "9":{"inside_wall":2.97, "door":1.63},
               "10":{"inside_wall":4.025, "door":1.63},
               "11":{"inside_wall":5.37, "door":1.63}
                         }
           },
    
    "5" : {"roomName" : "bedroom1", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":6,
           "areaOverlap":{
               "0":{"outside_wall":11.9, "window":1.2},
               "4":{"inside_wall":4.025, "door":1.63},
               "6":{"inside_wall":1.4375},
               "11":{"inside_wall":1.4375}
                          }
           },
    "6" : {"roomName" : "bedroom2", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 12, "tempPV" : 0, "area":6,
           "areaOverlap":{
               "0":{"outside_wall":8.8625, "window":1.2},
               "4":{"inside_wall":2.97, "door":1.63},
               "5":{"inside_wall":1.4375},
               "7":{"inside_wall":6.9}
                         }
           },
    "7" : {"roomName" : "bedroom3", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":6,
           "areaOverlap":{
               "0":{"outside_wall":3.4, "window":1.2},
               "4":{"inside_wall":9.87, "door":1.63},
               "6":{"inside_wall":6.9}
                         }
           },
    "8" : {"roomName" : "bedroom4", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":6,
           "areaOverlap":{
               "0":{"outside_wall":3.4, "window":1.2},
               "4":{"inside_wall":9.87, "door":1.63},
               "9":{"inside_wall":6.9}
                         }
           },
    "9" : {"roomName" : "bedroom5", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":6,
           "areaOverlap":{
               "0":{"outside_wall":8.8625, "window":1.2},
               "4":{"inside_wall":2.97, "door":1.63},
               "8":{"inside_wall":6.9},
               "10":{"inside_wall":1.4375}
                         }
           },
    "10" : {"roomName" : "bedroom6", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":6,
            "areaOverlap":{
                "0":{"outside_wall":11.9, "window":1.2},
                "2":{"inside_wall":1.4375},
                "4":{"inside_wall":4.025, "door":1.63},
                "9":{"inside_wall":1.4375}
                }
            },
    "11" : {"roomName" : "server", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 15, "tempPV" : 0, "area":6, 
            "areaOverlap":{
                "0":{"outside_wall":10.0625},
                "3":{"inside_wall":4.6},
                "4":{"inside_wall":5.37, "door":1.63},
                "5":{"inside_wall":1.4375}
                          }
            }
        
    }

defaultConductivityTable = {
    "outside_wall":31.3, # outside_wall
    "inside_wall":4.1, # inside_wall
    "ceiling":13, #ceiling
    "floor":12.7, #floor
    "window":4, # window
    "door":3, # door
    "air": 0.25
        }

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
                print("Room_ID: ", end="")
                print(i)

            #if self.rooms[room_ID]["areaOverlap"][i]:
                for j in self.rooms[room_ID]["areaOverlap"][i]:
                    print("Room Name:", end="")
                    print(j)
                    
                    
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
                    print(deltaT)
    
                    energy =  energy + 5.7 * area * deltaT / conductivity
                    print(energy)
                    
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
        print(temp)
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
    #print(s.roomPowerCalc("1", 1577836800))
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
    

    
