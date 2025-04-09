from collections import defaultdict
from copy import deepcopy

from planning_methods.base import StrategyRegistry, BasePlanningMethod
from planning_methods.first_johnson import FirstGeneralizationOfJohnson
from planning_methods.fourth_johnson import FourthGeneralizationOfJohnson
from planning_methods.second_johnson import SecondGeneralizationOfJohnson
from planning_methods.third_johnson import ThirdGeneralizationOfJohnson


@StrategyRegistry.register()
class FifthGeneralizationOfJohnson(BasePlanningMethod):
    NAME = "Пятое обобщение Джонсона"

    @staticmethod
    def sorted_matrix(matrix: list[list[float]], machines: int, details: int) -> list[list[float | int]]:
        first_generalization_result = (
            FirstGeneralizationOfJohnson.sorted_matrix(
                matrix, machines, details
            )
        )
        second_generalization_result = (
            SecondGeneralizationOfJohnson.sorted_matrix(
                matrix, machines, details
            )
        )
        third_generalization_result = (
            ThirdGeneralizationOfJohnson.sorted_matrix(
                matrix, machines, details
            )
        )
        fourth_generalization_result = (
            FourthGeneralizationOfJohnson.sorted_matrix(
                matrix, machines, details
            )
        )
        matrix = deepcopy(matrix)
        details_positions: defaultdict = defaultdict(int)
        for index, detail in enumerate(first_generalization_result):
            details_positions[detail[-2]] += index + 1
        for index, detail in enumerate(second_generalization_result):
            details_positions[detail[-2]] += index + 1
        for index, detail in enumerate(third_generalization_result):
            details_positions[detail[-2]] += index + 1
        for index, detail in enumerate(fourth_generalization_result):
            details_positions[detail[-2]] += index + 1
        for index, detail in enumerate(matrix):
            detail[-1] = details_positions[index + 1]
        return sorted(matrix, key=lambda det: det[-1])


