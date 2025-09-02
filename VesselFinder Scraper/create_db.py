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
            print("No pre-existing file with filename", created_filepath)
    
    try:
        conn = sqlite3.connect(created_filepath)
        curs = conn.cursor()

        curs.execute("CREATE TABLE IF NOT EXISTS mmsi_of_interest \
                     (id INTEGER PRIMARY KEY AUTOINCREMENT \
                     , mmsi INT)")
        
        curs.execute("CREATE TABLE IF NOT EXISTS area_of_interest\
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                     aoi_name TEXT, \
                     x1 FLOAT, \
                     y1 FLOAT, \
                     x2 FLOAT, \
                     y2 FLOAT, \
                     vessel_finder_zoom INTEGER)")

        curs.execute("CREATE TABLE IF NOT EXISTS TER_AIS_ship_data \
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                     mmsi INT, \
                     ship_name TEXT, \
                     callsign TEXT, \
                     AIS_transponer_class INT, \
                     country TEXT, \
                     ship_type TEXT, \
                     hull_length FLOAT, \
                     hull_width FLOAT, \
                     draught FLOAT, \
                     draught_max FLOAT, \
                     gross_tonnage INT, \
                     deadweight INT, \
                     imo INT, \
                     year_built INT)")
        
        curs.execute("CREATE TABLE IF NOT EXISTS TER_AIS_ship_geo_history \
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                     mmsi INT, \
                     ship_name TEXT, \
                     lat FLOAT, \
                     long FLOAT, \
                     timestamp UNIXEPOCH, \
                     navigational_status TEXT, \
                     speed FLOAT, \
                     coruse FLOAT, \
                     true_heading FLOAT, \
                     rate_of_turn FLOAT, \
                     next_port_dest TEXT, \
                     next_port_eta INTEGER, \
                     prev_port_dest TEXT, \
                     prev_port_eta INTEGER)")
        
        curs.execute("CREATE TABLE IF NOT EXISTS SAT_AIS_ship_geo_history \
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                     lat FLOAT, \
                     long FLOAT, \
                     timestamp UNIXEPOCH)")
        
        conn.commit()
        print("DB successfully created")
        
    except Exception as e:
        print("Error:", e)
