from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QTableWidget, QAbstractItemView, QTableWidgetItem, QWidget, \
    QHBoxLayout, QCheckBox, QPushButton, QVBoxLayout


class NewPurchaseDialog(QDialog):
    def __init__(self, persons, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Purchase")
        #self.setModal(True)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.persons = persons  # List of available persons
        self.selected_persons = {}

        # Purchase Name Input
        self.name_label = QLabel("Purchase Name:")
        self.name_input = QLineEdit()

        # Persons List
        self.persons_label = QLabel("Persons:")
        self.persons_table = QTableWidget()
        self.persons_table.setColumnCount(3)
        self.persons_table.setHorizontalHeaderLabels(["Name", "Days", "Buying"])
        self.persons_table.setColumnWidth(1, 50)
        self.persons_table.setColumnWidth(2, 50)

        self.persons_table.setRowCount(len(self.persons))
        self.persons_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)




        for row, person in enumerate(self.persons):
            name_item = QTableWidgetItem(person.first_name)
            name_item.setData(Qt.ItemDataRole.UserRole, person)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
            self.persons_table.setItem(row, 0, name_item)

            days_item = QTableWidgetItem(str(person.days_per_week))
            days_item.setFlags(days_item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
            days_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.persons_table.setItem(row, 1, days_item)

            # Create a QWidget to hold the layout and checkbox
            widget = QWidget()
            layout = QHBoxLayout(widget)  # Use a horizontal layout
            layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to fit the checkbox properly

            # Create the QCheckBox
            check_item = QCheckBox()
            check_item.setCheckState(Qt.CheckState.Checked if person.is_buying else Qt.CheckState.Unchecked)

            # Add the checkbox to the layout
            layout.addWidget(check_item)
            layout.setAlignment(check_item, Qt.AlignmentFlag.AlignCenter)  # Center the checkbox

            # Set the QWidget with the layout as the cell widget
            self.persons_table.setCellWidget(row, 2, widget)


        # Product List
        self.product_label = QLabel("Products:")
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(3)
        self.product_table.setHorizontalHeaderLabels(["Name", "Shop", "Price"])
        self.product_table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.product_table.setMinimumWidth(305)

        self.add_button = QPushButton("+")
        self.remove_button = QPushButton("-")

        # Control Buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        # Layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.name_label)
        input_layout.addWidget(self.name_input)

        persons_layout = QVBoxLayout()
        persons_layout.addWidget(self.persons_label)
        persons_layout.addWidget(self.persons_table)



        product_layout = QVBoxLayout()
        product_layout.addWidget(self.product_label)
        product_button_layout = QHBoxLayout()
        product_buttons = QVBoxLayout()
        product_buttons.addWidget(self.add_button)
        product_buttons.addWidget(self.remove_button)
        product_buttons.addStretch()
        product_button_layout.addWidget(self.product_table)
        product_button_layout.addLayout(product_buttons)


        product_layout.addLayout(product_button_layout)
        product_layout.addWidget(self.product_table)

        person_product_layout = QHBoxLayout()
        person_product_layout.addLayout(persons_layout)
        person_product_layout.addLayout(product_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addStretch()

        main_layout = QVBoxLayout()

        main_layout.addLayout(input_layout)
        main_layout.addLayout(person_product_layout)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        # Connections
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.add_button.clicked.connect(self.add_product)
        self.remove_button.clicked.connect(self.remove_product)

        self.product_table.itemChanged.connect(self.validate_product_table)

    def get_purchase_info(self):
        checked_persons = []
        for row in range(self.persons_table.rowCount()):
            person = self.persons_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            if person.is_buying:
                    checked_persons.append(person)

        checked_products = []
        for row in range(self.product_table.rowCount()):
            checked_products.append(ProductDTO(id=row,
                                               name=self.product_table.item(row, 0).text(),
                                               shop=self.product_table.item(row, 1).text(),
                                               cost=int(self.product_table.item(row, 2).text())))


        return self.name_input.text(), checked_persons, checked_products

    def add_product(self):
        self.product_table.insertRow(self.product_table.rowCount())

    def remove_product(self):
        self.product_table.removeRow(self.product_table.rowCount() - 1)

    @staticmethod
    def validate_product_table(item):
        column = item.column()
        text = item.text()

        if column in [0, 1]:  # Name and Shop columns
            if not isinstance(text, str):
                item.setText("")
        elif column == 2:  # Price column
            try:
                int_value = int(text)
                item.setText(str(int_value))
            except ValueError:
                item.setText("0")
