
from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
)
from PySide6.QtCore import Qt

from MainWindow.SettingMenu.SettingMenu import SettingMenu
from MainWindow.HelpMenu.HelpMenu import HelpMenu
from MainWindow.LeftToolBar.LeftToolBar import LeftToolBar
from MainWindow.pages.AccountsPage.AccountsPage import AccountsPage
from MainWindow.pages.ProcessesPage.ProcessesPage import ProcessesPage

class MainWindow(QMainWindow):
    accountsPage :AccountsPage
    processesPage :ProcessesPage

    def __init__(self):
        super().__init__()

        self.setWindowTitle('GSLogin')

        self.resize(800, 400)
        self.setFixedSize(self.size())

        self.menuBar().addMenu(SettingMenu(self))
        self.menuBar().addMenu(HelpMenu(self))

        self.toolbar = LeftToolBar(self)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)

        self.accountsPage = AccountsPage()
        self.processesPage = ProcessesPage()
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.stack.addWidget(self.accountsPage)
        self.stack.addWidget(self.processesPage)

        self.toolbar.actionTriggered.connect(self.onToolbarActionTriggered)

        if self.toolbar.processesAction.isChecked():
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

    def onToolbarActionTriggered(self, action):
        if action is self.toolbar.accountsAction:
            self.stack.setCurrentIndex(0)
        elif action is self.toolbar.processesAction:
            self.stack.setCurrentIndex(1)