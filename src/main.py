import sys
import os
from qt_material import apply_stylesheet
from MainWindow.MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon


def main():
    app = QApplication(sys.argv)
    # Set application icon (works when running frozen with PyInstaller or unpackaged)
    if getattr(sys, 'frozen', False):
        base = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        icon_path = os.path.join(base, 'src', 'images', 'icon.ico')
    else:
        base = os.path.dirname(__file__)
        icon_path = os.path.join(base, 'images', 'icon.ico')
    icon_path = os.path.normpath(icon_path)
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    apply_stylesheet(app, 'dark_blue.xml')
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
