from collections import defaultdict
from copy import deepcopy


class PlanningAlgorithms:

    @staticmethod
    def create_extended_matrix(
        matrix: list[list[float]],
    ) -> list[list[float | int]]:
        extended_matrix = deepcopy(matrix)
        for index, col in enumerate(extended_matrix):
            col.append(index + 1)
            col.append(0)
        return extended_matrix

    @staticmethod
    def first_generalization_of_johnson(
        matrix: list[list[float]], machines: int, details: int
    ) -> list[list[float | int]]:
        matrix = deepcopy(matrix)
        return sorted(matrix, key=lambda det: det[0])

    @staticmethod
    def second_generalization_of_johnson(
        matrix: list[list[float]], machines: int, details: int
    ) -> list[list[float | int]]:
        matrix = deepcopy(matrix)
        return sorted(matrix, key=lambda det: det[-3], reverse=True)

    @staticmethod
    def third_generalization_of_johnson(
        matrix: list[list[float]], machines: int, details: int
    ) -> list[list[float | int]]:
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

    @staticmethod
    def fourth_generalization_of_johnson(
        matrix: list[list[float]], machines: int, details: int
    ) -> list[list[float | int]]:
        matrix = deepcopy(matrix)
        for column in matrix:
            column[-1] = sum(column[:machines])
        return sorted(matrix, key=lambda col: col[-1], reverse=True)

    @staticmethod
    def fifth_generalization_of_johnson(
        matrix: list[list[float]], machines: int, details: int
    ) -> list[list[float | int]]:
        first_generalization_result = (
            PlanningAlgorithms.first_generalization_of_johnson(
                matrix, machines, details
            )
        )
        second_generalization_result = (
            PlanningAlgorithms.second_generalization_of_johnson(
                matrix, machines, details
            )
        )
        third_generalization_result = (
            PlanningAlgorithms.third_generalization_of_johnson(
                matrix, machines, details
            )
        )
        fourth_generalization_result = (
            PlanningAlgorithms.fourth_generalization_of_johnson(
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

    @staticmethod
    def first_petrov_sokolitsin(
        matrix: list[list[float]], machines: int, details: int
    ) -> list[list[float | int]]:
        matrix = deepcopy(matrix)
        for detail in matrix:
            detail[-1] = sum(detail[:-3])
        return sorted(matrix, key=lambda det: det[-1], reverse=True)

    @staticmethod
    def second_petrov_sokolitsin(
        matrix: list[list[float]], machines: int, details: int
    ) -> list[list[float | int]]:
        matrix = deepcopy(matrix)
        for detail in matrix:
            detail[-1] = sum(detail[1:-2])
        return sorted(matrix, key=lambda det: det[-1], reverse=True)

    @staticmethod
    def third_petrov_sokolitsin(
        matrix: list[list[float]], machines: int, details: int
    ) -> list[list[float | int]]:
        matrix = deepcopy(matrix)
        for detail in matrix:
            detail[-1] = detail[-3] - detail[0]
        return sorted(matrix, key=lambda det: det[-1], reverse=True)

    PLANNING_ALGORITHMS = {
        "Первое обобщение Джонсона": first_generalization_of_johnson,
        "Второе обобщение Джонсона": second_generalization_of_johnson,
        "Третье обобщение Джонсона": third_generalization_of_johnson,
        "Четвертое обобщение Джонсона": fourth_generalization_of_johnson,
        "Пятое обобщение Джонсона": fifth_generalization_of_johnson,
        "Первый метод суммы Петрова-Соколицина": first_petrov_sokolitsin,
        "Второй метод суммы Петрова-Соколицина": second_petrov_sokolitsin,
        "Метод разности Петрова-Соколицина": third_petrov_sokolitsin,
    }
