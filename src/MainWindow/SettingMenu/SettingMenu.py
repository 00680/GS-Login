from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

from MainWindow.SettingMenu.SettingDialog.SettingDialog import SettingsDialog
from utils.Translator import Translator
from utils.LanguageNotifier import LanguageNotifier

class SettingMenu(QMenu):
    settingAction: QAction
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settingAction = self.addAction('')
        self.settingAction.triggered.connect(self.openSettingDialog)

        self.updateTexts()

        LanguageNotifier.instance().languageChanged.connect(self.updateTexts)

    def openSettingDialog(self):
        dlg = SettingsDialog(self)
        dlg.exec()

    def updateTexts(self):
        self.setTitle(Translator.translate('settingMenu.title'))
        self.settingAction.setText(Translator.translate('settingMenu.settingsAction'))

