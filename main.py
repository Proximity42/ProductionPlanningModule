import atexit
import copy
import sys
import random

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog

from calculator import ProcessingTimeCalculator
from diagrams import DiagramCreator
from file_handler import FileHandler
from main_form import Ui_MainWindow
from bi_form import Ui_Dialog
from algorithms import PlanningAlgorithms
from threads import BIDialogLoadingThread


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Модуль планирования")
        self.source_matrix = []
        self.machines = 0
        self.details = 0
        self.result_matrix = []
        self.planning_matrix = []
        self.bi_form = None

        self.methods_combo_box.addItems(
            (
                method_name
                for method_name in PlanningAlgorithms.PLANNING_ALGORITHMS
            )
        )

        self.menu.actions()[0].triggered.connect(self.read_xls_file)
        self.menu.actions()[1].triggered.connect(self.generate_xls_file)
        self.menuBI.actions()[0].triggered.connect(self.show_bi_dialog)
        self.evaluate_result_button.clicked.connect(
            self.calculate_processing_time
        )

        atexit.register(self.delete_diagram_files)

    def read_xls_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            ".",
            "Файлы Excel (*.xls)",
        )
        if not file_name:
            self.status_bar.showMessage("Ошибка! Вы не выбрали файл!", 5000)
            return
        try:
            matrix, rows, cols = FileHandler.read_xls_file(file_name)
            self.machines = rows
            self.details = cols
            self.source_matrix = copy.deepcopy(matrix)
            self.label_number_machines.setText(str(rows))
            self.label_number_details.setText(str(cols))
            self.status_bar.showMessage(
                "Данные из файла были успешно загружены!"
            )
        except TypeError(
            "Ошибка при чтении файла! Убедитесь, что данные в файле корректны."
        ) as e:
            self.status_bar.showMessage(e, 5000)

    def generate_xls_file(self):
        details = random.randint(3, 101)
        machines = random.randint(3, 101)
        FileHandler.generate_xls_file(machines, details)
        self.status_bar.showMessage("Файл был успешно сгенерирован")

    def calculate_processing_time(self):
        if not self.source_matrix:
            self.status_bar.showMessage(
                "Ошибка! Вы не загрузили данные!", 5000
            )
            return
        chosen_method = self.methods_combo_box.currentText()
        extended_matrix = PlanningAlgorithms.create_extended_matrix(
            self.source_matrix
        )
        self.result_matrix = PlanningAlgorithms.PLANNING_ALGORITHMS[
            chosen_method
        ](extended_matrix, self.machines, self.details)
        self.planning_matrix = ProcessingTimeCalculator.build_planning_matrix(
            self.result_matrix, self.machines, self.details
        )
        result_time = self.planning_matrix[-1][-1]
        self.result_text_browser.setText(
            f"""Общее время обработки (в часах): {result_time}
            \nОчередь обработки деталей: {" - ".join([str(col[-2]) 
                for col in self.result_matrix])}""",
        )
        DiagramCreator.create_gantt_diagram(
            self.result_matrix, self.machines, self.details
        )
        self.web_engine_view.setUrl("file:///gantt.html")
        self.status_bar.showMessage("Расчет выполнен успешно!", 10000)

    def show_bi_dialog(self):
        if len(self.result_matrix) == 0:
            self.status_bar.showMessage(
                "Ошибка! Вы ещё не выполнили расчет!", 5000
            )
            return
        self.bi_form = BIDialog(
            self.planning_matrix,
            self.machines,
            self.details,
        )
        self.bi_form.exec()

    @staticmethod
    def delete_diagram_files():
        FileHandler.delete_file("gantt.html")
        FileHandler.delete_file("workload.html")
        FileHandler.delete_file("downtime.html")

    def closeEvent(self, event: QCloseEvent):
        """Переопределяем closeEvent для удаления файла при закрытии окна."""
        self.delete_diagram_files()
        super().closeEvent(event)


class BIDialog(QDialog, Ui_Dialog):
    def __init__(self, planning_matrix, machines, details, parent=None):
        super().__init__()
        self.setupUi(self)
        loading_html = "<h2 style='text-align: center; line-height: 90vh'>Загрузка диаграммы ...</h2>"
        self.bi_web_engine_view_1.setHtml(loading_html)
        self.bi_web_engine_view_2.setHtml(loading_html)
        self.thread = BIDialogLoadingThread(planning_matrix, machines, details)
        self.thread.finished.connect(self.on_diagrams_built)
        self.thread.start()

    def on_diagrams_built(self):
        self.bi_web_engine_view_1.setUrl("file:///downtime.html")
        self.bi_web_engine_view_2.setUrl("file:///workload.html")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
