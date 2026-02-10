import time
from database_init import DatabaseINIT
import sqlite3
import os
from datetime import datetime

class DatabaseMain:
    DATABASE_FOLDER_NAME = "db_folder"
    
    @staticmethod
    def main():
        DatabaseINIT.main()
        print("Initialised DB!")
        # while True:
        #     print("database.py is running.")
        #     time.sleep(4)

class AudtiDBActions:
    @staticmethod
    def getAuditDBConnection() -> sqlite3.Connection:
        """Get a connection to the main audit database"""
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DatabaseMain.DATABASE_FOLDER_NAME, "audit.db")
        return sqlite3.connect(db_path)
    
    @staticmethod
    def writeToAuditDB(eventType: str, callerName: str, desc: str) -> None:
        conn = AudtiDBActions.getAuditDBConnection()
        curs = conn.cursor()
        curs.execute("INSERT INTO AuditLog (eventType, timestamp, callerName, desc) VALUES (?, ?, ?, ?)",
                     (eventType, datetime.now(), callerName, desc))
        conn.commit()
        curs.close()
        conn.close()
        return
    


class AoiDBActions:
    @staticmethod
    def getAoiDBConnection() -> sqlite3.Connection:
        """Get a connection to the main audit database"""
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DatabaseMain.DATABASE_FOLDER_NAME, "aoi.db")
        return sqlite3.connect(db_path)
    
    @staticmethod
    def addAoi(lat1: float, lat2: float, long1: float, long2: float,
               placeName:str, domain: str, type: str) -> None:
        conn = AoiDBActions.getAoiDBConnection()
        if lat1 > lat2: lat1, lat2 = lat2, lat1
        if long1 > long2: long1, long2 = long2, long1
        try:
            curs = conn.cursor()
            curs.execute("INSERT INTO AoiPos (x1, x2, y1, y2) VALUES (?, ?, ?, ?)",
                        (lat1, lat2, long1, long2))
            curs.execute("INSERT INTO AoiDesc (aoiPosID, placeName, domain, type) " \
            "VALUES (?, ?, ?, ?)", (curs.lastrowid, placeName, domain, type))
            conn.commit()
        except Exception as e:
            print(f"ERROR - AoiDBActions - addAOI: {e}")
            AudtiDBActions.writeToAuditDB("error", "AoiDBActions - addAOI", f"{e}")
        finally:
            curs.close()
            conn.close()

    @staticmethod
    def getAoi(placeName: str) -> tuple:
        '''
        Returns x1, x2, y1, y2 of given placeName
        '''
        conn = AoiDBActions.getAoiDBConnection()
        try:
            curs = conn.cursor()
            curs.execute("SELECT AoiPos.x1, AoiPos.x2, AoiPos.y1, AoiPos.y2 FROM AoiPos, AoiDesc " \
            "WHERE AoiPos.id = AoiDesc.aoiPosID AND AoiDesc.placeName = ?", (placeName,))
            conn.commit()
            return curs.fetchone()
        except Exception as e:
            print(f"ERROR - AoiDBActions - getAoi: {e}")
            AudtiDBActions.writeToAuditDB("error", "AoiDBActions - getAoi", f"{e}")
        finally:
            curs.close()
            conn.close()

    @staticmethod
    def getAllAoi() -> tuple:
        '''
        Returns ALL aois placeName, x1, x2, y1, y2
        '''
        conn = AoiDBActions.getAoiDBConnection()
        try:
            curs = conn.cursor()
            curs.execute("SELECT AoiDesc.placeName, AoiPos.x1, AoiPos.x2, AoiPos.y1, AoiPos.y2 FROM AoiPos, AoiDesc " \
            "WHERE AoiPos.id = AoiDesc.aoiPosID")
            conn.commit()
            return curs.fetchall()
        except Exception as e:
            print(f"ERROR - AoiDBActions - getAllAoietAoi: {e}")
            AudtiDBActions.writeToAuditDB("error", "AoiDBActions - getAllAoi", f"{e}")
        finally:
            curs.close()
            conn.close()


class DataSourceDBActions:
    @staticmethod
    def getDataSourceDBConnection() -> sqlite3.Connection:
        """Get a connection to the main audit database"""
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DatabaseMain.DATABASE_FOLDER_NAME, "datasource.db")
        return sqlite3.connect(db_path)
    
    @staticmethod
    def addDataSourceToDataSourceDB(sourceName: str) -> None:
        conn = DataSourceDBActions.getDataSourceDBConnection()
        curs = conn.cursor()
        curs.execute("INSERT OR IGNORE INTO DataSource (sourceName) VALUES (?)",
                     (sourceName,))
        conn.commit()
        curs.close()
        conn.close()
        return



class ShipDBActions:
    @staticmethod
    def getDataDBConnection() -> sqlite3.Connection:
        """Get a connection to the main data database"""
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DatabaseMain.DATABASE_FOLDER_NAME, "data.db")
        return sqlite3.connect(db_path)

    @staticmethod
    def addGeoShip(mmsi: int, shipname: str, country: str, shiptype:str) -> None:
        """Checks GeoShipInfo, then adds to GeoShipInfo AND Vehicle if it does not already exists"""
        try:
            conn = ShipDBActions.getDataDBConnection()
            curs = conn.cursor()

            curs.execute("SELECT mmsi, shipName, country, shipType FROM GeoShipInfo " \
            "WHERE mmsi = ? AND shipName = ?", (mmsi, shipname))
            if curs.fetchone():
                pass
            else:
                curs.execute("INSERT INTO Vehicles (vehTypeID) VALUES ((SELECT id FROM VehicleType WHERE typeName = 'GeoShip')) ")
                curs.execute("INSERT INTO GeoShipInfo (vehID, mmsi, shipName, country, shipType) " \
                "VALUES (?, ?, ?, ?, ?)", (curs.lastrowid, mmsi, shipname, country, shiptype))

            conn.commit()
            curs.close()
            conn.close()
            # AudtiDBActions.writeToAuditDB("write", "addGeoShip", f"Added MMSI: {mmsi}, Ship Name: {shipname}")
        
        except Exception as e:
            print(f"ERROR - ShipDBActions - addGeoShip: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - addGeoShip", f"{e}")

        finally:
            conn.close()

    
    @staticmethod
    def addGeoShipLog(lat: float, long: float, timestamp: int,
                      mmsi: int, shipname: str, country: str, shiptype:str,
                      speed: float, course: float, trueHeading: float, rateOfTurn: float,
                      sourceID: int):
        try:
            dataconn = ShipDBActions.getDataDBConnection()
            datacurs = dataconn.cursor()

            ShipDBActions.addGeoShip(mmsi, shipname, country, shiptype)

            datacurs.execute("SELECT vehID FROM GeoShipInfo " \
            "WHERE mmsi = ? AND shipName = ?", (mmsi, shipname))

            vehid = datacurs.fetchone()[0]

            # CHECK IF ALREADY EXISTS
            datacurs.execute("SELECT timestamp, vehID, sourceID FROM LocationLog " \
            "WHERE lat = ? AND long = ? AND timestamp = ? AND vehID = ? AND sourceID = ?", (lat, long, timestamp, vehid, sourceID))
            if datacurs.fetchone():
                pass
            else:

                datacurs.execute("INSERT INTO LocationLog (lat, long, timestamp, vehID, sourceID) " \
                "VALUES (?, ?, ?, ?, ?)", (lat, long, timestamp, vehid, sourceID))

                datacurs.execute("INSERT INTO ShipStatusLog (locationLogID, speed, course, trueHeading, rateOfTurn) " \
                "VALUES (?, ?, ?, ?, ?)", (datacurs.lastrowid, speed, course, trueHeading, rateOfTurn))

            dataconn.commit()
            datacurs.close()
            dataconn.close()

        except Exception as e:
            print(f"ERROR - ShipDBActions - addGeoShipLog: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - addGeoShipLog", f"{e}")

        finally:
            dataconn.close()
            
    @staticmethod
    def addMmsiOfInterest(mmsi: int):
        try:
            dataconn = ShipDBActions.getDataDBConnection()
            datacurs = dataconn.cursor()
            datacurs.execute("INSERT INTO mmsiOfInterest (mmsi) VALUES (?)", (mmsi,))
            dataconn.commit()
            datacurs.close()
            dataconn.close()

        except Exception as e:
            print(f"ERROR - ShipDBActions - addMmsiOfInterest: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - addMmsiOfInterest", f"{e}")

        finally:
            dataconn.close()

    @staticmethod
    def getAllmmsiOfInterest() -> list:
        '''
        Returns ALL mmsiOfInterest mmsi
        '''

        conn = ShipDBActions.getDataDBConnection()
        try:
            curs = conn.cursor()
            curs.execute("SELECT mmsi FROM mmsiOfInterest")
            conn.commit()
            return curs.fetchall()
        except Exception as e:
            print(f"ERROR - ShipDBActions - getAllmmsiOfInterest: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - getAllmmsiOfInterest", f"{e}")
        finally:
            curs.close()
            conn.close()

    @staticmethod
    def getHistoryOfMMSI(mmsi: int) -> list:
        '''
        Returns history of mmsi
        '''
        conn = ShipDBActions.getDataDBConnection()
        try:
            output = []
            curs = conn.cursor()
            curs.execute("SELECT LocationLog.lat, LocationLog.long, LocationLog.timestamp FROM GeoShipInfo, LocationLog " \
            "WHERE GeoShipInfo.vehID = LocationLog.vehID AND mmsi = ? GROUP BY LocationLog.timestamp ORDER BY LocationLog.timestamp DESC", (mmsi, ))
            conn.commit()
            data = curs.fetchall()
            for d in data:
                output.append({"lat": d[0], "lng": d[1], "timestamp": d[2]})
            return output
        except Exception as e:
            print(f"ERROR - ShipDBActions - getHistoryOfMMSI: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - getHistoryOfMMSI", f"{e}")
        finally:
            curs.close()
            conn.close()

    @staticmethod
    def get24HHistoryOfMMSI(mmsi: int) -> list:
        '''
        Returns history of mmsi for the past 24 hrs
        '''
        conn = ShipDBActions.getDataDBConnection()
        try:
            output = []
            curs = conn.cursor()
            curs.execute("SELECT LocationLog.lat, LocationLog.long, LocationLog.timestamp FROM GeoShipInfo, LocationLog " \
            "WHERE GeoShipInfo.vehID = LocationLog.vehID AND mmsi = ? AND LocationLog.timestamp >= strftime('%s', 'now') - 86400 " \
            "GROUP BY LocationLog.timestamp ORDER BY LocationLog.timestamp DESC", (mmsi, ))
            conn.commit()
            data = curs.fetchall()
            for d in data:
                output.append({"lat": d[0], "lng": d[1], "timestamp": d[2]})
            return output
        except Exception as e:
            print(f"ERROR - ShipDBActions - getHistoryOfMMSI: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - getHistoryOfMMSI", f"{e}")
        finally:
            curs.close()
            conn.close()

    @staticmethod
    def getInfoOfMMSI(mmsi: int) -> dict:
        '''
        Returns vessel info of mmsi
        '''
        conn = ShipDBActions.getDataDBConnection()
        try:
            curs = conn.cursor()
            curs.execute("SELECT shipName, mmsi, country, shipType FROM GeoShipInfo WHERE mmsi = ?", (mmsi, ))
            conn.commit()
            data = curs.fetchone()
            output = {
                "name": f"{data[0]}",
                "mmsi": f"{data[1]}",
                "country": f"{data[2]}",
                "type": f"{data[3]}"
                }
            return output
        except Exception as e:
            print(f"ERROR - ShipDBActions - getInfoOfMMSI: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - getInfoOfMMSI", f"{e}")
        finally:
            curs.close()
            conn.close()

    @staticmethod
    def getShips24h() -> list:
        '''
        Returns most recent data for each ship captured in the past 24hrs
        '''
        conn = ShipDBActions.getDataDBConnection()
        try:
            output = []
            curs = conn.cursor()
            curs.execute("SELECT GeoShipInfo.mmsi, GeoShipInfo.shipName, " \
            "LocationLog.lat, LocationLog.long, MAX(LocationLog.timestamp), " \
            "ShipStatusLog.speed, ShipStatusLog.course, GeoShipInfo.shipType " \
            "FROM GeoShipInfo, LocationLog, ShipStatusLog " \
            "WHERE GeoShipInfo.vehID = LocationLog.vehID AND ShipStatusLog.locationLogID = LocationLog.id AND LocationLog.timestamp >= strftime('%s', 'now') - 86400 " \
            "GROUP BY GeoShipInfo.mmsi")
            conn.commit()
            data = curs.fetchall()
            for d in data:
                output.append({
                    "mmsi": d[0], "name": d[1],
                    "lat": d[2], "lng": d[3], "timestamp": d[4],
                    "speed": d[5], "course": d[6], "shiptype": d[7]
                })
            return output
        except Exception as e:
            print(f"ERROR - ShipDBActions - getShips24h: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - getShips24h", f"{e}")
        finally:
            curs.close()
            conn.close()
            
    @staticmethod
    def getShipsMoved24h(tolerance: float = 0.00005) -> list:
        '''
        Returns mmsi, name, lat, long, timestamp of ship who moved more than specified tolerance in the past 24h
        Default tolerance approx 5.55m
        '''
        conn = ShipDBActions.getDataDBConnection()
        try:
            output = []
            curs = conn.cursor()
            curs.execute("SELECT GeoShipInfo.mmsi, GeoShipInfo.shipName, " \
            "LocationLog.lat, LocationLog.long, LocationLog.timestamp, " \
            "FROM LocationLog, GeoShipInfo " \
            "WHERE LocationLog.vehID = GeoShipInfo.vehID GROUP BY LocationLog.vehID AND LocationLog.timestamp >= strftime('%s', 'now') - 86400" \
            "HAVING (MAX(LocationLog.lat) - MIN(LocationLog.lat)) > ?;", (tolerance, ))
            conn.commit()
            data = curs.fetchall()
            for d in data:
                output.append({
                    "mmsi": d[0], "name": d[1],
                    "lat": d[2], "lng": d[3], "timestamp": d[4]
                })
            return output
        except Exception as e:
            print(f"ERROR - ShipDBActions - getShipsMoved24h: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - getShipsMoved24h", f"{e}")
        finally:
            curs.close()
            conn.close()

    # UNUSED! Check logic again before implementing
    @staticmethod
    def getNShipsWithOffestMxN(n: int, m: int) -> dict:
        '''
        Returns N ships with offset of M * N
        eg N = 10, M = 2, will return ships with vehID 21 - 30 (inclusive) (1-indexed)
        '''
        conn = ShipDBActions.getDataDBConnection()
        try:
            curs = conn.cursor()
            curs.execute("SELECT mmsi, shipName, country, shipType FROM GeoShipInfo LIMIT ? OFFSET ?;", (n, n*m))
            conn.commit()
            output = []
            data = curs.fetchall()
            for d in data:
                output.append({
                    "mmsi": f"{d[0]}",
                    "name": f"{d[1]}",
                    "country": f"{d[2]}",
                    "type": f"{d[3]}"
                })
            return output
        except Exception as e:
            print(f"ERROR - ShipDBActions - getNShipsWithOffestMxN: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - getNShipsWithOffestMxN", f"{e}")
        finally:
            curs.close()
            conn.close()

    @staticmethod
    def getNShipsWithOffestMxNWithQuery(n: int, m: int, query: str) -> dict:
        '''
        Returns N ships with offset of M * N, filtered based on query.
        eg N = 10, M = 2, will return ships 21 - 30 (inclusive) (1-indexed) in the result
        '''
        conn = ShipDBActions.getDataDBConnection()
        try:
            curs = conn.cursor()
            # TODO check for sqli
            search = f"%{query}%"
            curs.execute("SELECT mmsi, shipName, country, shipType FROM GeoShipInfo \
                         WHERE mmsi LIKE ? \
                         OR shipName LIKE ? \
                         OR shipType LIKE ? \
                         OR country LIKE ? \
                         LIMIT ? OFFSET ?;", (search, search, search, search, n, n*m))
            conn.commit()
            output = []
            data = curs.fetchall()
            for d in data:
                output.append({
                    "mmsi": f"{d[0]}",
                    "name": f"{d[1]}",
                    "country": f"{d[2]}",
                    "type": f"{d[3]}"
                })
            return output
        except Exception as e:
            print(f"ERROR - ShipDBActions - getNShipsWithOffestMxNWithQuery: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - getNShipsWithOffestMxNWithQuery", f"{e}")
        finally:
            curs.close()
            conn.close()

    @staticmethod
    def getTotalGeoShipCount() -> list:
        '''
        Returns number of entries in GeoShipInfo
        '''

        conn = ShipDBActions.getDataDBConnection()
        try:
            curs = conn.cursor()
            curs.execute("SELECT COUNT(*) FROM GeoShipInfo")
            conn.commit()
            return curs.fetchone()
        except Exception as e:
            print(f"ERROR - ShipDBActions - getTotalGeoShipCount: {e}")
            AudtiDBActions.writeToAuditDB("error", "ShipDBActions - getTotalGeoShipCount", f"{e}")
        finally:
            curs.close()
            conn.close()



if __name__ == "__main__":
    DatabaseMain.main