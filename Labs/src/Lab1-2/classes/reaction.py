from classes.reaction_component import ReactionComponent, Role
from classes.si_prefix import metrics


class Reaction:
    def __init__(self, reaction: str):
        reaction = reaction.replace(' ', '')
        left, right = reaction.split("=>")
        agents = list([ReactionComponent(component, role=Role.REACTANT) for component in left.split('+')])
        products = list([ReactionComponent(component, role=Role.PRODUCT) for component in right.split('+')])
        self._reactants, self._products = agents, products
        self._components = self._reactants + self._products

    def __str__(self):
        return " + ".join([str(reactant) for reactant in self._reactants]) + " => " + " + ".join(
            [str(product) for product in self._products])

    def __contains__(self, item: str):
        return item in self.get_components(show_coefficients=False)

    def count(self, substance: str) -> int | dict:
        coefficients = {Role.REACTANT: 0, Role.PRODUCT: 0}
        for component in self._components:
            if substance == component.get_substance():
                coefficients[component.get_role()] += component.get_coefficient()
        return coefficients

    def get_components(self, string_like: bool = True, show_coefficients: bool = False):
        if string_like:
            if show_coefficients: return list([str(component) for component in self._components])
            return list([str(component.get_substance()) for component in self._components])
        return self._components

    def get_reactants(self, string_like: bool = True, show_coefficients: bool = False):
        if string_like:
            if show_coefficients: return list([str(agent) for agent in self._reactants])
            return list([str(agent.get_substance()) for agent in self._reactants])
        return self._reactants

    def get_products(self, string_like: bool = True, show_coefficients: bool = False):
        if string_like:
            if show_coefficients: return list([str(product) for product in self._products])
            return list([str(product.get_substance()) for product in self._products])
        return self._products

    @metrics
    def enthalpy(self, temperature: float) -> float:
        return sum([_.engineer_enthalpy(temperature) for _ in self._components])

    @metrics
    def entropy(self, temperature: float) -> float:
        return sum([_.entropy(temperature) for _ in self._components])

    @metrics
    def gfe(self, temperature: float) -> float:
        return self.enthalpy(temperature) - temperature * self.entropy(temperature)
