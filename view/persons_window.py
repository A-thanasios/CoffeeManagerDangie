from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QLabel,
    QPushButton,
    QCheckBox, QLineEdit, QComboBox, QSlider,
)
from PyQt6.QtGui import QPixmap, QColor, QMouseEvent, QPainter, QBrush


class CircleSlider(QSlider):
    def __init__(self, orientation=Qt.Orientation.Vertical, parent=None):
        super().__init__(orientation, parent)
        self.circle_color = QColor(0, 0, 0)  # Default circle color
        self.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.setTickInterval(1)

    def set_circle_color(self, color):
        self.circle_color = QColor(color)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        '''# Získání pozice a rozměrů slideru
        slider_pos = self.pos()
        slider_width = self.width()
        num_ticks = self.maximum() - self.minimum()
        margin = 12

        for i in range(num_ticks + 1):
            # Výpočet x souřadnice pro každé kolečko
            x = slider_pos.x() + margin + i * (slider_width - 2 * margin) / num_ticks
            y = slider_pos.y() + self.height() // 2 + 20

            # Nakreslení kolečka
            painter.setBrush(QColor(0, 0, 0))  # Černá
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(int(x) - 4, int(y) - 4, 8, 8)'''

        rect = self.rect()
        tick_count = self.maximum() - self.minimum() + 1
        if self.orientation() == Qt.Orientation.Vertical:
            slider_height = rect.height()
            tick_spacing = slider_height / (tick_count - 1) if tick_count > 1 else 0
            for i in range(tick_count):
                y = int(rect.top() + slider_height - i * tick_spacing)
                x = rect.left() + rect.width() / 2
                circle_rect = QRect(int(x - 1), int(y - 5), 10, 10)
                painter.setBrush(QBrush(self.circle_color))
                painter.drawEllipse(circle_rect)
        else:
            slider_width = rect.width()
            tick_spacing = slider_width / (tick_count - 1) if tick_count > 1 else 0

            for i in range(tick_count):
                x = int(rect.left() + i * tick_spacing)
                y = rect.top() + rect.height() / 2
                circle_rect = QRect(int(x - 6), int(y - 5), 10, 10)
                painter.setBrush(QBrush(self.circle_color))
                painter.drawEllipse(circle_rect)


class TitledSlider(QWidget):
    def __init__(self, labels, orientation=Qt.Orientation.Vertical):
        super().__init__()
        self.labels = labels
        self.orientation = orientation
        self.slider = CircleSlider(orientation)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(labels) - 1)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.slider.setTickInterval(1)
        self.labels_widget = QWidget()

        if orientation == Qt.Orientation.Vertical:
            labels_layout = QVBoxLayout()
            labels_layout.setContentsMargins(0, 10, 0, 12)
            self.labels_widget.setLayout(labels_layout)
            self.label_objects = []
            for label_text in self.labels:
                label = QLabel(label_text)
                label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                labels_layout.addWidget(label)
                self.label_objects.append(label)
            layout = QHBoxLayout()
            layout.addWidget(self.labels_widget)
            layout.addWidget(self.slider)
        else:
            layout = QVBoxLayout()
            self.labels.setAlignment(Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.slider)
            layout.addWidget(self.labels)

        self.setLayout(layout)

    def set_value(self, value):
        self.set_label(value)

    def set_label(self, value):
        self.label.setText(self.labels[value])

    def value(self):
        return self.slider.value()

    def setValue(self, value):
        self.slider.setValue(value)


class PersonsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.width = 100
        self.height = 200

        # Sample data (replace with your actual data source)
        self.persons = [
            {"image": "view/pexels-eberhardgross-1624496.jpg", "name": "John", "middle_name": "M", "can_update": True},
            {"image": "", "name": "Alice", "middle_name": "B", "can_update": False},
        ]

        # Main layout
        main_layout = QHBoxLayout()

        # List of persons
        self.person_list = QListWidget()
        for person in self.persons:
            self.person_list.addItem(person["name"])
        self.person_list.currentRowChanged.connect(self.display_person)
        self.person_list.setMaximumWidth(100)
        main_layout.addWidget(self.person_list)

        # Person display area
        self.person_display_layout = QHBoxLayout()

        self.image_label = QLabel()

        self.person_display_layout.addWidget(self.image_label)

        self.complete_name_layout = QVBoxLayout()

        # Update checkbox
        self.update_checkbox = QCheckBox("Can Update")
        self.update_checkbox.stateChanged.connect(self.toggle_editing)
        self.complete_name_layout.addWidget(self.update_checkbox)
        self.update_checkbox.setChecked(False)

        # Middle name
        self.middle_name = QHBoxLayout()

        self.middle_name_label = QLabel('Middle/nick name')
        self.middle_name_line = QLineEdit()
        self.middle_name_line.setMaximumWidth(200)

        self.middle_name.addWidget(self.middle_name_label)
        self.middle_name.addWidget(self.middle_name_line)
        self.middle_name.addStretch()

        self.complete_name_layout.addLayout(self.middle_name)

        # Name
        self.name_layout = QHBoxLayout()

        self.name_label = QLabel('Name')
        self.name_line = QLineEdit()
        self.name_line.setMaximumWidth(200)

        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_line)
        self.name_layout.addStretch()

        self.complete_name_layout.addLayout(self.name_layout)

        # Complete name
        self.complete_name_layout.addStretch()

        self.person_display_layout.addLayout(self.complete_name_layout)
        self.person_display_layout.addStretch()

        main_layout.addLayout(self.person_display_layout)

        # Slider layout
        labels = ['5', '4', '3', '2', '1', '0']
        self.day_bar = TitledSlider(labels)
        self.day_bar.slider.setMaximumHeight(400)
        self.day_bar.slider.setMinimumHeight(200)
        self.day_bar.slider.setMinimumWidth(50)
        self.day_bar.slider.setSingleStep(1)

        main_layout.addWidget(self.day_bar)
        main_layout.addStretch()
        self.setLayout(main_layout)

        # Display the first person initially
        self.toggle_editing(False)
        self.display_person(0)

    def display_person(self, index):
        person = self.persons[index]
        if person['image'] == '':
            image = QPixmap(self.width, self.height)
            image.fill(QColor('green'))
            self.image_label.setPixmap(image)
        else:
            self.image_label.setPixmap(QPixmap(person["image"]).scaled(self.width, self.height))

        self.image_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.name_line.setText(person['name'])
        self.middle_name_line.setText(person['middle_name'])

    def toggle_editing(self, state):
        self.name_line.setEnabled(state == Qt.CheckState.Checked.value)
        self.middle_name_line.setEnabled(state == Qt.CheckState.Checked.value)