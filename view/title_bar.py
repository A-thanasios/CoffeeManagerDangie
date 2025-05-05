from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QToolButton, QStyle

from configuration.settings import app_name


class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Highlight)
        #self.setFixedHeight(30)  # Increased height to accommodate both title and tabs
        self.initial_pos = None


        self.palette = QPalette()
        self.palette.setColor(QPalette.ColorRole.Window, QColor('lightgray'))
        self.setPalette(self.palette)

        self.title_label = QLabel(app_name)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.__button_layout = QHBoxLayout()

        # Min button
        self.min_button = QToolButton(self)
        min_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMinButton
        )
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)

        # Max button
        self.max_button = QToolButton(self)
        max_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMaxButton
        )
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)

        # Close button
        self.close_button = QToolButton(self)
        close_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarCloseButton
        )
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        # Normal button
        self.normal_button = QToolButton(self)
        normal_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarNormalButton
        )
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)
        # Add buttons
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(15, 15))
            button.setStyleSheet(
                """QToolButton { border: 2px solid white;
                                 border-radius: 12px;
                                }
                """
            )
            self.__button_layout.addWidget(button)


        # Set the layout for the title bar
        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(5, 5, 5, 5)
        self.__layout.setSpacing(5)
        self.__layout.addWidget(self.title_label)

        self.__layout.addStretch()  # Add stretch to push buttons to the right
        self.__layout.addLayout(self.__button_layout)
        self.setLayout(self.__layout)

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()