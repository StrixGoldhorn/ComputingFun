import time
from database import *
import classes.VesselFinderScraper
import threading

class ScraperMain:
    @staticmethod
    def VesselFinderScrapeAllAois():
        while True:
            aois = AoiDBActions.getAllAoi()
            for aoi in aois:
                coords = [aoi[1], aoi[2], aoi[3], aoi[4]]
                print(f"Scanning - {aoi[0]}")
                classes.VesselFinderScraper.VesselFinderScraper.scanAndSaveAreaToDB(coords, 15)
                time.sleep(60)
            print("Sleeping AOI scan for 600s")
            time.sleep(600)

    @staticmethod
    def VesselFinderScrapeAllMMSI():
        while True:
            mmsis = ShipDBActions.getAllmmsiOfInterest()
            for mmsi in mmsis:
                print(f"Scanning - {mmsi[0]}")
                classes.VesselFinderScraper.VesselFinderScraper.scanAndSaveShipToDB(mmsi[0])
                time.sleep(10)
            print("Sleeping MMSI of Interest scan for 60s")
            time.sleep(60)

    @staticmethod
    def main():
        print("RUNNING")
        threads = []

        VFAoiThread = threading.Thread(target=ScraperMain.VesselFinderScrapeAllAois)
        VFmmsiThread = threading.Thread(target=ScraperMain.VesselFinderScrapeAllMMSI)
        
        threads.append(VFAoiThread)
        threads.append(VFmmsiThread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()