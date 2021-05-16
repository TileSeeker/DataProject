# -*- coding: utf-8 -*-
"""
Created on Thu May 13 16:14:07 2021

@author: peter
"""
maxHouseCapacity = 18
maxGuestsPrPersion = 2


defaultRoomParameters = {
    # Windows = 1m * 1.2m = 1.2m^2
    # Doors = 1.63m^2
    # Ceiling height = 2.3m
    
    "0" : {"roomName" : "outside", "maxCapacity" : 12000000000, "peopleInRoom" : 8000000000, "tempSV" : 0, "tempPV" : 0, "area":0,
           "heatingFactor":0, "coolingFactor":0, "powerBilling":"public", "areaOverlap":{}},
    "1" : {"roomName" : "toilet", "maxCapacity" : 1, "peopleInRoom" : 0, "tempSV" : 28, "tempPV" : 0, "area":2.5,
           "heatingFactor":1, "coolingFactor":0, "powerBilling":"public",
           "areaOverlap":{
               "0":{"outside_wall":2.873}, 
               "2":{"inside_wall":4.4}, 
               "4":{"inside_wall":5.854, "door":1.63},
                         }
          },
    
    "2" : {"roomName" : "bathroom", "maxCapacity" : 1, "peopleInRoom" : 0, "tempSV" : 28, "tempPV" : 0, "area":3,
           "heatingFactor":1, "coolingFactor":0, "powerBilling":"public",
           "areaOverlap":{
               "0":{"outside_wall":6.8875}, 
               "1":{"inside_wall":4.4}, 
               "4":{"inside_wall":1.82, "door":1.63},
               "10":{"inside_wall":1.4375}
                         }
          },
    
    "3" : {"roomName" : "kitchen", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":8,
           "heatingFactor":1, "coolingFactor":0, "powerBilling":"public",
            "areaOverlap":{
               "0":{"outside_wall":10.0625}, 
               "4":{"inside_wall":4.6, "air":9.2}, 
               "11":{"inside_wall":4.6},
                        }
           },
    
    "4" : {"roomName" : "livingroom", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":28.5,
           "heatingFactor":0.263, "coolingFactor":0.179, "powerBilling":"public",
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
           "heatingFactor":1, "coolingFactor":0, "powerBilling":"private",
           "areaOverlap":{
               "0":{"outside_wall":11.9, "window":1.2},
               "4":{"inside_wall":4.025, "door":1.63},
               "6":{"inside_wall":1.4375},
               "11":{"inside_wall":1.4375}
                          }
           },
    "6" : {"roomName" : "bedroom2", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 12, "tempPV" : 0, "area":6,
           "heatingFactor":1, "coolingFactor":0, "powerBilling":"private",
           "areaOverlap":{
               "0":{"outside_wall":8.8625, "window":1.2},
               "4":{"inside_wall":2.97, "door":1.63},
               "5":{"inside_wall":1.4375},
               "7":{"inside_wall":6.9}
                         }
           },
    "7" : {"roomName" : "bedroom3", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":6,
           "heatingFactor":1, "coolingFactor":0, "powerBilling":"private",
           "areaOverlap":{
               "0":{"outside_wall":3.4, "window":1.2},
               "4":{"inside_wall":9.87, "door":1.63},
               "6":{"inside_wall":6.9}
                         }
           },
    "8" : {"roomName" : "bedroom4", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":6,
           "heatingFactor":1, "coolingFactor":0, "powerBilling":"private",
           "areaOverlap":{
               "0":{"outside_wall":3.4, "window":1.2},
               "4":{"inside_wall":9.87, "door":1.63},
               "9":{"inside_wall":6.9}
                         }
           },
    "9" : {"roomName" : "bedroom5", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":6,
           "heatingFactor":1, "coolingFactor":0, "powerBilling":"private",
           "areaOverlap":{
               "0":{"outside_wall":8.8625, "window":1.2},
               "4":{"inside_wall":2.97, "door":1.63},
               "8":{"inside_wall":6.9},
               "10":{"inside_wall":1.4375}
                         }
           },
    "10" : {"roomName" : "bedroom6", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 21, "tempPV" : 0, "area":6,
            "heatingFactor":1, "coolingFactor":0, "powerBilling":"private",
            "areaOverlap":{
                "0":{"outside_wall":11.9, "window":1.2},
                "2":{"inside_wall":1.4375},
                "4":{"inside_wall":4.025, "door":1.63},
                "9":{"inside_wall":1.4375}
                }
            },
    "11" : {"roomName" : "server", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 15, "tempPV" : 0, "area":6, 
            "heatingFactor":1, "coolingFactor":0, "powerBilling":"public",
            "areaOverlap":{
                "0":{"outside_wall":10.0625},
                "3":{"inside_wall":4.6},
                "4":{"inside_wall":5.37, "door":1.63},
                "5":{"inside_wall":1.4375}
                          }
            }
        
    }


defaultUsers = {
    "1" : {"name": "User1", "location":"0", "guests":"0", "activity":"0", "bedroom":"5"},
    "2" : {"name": "User2", "location":"0", "guests":"0", "activity":"0", "bedroom":"6"},
    "3" : {"name": "User3", "location":"0", "guests":"0", "activity":"0", "bedroom":"7"},
    "4" : {"name": "User4", "location":"0", "guests":"0", "activity":"0", "bedroom":"8"},
    "5" : {"name": "User5", "location":"0", "guests":"0", "activity":"0", "bedroom":"9"},
    "6" : {"name": "User6", "location":"0", "guests":"0", "activity":"0", "bedroom":"10"}
    }


ActivityPowerConsumption = {
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

conductivityTable = {
    "outside_wall":31.3, # outside_wall
    "inside_wall":4.1, # inside_wall
    "ceiling":13, #ceiling
    "floor":12.7, #floor
    "window":4, # window
    "door":3, # door
    "air": 0.25
        }