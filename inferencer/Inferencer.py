from abc import ABC, abstractmethod

class Inferencer(ABC):

    @abstractmethod
    def runInferencer(self,ruta):
        pass