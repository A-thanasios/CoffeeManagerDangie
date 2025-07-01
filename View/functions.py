from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QCheckBox, QHBoxLayout


def create_checkbox(value: bool, method) -> QWidget:
    container = QWidget()
    checkbox_buying = QCheckBox()

    layout = QHBoxLayout(container)
    checkbox_buying.setChecked(value)
    checkbox_buying.setFixedWidth(17)
    layout.addWidget(checkbox_buying)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setContentsMargins(0, 0, 6, 0)
    container.setMinimumWidth(checkbox_buying.sizeHint().width() + 8)
    checkbox_buying.stateChanged.connect(method)
    container.checkbox = checkbox_buying
    return container