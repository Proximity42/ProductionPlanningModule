from PySide6.QtCore import QThread, Signal

from diagrams import DiagramCreator


class BIDialogLoadingThread(QThread):
    finished = Signal()

    def __init__(self, planning_matrix, machines, details):
        super().__init__()

        self.planning_matrix = planning_matrix
        self.machines = machines
        self.details = details

    def run(self):
        DiagramCreator.create_bi_diagrams(
            self.planning_matrix, self.machines, self.details
        )
        self.finished.emit()
