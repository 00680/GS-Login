from PySide6.QtWidgets import QComboBox

from constants.languages import LANGUAGES
from utils.SettingsConfigManager import SettingsConfigManager

class LanguageComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        for key, name in LANGUAGES.items():
            self.addItem(name, key)

        currentLanguage = SettingsConfigManager.getLanguage()
        
        for i in range(self.count()):
            if self.itemData(i) == currentLanguage:
                self.setCurrentIndex(i)
                break