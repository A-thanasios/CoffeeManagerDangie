from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QSlider, QPushButton, QVBoxLayout, QHBoxLayout


class NewPersonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Person")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Middle name input
        self.middle_name_label = QLabel("Middle Name:")
        self.middle_name_input = QLineEdit()

        # Name input
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        # Days per week input
        self.days_per_week_label = QLabel("Days per Week:")
        self.days_per_week_input = QSlider(Qt.Orientation.Vertical)
        self.days_per_week_input.setRange(0, 5)




        # Buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        # Layout
        input_layout = QVBoxLayout()

        # Middle name layout
        middle_name_layout = QHBoxLayout()
        middle_name_layout.addWidget(self.middle_name_label)
        middle_name_layout.addWidget(self.middle_name_input)

        input_layout.addLayout(middle_name_layout)

        # Name layout
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)

        input_layout.addLayout(name_layout)

        # Days per week layout
        days_per_week_layout = QHBoxLayout()
        days_per_week_layout.addWidget(self.days_per_week_label)
        days_per_week_layout.addWidget(self.days_per_week_input)

        input_layout.addLayout(days_per_week_layout)



        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        # Connections
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_person_info(self):
        return self.middle_name_input.text(), self.name_input.text(), self.days_per_week_input.value()
