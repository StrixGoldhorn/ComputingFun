from .geoShipSource import geoShipSource
import requests
from database import ShipDBActions, AudtiDBActions, DataSourceDBActions
from random import randint
import json

class VesselFinderScraper(geoShipSource):
    DATASOURCE_ID = 1

    @staticmethod
    def addToDatasource():
        DataSourceDBActions.addDataSourceToDataSourceDB("VesselFinder")

    @staticmethod
    def getVesselInfoResponse(mmsi: int) -> dict:
            randint1 = randint(100, 999)
            randint2 = randint(100, 300)
            headers = {
                'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{randint1}.36 (KHTML, like Gecko) Chrome/{randint2}.0.0.0 Safari/{randint1}.36',
                'Dnt': '1',
                'Referer' : 'https://www.vesselfinder.com/api/pub/ml/'
            }
            vesseldata_url = f"https://www.vesselfinder.com/api/pub/click/{mmsi}"
            vesseldata = json.loads((requests.request("GET", vesseldata_url, headers=headers)).text)
            return vesseldata
    
    @staticmethod
    def getLatLongNameOfMMSI(mmsi: int) -> tuple[float, float, str]:
        baseurl = "https://www.vesselfinder.com/api/pub/ml/"
        randint1 = randint(100, 999)
        randint2 = randint(100, 300)
        headers = {
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{randint1}.36 (KHTML, like Gecko) Chrome/{randint2}.0.0.0 Safari/{randint1}.36',
            'Dnt': '1',
            'Referer' : 'https://www.vesselfinder.com/api/pub/ml/'
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


    
    @staticmethod
    def URLParamMaker(coords_arr: list, zoom: int, shipfilter: str = None) -> str:
        '''
        Creates the params required to scan area.
        Requires input of coords_arr, zoom level, and any ship filter
        '''
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
    
    @staticmethod
    def scanAndSaveAreaToDB(coords_arr: list, zoomLevel: int, shipfilter: str = None, display: bool = True) -> None:

        # Helper class
        def processResponseTerrestrial(data: bytes, zoomLevel: int) -> list[dict]:
            '''
            Outputs list of dict with MMSI, Ship Name, Latitude, Longitude, DisplayColor
            '''
            LOCAL_DEBUG = False
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


        try:
            randint1 = randint(100, 999)
            randint2 = randint(100, 300)
            params = VesselFinderScraper.URLParamMaker(coords_arr, zoomLevel, shipfilter=shipfilter)
            baseurl = "https://www.vesselfinder.com/api/pub/mp2?"
            payload = {}
            headers = {
                'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{randint1}.36 (KHTML, like Gecko) Chrome/{randint2}.0.0.0 Safari/{randint1}.{randint2}',
                'Dnt': '1'
            }
            response = requests.request("GET", baseurl+params, headers=headers, data=payload)

            print(f"VesselFinderScraper - scanAndSaveAreaToDB: Received response")
            
            info = processResponseTerrestrial(response.content, zoomLevel)
            info.sort(key = lambda x: x["MMSI"])
            
            def saveToDB(info):
                for vessel in info:
                    mmsi = vessel["MMSI"]
                    shipname = vessel["Ship Name"].decode("utf-8")
                    lat = vessel["Latitude"]
                    long = vessel["Longitude"]

                    moreinfo = VesselFinderScraper.getVesselInfoResponse(mmsi)
                    country = moreinfo["country"]
                    shiptype = moreinfo["type"]
                    speed = moreinfo["ss"]
                    course = moreinfo["cu"]
                    trueheading = None
                    rateofturn = None
                    timestamp = moreinfo["ts"]
                    
                    try:
                        ShipDBActions.addGeoShipLog(lat, long, timestamp, mmsi, shipname, country, shiptype, speed, course, trueheading, rateofturn, VesselFinderScraper.DATASOURCE_ID)
                        # AudtiDBActions.writeToAuditDB("write", "VesselFinderScraper - scanAndSaveAreaToDB", f"Saved area to DB, Area: {coords_arr}")
                    except Exception as e:
                        print(f"ERROR - VesselFinderScraper - scanAndSaveAreaToDB, Unable to save to DB: {e}")
                        AudtiDBActions.writeToAuditDB("error", "VesselFinderScraper - scanAndSaveAreaToDB", f"Unable to save to DB, Area: {coords_arr}")

            saveToDB(info)

        except Exception as e:
            print(f"ERROR - VesselFinderScraper - scanAndSaveAreaToDB, Scan failed: {e}")
            AudtiDBActions.writeToAuditDB("error", "VesselFinderScraper - scanAndSaveAreaToDB", f"Scan failed {e}")
    
    @staticmethod
    def scanAndSaveShipToDB(mmsi: int) -> None:
        someinfo = VesselFinderScraper.getLatLongNameOfMMSI(mmsi)
        lat = someinfo[0]
        long = someinfo[1]
        shipname = someinfo[2]

        moreinfo = VesselFinderScraper.getVesselInfoResponse(mmsi)
        country = moreinfo["country"]
        shiptype = moreinfo["type"]
        speed = moreinfo["ss"]
        course = moreinfo["cu"]
        trueheading = None
        rateofturn = None
        timestamp = moreinfo["ts"]
        
        try:
            ShipDBActions.addGeoShipLog(lat, long, timestamp, mmsi, shipname, country, shiptype, speed, course, trueheading, rateofturn, VesselFinderScraper.DATASOURCE_ID)
            # AudtiDBActions.writeToAuditDB("write", "VesselFinderScraper - scanAndSaveShipToDB", f"Saved ship to DB, MMSI: {mmsi}")
        except:
            AudtiDBActions.writeToAuditDB("error", "VesselFinderScraper - scanAndSaveShipToDB", f"Unable to save to DB, MMSI: {mmsi}")
