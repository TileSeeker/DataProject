# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:15:17 2021

@author: peter
"""
import pandas as pd
defaultRoomParameters = {
    "0" : {"roomName" : "outside", "maxCapacity" : 12000000000, "peopleInRoom" : 8000000000, "tempSV" : 0, "tempPV" : 0},
    "1" : {"roomName" : "toilet", "maxCapacity" : 1, "peopleInRoom" : 0, "tempSV" : 28, "tempPV" : 0},
    "2" : {"roomName" : "bathroom", "maxCapacity" : 1, "peopleInRoom" : 0, "tempSV" : 28, "tempPV" : 0},
    "3" : {"roomName" : "kitchen", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0},
    "4" : {"roomName" : "livingroom", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0},
    "5" : {"roomName" : "bedroom1", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0},
    "6" : {"roomName" : "bedroom2", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 12, "tempPV" : 0},
    "7" : {"roomName" : "bedroom3", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0},
    "8" : {"roomName" : "bedroom4", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0},
    "9" : {"roomName" : "bedroom5", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0},
    "10" : {"roomName" : "bedroom6", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0},
        }

defaultRoomTemp = {
    "00":15,
    "01":15,
    "02":15,
    "03":21,
    "04":21,
    "05":21,
    "06":21,
    "07":21,
    "08":21,
    "09":21,
    "10":21,
    "11":21,
    "12":21,
    "13":21,
    "14":21,
    "15":21,
    "16":21,
    "17":21,
    "18":21,
    "19":21,
    "20":21,
    "21":21,   
    "22":21,    
    "23":21,   
    "24":21
    }
#["outer_wall", "inner_wall", "ceiling", "floor", "window", "door"]
defaultAreaOverlap = {
    "1":{
        "0":[3, 0, 4, 4, 1, 0], 
        "2":[0, 4, 4, 4, 0, 0], 
        "3":[0, 4, 4, 4, 0, 0], 
        "4":[0, 2.37, 4, 4, 0, 1.63],
        "5":0
        }
    }

defaultConductivityTable = {
    "0": {"conductivity":31.3, "area":0}, # outside_wall
    "1": {"conductivity":4.1, "area":0}, # inside_wall
    "2": {"conductivity":13, "area":0}, #ceiling
    "3": {"conductivity":12.7, "area":0}, #floor
    "4": {"conductivity":4, "area":0}, # window
    "5": {"conductivity":3, "area":0} # door
        }
    




class heatingPowerSimulation():
    def __init__(self, rooms=defaultRoomParameters, areaOverlap=defaultAreaOverlap, conductivityTable = defaultConductivityTable):
        self.rooms = defaultRoomParameters
        self.areaOverlap = defaultAreaOverlap
        self.conductivityTable = conductivityTable
        
    def energyTransferCalc():
        pass
        
        # "1", 
    def roomPowerCalc(self, room_ID):
        roomTemp = self.rooms[room_ID]["tempSV"]
        
        l = []
        energy = 0
        for i in self.areaOverlap[room_ID]:
            if self.areaOverlap[room_ID][i]:
                #print(i)
                for j in range(len(self.areaOverlap[room_ID][i])):
                    #energy = self.areaOverlap[room_ID][i][j]
                    print(j) 
                
        print(l)
        return l
            
        
        
    
    def getRoomTempByTime(self):
        pass
    
    def getWeatherDataFromFile(self):
        #data = pd.read_csv("weatherHistoryHourly.csv", dtype={"dt": "int64", "clouds_all":"int64"}, parse_dates=["dt_iso"])
        data = pd.read_csv("newWeatherData.csv", dtype={"dt": "int64", "clouds_all":"int64"}, parse_dates=["dt_iso"])
        return data
    
if __name__ == "__main__":
    s = heatingPowerSimulation()
    s.roomPowerCalc("1")
    
