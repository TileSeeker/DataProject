# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:54:44 2021

@author: peter
"""

# Res format: 
# Input: startTime[datetime], stopTime[datetime], ID[int], 
# Return: statusCode[int]

from datetime import datetime
import pandas as pd

timeFormat = "%Y %m %d %H %M"
now = datetime.now().strftime(timeFormat)

room_capacity = {
    "Bathroom": 1,
    "Kitchen": 3,
    "Living room": 7
    }

#reservations = pd.DataFrame(columns =['room', 'userID', 'startTime', 'stopTime'])

def convert_to_datetime(date_raw, time_raw):
    # date and time need to be in the correct format
    # date: yymmdd [int/str]
    # time: hhmm  [int/str]
    date = str(date_raw)
    time = str(time_raw)
    
    year = date[0:2]
    year = '20'+ year
    
    month = date[2:4]
    day = date[4:6]
    
    #Formating Time
    timeLen = len(time)
    time = '0'*(4-timeLen) + time
    
    hour = time[0:2]
    minute = time[2:]
        
    dt = datetime.fromisoformat(f'{year}-{month}-{day} {hour}:{minute}:00')
    return(dt)
    
def open_res_from_file():
    df = pd.read_csv('room_reservations.csv', parse_dates=["startTime", "stopTime"])
    return df
def save_res_to_file(df):
    df.to_csv('room_reservations.csv', index=False)
  
def reset_reservations():
    reservations = open_res_from_file()
    reservations = pd.DataFrame(columns =['room', 'userID', 'startTime', 'stopTime'])
    save_res_to_file(reservations)

def check_reservations():
    reservations = open_res_from_file()
    return reservations 

def check_availability(data):
    """
    data = {
    'room':room, 
    'userID': userID, 
    'guests': guests
    'startTime':startTime, 
    'stopTime':stopTime  
        }

    Status Values:
        1: No conflict
        2: Overlap, but within capacity
        3: Room is full, booking canceled 
    """
    
    
    reservations = open_res_from_file()
    
    
    reservations = reservations.loc[reservations["room"] == data["room"]]
    reservations = reservations.loc[reservations["startTime"] < data["stopTime"]]
    reservations = reservations.loc[reservations["stopTime"] > data["startTime"]]
    
    
    if reservations.empty:
        return 1000
    
    else:
        for i in range(len(reservations.index)):
            df = reservations.loc[reservations["startTime"] < reservations.iloc[i]["stopTime"]]
            #print(df)
            #print(reservations.iloc[i])
            df = df.loc[reservations["stopTime"] > reservations.iloc[i]["startTime"]]
            #print(df)
            if len(df.index) < room_capacity[data["room"]]:
                return 2000
            else:
                return 3000
    
def reserve_room(room, userID, startTime_raw, stopTime_raw, startDate_raw=datetime.today().strftime("%y%m%d"), stopDate_raw=datetime.today().strftime("%y%m%d")):
    """
    Used to reserve the use of a room in the house
    
    

    Parameters
    ----------
    room : TYPE
        DESCRIPTION.
    userID : TYPE
        DESCRIPTION.
    startTime_raw : TYPE
        DESCRIPTION.
    stopTime_raw : TYPE
        DESCRIPTION.
    startDate_raw : TYPE, optional
        DESCRIPTION. The default is datetime.today().strftime("%y%m%d").
    stopDate_raw : TYPE, optional
        DESCRIPTION. The default is datetime.today().strftime("%y%m%d").

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    startTime = convert_to_datetime(startDate_raw, startTime_raw)
    stopTime = convert_to_datetime(stopDate_raw, stopTime_raw)
    
    data = {
    'room':room, 
    'userID':userID, 
    'startTime':startTime, 
    'stopTime':stopTime
            }
    
    status = check_availability(data)
     
    if status <3000:
        reservations = open_res_from_file()
        reservations = reservations.append(data, ignore_index=True)   
        reservation_pos = reservations.index[-1]
        save_res_to_file(reservations)
    
        availability_status = status + reservation_pos
        
        print(reservations)
        print(availability_status)
        
        return availability_status
    else:
        return 3000
    
def remove_reservation(row_index):
    reservations = open_res_from_file()
    reservations.iloc[row_index] = [None]*len(reservations.iloc[row_index])
    save_res_to_file(reservations)
 
"""
reserve_room('Bathroom', 1, '1130', '1230')
reserve_room('Kitchen', 2, 0800, )

"""

    