from PySide6.QtWidgets import QFormLayout,QDialog


from MainWindow.SettingMenu.SettingDialog.LanguageComboBox.LanguageComboBox import LanguageComboBox
from MainWindow.SettingMenu.SettingDialog.CapSolverApiKeyTextEdit.CapSolverApiKeyTextEdit import CapSolverApiKeyTextEdit
from MainWindow.SettingMenu.SettingDialog.SettingDialogButton.SettingDialogButton import SettingDialogButton
from utils.Translator import Translator
from utils.SettingsConfigManager import SettingsConfigManager

class SettingsDialog(QDialog):
    languagesComboBox: LanguageComboBox
    capsolverKeyTextEdit: CapSolverApiKeyTextEdit
    dialogButtons: SettingDialogButton

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(Translator.translate('settingDialog.title'))

        self.setFixedSize(290, 220)
        
        layout = QFormLayout(self)

        self.languagesComboBox = LanguageComboBox(self)
        layout.addRow(f"{Translator.translate('settingDialog.languageLabel')}: ", self.languagesComboBox)

        self.capsolverKeyTextEdit = CapSolverApiKeyTextEdit(self)
        layout.addRow(f"{Translator.translate('settingDialog.capsolverKeyLabel')}: ", self.capsolverKeyTextEdit)

        self.dialogButtons = SettingDialogButton(self)
        layout.addRow(self.dialogButtons)

    def accept(self):
        SettingsConfigManager.setLanguage(self.languagesComboBox.currentData())
        SettingsConfigManager.setCapSolverApiKey(self.capsolverKeyTextEdit.toPlainText())
        return super().accept()