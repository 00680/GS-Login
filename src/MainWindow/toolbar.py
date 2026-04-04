from PySide6.QtWidgets import QToolBar, QAction
from PySide6.QtCore import Qt


class LeftToolBar(QToolBar):
    def __init__(self, parent=None, button_width: int = 120):
        super().__init__("LeftTabs", parent)
        self.setOrientation(Qt.Vertical)
        self.setMovable(False)
        # Qt enum location may vary between bindings/versions; handle fallbacks
        try:
            toolbutton_text_only = Qt.ToolButtonTextOnly
        except AttributeError:
            try:
                toolbutton_text_only = Qt.ToolButtonStyle.ToolButtonTextOnly
            except AttributeError:
                toolbutton_text_only = None
        if toolbutton_text_only is not None:
            self.setToolButtonStyle(toolbutton_text_only)
        self.setStyleSheet(f"QToolButton {{ min-width: {button_width}px; max-width: {button_width}px; }}")

    def add_tab(self, name: str, callback, checked: bool = False) -> QAction:
        act = QAction(name, self)
        act.setCheckable(True)

        def _on_triggered(checked_flag=False, cb=callback, a=act):
            cb()
            self._update_checks(a)

        act.triggered.connect(_on_triggered)
        self.addAction(act)
        if checked:
            act.setChecked(True)
        return act

    def _update_checks(self, active_action: QAction):
        for a in self.actions():
            a.setChecked(a is active_action)
