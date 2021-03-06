# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 12:07:36 2021

@author: peter
"""
import datetime
import time

import Signals as s
import booking
import SolarPowerNow
import heatingSimulation
import powerPrices
import time_update
import forbruksModell
import sikringsskap_data
import roomParameters
maxHouseCapacity = roomParameters.maxHouseCapacity
maxGuestsPrPersion = roomParameters.maxGuestsPrPersion
rooms = roomParameters.defaultRoomParameters
users = roomParameters.defaultUsers

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
    users = roomParameters.defaultUsers
    users["1"]["location"] = str(s.Signal("19808", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk1In0.9bD-g6Gi40yjEiEYGOY1eoWl0wEuAZZN67yzS5gYOQs").get())
    users["2"]["location"] = str(s.Signal("24769", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk2In0.zADZlTeWjpJpbEmG_d1mcw07mDtT9ZJ30sMDtU1ex80").get())
    users["3"]["location"] = str(s.Signal("20536", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk3In0.es9iHyTEfrYM3ksN0QWtiULhRlQEcwatXWHFc5_fscc").get())
    users["4"]["location"] = str(s.Signal("3430", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk4In0.WP5pJqMaPL8AwEEii2TMFys9kQUabpl2iztyxBRdLuc").get())
    users["5"]["location"] = str(s.Signal("2105", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk5In0.fbZfuVuDshnMdUMW6EXrB6fSYhtdq0l2-j92h6AtlbM").get())
    users["6"]["location"] = str(s.Signal("10015", "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjAwIn0.nGZXNRU34wVFtzex9tS-0gVky_ppn3Gjmj_riA4oLZY").get())
    print("Done")
    updateRoomOccupancy ()
    
    
def updateRoomOccupancy ():
    users = roomParameters.defaultUsers
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
    users = roomParameters.defaultUsers
    users["1"]["guests"] = fillStrToLen(s.Signal("24425", guestToken).get(), 2)[0]
    users["2"]["guests"] = fillStrToLen(s.Signal("10799", guestToken).get(), 2)[0]
    users["3"]["guests"] = fillStrToLen(s.Signal("9663", guestToken).get(), 2)[0]
    users["4"]["guests"] = fillStrToLen(s.Signal("2277", guestToken).get(), 2)[0]
    users["5"]["guests"] = fillStrToLen(s.Signal("31631", guestToken).get(), 2)[0]
    users["6"]["guests"] = fillStrToLen(s.Signal("27545", guestToken).get(), 2)[0]       
    roomParameters.defaultUsers = users
    print("Done")
    
def bookRoom():
    print("Booking room... ", end=" ")
    bookingStatus = booking.bookRoom(rooms)
    if bookingStatus < 3000:      
        print("Room has been booked")
    else:
        print("Room was not booked")


def updateInit():
    print("Initialising Global Parameters")
    print("")
    updateRoomMaxCapacity()
    
    #Update Room Set-Temperature
    
    print("")
    print("Global Parameters Initialised")
    print("")
    
    
    print("")
    print("")
    
def updateDashboard():
    #The user that is used as a dashboard is Person1
    dashboardToken = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTk1In0.9bD-g6Gi40yjEiEYGOY1eoWl0wEuAZZN67yzS5gYOQs"
    
    #Update PowerCost in ??re/kWh
    powerPriceNow_key = "1753"
    powerPriceNow = forbruksModell.userPowerConsumption().recentPowerPrice()
    s.Signal(powerPriceNow_key, dashboardToken).write(powerPriceNow)
    
    
    #PowerUse
    
    
    
    #SolarPanel Production
    solarPP_key="2411"
    solarPanelPower = SolarPowerNow.SolarPower().getSolarPowerNow()
    s.Signal(solarPP_key, dashboardToken).write(solarPanelPower)
    
    #Weather
    currentWeather = SolarPowerNow.SolarPower().getWeatherNow()
    
    windSpeed = currentWeather["wind"]["speed"]
    temp = currentWeather["main"]["temp"] -273.15
    weatherID = currentWeather["weather"][0]["id"]
    
    windSpeed_key = "12054"
    s.Signal(windSpeed_key, dashboardToken).write(windSpeed)
    
    
    Global_variabler2_Token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjcwIn0.4GshD9I6ZBE0roZzIsjHpIBLasIbH0JLc3TRhJwxJg8"
    weatherID_key = "39"
    s.Signal(weatherID_key, Global_variabler2_Token).write(weatherID)
    
    temp_key = "20183"
    s.Signal(temp_key, Global_variabler2_Token).write(temp)
    


mainLoop = True



print("Program Start")

while mainLoop:
    currentTime = datetime.datetime.now()
    maxHouseCapacity = roomParameters.maxHouseCapacity
    maxGuestsPrPersion = roomParameters.maxGuestsPrPersion
    rooms = roomParameters.defaultRoomParameters
    users = roomParameters.defaultUsers

    
    
    # Upload global variables to CoT
    if runUpdateInit:
        updateInit()
        runUpdateInit = False
    
    fireSignal.get()
    
    # Check if there are any parameters that have been changed, and need updating
    parmu = str(parameterUpdate.get())
    
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
        updateDashboard()
    
    #Hourly
    if currentTime.strftime("%H") != last1hTime:
        last1hTime = currentTime.strftime("%H")
        
        # Getting live power data from house fuse box
        print("Getting power from fuse-box...", end='')
        sikringsskap_data.get_store_data()
        print("Done")
        
        # Convertig power to NOK and uploading to cloud
        print("Uploading power cost to CoT...", end='')
        sikringsskap_data.kWh_to_NOK_upload()
        print("Done")
        
        #Updating User location according to timetable
        print("Updating user location", end='')
        forbruksModell.userPowerConsumption().updateUserLocation()
        
        print("Done")
        
        
        
        
        
    
    #Daily
    if currentTime.strftime("%a") != last1dTime:
        last1dTime = currentTime.strftime("%a")
        print("Updating Current Date... ", end='')
        time_update.year_month_day(currentTime)
        print("Done")
        
        print("Updating Historic Weather data... ", end='')
        SP = SolarPowerNow.SolarPower()
        newWeatherData = SP.updateHistoricWeatherData()
        SP.updateHistoricSolarPowerGeneration()
        print("Done")
        
        print("Updating Historic Heating power Simulation...", end='')
        hs = heatingSimulation.heatingPowerSimulation()
        hs.updateHeatingSimulationData()
        print("Done")
        
        print("Updating Historic Power Prices...", end='')
        pp = powerPrices.powerPrices()
        pp.updateHistoricData()
        print("Done")
        
        print("Updating Historic User power...", end='')
        fm = forbruksModell.userPowerConsumption()
        fm.updateHistoricUserConsumption()
        print("Done")
        
    
    # Monthly
    if currentTime.strftime("%b") != last1MTime:
        
        # Create new sheet in excel document each month.
        print("Creating new monthly power sheet... ", end='')
        sikringsskap_data.create_datasheet()
        last1MTime = currentTime.strftime("%b")
    
    
    time.sleep(3)
    mainLoop = False
    
    
    
    
    
