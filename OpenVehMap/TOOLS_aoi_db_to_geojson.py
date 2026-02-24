import json
import sqlite3
import os

class db_actions:
    DATABASE_FOLDER_NAME = "db_folder"

    @staticmethod
    def getDataDBConnection() -> sqlite3.Connection:
        """Get a connection to the main data database"""
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_actions.DATABASE_FOLDER_NAME, "aoi.db")
        return sqlite3.connect(db_path)
    
    def getAOIs() -> list:
        '''
        Returns list of data
        '''
        conn = db_actions.getDataDBConnection()
        conn.row_factory = sqlite3.Row
        try:
            output = []
            curs = conn.cursor()
            curs.execute(" \
            SELECT aoiPosID, placeName, x1, x2, y1, y2 \
            FROM AoiPos AS ap \
            INNER JOIN AoiDesc AS ad ON ap.id = ad.aoiPosID \
            ")
            conn.commit()
            data = curs.fetchall()
            for d in data:
                output.append({
                    "type" : "Feature",
                    "geometry" : {
                        "type" : "Polygon",
                        "coordinates" : [
                            [
                                [ d['y1'], d['x1'] ],
                                [ d['y1'], d['x2'] ],
                                [ d['y2'], d['x2'] ],
                                [ d['y2'], d['x1'] ]
                            ]
                        ]
                    },
                    "properties" : {
                        "AOI_POS_ID" : 44,
                        "NAME" : d['placeName'],
                    }
                })
            return output
        
        finally:
            curs.close()
            conn.close()

def main():
    # ll.timestamp,, gs.mmsi, gs.shipName, gs.shipType
    geojson_template = {
        "type" : "FeatureCollection",
        "name" : "AOI"
    }

    aoi_data = db_actions.getAOIs()
    geojson_template.update({"features" : aoi_data})

    f_write = json.dumps(geojson_template, separators = (',', ':'))

    with open("AOI.geojson", "w") as f:
        f.write(f_write)

if __name__ == "__main__":
    main()