# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 12:07:36 2021

@author: peter
"""

import time
import datetime

import Signals as s
import booking
import SolarPowerNow
import heatingSimulation
import powerPrices
import time_update

maxHouseCapacity = 18
maxGuestsPrPersion = 2

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
    "10" : {"roomName" : "bedroom6", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
        }

users = {
    "1" : {"name": "Person1", "location":"0", "guests":"0", "activity":"0"},
    "2" : {"name": "Person2", "location":"0", "guests":"0", "activity":"0"},
    "3" : {"name": "Person3", "location":"0", "guests":"0", "activity":"0"},
    "4" : {"name": "Person4", "location":"0", "guests":"0", "activity":"0"},
    "5" : {"name": "Person5", "location":"0", "guests":"0", "activity":"0"},
    "6" : {"name": "Person6", "location":"0", "guests":"0", "activity":"0"}
    }

# Defining time function
last1mTime = 0# Previous 10m function
last10mTime = 0# Previous 10m function
last1hTime = None # Previous hourly function
last1dTime = None # Previous daily function
last1MTime = None # Previous monthy function



runUpdateInit = True
runRoomReservation = False

#COT Konfig
guestToken = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NDk1In0.EiWIxyQlEo84QAN1FwQe-q810LxQ1u1UOTjRGEwNW5U"
peopleInRoomToken = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjYwIn0.Ss7cSg7z1Q4TJezDLgBiBbJj3E80kyjBoSeA6rSRqtQ"
roomMaxCapacityToken = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTcxIn0.0PyyZPjdG8-Hr5LxA2pNGWNq2oJAMRxdKAtFy_n-7MY"


fireSignal = s.Signal("1324", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjcwIn0.4GshD9I6ZBE0roZzIsjHpIBLasIbH0JLc3TRhJwxJg8")
parameterUpdate = s.Signal("4600", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjcwIn0.4GshD9I6ZBE0roZzIsjHpIBLasIbH0JLc3TRhJwxJg8")

def fillStrToLen(n, length):
    s = str(n)
    if len(s) < length:
        s = "0"*(length - len(s)) + s
        return s
    
    return s

def fireCheck():
    return s.Signals.get()

def updateUserLocation():
    print("Downloading user location data... ", end=" ")
    users["1"]["location"] = str(s.Signal("19808", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk1In0.9bD-g6Gi40yjEiEYGOY1eoWl0wEuAZZN67yzS5gYOQs").get())
    users["2"]["location"] = str(s.Signal("24769", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk2In0.zADZlTeWjpJpbEmG_d1mcw07mDtT9ZJ30sMDtU1ex80").get())
    users["3"]["location"] = str(s.Signal("20536", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk3In0.es9iHyTEfrYM3ksN0QWtiULhRlQEcwatXWHFc5_fscc").get())
    users["4"]["location"] = str(s.Signal("3430", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk4In0.WP5pJqMaPL8AwEEii2TMFys9kQUabpl2iztyxBRdLuc").get())
    users["5"]["location"] = str(s.Signal("2105", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk5In0.fbZfuVuDshnMdUMW6EXrB6fSYhtdq0l2-j92h6AtlbM").get())
    users["6"]["location"] = str(s.Signal("10015", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjAwIn0.nGZXNRU34wVFtzex9tS-0gVky_ppn3Gjmj_riA4oLZY").get())
    print("Done")
    updateRoomOccupancy ()
    
    
def updateRoomOccupancy ():
    print("Updating room occupancy... ", end=" ")
    for i in range(len(rooms)):
        rooms[str(i)]["peopleInRoom"] = 0
        
        for j in range(1, len(users)):
            
            if users[str(j)]["location"] == str(i):
                rooms[str(i)]["peopleInRoom"] += 1
    print("Done")
    
    print("Uploading room occupancy... ", end=" ")
    #s.Signal("", peopleInRoomToken).write(rooms["0"]["peopleInRoom"]) # Outside
    s.Signal("20978", peopleInRoomToken).write(rooms["1"]["peopleInRoom"]) # Toilet
    s.Signal("15116", peopleInRoomToken).write(rooms["2"]["peopleInRoom"]) # Bathroom
    s.Signal("9237", peopleInRoomToken).write(rooms["3"]["peopleInRoom"])  # Kitchen 
    s.Signal("5933", peopleInRoomToken).write(rooms["4"]["peopleInRoom"])  # Livingroom
    s.Signal("30782", peopleInRoomToken).write(rooms["5"]["peopleInRoom"]) # Bedroom1
    s.Signal("19013", peopleInRoomToken).write(rooms["6"]["peopleInRoom"]) # Bedtoom2
    s.Signal("17378", peopleInRoomToken).write(rooms["7"]["peopleInRoom"]) # Bedroom3
    s.Signal("19280", peopleInRoomToken).write(rooms["8"]["peopleInRoom"]) # Bedroom4
    s.Signal("25397", peopleInRoomToken).write(rooms["9"]["peopleInRoom"]) # Bedroom5
    s.Signal("24559", peopleInRoomToken).write(rooms["10"]["peopleInRoom"])# Bedroom6
    print("Done")

def updateRoomMaxCapacity():
    print("Uploading Room Capacity... ", end=" ")
    s.Signal("1425", roomMaxCapacityToken).write(rooms["1"]["maxCapacity"]) # Toilet
    s.Signal("22847", roomMaxCapacityToken).write(rooms["2"]["maxCapacity"]) # Bathroom
    s.Signal("9237", roomMaxCapacityToken).write(rooms["3"]["maxCapacity"])  # Kitchen 
    s.Signal("19992", roomMaxCapacityToken).write(rooms["4"]["maxCapacity"])  # Livingroom
    s.Signal("308868", roomMaxCapacityToken).write(rooms["5"]["maxCapacity"]) # Bedroom1
    #s.Signal("308868", roomMaxCapacityToken).write(rooms["6"]["maxCapacity"]) # Bedtoom2
    #s.Signal("308868", roomMaxCapacityToken).write(rooms["7"]["maxCapacity"]) # Bedroom3
    #s.Signal("308868", roomMaxCapacityToken).write(rooms["8"]["maxCapacity"]) # Bedroom4
    #s.Signal("308868", roomMaxCapacityToken).write(rooms["9"]["maxCapacity"]) # Bedroom5
    #s.Signal("308868", roomMaxCapacityToken).write(rooms["10"]["maxCapacity"])# Bedroom6
    
    s.Signal("23508", roomMaxCapacityToken).write(maxHouseCapacity) # House capacity
    s.Signal("19992", roomMaxCapacityToken).write(maxGuestsPrPersion) # guests pr. persion
    print("Done")
    
                

def updateGuestData():
    print("Downloading guest data... ", end=" ")
    users["1"]["guests"] = fillStrToLen(s.Signal("24425", guestToken).get(), 2)[0]
    users["2"]["guests"] = fillStrToLen(s.Signal("10799", guestToken).get(), 2)[0]
    users["3"]["guests"] = fillStrToLen(s.Signal("9663", guestToken).get(), 2)[0]
    users["4"]["guests"] = fillStrToLen(s.Signal("2277", guestToken).get(), 2)[0]
    users["5"]["guests"] = fillStrToLen(s.Signal("31631", guestToken).get(), 2)[0]
    users["6"]["guests"] = fillStrToLen(s.Signal("27545", guestToken).get(), 2)[0]       
    print("Done")
    
def bookRoom():
    print("Booking room... ", end=" ")
    bookingStatus = booking.bookRoom(rooms)
    if bookingStatus < 3000:      
        print("Room has been booked")
    else:
        print("Room was not booked")

def updateHistoricData():
    pass 

def updateInit():
    print("Initialising Global Parameters")
    print("")
    updateRoomMaxCapacity()
    updateHistoricData()
    print("")
    print("Global Parameters Initialised")
    print("")
    
    
    print("")
    print("")


mainLoop = True



print("Program Start")

while mainLoop:
    currentTime = datetime.datetime.now()
    
    # Upload global variables to CoT
    if runUpdateInit:
        updateInit()
        runUpdateInit = False
    
    fireSignal.get()
    
    # Check if there are any paramters that have been changed, and need updating
    parmu = str(parameterUpdate.get())
    #print("parmu =", end="")
    parmu = "222"
    #print(parmu)
    
    # Booking
    if parmu[0] == "2":
        bookRoom()

    
    # User Location Change
    if parmu[1] == "2":
        updateUserLocation()
        
    # Guest Status Change    
    if parmu[2] == "2":
        updateGuestData()
        
    if parmu != "111":
        parameterUpdate.write(111)
           
    # Periodic functions
    # Every min
    if (int(currentTime.timestamp()) - 60) > last1mTime:
        last1mTime = int(currentTime.timestamp())
        
        print("Updating Current Time... ", end='')
        time_update.time_min(currentTime)
        print("Done")
    
    # Every 10 minutes
    if (int(currentTime.timestamp()) - 600) > last10mTime:
        last10mTime = int(currentTime.timestamp())
        #print(datetime.datetime.utcfromtimestamp(last10mTime).strftime("%M"))
    
    #Hourly
    if currentTime.strftime("%H") != last1hTime:
        last1hTime = currentTime.strftime("%H")
        #print(last1hTime)
    
    #Daily
    if currentTime.strftime("%a") != last1dTime:
        last1dTime = currentTime.strftime("%a")
        print("Updating Current Date... ", end='')
        time_update.year_month_day(currentTime)
        print("Done")
        
        print("Updating Historic Weather data... ", end='')
        s = SolarPowerNow.SolarPower()
        newWeatherData = s.updateHistoricWeatherData()
        s.updateHistoricSolarPowerGeneration()
        print("Done")
        
        print("Updating Historic Heating power Simulation...", end='')
        hs = heatingSimulation.heatingPowerSimulation()
        hs.updateHeatingSimulationData()
        print("Done")
        
        print("Updating Historic Power Prices...", end='')
        pp = powerPrices.powerPrices()
        pp.updateHistoricData()
        print("Done")
        
        #print(last1dTime)
    
    # Monthly
    if currentTime.strftime("%b") != last1MTime:
        last1MTime = currentTime.strftime("%b")
        #print(last1MTime)
    
    
    mainLoop = False
    
    
    
    
    
