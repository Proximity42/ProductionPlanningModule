from copy import deepcopy

from planning_methods.base import StrategyRegistry, BasePlanningMethod


@StrategyRegistry.register()
class ThirdGeneralizationOfJohnson(BasePlanningMethod):
    NAME = "Третье обобщение Джонсона"

    @staticmethod
    def sorted_matrix(matrix: list[list[float]], machines: int, details: int) -> list[list[float | int]]:
        matrix = deepcopy(matrix)
        current_detail = 0
        while current_detail < details:
            max_time = 0
            detail_index_of_max_time = 0
            for machine_index in range(machines):
                for detail_index in range(current_detail, details):
                    if matrix[detail_index][machine_index] >= max_time:
                        max_time = matrix[detail_index][machine_index]
                        detail_index_of_max_time = detail_index
            (
                matrix[current_detail],
                matrix[detail_index_of_max_time],
            ) = (
                matrix[detail_index_of_max_time],
                matrix[current_detail],
            )
            current_detail += 1
        return matrix


