from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtCore import QUrl

from utils.Translator import Translator
from utils.LanguageNotifier import LanguageNotifier


class HelpMenu(QMenu):
    userGuideEnAction: QAction
    userGuideZhAction: QAction

    def __init__(self, parent=None):
        super().__init__(parent)

        self.userGuideEnAction = self.addAction('')
        self.userGuideEnAction.triggered.connect(self.open_user_guide_en)

        self.userGuideZhAction = self.addAction('')
        self.userGuideZhAction.triggered.connect(self.open_user_guide_zh)

        self.updateTexts()
        LanguageNotifier.instance().languageChanged.connect(self.updateTexts)

    def open_user_guide_en(self):
        url = QUrl('https://github.com/00680/GS-Login/blob/master/USER_GUIDE_EN.md')
        QDesktopServices.openUrl(url)

    def open_user_guide_zh(self):
        url = QUrl('https://github.com/00680/GS-Login/blob/master/USER_GUIDE_ZH_TW.md')
        QDesktopServices.openUrl(url)

    def updateTexts(self):
        self.setTitle(Translator.translate('helpMenu.title'))
        self.userGuideEnAction.setText(Translator.translate('helpMenu.userGuideEN'))
        self.userGuideZhAction.setText(Translator.translate('helpMenu.userGuideZH_TW'))
