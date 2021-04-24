# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 12:07:36 2021

@author: peter
"""

import time
import datetime

rooms = {
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
    "10" : {"roomName" : "bedroom6", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0}
        }

users = {
    "1" : {"name": "Person1", "location":"0", "guests":"0"},
    "2" : {"name": "Person2", "location":"0", "guests":"0"},
    "3" : {"name": "Person3", "location":"0", "guests":"0"},
    "4" : {"name": "Person4", "location":"0", "guests":"0"},
    "5" : {"name": "Person5", "location":"0", "guests":"0"},
    "6" : {"name": "Person6", "location":"0", "guests":"0"}
    }

# Defining time function
last10mTime = 0# Previous 10m function
last1hTime = None # Previous hourly function
last1dTime = None # Previous daily function
last1MTime = None # Previous monthy function



updateInit = True
runRoomReservation = False

def fireCheck():
    pass

def statusChangeCheck():
    pass


mainLoop = True
while mainLoop:
    currentTime = datetime.datetime.now()
    
    
    if updateInit:
        pass
    
    

    if runRoomReservation:
        pass
    
    # Periodic functions
    # Every 10 minutes
    if (int(currentTime.timestamp()) - 600) > last10mTime:
        last10mTime = int(currentTime.timestamp())
        print(datetime.datetime.utcfromtimestamp(last10mTime).strftime("%M"))
    
    #Hourly
    if currentTime.strftime("%H") != last1hTime:
        last1hTime = currentTime.strftime("%H")
        print(last1hTime)
    
    #Daily
    if currentTime.strftime("%a") != last1dTime:
        last1dTime = currentTime.strftime("%a")
        print(last1dTime)
    
    # Monthly
    if currentTime.strftime("%b") != last1MTime:
        last1MTime = currentTime.strftime("%b")
        print(last1MTime)
    
    
    mainLoop = False
    
    
    
    
    
