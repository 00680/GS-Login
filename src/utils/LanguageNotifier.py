from PySide6.QtCore import QObject, Signal


class LanguageNotifier(QObject):
    languageChanged = Signal()

    _instance = None

    def __init__(self):
        super().__init__()

    @staticmethod
    def instance():
        if LanguageNotifier._instance is None:
            LanguageNotifier._instance = LanguageNotifier()
        return LanguageNotifier._instance
