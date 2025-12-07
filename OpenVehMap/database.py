import time
from database_init import DatabaseINIT
import sqlite3
import os
from datetime import datetime

class DatabaseMain:
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
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_folder", "audit.db")
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
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_folder", "aoi.db")
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
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_folder", "datasource.db")
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
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_folder", "data.db")
        return sqlite3.connect(db_path)

    @staticmethod
    def addGeoShip(mmsi: int, shipname: str, country: str, shiptype:str) -> None:
        """Checks GeoShipInfo, then adds to GeoShipInfo AND Vehicle if it does not already exists"""
        try:
            conn = ShipDBActions.getDataDBConnection()
            curs = conn.cursor()

            curs.execute("SELECT mmsi, shipName, country, shipType FROM GeoShipInfo " \
            "WHERE mmsi = ? AND shipName = ? AND country = ? AND shipType = ?", (mmsi, shipname, country, shiptype))
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
                      speed: float, course: float, trueHeading: float, rateOfTurn: float):
        try:
            dataconn = ShipDBActions.getDataDBConnection()
            datacurs = dataconn.cursor()

            ShipDBActions.addGeoShip(mmsi, shipname, country, shiptype)

            datacurs.execute("SELECT vehID FROM GeoShipInfo " \
            "WHERE mmsi = ? AND shipName = ? AND country = ? AND shipType = ?", (mmsi, shipname, country, shiptype))

            vehid = datacurs.fetchone()[0]

            datacurs.execute("INSERT INTO LocationLog (lat, long, timestamp, vehID, sourceID) " \
            "VALUES (?, ?, ?, ?, ?)", (lat, long, timestamp, vehid, -1))

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
    def getHistoryOfMMSI(mmsi: int) -> tuple:
        '''
        Returns history of mmsi
        '''
        conn = ShipDBActions.getDataDBConnection()
        try:
            output = []
            curs = conn.cursor()
            curs.execute("SELECT LocationLog.lat, LocationLog.long, LocationLog.timestamp FROM GeoShipInfo, LocationLog " \
            "WHERE GeoShipInfo.vehID = LocationLog.vehID AND mmsi = ? ORDER BY LocationLog.timestamp", (mmsi, ))
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
    def getShips24h() -> tuple:
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
    def getShipsMoved24h(tolerance: float = 0.00005) -> tuple:
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


if __name__ == "__main__":
    DatabaseMain.main