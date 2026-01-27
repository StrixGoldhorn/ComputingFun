from .geoShipSource import geoShipSource
import requests
from database import ShipDBActions, AudtiDBActions, DataSourceDBActions, DatabaseMain
from random import randint
import json
import sqlite3
import os

class AISFriendsScraper(geoShipSource):
    DATASOURCE_ID = 3
    
    @staticmethod
    def addToDatasource():
        DataSourceDBActions.addDataSourceToDataSourceDB("AISFriendsScraper")

    @staticmethod
    def scanAndSaveAreaToDB(coords_arr: list, zoomLevel: int = 15):
        latmin = coords_arr[0]
        latmax = coords_arr[1]
        longmin = coords_arr[2]
        longmax = coords_arr[3]
        
        url = f"https://www.aisfriends.com/vessels/bounding-box?lon_min={longmin}&lat_min={latmin}&lon_max={longmax}&lat_max={latmax}&zoom={zoomLevel}"
        
        randint1 = randint(100, 999)
        randint2 = randint(100, 300)
        headers = {
                'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{randint1}.36 (KHTML, like Gecko) Chrome/{randint2}.0.0.0 Safari/{randint1}.36',
                'Dnt': '1',
                'referer': 'https://www.aisfriends.com/'
            }
        
        try:
            try:
                r = requests.get(url, headers=headers)
            except Exception as e:
                print(f"ERROR - AISFriendsScraper - scanAndSaveAreaToDB, Request failed: {e}")
                AudtiDBActions.writeToAuditDB("error", "AISFriendsScraper - scanAndSaveAreaToDB", f"Request failed {e}")
                
            data = json.loads(r.text)
            
            for vessel in data:
                # keys = ['id', 'vessel_id', 'class', 'imo', 'mmsi', 'name', 'name_ais', 'ship_type_id', 'detailed_type_id', 'timestamp_of_position',
                # 'length', 'beam', 'to_bow', 'to_stern', 'to_port', 'to_starboard', 'true_heading', 'course_over_ground', 'speed_over_ground', 'draught',
                # 'navigational_status_id', 'flag', 'latitude', 'longitude', 'lat_grid', 'lon_grid']
                
                vesseldata = AISFriendsScraper.getShipInfo(vessel['vessel_id'])
                
                lat = vesseldata['latitude']    
                long = vesseldata['longitude']
                timestamp = vesseldata['timestamp_of_position']
                mmsi = vesseldata['mmsi']
                shipname = vesseldata['name_ais']
                country = vesseldata['flag']
                shiptype = vesseldata['type']
                speed = vesseldata['speed_over_ground']
                course = vesseldata['course_over_ground']
                trueheading = vesseldata['true_heading']
                rateofturn = vesseldata['rate_of_turn']
            
                vessel_id = vesseldata['vessel_id']
            
                try:
                    ShipDBActions.addGeoShipLog(lat, long, timestamp, mmsi, shipname, country, shiptype, speed, course, trueheading, rateofturn, AISFriendsScraper.DATASOURCE_ID)
                    AISFriendsScraper.addToOwnDB(mmsi, vessel_id)
                    # AudtiDBActions.writeToAuditDB("write", "AISFriendsScraper - scanAndSaveAreaToDB", f"Saved area to DB, Area: {coords_arr}")
                except Exception as e:
                    print(f"ERROR - AISFriendsScraper - scanAndSaveAreaToDB, Unable to save to DB: {e}")
                    AudtiDBActions.writeToAuditDB("error", "AISFriendsScraper - scanAndSaveAreaToDB", f"Unable to save to DB, Area: {coords_arr}")

            
        except Exception as e:
            print(f"ERROR - AISFriendsScraper - scanAndSaveAreaToDB, Scan failed: {e}")
            AudtiDBActions.writeToAuditDB("error", "AISFriendsScraper - scanAndSaveAreaToDB", f"Scan failed {e}")
        
        pass
    
    @staticmethod
    def getShipInfo(vessel_id:int = 0):
        url = f"https://www.aisfriends.com/vessel/position/vessel_id:{vessel_id}"
        randint1 = randint(100, 999)
        randint2 = randint(100, 300)
        headers = {
                'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{randint1}.36 (KHTML, like Gecko) Chrome/{randint2}.0.0.0 Safari/{randint1}.36',
                'Dnt': '1',
                'referer': 'https://www.aisfriends.com/'
            }
        
        # keys = ['id', 'vessel_id', 'class', 'imo', 'eni', 'mmsi', 'name', 'name_ais', 'call_sign', 'ship_type_id', 
        # 'type', 'detailed_type', 'detailed_type_id', 'navy_type', 'flag', 'mid_code', 'country', 'length', 
        # 'beam', 'to_bow', 'to_stern', 'to_port', 'to_starboard', 'longitude', 'latitude', 'navigational_status_id', 
        # 'navigational_status', 'speed_over_ground', 'course_over_ground', 'true_heading', 'rate_of_turn', 
        # 'maneuver_indicator_id', 'maneuver_indicator', 'draught', 'gt', 'dwt', 'year', 'eta_month_utc', 
        # 'eta_day_utc', 'eta_hour_utc', 'eta_minute_utc', 'ais_destination', 'last_port', 'message_type', 
        # 'message_id', 'station_id', 'timestamp_of_position', 'created_at', 'updated_at', 'cached_name', 'source_table']
        
        
        r = requests.get(url, headers=headers)
        return json.loads(r.text)
        

    @staticmethod
    def scanAndSaveShipToDB(mmsi: int):
        # Unfortunately, this site does not have a direct way of getting a ship info from just its mmsi
        # Refer to getShipInfo for all the info required
        
        try:
            conn = AISFriendsScraper.getAISFriendsDBConnection()
            curs = conn.cursor()

            curs.execute("SELECT vessel_id FROM shipdata WHERE mmsi = ?", (mmsi,))
            vessel_id = curs.fetchone()[0]

            conn.commit()
            curs.close()
            conn.close()
            
            vesseldata = AISFriendsScraper.getShipInfo(vessel_id)
                
            lat = vesseldata['latitude']    
            long = vesseldata['longitude']
            timestamp = vesseldata['timestamp_of_position']
            mmsi = vesseldata['mmsi']
            shipname = vesseldata['name_ais']
            country = vesseldata['flag']
            shiptype = vesseldata['type']
            speed = vesseldata['speed_over_ground']
            course = vesseldata['course_over_ground']
            trueheading = vesseldata['true_heading']
            rateofturn = vesseldata['rate_of_turn']
        
            vessel_id = vesseldata['vessel_id']
        
            try:
                ShipDBActions.addGeoShipLog(lat, long, timestamp, mmsi, shipname, country, shiptype, speed, course, trueheading, rateofturn, AISFriendsScraper.DATASOURCE_ID)
            except Exception as e:
                print(f"ERROR - AISFriendsScraper - scanAndSaveShipToDB, Unable to save to DB: {e}")
                AudtiDBActions.writeToAuditDB("error", "AISFriendsScraper - scanAndSaveShipToDB", f"Unable to save to DB, MMSI: {mmsi}")
            
        except Exception as e:
            print(f"ERROR - AISFriendsScraper - scanAndSaveShipToDB: {e}")
            AudtiDBActions.writeToAuditDB("error", "AISFriendsScraper - scanAndSaveShipToDB", f"{e}")

        finally:
            conn.close()
        
    
    @staticmethod
    def getDBfilepath(dbname: str) -> str:
        ownfilepath = os.path.dirname(os.path.abspath(__file__))
        db_folder = os.path.join(ownfilepath, "../db_folder")
        os.makedirs(db_folder, exist_ok=True)
        created_filepath = os.path.join(db_folder, dbname)
        return created_filepath
    
    @staticmethod
    def initOwnDB():
        dbname = "AISFriends.db"
        created_filepath = AISFriendsScraper.getDBfilepath(dbname)
        
        try:
            conn = sqlite3.connect(created_filepath)
            curs = conn.cursor()

            curs.execute("CREATE TABLE IF NOT EXISTS shipdata \
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                        mmsi INTEGER NOT NULL, \
                        vessel_id INTEGER NOT NULL)")
            
            conn.commit()
            print(f"{dbname} successfully created")
            
        except Exception as e:
            print("Error:", e)
            
    @staticmethod
    def getAISFriendsDBConnection() -> sqlite3.Connection:
        """Get a connection to the AISFriends database"""
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", DatabaseMain.DATABASE_FOLDER_NAME, "AISFriends.db")
        return sqlite3.connect(db_path)
    
    @staticmethod
    def addToOwnDB(mmsi: int, vessel_id: int):
        try:
            conn = AISFriendsScraper.getAISFriendsDBConnection()
            curs = conn.cursor()

            curs.execute("SELECT mmsi, vessel_id FROM shipdata " \
            "WHERE mmsi = ? AND vessel_id = ?", (mmsi, vessel_id))
            if curs.fetchone():
                pass
            else:
                curs.execute("INSERT INTO shipdata (mmsi, vessel_id) VALUES (?, ?)", (mmsi, vessel_id))

            conn.commit()
            curs.close()
            conn.close()
        
        except Exception as e:
            print(f"ERROR - AISFriendsScraper - addToOwnDB: {e}")
            AudtiDBActions.writeToAuditDB("error", "AISFriendsScraper - addToOwnDB", f"{e}")

        finally:
            conn.close()