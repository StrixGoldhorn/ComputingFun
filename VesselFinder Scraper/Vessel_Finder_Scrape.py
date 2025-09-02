import requests
import time
import json

from datetime import datetime
from USER_SETTINGS import *

'''
 __      __   _        ___                   _               ___ _         __  __ 
 \ \    / /__| |__    / __| __ _ _ __ _ _ __(_)_ _  __ _    / __| |_ _  _ / _|/ _|
  \ \/\/ / -_) '_ \   \__ \/ _| '_/ _` | '_ \ | ' \/ _` |   \__ \  _| || |  _|  _|
   \_/\_/\___|_.__/   |___/\__|_| \__,_| .__/_|_||_\__, |   |___/\__|\_,_|_| |_|  
                                       |_|         |___/                          
'''
def unixTimeToHumanTime(unixtime: int) -> str:
    '''
    Converts unix time to  **LOCAL** time, returns string
    '''
    unixtime = int(unixtime)
    return datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')

def URLParamMaker(coords_arr: list, zoom: int, shipfilter: str = None) -> str:
    # smaller coords first then bigger
    processed_coords = coords_arr.copy()
    processed_coords.sort()

    for i in range(len(coords_arr)):
        processed_coords[i] = round(processed_coords[i] * 600000)
        
    coords = str(processed_coords[2]) + "%2C" + str(processed_coords[0]) + "%2C" + str(processed_coords[3]) + "%2C" + str(processed_coords[1])
    
    bbox_part = "bbox="+coords
    zoom_part = "zoom="+str(zoom)
    mmsi_part = "mmsi=0"
    
    if shipfilter is not None:
        shipfilter_part_special = "&filter=" + shipfilter
    else:
        shipfilter_part_special = ""
    
    OUTPUT_URL = bbox_part + "&" + zoom_part + "&" + mmsi_part + shipfilter_part_special
    
    return OUTPUT_URL
   
def printInfoTerrestrial(info: list):
    for cnt, data in enumerate(info):
        print(f'TER-{cnt : <3} | {data["MMSI"] : <9} | {data["Ship Name"].decode("utf-8") : <20} | {round(data["Latitude"], COORDS_ACCURACY)}, {round(data["Longitude"], COORDS_ACCURACY)}')       

def printInfoTerrestrial_WithFilters(info: list, blacklist: bool = True, whitelist: bool = False):    
    info_len_len = int(len(str(len(info))))
    
    for cnt, data in enumerate(info):
        time.sleep(1)
        
        vesseldata = getVesselData(data["MMSI"])
        
        if (blacklist and (vesseldata["type"] not in typefilter_blacklist))\
        or (whitelist and (vesseldata["type"] in typefilter_whitelist)):
            print(f'({cnt:<{info_len_len}} of {len(info):<{info_len_len}}) | TER-{cnt : <4} | {data["MMSI"] : <9} | {data["Ship Name"].decode("utf-8") : <20} | {vesseldata["type"] : <25} | {vesseldata["country"] : <20} | {round(data["Latitude"], COORDS_ACCURACY)}, {round(data["Longitude"], COORDS_ACCURACY)} | {unixTimeToHumanTime(vesseldata["ts"]):<20}')
        else:
            print(f'Skipping {cnt:<{info_len_len}} of {len(info):<{info_len_len}}', end="\r")
            
def processResponseTerrestrial(data: bytes, zoomLevel: int) -> list:
    LOCAL_DEBUG = False
    # LOCAL_DEBUG = True
    OUTPUT_shipdata = []
    
    if LOCAL_DEBUG:
        print("Response header")
        for b in data[:12]:
            print(hex(b), end = " ")
        print()
        
        print("Response body")
    
    idx = 12
    part_header_length = 2
    mmsi_length = 4
    lat_length = 4
    long_length = 4
    is_selected_length = 1
    
    extra_zoom_info_length = 10
    
    while idx < len(data):
        try:        
            part_header_data = data[idx:idx+part_header_length]
            idx += part_header_length
            
            mmsi_data = data[idx:idx+mmsi_length]
            mmsi = int.from_bytes(mmsi_data, "big")
            idx += mmsi_length
            
            lat_data = data[idx:idx+lat_length]
            lat = int.from_bytes(lat_data, "big") / 600000
            idx += lat_length
            
            long_data = data[idx:idx+long_length]
            long = int.from_bytes(long_data, "big") / 600000
            idx += long_length
            
            is_selected = data[idx:idx+is_selected_length]
            idx += is_selected_length
            
            ship_name_length = data[idx]
            idx += 1
            
            ship_name = data[idx:idx+ship_name_length]
            idx += ship_name_length
            
            if zoomLevel >= 14:
                idx += extra_zoom_info_length
            
            if LOCAL_DEBUG:
                print("-"*20)
                print(part_header_data)
                print("---mmsi---")
                print(mmsi_data)
                print(mmsi)
                print("---coords---")
                print(lat_data)
                print(long_data)
                print(lat)
                print(long)
                print("---selected---")
                print(is_selected)
                print("---length and name---")
                print(ship_name_length)
                print(ship_name)
            
            OUTPUT_shipdata.append({"MMSI" : mmsi, "Ship Name" : ship_name, "Latitude": lat, "Longitude": long, "DisplayColor": (int.from_bytes(part_header_data, "big") & 240) >> 4})
            
        except Exception as e:
            print("----- An error occurred. -----")
            print(e)
        
    return OUTPUT_shipdata

def getShipsOnMapTerrestrial(coords_arr: list, zoomLevel: int, shipfilter: str = None, display: bool = True) -> list:
    params = URLParamMaker(coords_arr, zoomLevel, shipfilter=shipfilter)
    baseurl = "https://www.vesselfinder.com/api/pub/mp2?"
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        # 'Cookie': 'ROUTEID=.1'
        'Dnt': '1'
    }
    response = requests.request("GET", baseurl+params, headers=headers, data=payload)
    
    info = processResponseTerrestrial(response.content, zoomLevel)
    info.sort(key = lambda x: x["MMSI"])
    
    if display:
        # printInfoTerrestrial(info)
        printInfoTerrestrial_WithFilters(info)
    
    return info

def getShipInfoFromMMSI(mmsi: int) -> dict:
    
    traveldata_url = f"https://www.vesselfinder.com/api/pub/vi2/{mmsi}?fv"
    vesseldata_url = f"https://www.vesselfinder.com/api/pub/click/{mmsi}"
    vesselweatherdata_url = f"https://www.vesselfinder.com/api/pub/weather/at/{mmsi}"
    vesselportdata_url = f"https://www.vesselfinder.com/api/pub/pcext/v4/{mmsi}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Cookie': 'ROUTEID=.1'
    }    
    
    traveldata = json.loads((requests.request("GET", traveldata_url, headers=headers)).text)
    vesseldata = json.loads((requests.request("GET", vesseldata_url, headers=headers)).text)
    vesselweatherdata = json.loads((requests.request("GET", vesselweatherdata_url, headers=headers)).text)
    vesselportdata = json.loads((requests.request("GET", vesselportdata_url, headers=headers)).text)
    
    OUTPUT_DICT = {"traveldata": traveldata, "vesseldata": vesseldata, "vesselweatherdata": vesselweatherdata, "vesselportdata": vesselportdata}
    
    return OUTPUT_DICT

def getVesselData(mmsi: int) -> dict:    
    vesseldata_url = f"https://www.vesselfinder.com/api/pub/click/{mmsi}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Cookie': 'ROUTEID=.1'
    }    
    
    vesseldata = json.loads((requests.request("GET", vesseldata_url, headers=headers)).text)
    
    return vesseldata

def getVesselData_MMSIOfInterest(mmsi: int) -> tuple:
    baseurl = "https://www.vesselfinder.com/api/pub/ml/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        # 'Cookie': 'ROUTEID=.1'
        'Dnt': '1'
    }
    response = requests.request("GET", baseurl+str(mmsi), headers=headers)
    
    data = response.content
    idx = 3
    lat_length = 4
    long_length = 4
    
    long_data = data[idx:idx+long_length]
    long = int.from_bytes(long_data, "big") / 600000
    idx += long_length
    
    lat_data = data[idx:idx+lat_length]
    lat = int.from_bytes(lat_data, "big") / 600000
    idx += lat_length
    
    ship_name_length = data[idx]
    idx += 1
    
    ship_name = data[idx:idx+ship_name_length].decode("utf-8")
    idx += ship_name_length
    
    return (lat, long, ship_name)



def printInfoSatellite(info: list):
    for cnt, data in enumerate(info):
        print(f'SAT-{cnt : <3} | {str(round(data["Latitude"], COORDS_ACCURACY)) + ", " + str(round(data["Longitude"], COORDS_ACCURACY)):<25} \t| {round((int(data["msSinceLastPing"]) / 60000), 2)}')

def processResponseSatellite(data: bytes) -> list:
    LOCAL_DEBUG = False
    # LOCAL_DEBUG = True
    OUTPUT_shipdata = []
    
    if LOCAL_DEBUG:
        print("Response header")
        for b in data[:4]:
            print(hex(b), end = " ")
        print()
        
        print("Response body")
    
    idx = 4
    lat_length = 4
    long_length = 4    
    last_ping_length = 3
    
    while idx < len(data):
        try:
            lat_data = data[idx:idx+lat_length]
            lat = int.from_bytes(lat_data, "big") / 600000
            idx += lat_length
            
            long_data = data[idx:idx+long_length]
            long = int.from_bytes(long_data, "big") / 600000
            idx += long_length
            
            last_ping_data = data[idx:idx+last_ping_length]
            last_ping = int.from_bytes(last_ping_data, "big")
            idx += last_ping_length
            
            if LOCAL_DEBUG:
                print("-"*20)
                print("---coords---")
                print(lat_data)
                print(long_data)
                print(lat)
                print(long)
                print("---last_ping---")
                print(last_ping_data)
                print(last_ping)
            
            OUTPUT_shipdata.append({"Latitude": lat, "Longitude": long, "msSinceLastPing" : last_ping})
            
        except Exception as e:
            print("----- An error occurred. -----")
            print(e)
        
    return OUTPUT_shipdata

def getShipsOnMapSatellite(coords_arr: list, zoomLevel: int, shipfilter: str = None, display: bool = True) -> list:
    params = URLParamMaker(coords_arr, zoomLevel, shipfilter=shipfilter)
    baseurl = "https://www.vesselfinder.com/api/pub/sfl?"
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Cookie': 'ROUTEID=.1'
    }
    response = requests.request("GET", baseurl+params, headers=headers, data=payload)
    
    info = processResponseSatellite(response.content)
    info.sort(key = lambda x: x["msSinceLastPing"])
    
    if display:
        printInfoSatellite(info)






