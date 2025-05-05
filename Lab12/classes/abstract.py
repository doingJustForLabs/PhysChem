from abc import ABC, abstractmethod


class Enthalpy(ABC):

    @abstractmethod
    def get_enthalpy(self, temperature: int):
        pass


class Entropy(ABC):

    @abstractmethod
    def get_entropy(self, temperature: int):
        pass


class HeatCapacity(ABC):

    @abstractmethod
    def get_heat_capacity(self, temperature: int):
        pass
