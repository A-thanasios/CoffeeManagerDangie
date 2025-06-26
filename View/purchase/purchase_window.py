from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, \
    QListWidgetItem

from Module.services.person_service import PersonService
from Module.services.purchase_service import PurchaseService
from View.purchase.mpl_canvas import MplCanvas
from View.purchase.new_purchase_dialog import NewPurchaseDialog

class PurchaseWindow(QWidget):
    def __init__(self, person_service: PersonService, purchase_service: PurchaseService):
        super().__init__()
        self.person_service = person_service
        self.purchase_service = purchase_service


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
        self.canvas.figure.set_facecolor((0, 0, 0, 0))
        self.canvas.setStyleSheet("background: transparent")
        self.purchase_layout.addWidget(self.canvas)


        # Persons layout
        self.persons_layout = QVBoxLayout()
        self.purchase_layout.addLayout(self.persons_layout)


        self.purchase_display_layout.addLayout(self.purchase_layout)

        # Operations layout
        self.operations_layout = QHBoxLayout()

        # Operation buttons
            # New Purchase
        self.new_purchase_button = QPushButton("New Purchase")
        self.new_purchase_button.setMaximumWidth(100)
        self.new_purchase_button.clicked.connect(self.new_purchase)
        self.operations_layout.addWidget(self.new_purchase_button)

            # Delete Purchase
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
        self.purchases = self.purchase_service.read_all()

        self.purchase_list.clear()
        for purchase in self.purchases:
            new_purchase = QListWidgetItem()
            new_purchase.setData(Qt.ItemDataRole.UserRole, purchase)
            new_purchase.setText(purchase['name'])
            self.purchase_list.addItem(new_purchase)



    def display_purchase(self, index):
        if len(self.purchases) == 0:
            self.clear_persons_layout()
            self.canvas.axes.cla()
            self.canvas.axes.set_axis_off()
            self.canvas.draw()
            self.purchases_name.setText('')
            return
        if not self.purchase_list.item(index):
            return

        # Refresh purchases
        self.fill_list()
        purchase = self.purchase_list.item(index).data(Qt.ItemDataRole.UserRole)
        print(purchase['purchase_settlements'])

        self.canvas.axes.cla()
        self.canvas.draw()
        self.purchases_name.setText(purchase['name'])



        self.canvas.axes.pie([x['amount'] for x in purchase['purchase_settlements']],
                             labels=[x['person'].detail.name for x in purchase['purchase_settlements']],
                             autopct='%1.1f%%',
                             startangle=90,
                             textprops={'color': 'white'},
                             colors=['gray' if not x['is_paid'] else 'tab:blue'
                                    for x in purchase['purchase_settlements']])

        self.canvas.draw()

        # Clear previous persons
        self.clear_persons_layout()
        # Add new persons
        for settlement in purchase['purchase_settlements']:
            amount = settlement['amount']
            person = settlement['person']
            person_label = QLabel(person.detail.name)
            person_label.setText(f"{person.detail.name}: {amount}")
            person_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.persons_layout.addWidget(person_label)

        self.persons_layout.addStretch()

        sum_label = QLabel(f"---\nTotal: {sum(x['amount'] for x in purchase['purchase_settlements'])}")
        sum_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.persons_layout.addWidget(sum_label)

    def clear_persons_layout(self):
        for i in reversed(range(self.persons_layout.count())):
            widget = self.persons_layout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def new_purchase(self):
        persons = self.person_service.read_all()
        dialog = NewPurchaseDialog(persons, parent=self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            purchase_name, selected_persons, products = dialog.get_purchase_info()


            self.purchase_service.create(name=purchase_name, date=datetime.now(),
                                         person_ids=selected_persons,
                                         products=products,
                                         strategy_type='ByPerson')
            self.fill_list()
            self.purchase_list.setCurrentRow(len(self.purchases) - 1)

    def delete_purchase(self):
        # Get the current row
        current_row = self.purchase_list.currentRow()
        if current_row != -1:
            # Remove the purchase from the list and the display
            self.purchase_service.remove(self.purchase_list.item(current_row).data(Qt.ItemDataRole.UserRole)['db_id'])
            self.fill_list()
            if current_row < len(self.purchases):
                self.purchase_list.setCurrentRow(current_row)
            else:
                self.purchase_list.setCurrentRow(len(self.purchases) - 1)
            self.display_purchase(current_row)