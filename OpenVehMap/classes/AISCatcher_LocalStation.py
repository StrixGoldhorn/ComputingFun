from .geoShipSource import geoShipSource
from database import ShipDBActions, AudtiDBActions, DataSourceDBActions
import socket
import select
from pyais import decode
import time

class AISCatcher_LocalStation(geoShipSource):
    DATASOURCE_ID = 99
    LISTENER_UP = False

    # Default AISCatcher port to listen to, can add more if required.
    # Run this in your AISCatcher folder: .\start.bat -u 127.0.0.1 10110 -u 127.0.0.1 10111
    ports = [10110]
    sockets = []

    @staticmethod
    def LocalStationFactory():
        '''
        Factory method for AISCatcher_LocalStation

        Creates new listener
        Expects NMEA messages in byte string
        Will start adding to DB once any data is received
        '''
        AISCatcher_LocalStation.startListener()
        AISCatcher_LocalStation.scanAndSaveAreaToDB()

    @staticmethod
    def startListener():
        def saveShipToDB(message: str):
            decoded_msg = decode(message)
            dict_msg = decoded_msg.asdict()

            lat = dict_msg.get("lat", -1000.0)
            long = dict_msg.get("lon", -1000.0)
            timestamp = int(time.time())
            mmsi = dict_msg.get("mmsi", 0)
            shipname = "NIL" # Unsupported on Type 1/2/3 position messages
            country = "NIL" # Unsupported on Type 1/2/3 position messages (unless derive from first 3 digits of MMSI)
            shiptype = "NIL" # Unsupported on Type 1/2/3 position messages
            speed = dict_msg.get("speed", -1000.0)
            course = dict_msg.get("course", -1000.0)
            trueheading = dict_msg.get("heading", -1000.0)
            rateofturn = dict_msg.get("turn", -1000.0)


            try:
                ShipDBActions.addGeoShipLog(lat, long, timestamp, mmsi, shipname, country, shiptype, speed, course, trueheading, rateofturn, AISCatcher_LocalStation.DATASOURCE_ID)
            except Exception as e:
                print(f"ERROR - AISCatcher_LocalStation - startListener - saveShipToDB, Unable to save to DB: {e}")
                AudtiDBActions.writeToAuditDB("error", "AISCatcher_LocalStation - startListener - saveShipToDB", f"Unable to save to DB, message {message}")

        # If already listening, don't start another one.
        if AISCatcher_LocalStation.LISTENER_UP:
            pass

        else:
            for port in AISCatcher_LocalStation.ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind(("127.0.0.1", port))
                AISCatcher_LocalStation.sockets.append(sock)
                print(f"AISCatcher_LocalStation: Listening on UDP port {port}...")

            while True:
                readable, _, _ = select.select(AISCatcher_LocalStation.sockets, [], [])

                for sock in readable:
                    data, addr = sock.recvfrom(4096)
                    message = data.decode(errors="ignore")
                    port = sock.getsockname()[1]
                    print(f"AISCatcher_LocalStation: Message received - {message}")
                    saveShipToDB(message)
        

    @staticmethod
    def addToDatasource():
        DataSourceDBActions.addDataSourceToDataSourceDB("AISCatcher_LocalStation")

    @staticmethod
    def scanAndSaveAreaToDB():
        # Will just output whichever vessels it manages to pickup, unable to selectively scan areas
        AISCatcher_LocalStation.startListener()
        pass

    @staticmethod
    def scanAndSaveShipToDB():
        # Unable to selectiely scan ship.
        pass