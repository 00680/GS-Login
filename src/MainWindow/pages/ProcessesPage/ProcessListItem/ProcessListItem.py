from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QComboBox
from PySide6.QtCore import QSize, Signal, Qt
from PySide6.QtGui import QColor
from utils.GersangChecker import GersangChecker
from qt_material_icons import MaterialIcon

from utils.AccountsConfigManager import AccountsConfigManager
from utils.Translator import Translator

class ProcessListItem(QWidget):
    editRequested = Signal(object)
    deleteRequested = Signal(object)
    runRequested = Signal(object, object)
    checker: GersangChecker

    def __init__(self, processData: dict, parent=None):
        super().__init__(parent)

        self.processId = processData.get('path')
        self.processData = processData

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)

        path = self.processData.get('path', '')

        self.statusLabel = QLabel(self)
        self.statusLabel.setFixedWidth(18)
        self.statusLabel.setAlignment(self.statusLabel.alignment())
        layout.addWidget(self.statusLabel)

        self.infoLabel = QLabel(f"{path}", self)
        layout.addWidget(self.infoLabel)

        self.accountCombo = QComboBox(self)
        self.accountCombo.setEditable(False)
        self.accountCombo.setFixedWidth(200)
        self.accountCombo.addItem(Translator.translate('processListItem.selectAccount'), None)

        self.populateAccountCombo()

        self.accountCombo.setCurrentIndex(0)

        layout.addWidget(self.accountCombo, alignment=Qt.AlignVCenter)

        self.runBtn = QPushButton(self)
        runIcon = MaterialIcon('play_arrow', size=40)
        runIconColor = QColor('#4CAF50')
        runIcon.set_color(runIconColor)
        self.runBtn.setIcon(runIcon)
        self.runBtn.setIconSize(QSize(30, 30))
        self.runBtn.setFixedSize(30, 30)
        self.runBtn.setFlat(True)
        self.runBtn.setEnabled(False)
        self.runBtn.clicked.connect(self.onRunClicked)
        layout.addWidget(self.runBtn)

        def onAccountChanged(idx):
            try:
                data = self.accountCombo.itemData(idx)
            except Exception:
                data = None
            try:
                self._updateRunButtonState()
            except Exception:
                self.runBtn.setEnabled(bool(data))

        self.accountCombo.currentIndexChanged.connect(onAccountChanged)

        editBtn = QPushButton(self)
        editBtnIcon = MaterialIcon('open_in_new', size=40)
        editBtnIconColor = QColor('#3F51B5')
        editBtnIcon.set_color(editBtnIconColor)
        editBtn.setIcon(editBtnIcon)
        editBtn.setIconSize(QSize(30, 30))
        editBtn.setFixedSize(30, 30)
        editBtn.setFlat(True)
        editBtn.clicked.connect(lambda: self.editRequested.emit(self.processId))
        layout.addWidget(editBtn)

        delBtn = QPushButton(self)
        delBtnIcon = MaterialIcon('delete_forever', size=40)
        delBtnIconColor = QColor('#F44336')
        delBtnIcon.set_color(delBtnIconColor)
        delBtn.setIcon(delBtnIcon)
        delBtn.setIconSize(QSize(30, 30))
        delBtn.setFixedSize(30, 30)
        delBtn.setFlat(True)
        delBtn.clicked.connect(lambda: self.deleteRequested.emit(self.processId))
        layout.addWidget(delBtn)

        self.setLayout(layout)

        path = self.processData.get('path', '')
        # Do NOT set the thread's parent to the widget: if the widget is destroyed
        # while the thread is still running, Qt will warn `QThread: Destroyed while
        # thread '' is still running` and the app can freeze. Keep the thread
        # independent and delete it when it finishes.
        self.checker = GersangChecker(path, interval=5.0, parent=None)
        self.checker.statusChanged.connect(self.onCheckerStatus)
        # ensure we clean up the thread object when it finishes
        try:
            self.checker.finished.connect(self._onCheckerFinished)
        except Exception:
            pass
        self.checker.start()

        # internal state for run button control
        self._checker_running = None
        self._disabled_by_login = False

        self.destroyed.connect(lambda: self.stopChecker())

        self.statusLabel.setText('?')
        self.statusLabel.setStyleSheet('color: #FFC107; font-size: 12px;')

    def populateAccountCombo(self):
        # populate combo preserving selection if possible
        try:
            current = self.accountCombo.currentData()
        except Exception:
            current = None

        # reset but keep the first entry (selectAccount)
        self.accountCombo.blockSignals(True)
        self.accountCombo.clear()
        self.accountCombo.addItem(Translator.translate('processListItem.selectAccount'), None)

        accounts = AccountsConfigManager.getAccounts()
        selected_index = 0
        idx = 1

        for accId, accData in accounts.items():
            username = accData.get('username', '')
            display = f"{username}"
            self.accountCombo.addItem(display, accId)
            if current == accId:
                selected_index = idx
            idx += 1

        try:
            self.accountCombo.setCurrentIndex(selected_index)
        except Exception:
            self.accountCombo.setCurrentIndex(0)

        self.accountCombo.blockSignals(False)
        try:
            self._updateRunButtonState()
        except Exception:
            pass

    def refreshAccounts(self):
        # Called when accounts list changes
        try:
            self.populateAccountCombo()
        except Exception:
            pass

    def onRunClicked(self):
        try:
            accId = self.accountCombo.currentData()
        except Exception:
            accId = None
        self.runRequested.emit(self.processId, accId)

    def stopChecker(self):
        # Request the checker thread to stop but do not block the GUI.
        try:
            try:
                self.checker.statusChanged.disconnect(self.onCheckerStatus)
            except Exception:
                pass

            # ask the thread to stop
            self.checker.requestInterruption()

            # if it's already finished, schedule deletion and clear reference
            if not self.checker.isRunning():
                try:
                    self.checker.deleteLater()
                except Exception:
                    pass
                self.checker = None
            else:
                # otherwise leave the object alive; _onCheckerFinished will
                # clear the reference when the thread emits `finished`.
                try:
                    # ensure finished handler is connected
                    self.checker.finished.connect(self._onCheckerFinished)
                except Exception:
                    pass
        except Exception:
            pass

    def onCheckerStatus(self, running):
        # remember checker state and update run button accordingly
        try:
            self._checker_running = running
        except Exception:
            self._checker_running = None

        if running is True:
            self.statusLabel.setText('●')
            self.statusLabel.setStyleSheet('color: #4CAF50; font-size: 16px;')
        elif running is False:
            self.statusLabel.setText('●')
            self.statusLabel.setStyleSheet('color: #BDBDBD; font-size: 16px;')
        else:
            self.statusLabel.setText('?')
            self.statusLabel.setStyleSheet('color: #FFC107; font-size: 12px;')

        try:
            self._updateRunButtonState()
        except Exception:
            pass

    def _updateRunButtonState(self):
        try:
            has_account = bool(self.accountCombo.currentData())
        except Exception:
            has_account = False

        checker_ok = (self._checker_running is False)

        enabled = bool(has_account and checker_ok and not self._disabled_by_login)
        self.runBtn.setEnabled(enabled)

    def setLoginDisabled(self, disabled: bool):
        try:
            self._disabled_by_login = bool(disabled)
            self._updateRunButtonState()
        except Exception:
            try:
                self.runBtn.setEnabled(not disabled)
            except Exception:
                pass

    def updateDisplay(self):
        try:
            path = self.processData.get('path', '')
            self.infoLabel.setText(f"{path}")
        except Exception:
            pass

    def _onCheckerFinished(self):
        try:
            # safe cleanup when thread exits
            if getattr(self, 'checker', None):
                try:
                    self.checker.deleteLater()
                except Exception:
                    pass
            self.checker = None
        except Exception:
            pass

