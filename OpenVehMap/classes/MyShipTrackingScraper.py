from .geoShipSource import geoShipSource
import requests
from database import ShipDBActions, AudtiDBActions, DataSourceDBActions
from random import randint
import json

class MyShipTrackingScraper(geoShipSource):
    @staticmethod
    def addToDatasource():
        DataSourceDBActions.addDataSourceToDataSourceDB("MyShipTrackingScraper")

    @staticmethod
    def scanAndSaveAreaToDB(coords_arr: list):
        def processRowAndSaveToDB(row:list) -> None:
            if row[0] not in ["1", "30"]:
                lat = row[4]
                long = row[5]
                timestamp = row[13]
                mmsi = row[2]
                shipname = row[3]
                country = None
                shiptype = None
                speed = row[6]
                course = row[7]
                trueheading = None
                rateofturn = None
                
                # isSat = True if row[1] == "1" else False
                
                try:
                    ShipDBActions.addGeoShipLog(lat, long, timestamp, mmsi, shipname, country, shiptype, speed, course, trueheading, rateofturn)
                    # AudtiDBActions.writeToAuditDB("write", "MyShipTrackingScraper - scanAndSaveAreaToDB", f"Saved area to DB, Area: {coords_arr}")
                except Exception as e:
                    print(f"ERROR - MyShipTrackingScraper - scanAndSaveAreaToDB, Unable to save to DB: {e}")
                    AudtiDBActions.writeToAuditDB("error", "MyShipTrackingScraper - scanAndSaveAreaToDB", f"Unable to save to DB, Area: {coords_arr}")
                
            elif row[0] == "1":
                # todo
                # r[1]: Port ID
                # r[2]: Port name
                # r[3-4]: Coordinates
                pass
            
        latmin = coords_arr[0]
        latmax = coords_arr[1]
        longmin = coords_arr[2]
        longmax = coords_arr[3]

        url = f"https://www.myshiptracking.com/requests/vesselsonmaptempTTT.php?type=json&minlat={latmin}&maxlat={latmax}&minlon={longmin}&maxlon={longmax}&zoom=15&selid=-1&seltype=0&timecode=-1"

        randint1 = randint(100, 999)
        randint2 = randint(100, 300)
        headers = {
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{randint1}.36 (KHTML, like Gecko) Chrome/{randint2}.0.0.0 Safari/{randint1}.36',
            'Accept':'application/json',
            'Connection':'keep-alive',
            'Referer':'https://www.myshiptracking.com/'
        }

        r = requests.request("GET", url, headers=headers)
        rawdata = r.text.split("\n")

        for row in rawdata[2:-2]:
            tmp = row.split("\t")
            processRowAndSaveToDB(tmp)


    @staticmethod
    def getShipInfo(vessel_id:int = 0):
        # todo
        pass