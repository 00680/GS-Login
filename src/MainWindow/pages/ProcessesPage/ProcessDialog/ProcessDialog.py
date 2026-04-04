from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
import time
import os

from utils.Translator import Translator
from utils.ProcessesConfigManager import ProcessesConfigManager
from MainWindow.pages.AccountsPage.AccountDialog.AccountDialogButton.AccountDialogButton import AccountDialogButton
from MainWindow.pages.AccountsPage.AccountDialog.ServerComboBox.ServerComboBox import ServerComboBox


class ProcessDialog(QDialog):
    def __init__(self, parent=None, processData=None):
        super().__init__(parent)

        layout = QFormLayout(self)
        self.setWindowTitle(Translator.translate('processDialog.title'))

        self.serversComboBox = ServerComboBox(self)
        layout.addRow(f"{Translator.translate('processDialog.serverLabel')}: ", self.serversComboBox)

        pathRow = QHBoxLayout()
        self.pathLineEdit = QLineEdit(self)
        browseBtn = QPushButton(Translator.translate('processDialog.browseButton'), self)
        browseBtn.clicked.connect(self.onBrowse)
        pathRow.addWidget(self.pathLineEdit)
        pathRow.addWidget(browseBtn)
        layout.addRow(f"{Translator.translate('processDialog.pathLabel')}: ", pathRow)

        self.dialogButtons = AccountDialogButton(self)
        layout.addRow(self.dialogButtons)

        if processData:
            for i in range(self.serversComboBox.count()):
                if self.serversComboBox.itemData(i) == processData.get('server'):
                    self.serversComboBox.setCurrentIndex(i)
                    break
            self.pathLineEdit.setText(processData.get('path', ''))

    def onBrowse(self):
        path = QFileDialog.getExistingDirectory(self, Translator.translate('processDialog.fileDialogTitle'))
        if path:
            self.pathLineEdit.setText(path)

    def getData(self):
        return {
            'server': self.serversComboBox.currentData(),
            'path': self.pathLineEdit.text().strip(),
        }

    def accept(self):
        data = self.getData()
        path = data.get('path', '')
        if not path or not os.path.isdir(path):
            QMessageBox.warning(self, Translator.translate('processDialog.invalidPathTitle'), Translator.translate('processDialog.invalidPathMessage'))
            return

        run_exe = os.path.join(path, 'run.exe')
        gersang_exe = os.path.join(path, 'Gersang.exe')
        if not (os.path.isfile(run_exe) and os.path.isfile(gersang_exe)):
            QMessageBox.warning(self, Translator.translate('processDialog.missingFilesTitle'), Translator.translate('processDialog.missingFilesMessage'))
            return

        ProcessesConfigManager.addOrUpdateProcess(data)
        return super().accept()
