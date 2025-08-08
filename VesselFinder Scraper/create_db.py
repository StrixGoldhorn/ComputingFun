import sqlite3
import os



def generateDB(force_reset: bool = False):
    ownfilepath = os.path.dirname(os.path.abspath(__file__))
    created_filepath = os.path.join(ownfilepath, "ships.db")
    
    if force_reset:
        try:
            os.remove(created_filepath)
            print("Deleted pre-existing file")
        except:
            print("No pre-existing file")
    
    try:
        conn = sqlite3.connect(created_filepath)
        curs = conn.cursor()

        curs.execute("CREATE TABLE IF NOT EXISTS ship (id INTEGER PRIMARY KEY AUTOINCREMENT, mmsi INT, name TEXT, country TEXT, ship_type TEXT)")
        curs.execute("CREATE TABLE IF NOT EXISTS mmsi_of_interest (id INTEGER PRIMARY KEY AUTOINCREMENT, mmsi INT)")
        curs.execute("CREATE TABLE IF NOT EXISTS ship_history (id INTEGER PRIMARY KEY AUTOINCREMENT, mmsi INT, name TEXT, lat FLOAT, long FLOAT, timestamp UNIXEPOCH)")
        
        conn.commit()
        print("DB successfully created")
        
    except Exception as e:
        print("Error:", e)
