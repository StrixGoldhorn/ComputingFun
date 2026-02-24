import json
import sqlite3
import os
import time

START_EPOCH = time.time() - 60 * 60 * 0.5 * 1
START_EPOCH = 1771368480 - 60 * 60 * 0.5 * 1
#                         s   min  hrs  days
END_EPOCH = START_EPOCH + 60 * 60 * 0.5 * 1

class db_actions:
    DATABASE_FOLDER_NAME = "db_folder"

    @staticmethod
    def getDataDBConnection() -> sqlite3.Connection:
        """Get a connection to the main data database"""
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_actions.DATABASE_FOLDER_NAME, "18Feb26_0630_Scan.db")
        return sqlite3.connect(db_path)
    
    def getDataBetweenTimeframe(start_epoch: int, end_epoch: int) -> list:
        '''
        Returns list of data
        '''
        conn = db_actions.getDataDBConnection()
        conn.row_factory = sqlite3.Row
        try:
            output = []
            curs = conn.cursor()
            curs.execute(" \
            SELECT ll.id AS llid, ll.lat, ll.long, ll.timestamp, gs.vehID, gs.id AS gsid, gs.mmsi, gs.shipName, gs.shipType \
            FROM LocationLog AS ll \
            INNER JOIN GeoShipInfo AS gs ON ll.vehID = gs.vehID \
            WHERE ? < ll.timestamp AND ll.timestamp < ? \
            GROUP BY gs.mmsi \
            ", (start_epoch, end_epoch))
            conn.commit()
            data = curs.fetchall()
            for d in data:
                output.append({
                    "type" : "Feature",
                    "geometry" : {
                        "type" : "Point",
                        "coordinates" : [ d["long"], d["lat"] ]
                    },
                    "properties" : {
                        "LOCATION_LOG_ID" : d["llid"],
                        "VEH_ID" : d["vehID"],
                        "GEO_SHIP_ID" : d["gsid"],
                        "MMSI" : d["mmsi"],
                        "SHIP_NAME" : d["shipname"],
                        "SHIP_TYPE" : "Tug",
                        "TIMESTAMP" : d["timestamp"],
                        "LATITUDE" : d["lat"],
                        "LONGITUDE" : d["long"]
                    }
                })
            print(f"Records processed: {len(data)}")
            return output
        
        finally:
            curs.close()
            conn.close()

def main():
    # ll.timestamp,, gs.mmsi, gs.shipName, gs.shipType
    geojson_template = {
        "type" : "FeatureCollection",
        "name" : "Location_Log"
    }

    ll_data = db_actions.getDataBetweenTimeframe(START_EPOCH, END_EPOCH)
    geojson_template.update({"features" : ll_data})

    f_write = json.dumps(geojson_template, separators = (',', ':'))

    with open("LocationLog.geojson", "w") as f:
        f.write(f_write)

if __name__ == "__main__":
    main()