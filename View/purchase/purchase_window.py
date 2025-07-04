from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMovie, QColor, QPalette
from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, \
    QListWidgetItem, QTableWidget, QTableWidgetItem, QCheckBox, QAbstractItemView, QHeaderView

from Module.services.mail_service import MailService
from Module.services.payment_service import PaymentService
from Module.services.person_service import PersonService
from Module.services.purchase_service import PurchaseService
from View.functions import create_checkbox
from View.purchase.mpl_canvas import MplCanvas
from View.purchase.new_purchase_dialog import NewPurchaseDialog

class PurchaseWindow(QWidget):
    def __init__(self, person_service: PersonService, purchase_service: PurchaseService, payment_service: PaymentService, mail_service: MailService ):
        super().__init__()
        self.person_service = person_service
        self.purchase_service = purchase_service
        self.payment_service = payment_service
        self.mail_service = mail_service

        self.person_width = 100
        self.to_pay_width = 60
        self.payed_width = 60
        self.paid_color = tuple([0, 100, 200])
        self.unpaid_color = tuple([255, 0, 0])


        self.purchases = []
        self.displayed_purchase = None
        self.displayed_purchase_row = -1

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

        # Purchase chart and person layout
        self.purchase_layout = QHBoxLayout()

        # Purchase chart
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.figure.set_facecolor((0, 0, 0, 0))
        self.canvas.setStyleSheet("background: transparent")
        self.purchase_layout.addWidget(self.canvas)


        # Persons layout
        self.persons_layout = QVBoxLayout()
        self.person_table = QTableWidget()
        self.purchase_layout.addLayout(self.persons_layout)


        self.purchase_display_layout.addLayout(self.purchase_layout)

        # QR view
        self.qr_label = QLabel()
        self.purchase_layout.addWidget(self.qr_label)



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
        self.send_mail_button = QPushButton("Send Mails")
        self.send_mail_button.setMaximumWidth(100)
        self.send_mail_button.clicked.connect(self.send_mails)
        self.operations_layout.addWidget(self.send_mail_button)

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
        self.displayed_purchase = purchase
        self.displayed_purchase_row = index

        self.canvas.axes.cla()
        self.canvas.draw()
        self.purchases_name.setText(purchase['name'])



        self.canvas.axes.pie([x['amount'] for x in purchase['purchase_settlements']],
                             labels=[x['person'].detail.name for x in purchase['purchase_settlements']],
                             autopct='%1.1f%%',
                             startangle=90,
                             textprops={'color': 'white'},
                             colors=['gray' if not x['is_paid'] else (0, self.paid_color[1]/255, self.paid_color[2]/255)
                                    for x in purchase['purchase_settlements']])

        self.canvas.draw()


        self.clear_persons_layout()
        # Add a new table
        self.person_table = QTableWidget()
        self.person_table.setColumnCount(4)
        self.person_table.setHorizontalHeaderLabels(['id','Person', 'To pay', 'Payed?'])
        self.person_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.person_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.person_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.person_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.person_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.person_table.setStyleSheet("""
            QTableWidget::item:selected {
                background-color: rgb(78, 49, 45);
            }
        """)

        self.person_table.clicked.connect(self.handle_click)

        self.person_table.setColumnHidden(0, True)
        self.person_table.setColumnWidth(1,self.person_width)
        self.person_table.setColumnWidth(2,self.to_pay_width)
        self.person_table.setColumnWidth(3,self.payed_width)
        self.person_table.setFixedWidth(self.person_width + self.to_pay_width + self.payed_width + 18)

        # Add new persons
        for i, settlement in enumerate(purchase['purchase_settlements']):
            amount = settlement['amount']
            person = settlement['person']
            check_box = create_checkbox(settlement['is_paid'], self.on_checkbox_change)
            self.person_table.insertRow(i)
            self.person_table.setItem(i, 0, QTableWidgetItem(str(person.id)))
            self.person_table.setItem(i, 1, QTableWidgetItem(person.detail.name))
            self.person_table.setItem(i, 2, QTableWidgetItem(str(round(amount))))
            self.person_table.item(i, 2).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.person_table.setCellWidget(i, 3, check_box)
            self.set_row_background_color(i, QColor(*self.unpaid_color) if not settlement['is_paid'] else QColor(*self.paid_color))


            self.persons_layout.addWidget(self.person_table)

        self.persons_layout.addStretch()

        sum_label = QLabel(f"---\nTotal: {sum(x['amount'] for x in purchase['purchase_settlements'])}")
        sum_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.persons_layout.addWidget(sum_label)

    def clear_persons_layout(self):
        for i in reversed(range(self.persons_layout.count())):
            widget = self.persons_layout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()


    def on_checkbox_change(self, state):
        checkbox = self.sender()
        pos = checkbox.mapTo(self.person_table.viewport(), checkbox.rect().center())
        row = self.person_table.indexAt(pos).row()

        self.edit_settlement(row, state)

    def edit_settlement(self, row, state):
        person_id = int(self.person_table.item(row, 0).text())
        self.purchase_service.update(self.displayed_purchase['db_id'],
                                     type='payment',
                                     person_id=person_id, state=bool(state))
        self.display_purchase(self.displayed_purchase_row)

    def handle_click(self, index):
        self.person_table.clearSelection()
        self.person_table.selectRow(index.row())
        self.show_person_qr()

    def set_row_background_color(self, row, color=None):
        if not color:
            return
        for column in range(self.person_table.columnCount()):
            item = self.person_table.item(row, column)
            if item:
                item.setBackground(color)

    def show_person_qr(self):
        rows = self.person_table.selectionModel().selectedIndexes()
        if rows:
            row = rows[0].row()
            self.person_table.columnAt(0)
            person_id = int(self.person_table.item(row, 0).text())
            print(person_id)
            if self.displayed_purchase:
                qr_dir_path = self.payment_service.read(self.displayed_purchase['db_id'])
                qr_code_name = [purchase['person'].detail.days_per_week
                                for purchase in self.displayed_purchase['purchase_settlements'] if purchase['person'].id == person_id][0]
                print(f'{qr_dir_path}/{qr_code_name}.gif')
                print(qr_code_name)
                movie = QMovie(f'{qr_dir_path}/qr_{qr_code_name}.gif')
                self.qr_label.setMovie(movie)
                self.qr_label.movie().start()

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
        current_row = self.displayed_purchase_row
        print(self.displayed_purchase_row)
        if current_row != -1:
            # Remove the purchase from the list and the display
            self.purchase_service.delete(self.purchase_list.item(current_row).data(Qt.ItemDataRole.UserRole)['db_id'])
            self.fill_list()
            if current_row < len(self.purchases):
                self.purchase_list.setCurrentRow(current_row)
            else:
                self.purchase_list.setCurrentRow(len(self.purchases) - 1)
            self.display_purchase(current_row)

    def send_mails(self):
        purchase_id = self.displayed_purchase['db_id']
        print(purchase_id)

        self.mail_service.send_payment_mail(purchase_id)