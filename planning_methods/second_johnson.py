from copy import deepcopy

from planning_methods.base import StrategyRegistry, BasePlanningMethod


@StrategyRegistry.register()
class SecondGeneralizationOfJohnson(BasePlanningMethod):
    NAME = "Второе обобщение Джонсона"

    @staticmethod
    def sorted_matrix(matrix: list[list[float]], machines: int, details: int) -> list[list[float | int]]:
        matrix = deepcopy(matrix)
        return sorted(matrix, key=lambda det: det[-3], reverse=True)
