from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, \
    QListWidgetItem

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure



from View.purchase.new_purchase_dialog import NewPurchaseDialog


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
        self.purchases = []

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

            self.purchase_provider.create(None)
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