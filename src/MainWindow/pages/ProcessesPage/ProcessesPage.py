from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QListWidgetItem
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QColor
from qt_material_icons import MaterialIcon

from MainWindow.pages.ProcessesPage.ProcessListItem.ProcessListItem import ProcessListItem
from MainWindow.pages.ProcessesPage.ProcessDialog.ProcessDialog import ProcessDialog
from utils.ProcessesConfigManager import ProcessesConfigManager
from utils.Translator import Translator
from utils.LanguageNotifier import LanguageNotifier
from utils.AccountsNotifier import AccountsNotifier
from utils.AutoLogin import startLogin

class ProcessesPage(QWidget):
    title: QLabel
    addBtn: QPushButton
    processList: QListWidget

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.processList = QListWidget(self)
        layout.addWidget(self.processList)

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

        self.loadProcesses()
        self.updateTexts()

        LanguageNotifier.instance().languageChanged.connect(self.updateTexts)
        try:
            AccountsNotifier.instance().accountsChanged.connect(self.onAccountsChanged)
        except Exception:
            pass

    def onAccountsChanged(self):
        # refresh account combos for all visible process items
        for i in range(self.processList.count()):
            item = self.processList.item(i)
            widget = self.processList.itemWidget(item)
            try:
                if widget:
                    widget.refreshAccounts()
            except Exception:
                pass

    def updateTexts(self):
        self.title.setText(Translator.translate('processesPage.title'))
        # update child process items so their localized strings refresh
        try:
            for i in range(self.processList.count()):
                item = self.processList.item(i)
                widget = self.processList.itemWidget(item)
                try:
                    if widget:
                        widget.populateAccountCombo()
                        try:
                            widget.updateDisplay()
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception:
            pass

    def loadProcesses(self):
        self.processList.clear()
        for id, procData in ProcessesConfigManager.getProcesses().items():
            item = QListWidgetItem()
            widget = ProcessListItem(procData, self.processList)
            widget.editRequested.connect(self.onEditProcess)
            widget.deleteRequested.connect(self.onDeleteProcess)
            widget.runRequested.connect(self.onRunProcess)
            item.setSizeHint(QSize(0, 56))
            self.processList.addItem(item)
            self.processList.setItemWidget(item, widget)

    def findItemWidget(self, processId):
        for i in range(self.processList.count()):
            item = self.processList.item(i)
            widget = self.processList.itemWidget(item)
            if widget and getattr(widget, 'processId', None) == processId:
                return i, item, widget
        return None, None, None

    def refreshProcess(self, processId):
        idx, item, widget = self.findItemWidget(processId)
        procData = ProcessesConfigManager.getProcessById(processId)
        if widget is None:
            self.loadProcesses()
            return

        if not procData:
            widget.checker.stop()
            self.processList.takeItem(idx)
            return

        widget.processData = procData

        widget.checker.folder = procData.get('path', '')

        widget.updateDisplay()


    def onAddButtonClicked(self):
        dlg = ProcessDialog(self)
        dlg.exec()
        self.loadProcesses()

    def onEditProcess(self, processId):
        procData = ProcessesConfigManager.getProcessById(processId)
        dlg = ProcessDialog(self, procData)
        dlg.exec()

        self.refreshProcess(processId)

    def onDeleteProcess(self, processId):
        if processId:
            ProcessesConfigManager.deleteProcess(processId)
            self.refreshProcess(processId)

    def onRunProcess(self, processId, accountId):
        if not accountId:
            return
        idx, item, widget = self.findItemWidget(processId)
        if widget is None:
            # fallback: just start
            startLogin(processId, accountId)
            return

        # mark widget as disabled by login process (it will manage re-enable)
        try:
            widget.setLoginDisabled(True)
        except Exception:
            widget.runBtn.setEnabled(False)

        thread = startLogin(processId, accountId)

        # poll the thread and clear the login-disabled flag when done
        try:
            timer = QTimer(self)
            timer.setInterval(300)

            def check():
                try:
                    alive = thread.is_alive()
                except Exception:
                    alive = False

                if not alive:
                    try:
                        widget.setLoginDisabled(False)
                    except Exception:
                        widget.runBtn.setEnabled(True)

                    timer.stop()

            timer.timeout.connect(check)
            timer.start()
        except Exception:
            pass
