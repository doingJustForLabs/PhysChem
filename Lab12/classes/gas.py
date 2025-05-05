from math import log

R = 8.314


class Gas:
    def __init__(self, substance: str, volume: int, pressure: int, temperature: int):
        self._substance = substance
        self._volume = volume * 1e-4
        self._pressure = pressure
        self._temperature = temperature
        self._moles = (self._pressure * self._volume) / (R * self._temperature)

    @property
    def get_volume(self):
        return self._volume

    @property
    def get_moles(self):
        return self._moles


class GasMixing:

    def __init__(self, gas1: Gas, gas2: Gas):
        self._gas1 = gas1
        self._gas2 = gas2

    def find_delta_entropy(self) -> float:
        s1 = (
            self._gas1.get_moles
            * R
            * log(
                (self._gas1.get_volume + self._gas2.get_volume) / self._gas1.get_volume
            )
        )
        s2 = (
            self._gas2.get_moles
            * R
            * log(
                (self._gas1.get_volume + self._gas2.get_volume) / self._gas2.get_volume
            )
        )
        return s1 + s2
