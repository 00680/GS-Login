from PySide6.QtWidgets import QComboBox

from constants.servers import SERVERS
from utils.SettingsConfigManager import SettingsConfigManager

class ServerComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        for key, name in SERVERS.items():
            self.addItem(name, key)
