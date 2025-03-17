import math

from db.data import k_CONST, R_CONST


class Gas:

    def __init__(self, name: str, volume: float, temperature: float, pressure: float):
        self.name = name
        self.volume = volume
        self.temperature = temperature
        self.pressure = pressure

    def mol(self):
        return (self.pressure * self.volume) / (self.temperature * R_CONST)

    def __str__(self):
        return f"Gas {self.name}:\n\tvolume: {self.volume} m^\n\ttemperature: {self.temperature} K\n\tpressure: {self.pressure} Pa"

class GasMix:

    def __init__(self, gases: list[Gas]):
        self.gases = gases

    def entropy(self):
        full_volume = sum([gas.volume for gas in self.gases])
        return -1 * sum([gas.mol() for gas in self.gases]) * R_CONST * sum(
            [(gas.volume / full_volume) * math.log(gas.volume / full_volume) for gas in self.gases])