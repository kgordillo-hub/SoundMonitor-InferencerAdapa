from abc import ABC, abstractmethod

class Inferenciador(ABC):

    @abstractmethod
    def runInferencer(self,ruta):
        pass