from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QLineEdit, \
    QAbstractItemView, QListWidgetItem, QTableWidget, QTableWidgetItem, QCheckBox

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from module.dto.product_dto import ProductDTO
from module.dto.purchase_dto import PurchaseDTO
from module.services.strategy_service import StrategyService
from provider.person_provider import PersonProvider


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class PurchaseWindow(QWidget):
    def __init__(self, person_provider, purchase_provider, product_provider, app_service):
        super().__init__()
        self.person_provider = person_provider
        self.purchase_provider = purchase_provider
        self.product_provider = product_provider
        self.app_service = app_service


        self.purchases = []

        main_layout = QHBoxLayout()

        # List of purchases
        self.purchase_list = QListWidget()
        self.fill_list()

        self.purchase_list.currentRowChanged.connect(self.display_purchase)
        self.purchase_list.setMaximumWidth(100)
        main_layout.addWidget(self.purchase_list)

        # Purchase display area
        self.purchase_display_layout = QVBoxLayout()

        # Purchase name
        self.purchases_name = QLabel()
        self.purchase_display_layout.addWidget(self.purchases_name)

        # Purchase chart and persons layout
        self.purchase_layout = QHBoxLayout()

        # Purchase chart
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.purchase_layout.addWidget(self.canvas)


        # Persons layout
        self.persons_layout = QVBoxLayout()
        self.purchase_layout.addLayout(self.persons_layout)


        self.purchase_display_layout.addLayout(self.purchase_layout)

        # Operations layout
        self.operations_layout = QHBoxLayout()

        self.new_purchase_button = QPushButton("New Purchase")
        self.new_purchase_button.setMaximumWidth(100)
        self.new_purchase_button.clicked.connect(self.new_purchase)
        self.operations_layout.addWidget(self.new_purchase_button)
        self.delete_purchase_button = QPushButton("Delete Purchase")
        self.delete_purchase_button.setMaximumWidth(100)
        self.delete_purchase_button.clicked.connect(self.delete_purchase)
        self.operations_layout.addWidget(self.delete_purchase_button)
        self.operations_layout.addStretch()
        self.purchase_display_layout.addLayout(self.operations_layout)


        main_layout.addLayout(self.purchase_display_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)

        # Display the first purchase by default
        self.display_purchase(0)

    def fill_list(self):
        self.purchases = self.purchase_provider.get([])

        self.purchase_list.clear()
        for purchase in self.purchases:
            new_purchase = QListWidgetItem()
            new_purchase.setData(Qt.ItemDataRole.UserRole, purchase)
            new_purchase.setText(purchase.name)
            self.purchase_list.addItem(new_purchase)



    def display_purchase(self, index):
        if len(self.purchases) == 0:
            return

        purchase = self.purchases[index]
        self.canvas.axes.cla()
        self.purchases_name.setText(purchase.name)

        strategy = self.app_service.calculate_purchase_costs(purchase.id)


        self.canvas.axes.pie([x for x in strategy.values()],
                             labels=[x.name.first_name for x in strategy.keys()],
                             autopct='%1.1f%%',
                             startangle=90)
        self.canvas.draw()

        # Clear previous persons
        for i in reversed(range(self.persons_layout.count())):
            widget = self.persons_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        # Add new persons
        for key, value in strategy.items():
            person_label = QLabel(key.name.full_name)
            person_label.setText(f"{key.name.full_name}: {value}")
            person_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.persons_layout.addWidget(person_label)

        self.persons_layout.addStretch()

        sum_label = QLabel(f"---\nTotal: {sum(strategy.values())}")
        sum_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.persons_layout.addWidget(sum_label)

    def new_purchase(self):
        persons = self.person_provider.get([])
        dialog = NewPurchaseDialog(persons, self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            purchase_name, selected_persons, products = dialog.get_purchase_info()
            product_id_list = []
            for product in products:
                product_id_list.append(self.product_provider.create(product))

            if not product_id_list:
                return

            self.purchase_provider.create(PurchaseDTO(id=0,
                                                      name=purchase_name,
                                                      persons_id=[person.id for person in selected_persons],
                                                      products_id=product_id_list,
                                                      date=datetime.now()))
            self.fill_list()
            self.purchase_list.setCurrentRow(len(self.purchases) - 1)

    def delete_purchase(self):
        # Get the current row
        current_row = self.purchase_list.currentRow()
        if current_row != -1:
            # Remove the purchase from the list and the display
            self.purchase_provider.delete(self.purchase_list.item(current_row).data(Qt.ItemDataRole.UserRole).id)
            self.fill_list()
            if current_row < len(self.purchases):
                self.purchase_list.setCurrentRow(current_row)
            else:
                self.purchase_list.setCurrentRow(len(self.purchases) - 1)



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
