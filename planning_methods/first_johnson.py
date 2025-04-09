from copy import deepcopy
from planning_methods.base import BasePlanningMethod, StrategyRegistry


@StrategyRegistry.register()
class FirstGeneralizationOfJohnson(BasePlanningMethod):
    NAME = "Первое обобщение Джонсона"

    @staticmethod
    def sorted_matrix(matrix: list[list[float]], machines: int, details: int) -> list[list[float | int]]:
        matrix = deepcopy(matrix)
        return sorted(matrix, key=lambda det: det[0])
