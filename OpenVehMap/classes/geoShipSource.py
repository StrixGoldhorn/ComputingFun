from abc import ABC, abstractmethod

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