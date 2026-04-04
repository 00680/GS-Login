from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class ProcessesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        lbl = QLabel("Processes")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(lbl)
