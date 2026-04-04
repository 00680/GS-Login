from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QHBoxLayout,
    QDialog,

    QListWidgetItem,
)
from PySide6.QtCore import Qt

from config.ConfigLoader import Config
from MainWindow.pages.AccountsPage.AccountDialog.AccountDialog import AccountDialog
from utils.Translator import Translator

class AccountsPage(QWidget):
    title :QLabel
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())

        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.title)

        self.accountList = QListWidget(self)
        self.layout().addWidget(self.accountList)

        btn_row = QHBoxLayout(self)
        self.add_btn = QPushButton(self)
        self.add_btn.clicked.connect(self.on_add_clicked)
        btn_row.addWidget(self.add_btn)
        btn_row.addStretch()

        self.layout().addLayout(btn_row)

        self.load_accounts()

        self.updateTexts()

    def updateTexts(self):
        self.title.setText(Translator.translate('accountsPage.title'))
        self.add_btn.setText(Translator.translate('accountsPage.addButton'))

    def load_accounts(self):
        self.accountList.clear()

        for a in Config.get('accounts', []):
            name = a.get('name') or 'fff'
            server = a.get('server') or 'ssss'
            username = a.get('username') or 'asdfsadf'
            display = f"{name} — {username}@{server}" if name else f"{username}@{server}"
            item = QListWidgetItem(display)
            self.accountList.addItem(item)

        a = {}
        name = a.get('name') or 'fff'
        server = a.get('server') or 'ssss'
        username = a.get('username') or 'asdfsadf'
        display = f"{name} — {username}@{server}" if name else f"{username}@{server}"
        item = QListWidgetItem(display)
        self.accountList.addItem(item)

    def on_add_clicked(self):
        dlg = AccountDialog(self)
        if dlg.exec() == QDialog.Accepted:
            acct = dlg.get_data()
            # basic validation: username and server required
            if not acct.get('username') or not acct.get('server'):
                return
            accounts = Config.get('accounts', []) or []
            accounts.append(acct)
            Config.cfg['accounts'] = accounts
            Config.save()
            self.load_accounts()
