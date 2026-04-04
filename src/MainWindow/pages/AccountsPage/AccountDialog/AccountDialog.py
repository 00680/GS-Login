from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit
import time

from utils.Translator import Translator
from MainWindow.pages.AccountsPage.AccountDialog.AccountDialogButton.AccountDialogButton import AccountDialogButton


class AccountDialog(QDialog):
    def __init__(self, parent=None, accountData=None):
        super().__init__(parent)

        layout = QFormLayout(self)
        self.setWindowTitle(Translator.translate('accountDialog.title'))

        self.idLineEdit = QLineEdit(self)
        self.idLineEdit.setText(str(int(time.time() * 1000)))
        self.idLineEdit.setVisible(False)
        
        self.serverLineEdit = QLineEdit(self)
        layout.addRow(Translator.translate('accountDialog.serverLabel'), self.serverLineEdit)

        self.usernameLineEdit = QLineEdit(self)
        layout.addRow(Translator.translate('accountDialog.usernameLabel'), self.usernameLineEdit)

        self.passwordLineEdit = QLineEdit(self)
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(Translator.translate('accountDialog.passwordLabel'), self.passwordLineEdit)

        self.otpLineEdit = QLineEdit(self)
        layout.addRow(Translator.translate('accountDialog.otpLabel'), self.otpLineEdit)

        self.dialogButtons = AccountDialogButton(self)
        layout.addRow(self.dialogButtons)

        if accountData:
            self.idLineEdit.setText(accountData.get('id', ''))
            self.serverLineEdit.setText(accountData.get('server', ''))
            self.usernameLineEdit.setText(accountData.get('username', ''))
            self.passwordLineEdit.setText(accountData.get('password', ''))
            self.otpLineEdit.setText(accountData.get('otp', ''))

    def getData(self):
        return {
            'id': self.idLineEdit.text().strip() or None,
            'server': self.serverLineEdit.text().strip(),
            'username': self.usernameLineEdit.text().strip(),
            'password': self.passwordLineEdit.text(),
            'otp': self.otpLineEdit.text().strip() or None,
        }