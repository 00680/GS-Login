from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QComboBox
from PySide6.QtCore import QSize, Signal, Qt
from PySide6.QtGui import QColor
from utils.GersangChecker import GersangChecker
from qt_material_icons import MaterialIcon

from constants.servers import SERVERS
from utils.GersangUtils import GersangUtils
from utils.AccountsConfigManager import AccountsConfigManager
from utils.Translator import Translator

class ProcessListItem(QWidget):
    editRequested = Signal(object)
    deleteRequested = Signal(object)
    runRequested = Signal(object, object)
    checker :GersangChecker

    def __init__(self, processData: dict, parent=None):
        super().__init__(parent)
    
        self.processId = processData.get('path')
        self.processData = processData

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)

        path = self.processData.get('path', '')
        server = self.processData.get('server', '')

        self.statusLabel = QLabel(self)
        self.statusLabel.setFixedWidth(18)
        self.statusLabel.setAlignment(self.statusLabel.alignment())
        layout.addWidget(self.statusLabel)

        self.infoLabel = QLabel(f"{SERVERS.get(server)} @ {path}", self)
        layout.addWidget(self.infoLabel)

        self.accountCombo = QComboBox(self)
        self.accountCombo.setEditable(False)
        self.accountCombo.setFixedWidth(200)
        self.accountCombo.addItem(Translator.translate('processListItem.selectAccount'), None)

        accounts = AccountsConfigManager.getAccounts()
        procServer = self.processData.get('server', '')
        for accId, accData in accounts.items():
            accServer = accData.get('server', '')
            if accServer != procServer:
                continue
            username = accData.get('username', '')
            display = f"{username}@{SERVERS.get(accServer)}"
            self.accountCombo.addItem(display, accId)

        self.accountCombo.setCurrentIndex(0)

        layout.addWidget(self.accountCombo, alignment=Qt.AlignVCenter)

        runBtn = QPushButton(self)
        runIcon = MaterialIcon('play_arrow', size=40)
        runIconColor = QColor('#4CAF50')
        runIcon.set_color(runIconColor)
        runBtn.setIcon(runIcon)
        runBtn.setIconSize(QSize(30, 30))
        runBtn.setFixedSize(30, 30)
        runBtn.setFlat(True)
        runBtn.setEnabled(False)
        runBtn.clicked.connect(self.onRunClicked)
        layout.addWidget(runBtn)

        def onAccountChanged(idx):
            try:
                data = self.accountCombo.itemData(idx)
            except Exception:
                data = None
            runBtn.setEnabled(bool(data))

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
        self.checker = GersangChecker(path, interval=5.0, parent=self)
        self.checker.statusChanged.connect(self.onCheckerStatus)
        self.checker.start()

        self.destroyed.connect(lambda: self.stopChecker())

        self.statusLabel.setText('?')
        self.statusLabel.setStyleSheet('color: #FFC107; font-size: 12px;')

    def onRunClicked(self):
        try:
            accId = self.accountCombo.currentData()
        except Exception:
            accId = None
        self.runRequested.emit(self.processId, accId)

    def stopChecker(self):
        try:
            self.checker.requestInterruption()
        except Exception:
            pass

        try:
            self.checker.wait(1000)
        except Exception:
            pass
        
        try:
            self.checker.stop()
        except Exception:
            pass
        self.checker = None

    def onCheckerStatus(self, running):
        if running is True:
            self.statusLabel.setText('●')
            self.statusLabel.setStyleSheet('color: #4CAF50; font-size: 16px;')
        elif running is False:
            self.statusLabel.setText('●')
            self.statusLabel.setStyleSheet('color: #BDBDBD; font-size: 16px;')
        else:
            self.statusLabel.setText('?')
            self.statusLabel.setStyleSheet('color: #FFC107; font-size: 12px;')

    def updateDisplay(self):
        try:
            path = self.processData.get('path', '')
            server = self.processData.get('server', '')
            self.infoLabel.setText(f"{SERVERS.get(server)} @ {path}")
        except Exception:
            pass
