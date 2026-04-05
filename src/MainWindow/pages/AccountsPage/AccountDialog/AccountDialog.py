from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QMessageBox
import time

from utils.Translator import Translator
from utils.AccountsConfigManager import AccountsConfigManager
from MainWindow.pages.AccountsPage.AccountDialog.AccountDialogButton.AccountDialogButton import AccountDialogButton

class AccountDialog(QDialog):
    def __init__(self, parent=None, accountData=None):
        super().__init__(parent)

        layout = QFormLayout(self)
        self.setWindowTitle(Translator.translate('accountDialog.title'))

        self.idLineEdit = QLineEdit(self)
        self.idLineEdit.setText(str(int(time.time() * 1000)))
        self.idLineEdit.setVisible(False)
        
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
            self.usernameLineEdit.setText(accountData.get('username', ''))
            self.passwordLineEdit.setText(accountData.get('password', ''))
            self.otpLineEdit.setText(accountData.get('otp', ''))

    def getData(self):
        return {
            'id': self.idLineEdit.text().strip() or None,
            'username': self.usernameLineEdit.text().strip(),
            'password': self.passwordLineEdit.text(),
            'otp': self.otpLineEdit.text().strip() or None,
        }

    def accept(self):
        data = self.getData()
        # Validate required fields
        missing = []
        if not data.get('username'):
            missing.append(Translator.translate('accountDialog.usernameLabel'))
        if not data.get('password'):
            missing.append(Translator.translate('accountDialog.passwordLabel'))
        if not data.get('otp'):
            missing.append(Translator.translate('accountDialog.otpLabel'))

        if missing:
            QMessageBox.warning(self, Translator.translate('accountDialog.title'),
                                Translator.translate('accountDialog.requiredFieldsMissing') % (', '.join(missing)))
            return

        try:
            AccountsConfigManager.addOrUpdateAccount(data)
        except Exception as e:
            QMessageBox.critical(self, Translator.translate('accountDialog.title'), str(e))
            return

        return super().accept()