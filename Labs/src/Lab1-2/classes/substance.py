from math import log
from re import findall, sub

from classes.si_prefix import metrics
from db.data import NASA, R_CONST

class Substance:

    def __init__(self, substance: str):
        if substance[0].isdigit():
            coefficient = findall(r"\d+", substance)[0]
            self._substance = substance.replace(coefficient, '', 1)
            self._coefficient = int(coefficient)
        else:
            self._substance = substance
            self._coefficient = 1


    def __str__(self):
        return str(self._coefficient) + self._substance

    def nasa_7(self, index: int = None) -> list[float]:
        try:
            nasa_coefficients = NASA[self._substance]
            return nasa_coefficients if not index else nasa_coefficients[index]
        except KeyError:
            print(f"There is no {self._substance} data in NASA.")

    @metrics
    def entropy(self, temperature: float):
        coefficients = self.nasa_7()
        try:
            entropy = coefficients[0]*log(temperature) + coefficients[6]
            for i in range(1, 5):
                entropy += (coefficients[i] / i) * (temperature ** i)
            return entropy * self._coefficient * R_CONST
        except ZeroDivisionError:
            print("Division by zero.")

    @metrics
    def capacity_p(self, temperature: float):
        coefficients = self.nasa_7()
        entropy = coefficients[0]
        for i in range(1, 5):
            entropy += coefficients[i] * (temperature ** i)
        return entropy * self._coefficient * R_CONST

    def get_substance(self):
        return self._substance

    def get_coefficient(self):
        return self._coefficient
