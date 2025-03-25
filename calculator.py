class ProcessingTimeCalculator:

    @staticmethod
    def build_planning_matrix(
        source_matrix: list[list[float | int]], machines: int, details: int
    ) -> list[list[float | int]]:
        planning_matrix = [
            [0.0 for _ in range(machines)] for _ in range(details)
        ]
        planning_matrix[0][0] = source_matrix[0][0]
        # Заполнение первого столбца матрицы
        for machine_index in range(1, machines):
            planning_matrix[0][machine_index] = (
                planning_matrix[0][machine_index - 1]
                + source_matrix[0][machine_index]
            )
        # Заполнение первой строки матрицы
        for detail_index in range(1, details):
            planning_matrix[detail_index][0] = (
                planning_matrix[detail_index - 1][0]
                + source_matrix[detail_index][0]
            )
        # Заполнение остальных ячеек матрицы
        for detail_index in range(1, details):
            for machine_index in range(1, machines):
                planning_matrix[detail_index][machine_index] = round(
                    max(
                        planning_matrix[detail_index - 1][machine_index],
                        planning_matrix[detail_index][machine_index - 1],
                    )
                    + source_matrix[detail_index][machine_index],
                    2,
                )
        return planning_matrix
