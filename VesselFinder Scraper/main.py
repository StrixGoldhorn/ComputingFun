

# This is PURELY to track container ships and nothing else.
import innocent_container_ships_ports
# REDLAND_innocent_container_ships_ports_aoi_dict = innocent_container_ships_ports.REDLAND_innocent_container_ships_ports_aoi_dict
BLUELAND_innocent_container_ships_ports_aoi_dict = innocent_container_ships_ports.BLUELAND_innocent_container_ships_ports_aoi_dict
# WHOLE_OF_BLUELAND_innocent_container_ships_ports_aoi_dict = innocent_container_ships_ports.WHOLE_OF_BLUELAND_innocent_container_ships_ports_aoi_dict
# GOLDLAND_TEST_aoi_dict = innocent_container_ships_ports.GOLDLAND_TEST_aoi_dict

from Vessel_Finder_Scrape import *
from server import *


from USER_SETTINGS import *

import requests
import string
import json
import time
from datetime import datetime
import sqlite3
import os
import create_db
import threading


# def unixTimeToHumanTime(unixtime: int) -> str:
#     '''
#     Converts unix time to  **LOCAL** time, returns string
#     '''
#     unixtime = int(unixtime)
#     return datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')




'''
  ___  ___     ___ _         __  __ 
 |   \| _ )   / __| |_ _  _ / _|/ _|
 | |) | _ \   \__ \  _| || |  _|  _|
 |___/|___/   |___/\__|\_,_|_| |_|  
'''

def runDBCommandsTerrestrial(terrestrial_info):
    info_len_len = int(len(str(len(terrestrial_info))))
    
    for cnt, data in enumerate(terrestrial_info):
        time.sleep(USER_DEFINED_REQ_PAUSE)
        
        print(f"Processing {cnt+1:<{info_len_len}} of {len(terrestrial_info):<{info_len_len}}")
        vesseldata = getVesselData(data["MMSI"])
        
        insertDBShipHistory(data["MMSI"], vesseldata["name"], round(data["Latitude"], COORDS_ACCURACY), round(data["Longitude"], COORDS_ACCURACY), vesseldata["ts"])
        insertDBShip(data["MMSI"], vesseldata["name"], vesseldata["country"], vesseldata["type"])
    


def getDBFilepath() -> str:
    # ownfilepath = os.path.dirname(os.path.abspath(__file__))
    # db_filepath = os.path.join(ownfilepath, "ships.db")

    # TEMP FIX (error when trying to get __file__)
    db_filepath = "./ships.db"
    return db_filepath

def checkDBExistsShip(mmsi: int, ship_name: str) -> bool:
    db_filepath = getDBFilepath()
    
    try:
        conn = sqlite3.connect(db_filepath)
        curs = conn.cursor()
        curs.execute("SELECT * FROM TER_AIS_ship_data WHERE mmsi = ? AND ship_name = ?", (mmsi, ship_name))
        exists = curs.fetchall()
        
        if exists: return True
        else: return False
        
    except Exception as e:
        print("Error:", e)
                
def insertDBShip(mmsi: int, ship_name: str, country: str, ship_type: str):
    db_filepath = getDBFilepath()
    
    if not checkDBExistsShip(mmsi, ship_name):
        try:
            conn = sqlite3.connect(db_filepath)
            curs = conn.cursor()

            curs.execute("\
                        INSERT INTO TER_AIS_ship_data (mmsi, ship_name, country, ship_type) \
                        VALUES (?, ?, ?, ?)\
                ", (mmsi, ship_name, country, ship_type))
            
            conn.commit()
            if GLOBAL_DB_DEBUG:
                print(f"Ship {mmsi} successfully inserted")
            
        except Exception as e:
            print("Error:", e)
    else:
        if GLOBAL_DB_DEBUG:
            print(f"Ship {mmsi} already exists!")
        pass


def checkDBExistsShipHistory(mmsi: int, ship_name:str, unixtime: int, lat: str, long: str) -> bool:
    db_filepath = getDBFilepath()
    
    try:
        conn = sqlite3.connect(db_filepath)
        curs = conn.cursor()
        curs.execute("SELECT * FROM TER_AIS_ship_geo_history\
                     WHERE mmsi = ? AND ship_name = ? AND timestamp = ? AND lat = ? AND long = ?",\
                     (mmsi, ship_name, unixtime, lat, long))
        exists = curs.fetchall()
        
        if exists: return True
        else: return False
        
    except Exception as e:
        print("Error:", e)

def insertDBShipHistory(mmsi: int, ship_name:str, lat: str, long: str, unixtime: int):
    db_filepath = getDBFilepath()
    
    if not checkDBExistsShipHistory(mmsi, ship_name, unixtime, lat, long):
        try:
            conn = sqlite3.connect(db_filepath)
            curs = conn.cursor()

            curs.execute("\
                        INSERT INTO TER_AIS_ship_geo_history (mmsi, ship_name, lat, long, timestamp) \
                        VALUES (?, ?, ?, ?, ?)\
                ", (mmsi, ship_name, lat, long, unixtime))
            
            conn.commit()
            if GLOBAL_DB_DEBUG:
                print(f"Ship history for ship {mmsi} successfully inserted")
            
        except Exception as e:
            print("Error:", e)
    else:
        if GLOBAL_DB_DEBUG:
            print(f"Ship history for ship {mmsi} already exists!")
        pass


def checkDBExistsMMSIOfInterest(mmsi: int) -> bool:
    db_filepath = getDBFilepath()
    
    try:
        conn = sqlite3.connect(db_filepath)
        curs = conn.cursor()
        curs.execute("SELECT * FROM mmsi_of_interest WHERE mmsi = ?", (mmsi,))
        exists = curs.fetchall()
        
        if exists: return True
        else: return False
        
    except Exception as e:
        print("Error:", e)

def insertDBMMSIOfInterest(mmsi: int):
    db_filepath = getDBFilepath()
    
    if not checkDBExistsMMSIOfInterest(mmsi):
        try:
            conn = sqlite3.connect(db_filepath)
            curs = conn.cursor()

            curs.execute("\
                        INSERT INTO mmsi_of_interest (mmsi) \
                        VALUES (?)\
                ", (mmsi,))
            
            conn.commit()
            if GLOBAL_DB_DEBUG:
                print(f"MMSI of Intereest for ship {mmsi} successfully inserted")
            
        except Exception as e:
            print("Error:", e)
    else:
        if GLOBAL_DB_DEBUG:
            print(f"MMSI of Intereest for ship {mmsi} already exists!")
        pass


def updateDBShipHistory_ALL_MMSIOfInterest():
    db_filepath = getDBFilepath()
    
    try:
        conn = sqlite3.connect(db_filepath)
        curs = conn.cursor()
        curs.execute("SELECT mmsi FROM mmsi_of_interest")
        exists = curs.fetchall()
        
        if exists:
            for row in exists:
                mmsi = row[0]
                vesselLoc = getVesselData_MMSIOfInterest(mmsi)
                vesselData = getVesselData(mmsi)
                insertDBShipHistory(mmsi, vesselLoc[2], round(vesselLoc[0], COORDS_ACCURACY), round(vesselLoc[1], COORDS_ACCURACY), vesselData["ts"])
                
                time.sleep(0.5)
        else:
            print("No MMSI of Interest!")
        
    except Exception as e:
        print("Error:", e)



def sleepTimerWithBar(sleepTime: int, dispIntervals: int):
    def sleepTimerWithBarOutput(curr: int, total: int):
        print("[" + "#" * curr + "-" * (total-curr) + "]", end="\r")
    
    for cnt in range(sleepTime):
        sleepTimerWithBarOutput(cnt//dispIntervals, sleepTime//dispIntervals)
        time.sleep(1)
        
    print("[" + "#" * (sleepTime//dispIntervals) + "]")
        

def constantUpdate_ShipHistory_MMSIOfInterest(updateInterval: int):
    while True:
        updateDBShipHistory_ALL_MMSIOfInterest()
        print(f"Last update: {datetime.now()}")
        sleepTimerWithBar(updateInterval, 1)
        

def iterateThroughAOI(aoi_dict: dict, shipfilter: str = None):
    for key, value in aoi_dict.items():        
        print("-"*50)
        print(key)
        terrestrial_info = getShipsOnMapTerrestrial(value["coords"], value["zoom"], shipfilter=shipfilter)
        # getShipsOnMapSatellite(value["coords"], value["zoom"])
        runDBCommandsTerrestrial(terrestrial_info)


def CUSTOM_QUERIES():    
    # iterateThroughAOI(REDLAND_innocent_container_ships_ports_aoi_dict)
    # iterateThroughAOI(WHOLE_OF_BLUELAND_innocent_container_ships_ports_aoi_dict)
    iterateThroughAOI(BLUELAND_innocent_container_ships_ports_aoi_dict)
    # iterateThroughAOI(GOLDLAND_TEST_aoi_dict, shipfilter=mil_unk_filter)
    
    
        
def TEST_QUERY():
    # constantUpdate_ShipHistory_MMSIOfInterest(5)
    while True:
        iterateThroughAOI(BLUELAND_innocent_container_ships_ports_aoi_dict)
        sleepTimerWithBar(10, 1)

def THREADING_MASTER():
    thread1 = threading.Thread(target=TEST_QUERY)
    thread2 = threading.Thread(target=START_FLASK_APP)

    thread1.start()
    thread2.start()




def main():
    # create_db.generateDB(force_reset=True)
    # TEST_QUERY()
    # CUSTOM_QUERIES()
    # START_FLASK_APP()

    THREADING_MASTER()
    
    
        


# LEGACY, works based on guessing...
def getValidNames(rawdata:str, sensitivity:int) -> list:
    cnt = 0
    currstr = ""
    output = []
    
    for char in rawdata:
        # print(char, cnt, currstr)
        if char in string.ascii_letters or char in string.digits or char == " ":
            cnt += 1
            currstr += char
        else:
            if cnt >= sensitivity:
                output.append(currstr)
            cnt = 0
            currstr = ""
            
    if cnt >= sensitivity:
        output.append(currstr)
        
    return output

if __name__ == "__main__":
    main()