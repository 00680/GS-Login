from PySide6.QtCore import QObject, Signal


class AccountsNotifier(QObject):
    accountsChanged = Signal()

    _instance = None

    def __init__(self):
        super().__init__()

    @staticmethod
    def instance():
        if AccountsNotifier._instance is None:
            AccountsNotifier._instance = AccountsNotifier()
        return AccountsNotifier._instance
