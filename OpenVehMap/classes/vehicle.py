from coords import *
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, _coords: Coords, _name: str):
        self._coords = _coords
        self._name = _name
    
    def getCoords(self):
        return self._coords

    def getName(self):
        return self._name
    
    @abstraactmethod
    def __str__(self):
        pass