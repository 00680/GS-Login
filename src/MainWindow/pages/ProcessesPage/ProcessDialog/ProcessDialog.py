from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QMessageBox

import os

from utils.Translator import Translator
from utils.ProcessesConfigManager import ProcessesConfigManager
from MainWindow.pages.AccountsPage.AccountDialog.AccountDialogButton.AccountDialogButton import AccountDialogButton

class ProcessDialog(QDialog):
    def __init__(self, parent=None, processData=None):
        super().__init__(parent)

        layout = QFormLayout(self)
        self.setWindowTitle(Translator.translate('processDialog.title'))

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
            self.pathLineEdit.setText(processData.get('path', ''))

    def onBrowse(self):
        path = QFileDialog.getExistingDirectory(self, Translator.translate('processDialog.fileDialogTitle'))
        if path:
            self.pathLineEdit.setText(path)

    def getData(self):
        return {
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
