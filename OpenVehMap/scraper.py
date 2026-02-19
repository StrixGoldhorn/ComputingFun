import time
from database import *
import classes.VesselFinderScraper, classes.AISFriendsScraper, classes.MyShipTrackingScraper
import threading
import random

class ScraperMain:
    @staticmethod
    def VesselFinderScrapeAllAois():
        SLEEP_TIME = 600
        while True:
            aois = AoiDBActions.getAllAoi()
            random.shuffle(aois)
            for aoi in aois:
                coords = [aoi[1], aoi[2], aoi[3], aoi[4]]
                print(f"Scanning VesselFinderScraper - AOI - {aoi[0]}")
                classes.VesselFinderScraper.VesselFinderScraper.scanAndSaveAreaToDB(coords, 15)
                time.sleep(120 + random.randint(0,60))
            print(f"Sleeping VesselFinderScraper AOI scan for {SLEEP_TIME}s")
            time.sleep(SLEEP_TIME)

    @staticmethod
    def VesselFinderScrapeAllMMSI():
        SLEEP_TIME = 300
        while True:
            mmsis = ShipDBActions.getAllmmsiOfInterest()
            random.shuffle(mmsis)
            for mmsi in mmsis:
                print(f"Scanning VesselFinderScraper - MMSI - {mmsi[0]}")
                classes.VesselFinderScraper.VesselFinderScraper.scanAndSaveShipToDB(mmsi[0])
                time.sleep(180 + random.randint(0,20))
            print(f"Sleeping VesselFinderScraper MMSI of Interest scan for {SLEEP_TIME}s")
            time.sleep(SLEEP_TIME)
            
    @staticmethod
    def AISFriendsScrapeAllAois():
        SLEEP_TIME = 60
        while True:
            aois = AoiDBActions.getAllAoi()
            random.shuffle(aois)
            for aoi in aois:
                coords = [aoi[1], aoi[2], aoi[3], aoi[4]]
                print(f"Scanning AISFriendsScraper - AOI - {aoi[0]}")
                classes.AISFriendsScraper.AISFriendsScraper.scanAndSaveAreaToDB(coords, 15)
                time.sleep(0 + random.randint(0,20))
            print(f"Sleeping AISFriendsScraper AOI scan for {SLEEP_TIME}s")
            time.sleep(SLEEP_TIME)
            
    @staticmethod
    def AISFriendsScrapeAllMMSI():
        SLEEP_TIME = 120
        while True:
            mmsis = ShipDBActions.getAllmmsiOfInterest()
            random.shuffle(mmsis)
            for mmsi in mmsis:
                print(f"Scanning AISFriendsScraper - MMSI - {mmsi[0]}")
                classes.AISFriendsScraper.AISFriendsScraper.scanAndSaveShipToDB(mmsi[0])
                time.sleep(10 + random.randint(0,20))
            print(f"Sleeping AISFriendsScraper MMSI of Interest scan for {SLEEP_TIME}s")
            time.sleep(SLEEP_TIME)
            
    @staticmethod
    def MyShipTrackingScrapeAllAois():
        SLEEP_TIME = 60
        while True:
            aois = AoiDBActions.getAllAoi()
            random.shuffle(aois)
            for aoi in aois:
                coords = [aoi[1], aoi[2], aoi[3], aoi[4]]
                print(f"Scanning MyShipTrackingScraper - AOI - {aoi[0]}")
                classes.MyShipTrackingScraper.MyShipTrackingScraper.scanAndSaveAreaToDB(coords)
                time.sleep(0 + random.randint(0,30))
            print(f"Sleeping MyShipTrackingScraper AOI scan for {SLEEP_TIME}s")
            time.sleep(SLEEP_TIME)
            
            

    @staticmethod
    def main():
        print("Scraper RUNNING")
        threads = []

        VFAoiThread = threading.Thread(target=ScraperMain.VesselFinderScrapeAllAois)
        VFmmsiThread = threading.Thread(target=ScraperMain.VesselFinderScrapeAllMMSI)
        # threads.append(VFAoiThread)
        # threads.append(VFmmsiThread)
        
        classes.AISFriendsScraper.AISFriendsScraper.initOwnDB()
        AISFAoiThread = threading.Thread(target=ScraperMain.AISFriendsScrapeAllAois)
        AISFmmsiThread = threading.Thread(target=ScraperMain.AISFriendsScrapeAllMMSI)
        threads.append(AISFAoiThread)
        threads.append(AISFmmsiThread)
        
        MSTAoiThread = threading.Thread(target=ScraperMain.MyShipTrackingScrapeAllAois)
        threads.append(MSTAoiThread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()