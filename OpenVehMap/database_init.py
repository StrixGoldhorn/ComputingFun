import sqlite3
import os



def getDBfilepath(dbname: str) -> str:
    ownfilepath = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(ownfilepath, "db_folder")
    os.makedirs(db_folder, exist_ok=True)
    created_filepath = os.path.join(db_folder, dbname)
    return created_filepath


def deleteDBIfExists(dbname: str):
    created_filepath = getDBfilepath(dbname)

    try:
        os.remove(created_filepath)
        print(f"Deleted pre-existing {dbname}")
    except:
        print(f"No pre-existing file with filename {dbname}")


def generateAuditDB(force_reset: bool = False):
    dbname = "audit.db"
    created_filepath = getDBfilepath(dbname)
    
    if force_reset:
        deleteDBIfExists(dbname)
    
    try:
        conn = sqlite3.connect(created_filepath)
        curs = conn.cursor()

        curs.execute("CREATE TABLE IF NOT EXISTS AuditLog \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    eventType TEXT CHECK(eventType IN ('write', 'error')), \
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, \
                    callerName TEXT, \
                    desc TEXT)")
        
        conn.commit()
        print(f"{dbname} successfully created")
        
    except Exception as e:
        print("Error:", e)


def generateDataSourceDB(force_reset: bool = False):
    dbname = "datasource.db"
    created_filepath = getDBfilepath(dbname)
    
    if force_reset:
        deleteDBIfExists(dbname)
    
    try:
        conn = sqlite3.connect(created_filepath)
        curs = conn.cursor()

        curs.execute("CREATE TABLE IF NOT EXISTS DataSource \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    sourceName TEXT NOT NULL UNIQUE)")
        
        conn.commit()
        print(f"{dbname} successfully created")
        
    except Exception as e:
        print("Error:", e)


def generateAOIDB(force_reset: bool = False):
    dbname = "aoi.db"
    created_filepath = getDBfilepath(dbname)
    
    if force_reset:
        deleteDBIfExists(dbname)
    
    try:
        conn = sqlite3.connect(created_filepath)
        curs = conn.cursor()

        # Create AoiDesc table
        curs.execute("CREATE TABLE IF NOT EXISTS AoiDesc \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    aoiPosID INTEGER NOT NULL, \
                    placeName TEXT NOT NULL UNIQUE, \
                    domain TEXT CHECK(domain IN ('air', 'naval', 'land')), \
                    type TEXT CHECK(type IN ('passive', 'evaluate')), \
                    FOREIGN KEY(aoiPosID) REFERENCES AoiPos(id))")
        
        # Create AoiPos table
        curs.execute("CREATE TABLE IF NOT EXISTS AoiPos \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    x1 FLOAT NOT NULL, \
                    x2 FLOAT NOT NULL, \
                    y1 FLOAT NOT NULL, \
                    y2 FLOAT NOT NULL)")
        
        conn.commit()
        print(f"{dbname} successfully created")
        
    except Exception as e:
        print("Error:", e)


def generateDataDB(force_reset: bool = False):
    dbname = "data.db"
    created_filepath = getDBfilepath(dbname)
    
    if force_reset:
        deleteDBIfExists(dbname)
    
    try:
        conn = sqlite3.connect(created_filepath)
        curs = conn.cursor()

        # Create Vehicles table
        curs.execute("CREATE TABLE IF NOT EXISTS Vehicles \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    vehTypeID INTEGER, \
                    FOREIGN KEY(vehTypeID) REFERENCES VehicleType(id))")
        
        # Create VehicleType table
        curs.execute("CREATE TABLE IF NOT EXISTS VehicleType \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    typeName TEXT)")
        
        # Add GeoShip
        curs.execute("INSERT INTO VehicleType (typeName) VALUES ('GeoShip')")
        
        # Add SatShip
        curs.execute("INSERT INTO VehicleType (typeName) VALUES ('SatShip')")
        
        # Create LocationLog table
        curs.execute("CREATE TABLE IF NOT EXISTS LocationLog \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    lat FLOAT NOT NULL, \
                    long FLOAT NOT NULL, \
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, \
                    vehID INTEGER NOT NULL, \
                    sourceID INTEGER NOT NULL, \
                    FOREIGN KEY(vehID) REFERENCES Vehicles(id))")
        
        # Create ShipStatusLog table
        curs.execute("CREATE TABLE IF NOT EXISTS ShipStatusLog \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    locationLogID INTEGER NOT NULL, \
                    speed FLOAT, \
                    course FLOAT, \
                    trueHeading FLOAT, \
                    rateOfTurn FLOAT, \
                    FOREIGN KEY(locationLogID) REFERENCES LocationLog(id))")
        
        # Create GeoShipInfo table
        curs.execute("CREATE TABLE IF NOT EXISTS GeoShipInfo \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    vehID INTEGER NOT NULL, \
                    mmsi TEXT NOT NULL, \
                    shipName TEXT NOT NULL, \
                    country TEXT, \
                    shipType TEXT, \
                    FOREIGN KEY(vehID) REFERENCES Vehicles(id))")
        
        # Create SatShipInfo table
        curs.execute("CREATE TABLE IF NOT EXISTS SatShipInfo \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    vehID INTEGER NOT NULL, \
                    shipName TEXT NOT NULL, \
                    FOREIGN KEY(vehID) REFERENCES Vehicles(id))")
        
        # Create mmsiOfInterest table
        curs.execute("CREATE TABLE IF NOT EXISTS mmsiOfInterest \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    mmsi INTEGER NOT NULL)")
        conn.commit()
        print(f"{dbname} successfully created")
        
    except Exception as e:
        print("Error:", e)

class DatabaseINIT():
    def main():
        print("------ DB generation started! ------")
        reset = False
        generateAuditDB(force_reset = reset)
        generateDataSourceDB(force_reset = reset)
        generateAOIDB(force_reset = reset)
        generateDataDB(force_reset = reset)
        print("------ DB generation complete! ------")


        
if __name__ == "__main__":
    DatabaseINIT.main()
