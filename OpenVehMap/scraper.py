import time
from database import *
import classes.VesselFinderScraper, classes.AISFriendsScraper, classes.MyShipTrackingScraper
import threading
import random

class ScraperMain:
    @staticmethod
    def VesselFinderScrapeAllAois():
        while True:
            aois = AoiDBActions.getAllAoi()
            random.shuffle(aois)
            for aoi in aois:
                coords = [aoi[1], aoi[2], aoi[3], aoi[4]]
                print(f"Scanning VesselFinderScraper - AOI - {aoi[0]}")
                classes.VesselFinderScraper.VesselFinderScraper.scanAndSaveAreaToDB(coords, 15)
                time.sleep(120)
            print("Sleeping VesselFinderScraper AOI scan for 600s")
            time.sleep(600)

    @staticmethod
    def VesselFinderScrapeAllMMSI():
        while True:
            mmsis = ShipDBActions.getAllmmsiOfInterest()
            random.shuffle(mmsis)
            for mmsi in mmsis:
                print(f"Scanning VesselFinderScraper - MMSI - {mmsi[0]}")
                classes.VesselFinderScraper.VesselFinderScraper.scanAndSaveShipToDB(mmsi[0])
                time.sleep(60)
            print("Sleeping VesselFinderScraper MMSI of Interest scan for 60s")
            time.sleep(120)
            
    @staticmethod
    def AISFriendsScrapeAllAois():
        while True:
            aois = AoiDBActions.getAllAoi()
            random.shuffle(aois)
            for aoi in aois:
                coords = [aoi[1], aoi[2], aoi[3], aoi[4]]
                print(f"Scanning AISFriendsScraper - AOI - {aoi[0]}")
                classes.AISFriendsScraper.AISFriendsScraper.scanAndSaveAreaToDB(coords, 15)
                time.sleep(60)
            print("Sleeping AISFriendsScraper AOI scan for 60s")
            time.sleep(60)
            
    @staticmethod
    def AISFriendsScrapeAllMMSI():
        while True:
            mmsis = ShipDBActions.getAllmmsiOfInterest()
            random.shuffle(mmsis)
            for mmsi in mmsis:
                print(f"Scanning AISFriendsScraper - MMSI - {mmsi[0]}")
                classes.AISFriendsScraper.AISFriendsScraper.scanAndSaveShipToDB(mmsi[0])
                time.sleep(60)
            print("Sleeping AISFriendsScraper MMSI of Interest scan for 60s")
            time.sleep(120)
            
    @staticmethod
    def MyShipTrackingScrapeAllAois():
        while True:
            aois = AoiDBActions.getAllAoi()
            random.shuffle(aois)
            for aoi in aois:
                coords = [aoi[1], aoi[2], aoi[3], aoi[4]]
                print(f"Scanning MyShipTrackingScraper - AOI - {aoi[0]}")
                classes.MyShipTrackingScraper.MyShipTrackingScraper.scanAndSaveAreaToDB(coords)
                time.sleep(60)
            print("Sleeping MyShipTrackingScraper AOI scan for 60s")
            time.sleep(60)
            
            

    @staticmethod
    def main():
        print("Scraper RUNNING")
        threads = []

        VFAoiThread = threading.Thread(target=ScraperMain.VesselFinderScrapeAllAois)
        VFmmsiThread = threading.Thread(target=ScraperMain.VesselFinderScrapeAllMMSI)
        threads.append(VFAoiThread)
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