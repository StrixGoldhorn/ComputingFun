# Open Vehicle Map

## DISCLAIMER
UI/UX was designed and implemented with the help of LLM (Qwen).

The rest of the code (backend) was done by yours truly.

## Description
Designed to be a modular dashboard, where users can easily add info from **multiple data sources**, supplying location of various assets.

![overview](./showcase_assets/overview.png)

Currently, as a proof of concept, **3** data sources are being used.

- [VesselFinder](https://www.vesselfinder.com/)
- [AISFriends](https://www.aisfriends.com/)
- [MyShipTracking](https://www.myshiptracking.com/)

Users are able to add vehicle IDs of interest to specifically track them.

Users are able to add Area Of Interests (AOIs) to track geographical regions.

Users are able to view all ships, and filter based on country, ship name, ship type, and MMSI

![homepage](./showcase_assets/homepage.png)

![mmsiofinterest](./showcase_assets/mmsiofinterest.png)

![allships](./showcase_assets/allships.png)

## How to use
`python -m main.py`

Then, go to `http://127.0.0.1:5000/` (yes, you host the site locally)

Add AOIs to the AOI db, the site will scan them regularly.

## To add sources
To add sources for maritime traffic, make them a subclass of `geoShipSource` and ensure they override the following abstract functions
You MUST change the `DATASOURCE_ID` and add it to `datasource.db`.

```py
class geoShipSource(ABC):    
    DATASOURCE_ID = -1

    @staticmethod
    @abstractmethod
    def addToDatasource():
        pass

    @staticmethod
    @abstractmethod
    def scanAndSaveAreaToDB():
        pass

    @staticmethod
    @abstractmethod
    def scanAndSaveShipToDB():
        pass
```

Also add a function to run your scraper in `scraper.py`

## To edit more stuff

Below is the DB structure

![dbstructure](./showcase_assets/dbstructure.png)