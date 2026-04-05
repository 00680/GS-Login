from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QColor
from qt_material_icons import MaterialIcon

class AccountListItem(QWidget):
    editRequested = Signal(object)
    deleteRequested = Signal(object)

    def __init__(self, accountData: dict, parent=None):
        super().__init__(parent)
        self.accountId = accountData.get('id')
        self.accountData = accountData

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)

        username = self.accountData.get('username', '')
        label = QLabel(f"{username}", self)
        layout.addWidget(label)

        layout.addStretch()

        editBtn = QPushButton(self)
        editBtnIcon = MaterialIcon('open_in_new', size=40)
        editBtnIconColor = QColor('#3F51B5')
        editBtnIcon.set_color(editBtnIconColor)
        editBtn.setIcon(editBtnIcon)
        editBtn.setIconSize(QSize(30, 30))
        editBtn.setFixedSize(30, 30)
        editBtn.setFlat(True)
        editBtn.clicked.connect(lambda: self.editRequested.emit(self.accountId))
        layout.addWidget(editBtn)

        delBtn = QPushButton(self)
        delBtnIcon = MaterialIcon('delete_forever', size=40)
        delBtnIconColor = QColor('#F44336')
        delBtnIcon.set_color(delBtnIconColor)
        delBtn.setIcon(delBtnIcon)
        delBtn.setIconSize(QSize(30, 30))
        delBtn.setFixedSize(30, 30)
        delBtn.setFlat(True)
        delBtn.clicked.connect(lambda: self.deleteRequested.emit(self.accountId))
        layout.addWidget(delBtn)

        self.setLayout(layout)

        