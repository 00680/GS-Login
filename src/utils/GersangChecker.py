import time
from PySide6.QtCore import QThread, Signal
from .GersangUtils import GersangUtils

class GersangChecker(QThread):
    statusChanged = Signal(object)

    def __init__(self, folder: str, interval: float = 5.0, parent=None):
        super().__init__(parent)
        self.folder = folder or ''
        self.interval = float(interval)

    def run(self):
        while not self.isInterruptionRequested():
            try:
                status = GersangUtils.isGersangRunning(self.folder)
            except Exception:
                status = None
            try:
                self.statusChanged.emit(status)
            except Exception:
                pass

            slept = 0.0
            step = 0.1
            while not self.isInterruptionRequested() and slept < self.interval:
                time.sleep(step)
                slept += step

    def stop(self, wait: float = 1.0):
        try:
            self.requestInterruption()
        except Exception:
            pass
        try:
            self.wait(int(wait * 1000))
        except Exception:
            pass
