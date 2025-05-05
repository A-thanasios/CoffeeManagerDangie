from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QStackedWidget
)
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPalette, QColor

from configuration.settings import app_name
from view.persons_window import PersonsWindow
from view.purchase_window import PurchaseWindow
from view.title_bar import TitleBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title_bar = TitleBar(self)
        self.purchase_window = PurchaseWindow()
        self.persons_window = PersonsWindow()

        self.setWindowTitle(app_name)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Get the screen geometry
        self.screen = QApplication.primaryScreen()
        self.screen_geometry = self.screen.geometry()

        self.set_window_geometry()



        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setAutoFillBackground(True)
        self.tabs.setTabsClosable(False)  # Hide the body of the tabs

        # Add tabs

        self.tabs.addTab(self.persons_window, "Persons")
        self.tabs.addTab(self.purchase_window, "Purchases")


        # Add the tab widget to the main layout
        #title_main_layout.addWidget(self.tabs)



        # Create a main layout for the window
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.title_bar)
        main_layout.setAlignment(self.title_bar, Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(self.tabs)



        central_widget = QWidget()
        central_widget.setObjectName('Container')
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()



    def set_window_geometry(self):
        # Calculate the window size and center position
        window_width = int(self.screen_geometry.width() * 0.4)
        window_height = int(self.screen_geometry.height() * 0.4)
        x = (self.screen_geometry.width() - window_width) // 2
        y = (self.screen_geometry.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)
