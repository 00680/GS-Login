import sys
from pathlib import Path
from config.ConfigLoader import Config
from qt_material import apply_stylesheet
from MainWindow.MainWindow import MainWindow
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, 'dark_blue.xml')
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
