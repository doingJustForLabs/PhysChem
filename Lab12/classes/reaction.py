from .abstract import Enthalpy, Entropy
from .substance import Substance


class Reaction(Enthalpy, Entropy):
    R = 8.314

    def __init__(self, reaction: str):
        super().__init__()
        self._reaction = reaction
        self._reagents, self._products = self.divide_reaction_by_reagents_and_products()
        self.R = 8.314

    def __str__(self):
        return self._reaction

    def divide_reaction_by_reagents_and_products(
        self,
    ) -> (list[Substance], list[Substance]):
        reagents, products = self._reaction.split("=>")
        reagents = [i.strip() for i in reagents.split("+")]
        products = [i.strip() for i in products.split("+")]
        return reagents, products

    def get_enthalpy(self, temperature: float, heat: bool = False) -> float:
        res = 0

        for substance in self._reagents:
            substance_enthalpy = Substance(substance).get_enthalpy(temperature)
            res -= substance_enthalpy

        for substance in self._products:
            substance_enthalpy = Substance(substance).get_enthalpy(temperature)
            res += substance_enthalpy
        return res

    def get_entropy(self, temperature: float) -> float:
        res = 0

        for substance in self._reagents:
            substance_enthalpy = Substance(substance).get_entropy(temperature)
            res -= substance_enthalpy

        for substance in self._products:
            substance_enthalpy = Substance(substance).get_entropy(temperature)
            res += substance_enthalpy
        return res

    def get_gibbs_free_energy(self, temperature: float) -> float:
        return self.get_enthalpy(temperature) - temperature * self.get_entropy(
            temperature
        )

    @property
    def get_reagents(self) -> list[str]:
        return self._reagents

    @property
    def get_products(self) -> list[str]:
        return self._products
