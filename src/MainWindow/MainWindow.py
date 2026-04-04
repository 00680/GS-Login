
from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
)
from PySide6.QtCore import Qt

from MainWindow.SettingMenu.SettingMenu import SettingMenu
from MainWindow.LeftToolBar.LeftToolBar import LeftToolBar
from MainWindow.pages.AccountsPage.AccountsPage import AccountsPage
from MainWindow.pages.ProcessesPage.ProcessesPage import ProcessesPage

class MainWindow(QMainWindow):
    accountsPage :AccountsPage
    processesPage :ProcessesPage

    def __init__(self):
        super().__init__()

        self.setWindowTitle('GSLogin')

        self.resize(1100, 640)
        self.setFixedSize(self.size())

        # Menu
        self.menuBar().addMenu(SettingMenu(self))

        # Left toolbar
        self.toolbar = LeftToolBar(self)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)

        self.accountsPage = AccountsPage()
        self.processesPage = ProcessesPage()
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.stack.addWidget(self.accountsPage)
        self.stack.addWidget(self.processesPage)

        # Connect toolbar action signal to change pages
        self.toolbar.actionTriggered.connect(self.onToolbarActionTriggered)

        # Ensure stack matches the toolbar's initial checked action
        if self.toolbar.processesAction.isChecked():
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

        # # Add tabs on toolbar
        # self.toolbar.add_tab('Home', lambda: self.stack.setCurrentIndex(0), checked=True)
        # self.toolbar.add_tab('Login', lambda: self.stack.setCurrentIndex(1))
        # self.toolbar.add_tab('Settings', lambda: self.stack.setCurrentIndex(2))

    def onToolbarActionTriggered(self, action):
        # Map toolbar actions to stack indices
        if action is self.toolbar.accountsAction:
            self.stack.setCurrentIndex(0)
        elif action is self.toolbar.processesAction:
            self.stack.setCurrentIndex(1)