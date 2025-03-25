import datetime
import os
import random

import xlrd
import xlwt


class FileHandler:

    @staticmethod
    def generate_xls_file(rows: int, cols: int) -> None:
        work_book = xlwt.Workbook()
        sheet = work_book.add_sheet("A test data")
        for row_index in range(rows):
            for col_index in range(cols):
                sheet.write(
                    row_index, col_index, round(random.random() * 20 % 20, 1)
                )
        work_book.save(
            "data["
            + str(rows)
            + "]["
            + str(cols)
            + "] "
            + datetime.datetime.now().strftime("%d.%m.%y")
            + ".xls"
        )

    @staticmethod
    def read_xls_file(file_name: str) -> tuple[list[list[float]], int, int]:
        source_matrix = []
        file = xlrd.open_workbook(file_name)
        sheet = file.sheet_by_index(0)

        for col_index in range(sheet.ncols):
            col = []
            for row_index in range(sheet.nrows):
                col.append(sheet.cell(row_index, col_index).value)
            source_matrix.append(col)
        return source_matrix, sheet.nrows, sheet.ncols

    @staticmethod
    def delete_file(file: str) -> None:
        if os.path.exists(file):
            os.remove(file)
