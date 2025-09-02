import sqlite3
import os

def getDBFilepath() -> str:
    ownfilepath = os.path.dirname(os.path.abspath(__file__))
    db_filepath = os.path.join(ownfilepath, "ships.db")
    return db_filepath

def getAllRecent(hours:int) -> list:
    db_filepath = getDBFilepath()
    
    try:
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        
        curs.execute("SELECT lat, long, timestamp, ship_name FROM TER_AIS_ship_geo_history \
                    WHERE (unixepoch('now') - timestamp) < 60 * 60 * ? \
                    GROUP BY ship_name \
                    HAVING MAX(timestamp) \
                    ORDER BY timestamp DESC",\
                    (hours,))
        shipPoints = curs.fetchall()

        # Dear future me,
        # Please fix the next few lines.

        # convert Sqlite3.Row to dict
        shipPoints = [dict(row) for row in shipPoints]

        # iterate through to convert all ship_name into only having alphanumeric chars
        for ship in shipPoints:
            ship["ship_name_modded"] = ''.join(x for x in ship["ship_name"] if (x.isalpha() or x.isnumeric()))

        return shipPoints
        
    except Exception as e:
        print("Error:", e)
        return None


getAllRecent(12)