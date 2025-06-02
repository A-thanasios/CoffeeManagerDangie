
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QLabel,
    QPushButton,
    QCheckBox, QLineEdit, QSlider, QDialog,
)
from PyQt6.QtGui import QPixmap, QColor

from MVP.Module import PersonDTO
from MVP.Provider.person_provider import PersonProvider


class PersonsWindow(QWidget):
    def __init__(self, person_provider : PersonProvider):
        super().__init__()

        self.person_provider = person_provider
        self.width = 100
        self.height = 200


        self.persons = []

        # Main layout
        main_layout = QHBoxLayout()

        # List of persons
        self.person_list = QListWidget()
        self.fill_list()
        self.person_list.currentRowChanged.connect(self.display_person)
        self.person_list.setMaximumWidth(100)
        main_layout.addWidget(self.person_list)

        # Person display area
        self.person_layout = QVBoxLayout()
        self.person_display_layout = QHBoxLayout()
        self.person_layout.addLayout(self.person_display_layout)

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
        self.middle_name_line.editingFinished.connect(self.edit_person)
        self.middle_name_line.setMaximumWidth(200)

        self.middle_name.addWidget(self.middle_name_label)
        self.middle_name.addWidget(self.middle_name_line)
        self.middle_name.addStretch()

        self.complete_name_layout.addLayout(self.middle_name)

        # Name
        self.name_layout = QHBoxLayout()

        self.name_label = QLabel('Name')
        self.name_line = QLineEdit()
        self.name_line.editingFinished.connect(self.edit_person)
        self.name_line.setMaximumWidth(200)

        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_line)
        self.name_layout.addStretch()

        self.complete_name_layout.addLayout(self.name_layout)

        # Complete name
        self.complete_name_layout.addStretch()

        self.person_display_layout.addLayout(self.complete_name_layout)

        self.person_display_layout.addStretch()

        main_layout.addLayout(self.person_layout)

        # Slider layout
        labels = ['5', '4', '3', '2', '1', '0']
        self.day_bar = QSlider(Qt.Orientation.Vertical)
        self.day_bar.setMaximumHeight(400)
        self.day_bar.setMinimumHeight(200)
        self.day_bar.setMinimumWidth(50)
        self.day_bar.setSingleStep(1)
        self.day_bar.setRange(0, 5)
        self.day_bar.setTickInterval(1)
        self.day_bar.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.day_bar.valueChanged.connect(self.update_day_bar)


        self.person_display_layout.addWidget(self.day_bar)

        # Operations layout
        self.operations_layout = QHBoxLayout()
        self.new_person_button = QPushButton("New Person")
        self.new_person_button.setMaximumWidth(100)
        self.new_person_button.clicked.connect(self.new_person)
        self.operations_layout.addWidget(self.new_person_button)
        self.delete_person_button = QPushButton("Delete Person")
        self.delete_person_button.setMaximumWidth(100)
        self.delete_person_button.clicked.connect(self.delete_person)
        self.operations_layout.addWidget(self.delete_person_button)
        self.operations_layout.addStretch()
        self.person_layout.addLayout(self.operations_layout)


        main_layout.addStretch()
        self.setLayout(main_layout)

        # Display the first person initially
        self.toggle_editing(False)
        self.display_person(0)

    def fill_list(self):
        self.persons = self.person_provider.get([])
        self.person_list.clear()
        for person in self.persons:
            self.person_list.addItem(person.first_name + " " + person.last_name)

    def display_person(self, index):
        if len(self.persons) == 0:
            self.set_layout_visible(self.person_display_layout, False)
            return

        person = self.persons[index]
        self.set_layout_visible(self.person_display_layout, True)
        if person.img == '':
            image = QPixmap(self.width, self.height)
            image.fill(QColor('green'))
            self.image_label.setPixmap(image)
        else:
            self.image_label.setPixmap(QPixmap(person.img).scaled(self.width, self.height))

        self.image_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.name_line.setText(person.first_name + " " + person.last_name)
        self.middle_name_line.setText(person.middle_name)
        self.person_list.setCurrentRow(index)
        self.day_bar.setValue(person.days_per_week)

    def set_layout_visible(self, layout, enabled):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setVisible(enabled)
            elif item.layout():
                self.set_layout_visible(item.layout(), enabled)

    def toggle_editing(self, state):
        self.name_line.setEnabled(state == Qt.CheckState.Checked.value)
        self.middle_name_line.setEnabled(state == Qt.CheckState.Checked.value)

    def edit_person(self):
        # Update the person's name and middle name
        current_row = self.person_list.currentRow()
        if current_row >= 0:
            name = self.name_line.text()
            first_name, last_name = name.split(' ', 1) if ' ' in name else (name, '')
            middle_name = self.middle_name_line.text()
            self.person_provider.update(self.persons[current_row].id,
                                        {"first_name": first_name,
                                         "last_name": last_name,
                                         "middle_name": middle_name})
            self.fill_list()
            self.display_person(current_row)

    def update_day_bar(self):
        # Update the person's days per week
        current_row = self.person_list.currentRow()
        if current_row >= 0:
            person = self.persons[current_row]
            if person.days_per_week != self.day_bar.value():
                self.person_provider.update(person.id,
                                            {"days_per_week": self.day_bar.value()})
                self.fill_list()
                self.display_person(current_row)

    def new_person(self):
        dialog = NewPersonDialog(self)
        result = dialog.exec()



        if result == QDialog.DialogCode.Accepted:
            middle_name, name, days_per_week = dialog.get_person_info()
            first_name, last_name = name.split(' ', 1) if ' ' in name else (name, '')
            new_person = PersonDTO(id= 9999,
                                    first_name=first_name,
                                   last_name=last_name,
                                   middle_name=middle_name,
                                   days_per_week=days_per_week,
                                   is_buying=True,
                                   img=''
                                   )
            self.person_provider.create(new_person)
            self.fill_list()
            self.display_person(len(self.persons) - 1)
            '''self.persons.append(new_person)
            self.person_list.addItem(new_person["name"])
            self.person_list.setCurrentRow(len(self.persons) - 1)
            self.display_person(len(self.persons) - 1)'''



    def delete_person(self):
        # Remove the selected person from the list
        current_row = self.person_list.currentRow()
        if current_row >= 0:
            person_id = self.persons[current_row].id
            self.person_provider.delete(person_id)
            self.fill_list()
            if current_row > 0:
                self.display_person(current_row - 1)
            elif current_row == 0:
                self.display_person(0)


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