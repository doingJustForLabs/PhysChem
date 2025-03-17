from math import log
from enum import Enum


from db.data import R_CONST
from classes.substance import Substance


class Role(Enum):
    REACTANT = -1
    PRODUCT = 1

class ReactionComponent(Substance):
    def __init__(self, substance: str, role: Role = Role.REACTANT):
        super().__init__(substance)
        self._role = role

    def engineer_enthalpy(self, temperature: float):
        coefficients = self.nasa_7()
        try:
            enthalpy = coefficients[0] + coefficients[5] / temperature
            for i in range(1, 5):
                enthalpy += (coefficients[i] / (i + 1)) * (temperature ** i)
            return enthalpy * self._role.value * self._coefficient * temperature * R_CONST
        except ZeroDivisionError:
            print("Division by zero.")

    def entropy(self, temperature: float):
        coefficients = self.nasa_7()
        try:
            entropy = coefficients[0]*log(temperature) + coefficients[6]
            for i in range(1, 5):
                entropy += (coefficients[i] / i) * (temperature ** i)
            return entropy * self._coefficient * self._role.value * R_CONST
        except ZeroDivisionError:
            print("Division by zero.")

    def get_role(self):
        return self._role

