from vehicle import *
from coords import *
import random
import string

class Ship(Vehicle):
    def __init__(self, _coords: Coords, _name: str, _timestamp: int):
        super(_coords, _name)
        self._timestamp = _timestamp
    
    def getTimestamp(self) -> int:
        return self._timestamp
    
    def getClosestToPort(self):
        return "PORTNAME_HERE"
    
    @abstractmethod
    def __str__(self):
        pass
    
class GeoShip(Ship):
    def __init__(self, _coords: Coords, _name: str, _timestamp: int,
                 _mmsi: int, _shipname: str, _country: str, _shiptype: str):
        super(_coords, _name, _timestamp)
        self._mmsi = _mmsi
        self._shipname = _shipname
        self._country = _country
        self._shiptype = _shiptype
        self._coords_history = [_coords]

    def getMMSI(self) -> int:
        return self._mmsi
    
    def getShipname(self) -> str:
        return self._shipname
    
    def getCountry(self) -> str:
        return self._country
    
    def getShiptype(self) -> str:
        return self._shiptype

    def getShipHistory(self) -> list[Coords]:
        return self._coords_history
    
    def __str__(self) -> str:
        return f"Ship (Ownself AIS): {self._shipname} | {self._coords}"
    
class SatShip(Ship):
    # Static field
    RANDOM_NAME_LENGTH = 10

    def __init__(self, _coords: Coords, _timestamp: int):
        # Helper method
        def randomName(length: int) -> str:
            return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
        _name = randomName(SatShip.RANDOM_NAME_LENGTH)
        super(_coords, _name, _timestamp)

    def __str__(self) -> str:
        return f"Ship (Sat AIS): {self._coords}"