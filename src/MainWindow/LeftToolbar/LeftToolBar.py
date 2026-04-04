from PySide6.QtWidgets import QToolBar
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QActionGroup

from utils.Translator import Translator


class LeftToolBar(QToolBar):
    actionTriggered = Signal(object)
    processesAction :QAction
    accountsAction :QAction

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOrientation( Qt.Orientation.Vertical)
        self.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.setStyleSheet(f"QToolButton {{ min-width: 80; max-width: 80; }}")

        self.processesAction = QAction(self)
        self.processesAction.setCheckable(True)
        self.processesAction.setChecked(True)
        
        self.accountsAction = QAction(self)
        self.accountsAction.setCheckable(True)

        self.actionGroup = QActionGroup(self)
        self.actionGroup.setExclusive(True)
        self.actionGroup.addAction(self.processesAction)
        self.actionGroup.addAction(self.accountsAction)

        self.actionGroup.triggered.connect(self.updateChecks)

        self.addAction(self.processesAction)
        self.addAction(self.accountsAction)

        self.updateTexts()

    def updateChecks(self, activeAction: QAction):
        if activeAction:
            activeAction.setChecked(True)
            self.actionTriggered.emit(activeAction)

    def updateTexts(self):
        self.processesAction.setText(Translator.translate('leftToolBar.processAction.title'))
        self.accountsAction.setText(Translator.translate('leftToolBar.accountAction.title'))