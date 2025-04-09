from copy import deepcopy

from planning_methods.base import StrategyRegistry, BasePlanningMethod


@StrategyRegistry.register()
class FirstPetrovSokolitsin(BasePlanningMethod):
    NAME = "Первый метод суммы Петрова-Соколицына"

    @staticmethod
    def sorted_matrix(matrix: list[list[float]], machines: int, details: int) -> list[list[float | int]]:
        matrix = deepcopy(matrix)
        for detail in matrix:
            detail[-1] = sum(detail[:-3])
        return sorted(matrix, key=lambda det: det[-1], reverse=True)

