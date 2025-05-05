from .abstract import Enthalpy, Entropy, HeatCapacity
from .nasa import nasa_db
from math import log


class Substance(Enthalpy, Entropy, HeatCapacity):

    def __init__(self, substance: str):
        super().__init__()
        self._substance = substance
        self.R = 8.314

    def find_substance_coefficient(self) -> list[int | str]:
        if self._substance in nasa_db.get_NASA():
            return [1, self._substance]
        else:
            prod = ""
            point = 0
            for let in self._substance:
                if let not in "0123456789":
                    break
                prod += let
                point += 1
            return [int(prod), self._substance[point:]]

    def get_enthalpy(self, temperature: int) -> float:
        res = 0
        substance_coefficient, cur_substance = self.find_substance_coefficient()
        coefficients = nasa_db.get_NASA()[cur_substance]

        for idx in range(len(coefficients) - 2):
            res += (coefficients[idx] * temperature**idx) / (idx + 1)
        res += coefficients[-2] / temperature
        return (substance_coefficient * res) * (self.R * temperature)

    def get_heat_capacity(self, temperature: int) -> float:
        res = 0
        substance_coefficient, cur_substance = self.find_substance_coefficient()
        coefficients = nasa_db.get_NASA()[cur_substance]

        for idx in range(len(coefficients) - 2):
            res += coefficients[idx] * temperature**idx
        return (substance_coefficient * res) * self.R

    def get_entropy(self, temperature: int) -> float:
        res = 0
        substance_coefficient, cur_substance = self.find_substance_coefficient()
        coefficients = nasa_db.get_NASA()[cur_substance]

        res += coefficients[0] * log(temperature)

        for idx in range(1, len(coefficients) - 2):
            res += (coefficients[idx] * temperature**idx) / idx
        res += coefficients[-1]

        return (substance_coefficient * res) * self.R

    def __str__(self):
        return self._substance
