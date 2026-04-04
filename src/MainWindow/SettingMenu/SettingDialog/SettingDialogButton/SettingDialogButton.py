from PySide6.QtWidgets import QDialog, QDialogButtonBox

class SettingDialogButton(QDialogButtonBox):
    def __init__(self, parent: QDialog = None):
        super().__init__(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent)

        if parent is not None:
            self.accepted.connect(parent.accept)
            self.rejected.connect(parent.reject)
    
