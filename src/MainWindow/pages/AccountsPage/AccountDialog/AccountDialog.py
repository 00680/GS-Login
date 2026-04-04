from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit
import time

from utils.Translator import Translator
from utils.AccountsConfigManager import AccountsConfigManager
from MainWindow.pages.AccountsPage.AccountDialog.AccountDialogButton.AccountDialogButton import AccountDialogButton
from MainWindow.pages.AccountsPage.AccountDialog.ServerComboBox.ServerComboBox import ServerComboBox

class AccountDialog(QDialog):
    def __init__(self, parent=None, accountData=None):
        super().__init__(parent)

        layout = QFormLayout(self)
        self.setWindowTitle(Translator.translate('accountDialog.title'))

        self.idLineEdit = QLineEdit(self)
        self.idLineEdit.setText(str(int(time.time() * 1000)))
        self.idLineEdit.setVisible(False)
        
        self.serversComboBox = ServerComboBox(self)
        layout.addRow(f"{Translator.translate('accountDialog.serverLabel')}: ", self.serversComboBox)

        self.usernameLineEdit = QLineEdit(self)
        layout.addRow(f"{Translator.translate('accountDialog.usernameLabel')}: ", self.usernameLineEdit)

        self.passwordLineEdit = QLineEdit(self)
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(f"{Translator.translate('accountDialog.passwordLabel')}: ", self.passwordLineEdit)
        self.otpLineEdit = QLineEdit(self)
        layout.addRow(f"{Translator.translate('accountDialog.otpLabel')}: ", self.otpLineEdit)

        self.dialogButtons = AccountDialogButton(self)
        layout.addRow(self.dialogButtons)

        if accountData:
            self.idLineEdit.setText(accountData.get('id', ''))
            for i in range(self.serversComboBox.count()):
                if self.serversComboBox.itemData(i) == accountData.get('server'):
                    self.serversComboBox.setCurrentIndex(i)
                    break
            self.usernameLineEdit.setText(accountData.get('username', ''))
            self.passwordLineEdit.setText(accountData.get('password', ''))
            self.otpLineEdit.setText(accountData.get('otp', ''))

    def getData(self):
        return {
            'id': self.idLineEdit.text().strip() or None,
            'server': self.serversComboBox.currentData(),
            'username': self.usernameLineEdit.text().strip(),
            'password': self.passwordLineEdit.text(),
            'otp': self.otpLineEdit.text().strip() or None,
        }

    def accept(self):
        AccountsConfigManager.addOrUpdateAccount(self.getData())
        return super().accept()