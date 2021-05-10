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
    
    
    
    "0" : {"roomName" : "outside", "maxCapacity" : 12000000000, "peopleInRoom" : 8000000000, "tempSV" : 0, "tempPV" : 0, "area":510064472000, "areaOverlap":{}},
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


"""
defaultAreaOverlap = {
    "1":{
        "0":{"outside_wall":3, "window":1.2}, 
        "2":{"inside_wall":4}, 
        "3":{"inside_wall":4}, 
        "4":{"inside_wall":2.37, "door":1.63},
        },
    "2":{
        "0":{"outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1.2, "door":0}, 
        "1":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "3":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "4":{"outside_wall":0,"inside_wall":2.37, "ceiling":4, "floor":4, "window":0, "door":1.63},
        "5":0
        },
    "3":{
        "0":{"outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1, "door":0}, 
        "1":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "2":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "4":{"outside_wall":0,"inside_wall":2.37, "ceiling":4, "floor":4, "window":0, "door":1.63},
        "5":0
        },
    "4":{
        "0":{"outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1, "door":0}, 
        "2":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "3":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "4":{"outside_wall":0,"inside_wall":2.37, "ceiling":4, "floor":4, "window":0, "door":1.63},
        "5":0
        },
    "5":{
        "0":{"outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1, "door":0}, 
        "2":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "3":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "4":{"outside_wall":0,"inside_wall":2.37, "ceiling":4, "floor":4, "window":0, "door":1.63},
        "5":0
        },
    "6":{
        "0":{"outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1, "door":0}, 
        "2":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "3":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "4":{"outside_wall":0,"inside_wall":2.37, "ceiling":4, "floor":4, "window":0, "door":1.63},
        "5":0
        },
    "7":{
        "0":{"outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1, "door":0}, 
        "2":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "3":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "4":{"outside_wall":0,"inside_wall":2.37, "ceiling":4, "floor":4, "window":0, "door":1.63},
        "5":0
        },
    "8":{
        "0":{"outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1, "door":0}, 
        "2":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "3":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "4":{"outside_wall":0,"inside_wall":2.37, "ceiling":4, "floor":4, "window":0, "door":1.63},
        "5":0
        },
    "9":{
        "0":{"outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1, "door":0}, 
        "2":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "3":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "4":{"outside_wall":0,"inside_wall":2.37, "ceiling":4, "floor":4, "window":0, "door":1.63},
        "5":0
        },
    "10":{
        "0":{"outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1, "door":0}, 
        "2":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "3":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "4":{"outside_wall":0,"inside_wall":2.37, "ceiling":4, "floor":4, "window":0, "door":1.63},
        "5":0
        },
    "11":{
        "0":{"outside_wall":3,"inside_wall":0, "ceiling":4, "floor":4, "window":1, "door":0}, 
        "2":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "3":{"outside_wall":0,"inside_wall":4, "ceiling":4, "floor":4, "window":0, "door":0}, 
        "4":{"outside_wall":0,"inside_wall":2.37, "ceiling":4, "floor":4, "window":0, "door":1.63},
        "5":0
        }
    }
"""
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

            #if self.rooms[room_ID]["areaOverlap"][i]:
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
        
        return energy
        
            
        
        
    
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
    
    def updateHeatingSimulationData(self):
        data = data2 =  self.getWeatherDataFromFile().drop_duplicates(subset=["dt"])
        for i in self.rooms:
            # i == room_ID: {"0", "1", "2", ...}
            #data[f"{self.rooms[i]['roomName']}_heating_power [W/h]"] = self.roomPowerCalc(i, data2["dt"])
            data[f"{self.rooms[i]['roomName']}_heating_power [W/h]"] = 0
        """    
        for i in data["dt"]:
            for j in self.rooms:
                data.loc[data["dt"]==i, self.rooms[j]["roomName"]] = self.roomPowerCalc(j, i)
        """
        """
        for i in self.rooms:
            data[f"{self.rooms[i]['roomName']}_heating_power [W/h]"] = 
        """
        return data
        #maxIndex = len(data["dt"])-1
        #minIndex = 

    
    def enterDataAfterLastColumnValue(self, column, data, dataset=None,):
        if not(dataset):
            dataset = self.getWeatherDataFromFile()
        pass
    
        
    
if __name__ == "__main__":
    s = heatingPowerSimulation()
    
    data = s.getWeatherDataFromFile()
    print(s.roomPowerCalc("1", 1577836800))
    print(s.getRoomTempByTime("1", 1577836800))
    
    roomTempTimetable = s.getRoomTempTimetableFromFile()
    s.getOutsideTempByTime(1577836800)
    historic_weather = s.getWeatherDataFromFile()
    x = historic_weather[historic_weather["dt"] == 1578258000]["temp"]
    
    
    #data2 = s.updateHeatingSimulationData()
    df = s.roomPowerCalc("1", data["dt"])
    

    
