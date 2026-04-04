from PySide6.QtWidgets import QTextEdit

from utils.SettingsConfigManager import SettingsConfigManager

class CapSolverApiKeyTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setPlaceholderText('CapSolver API Key')

        self.setText(SettingsConfigManager.getCapSolverApiKey())