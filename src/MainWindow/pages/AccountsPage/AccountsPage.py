from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QListWidgetItem, QStyle
from PySide6.QtCore import Qt, QSize
from qt_material_icons import MaterialIcon
from PySide6.QtGui import QColor

from MainWindow.pages.AccountsPage.AccountDialog.AccountDialog import AccountDialog
from MainWindow.pages.AccountsPage.AccountListItem.AccountListItem import AccountListItem
from utils.AccountsConfigManager import AccountsConfigManager
from utils.Translator import Translator
from utils.LanguageNotifier import LanguageNotifier

class AccountsPage(QWidget):
    title :QLabel
    addBtn :QPushButton
    accountList :QListWidget

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.accountList = QListWidget(self)
        layout.addWidget(self.accountList)

        btnRow = QHBoxLayout(self)
        self.addBtn = QPushButton(self)
        addBtnIcon = MaterialIcon('add', size=40)
        addBtnIconColor = QColor('#2196F3')
        addBtnIcon.set_color(addBtnIconColor)
        self.addBtn.setIcon(addBtnIcon)
        self.addBtn.setIconSize(QSize(40, 40))
        self.addBtn.setFixedSize(40, 40)
        self.addBtn.setFlat(True)
        self.addBtn.setStyleSheet(
            f"border: 2px solid {addBtnIconColor.name()}; border-radius: 6px;"
        )
        
        self.addBtn.clicked.connect(self.onAddButtonClicked)
        btnRow.addWidget(self.addBtn)
        btnRow.addStretch()
        layout.addLayout(btnRow)

        self.loadAccounts()

        self.updateTexts()

        LanguageNotifier.instance().languageChanged.connect(self.updateTexts)

    def updateTexts(self):
        self.title.setText(Translator.translate('accountsPage.title'))

    def loadAccounts(self):
        self.accountList.clear()
        for id, accountData in AccountsConfigManager.getAccounts().items():
            item = QListWidgetItem()
            widget = AccountListItem(accountData, self.accountList)
            widget.editRequested.connect(self.onEditAccount)
            widget.deleteRequested.connect(self.onDeleteAccount)
            item.setSizeHint(QSize(0, 56))
            self.accountList.addItem(item)
            self.accountList.setItemWidget(item, widget)

    def onAddButtonClicked(self):
        dlg = AccountDialog(self)
        dlg.exec()
        self.loadAccounts()

    def onEditAccount(self, accountId):
        accountData = AccountsConfigManager.getAccountById(accountId)
        dlg = AccountDialog(self, accountData)
        dlg.exec()
        self.loadAccounts()

    def onDeleteAccount(self, accountId):
        if accountId:
            AccountsConfigManager.deleteAccount(accountId)
            self.loadAccounts()
