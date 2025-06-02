from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QColor, QPainter, QBrush
from PyQt6.QtWidgets import QSlider, QWidget, QVBoxLayout, QLabel, QHBoxLayout


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
        self.labels.setText(self.labels[value])

    def value(self):
        return self.slider.value()

    def setValue(self, value):
        self.slider.setValue(value)