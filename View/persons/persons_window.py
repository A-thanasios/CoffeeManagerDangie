from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QCheckBox, QSlider, QTableWidget, QTableWidgetItem,
)


from Module.services.person_service import PersonService



class PersonsWindow(QWidget):
    def __init__(self, person_service: PersonService ):
        super().__init__()

        self.person_service = person_service
        self.width = 100
        self.height = 200
        self.is_loading = False


        self.persons = []
        self.selected_person_row = []

        # Main layout
        self.main_layout = QVBoxLayout()

        # Person display table
        self.persons_table = QTableWidget()

        self.persons_table.setColumnCount(5)
        self.persons_table.setHorizontalHeaderLabels(["id", "Name", "Em@il", "Days per Week", "Buying"])
        self.persons_table.setColumnHidden(0, False)
        self.persons_table.itemSelectionChanged.connect(self.focus_person_row)
        self.persons_table.cellChanged.connect(self.edit_person)
        self.main_layout.addWidget(self.persons_table)
        self.fill_list()

        # Control panel
        self.control_panel = QHBoxLayout()

            # Add button
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_person)
        self.control_panel.addWidget(self.add_button)

            # Remove Button
        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_person)
        self.control_panel.addWidget(self.remove_button)


        self.main_layout.addLayout(self.control_panel)




        self.main_layout.addStretch()
        self.setLayout(self.main_layout)


    def fill_list(self):
        self.is_loading = True
        self.persons = self.person_service.read_all()
        self.persons_table.clearContents()
        self.persons_table.setRowCount(len(self.persons))

        if len(self.persons) > 0:
            for i, (db_id, person) in enumerate(self.persons.items()):
                check_box = self.create_checkbox(person)
                slider = self.create_slider(person)

                self.persons_table.setItem(i, 0, QTableWidgetItem(str(db_id)))
                self.persons_table.setItem(i, 1, QTableWidgetItem(person['name']))
                self.persons_table.setItem(i, 2, QTableWidgetItem(person['e_mail']))
                self.persons_table.setCellWidget(i, 3, slider)
                self.persons_table.setCellWidget(i, 4, check_box)

        self.is_loading = False

    @staticmethod
    def create_slider(person):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(5)
        slider.setValue(person['days_per_week'])
        slider.setSingleStep(1)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        return slider

    @staticmethod
    def create_checkbox(person):
        container = QWidget()
        checkbox_buying = QCheckBox()
        layout = QHBoxLayout(container)
        checkbox_buying.setChecked(person['is_buying'])
        layout.addWidget(checkbox_buying)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        return container

    def focus_person_row(self):
        self.selected_person_row.clear()
        selected_items = self.persons_table.selectedItems()
        for selected_item in selected_items:
            self.selected_person_row.append(selected_item.row())


    def add_person(self):
        index = 0
        while True:
            name = 'Give me name' + (f'{index}' if index > 0 else '')

            if not any(person['name'] == name for person in self.persons.values()):
                break
            index += 1


        try:
            self.person_service.create(name=name,
                                       e_mail='my@email.not',
                                       days_per_week=0,
                                       is_buying=False)
            self.fill_list()
        except Exception as e:
            print(f"Error creating person: {e}")


    def remove_person(self):
        try:
            for person in self.selected_person_row:
                db_id = int(self.persons_table.item(person, 0).text())
                self.person_service.remove(db_id)

            self.fill_list()
        except Exception as e:
            print(f"Error removing person: {e}")


    def edit_person(self, row, column):
        if self.is_loading:
            return
        try:
            if not self.persons_table.item(row, column).text():
                return

            person_id = int(self.persons_table.item(row, 0).text())

            match column:
                case 1:
                    item = self.persons_table.item(row, column).text().strip()
                    self.person_service.update(person_id=person_id,
                                               name=item)
                case 2:
                    item = self.persons_table.item(row, column).text().strip()
                    self.person_service.update(person_id=person_id,
                                               e_mail=item)
                case 3:
                    item = int(self.persons_table.item(row, column).text())
                    self.person_service.update(person_id=person_id,
                                               days_per_week=item)
                case 4:
                    item = bool(self.persons_table.item(row, column).text())
                    self.person_service.update(person_id=person_id,
                                               is_buying=item)
                case _:
                    return

            self.fill_list()
        except Exception as e:
            print(f"Error editing person: {e}")