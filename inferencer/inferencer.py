from abc import ABC, abstractmethod


class Inferencer(ABC):

    @abstractmethod
    def run_inferencer(self, ruta):
        pass
