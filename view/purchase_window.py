from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QLineEdit, \
    QAbstractItemView, QListWidgetItem

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class PurchaseWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.purchases = [
            {"name": "Purchase 1", 'price' : {"Person1": 100, "Person2": 200, "Person3": 300}},
            {"name": "Purchase 2", "price": {"Person1": 50, "Person2": 88, "Person3": 96}},
            {"name": "Purchase 3", "price": {"Person1": 1, "Person2": 2, "Person3": 3}},
        ]

        main_layout = QHBoxLayout()

        # List of purchases
        self.purchase_list = QListWidget()
        for purchase in self.purchases:
            self.purchase_list.addItem(purchase["name"])

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

        self.display_purchase(0)  # Display the first purchase by default

    def display_purchase(self, index):
        purchase = self.purchases[index]
        self.canvas.axes.cla()
        self.purchases_name.setText(purchase["name"])
        self.canvas.axes.pie([x for x in purchase['price'].values()],
                             labels=[x for x in purchase['price'].keys()],
                             autopct='%1.1f%%',
                             startangle=90)
        self.canvas.draw()

        # Clear previous persons
        for i in reversed(range(self.persons_layout.count())):
            widget = self.persons_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        # Add new persons
        for person in purchase['price'].keys():
            person_label = QLabel(person)
            person_label.setText(f"{person}: {purchase['price'][person]}")
            person_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.persons_layout.addWidget(person_label)

        self.persons_layout.addStretch()

        sum_label = QLabel(f"---\nTotal: {sum(purchase['price'].values())}")
        sum_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.persons_layout.addWidget(sum_label)

    def new_purchase(self):
        # Example list of persons (replace with your actual list)
        persons = [{"Person1" : 999}, {"Person2":888}, {"Person3":777}, {"Person4":666}]

        dialog = NewPurchaseDialog(persons, self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            purchase_name, selected_persons = dialog.get_purchase_info()
            new_purchase = {"name": purchase_name, "price": selected_persons}
            self.purchases.append(new_purchase)
            self.purchase_list.addItem(new_purchase["name"])
            self.purchase_list.setCurrentRow(len(self.purchases) - 1)

    def delete_purchase(self):
        # Get the current row
        current_row = self.purchase_list.currentRow()
        if current_row != -1:
            # Remove the purchase from the list and the display
            self.purchases.pop(current_row)
            self.purchase_list.takeItem(current_row)
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
        self.persons_list = QListWidget()
        self.persons_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        for person in self.persons:
            person_name = list(person.keys())[0]  # Extract person name
            item = QListWidgetItem(person_name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.persons_list.addItem(item)

        # Buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        # Layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.name_label)
        input_layout.addWidget(self.name_input)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.persons_label)
        main_layout.addWidget(self.persons_list)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        # Connections
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_purchase_info(self):
        checked_persons = {}
        for i in range(self.persons_list.count()):
            item = self.persons_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                person_name = item.text()
                # Find the corresponding value from the persons list
                for person_dict in self.persons:
                    if person_name in person_dict:
                        checked_persons[person_name] = person_dict[person_name]
                        break
        return self.name_input.text(), checked_persons
