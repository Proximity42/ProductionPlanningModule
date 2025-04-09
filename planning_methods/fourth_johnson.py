from copy import deepcopy

from planning_methods.base import StrategyRegistry, BasePlanningMethod


@StrategyRegistry.register()
class FourthGeneralizationOfJohnson(BasePlanningMethod):
    NAME = "Четвертое обобщение Джонсона"

    @staticmethod
    def sorted_matrix(matrix: list[list[float]], machines: int, details: int) -> list[list[float | int]]:
        matrix = deepcopy(matrix)
        for column in matrix:
            column[-1] = sum(column[:machines])
        return sorted(matrix, key=lambda col: col[-1], reverse=True)


