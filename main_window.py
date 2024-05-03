import json
import datetime
from functools import partial
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTabWidget,
                               QTableWidget, QTableWidgetItem, QMessageBox)


def error_message(msg):
    """ Shows Dialog for errors """
    dlg = QMessageBox()
    dlg.setWindowTitle("Error")
    dlg.setText(msg)
    dlg.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Finance Manager")
        self.setFixedSize(QSize(700, 300))

        # For Tabs in the Head of GUI
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)  # It will be within QMainWindow widget

        self.view_all_transactions_tab = QTableWidget()
        self.add_new_transaction_tab = QWidget()

        # Input fields
        self.date_input = QLineEdit()
        self.type_input = QLineEdit()
        self.category_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.description_input = QLineEdit()

        self.tab_widget.addTab(self.view_all_transactions_tab, "View All Transactions")
        self.tab_widget.addTab(self.add_new_transaction_tab, "Add New Transaction")

        self.transactions = []
        self.view_all_transactions()

        self.add_new_transaction()

    def add_new_transaction(self):
        layout = QVBoxLayout(self.add_new_transaction_tab)

        layout.addWidget(QLabel("Date:"))
        layout.addWidget(self.date_input)

        layout.addWidget(QLabel("Type:"))
        layout.addWidget(self.type_input)

        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_input)

        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)

        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.add_tr)
        layout.addWidget(submit_button)

    def add_tr(self):
        date_str = self.date_input.text()
        type_str = self.type_input.text()
        category = self.category_input.text()
        amount = self.amount_input.text()
        description = self.description_input.text()

        # Validation for Date
        try:
            datetime_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            error_message(msg="Invalid Datetime format")
            self.date_input.clear()
            return

        # Validation for Amount
        try:
            amount_val = float(amount)
        except ValueError:
            error_message(msg="Amount must be numerical")
            self.amount_input.clear()
            return

        # Add transaction to the data ` transactions.json file
        self.transactions.append({"date": date_str,
                                  "type": type_str,
                                  "category": category,
                                  "amount": float(amount),
                                  "description": description})
        self.save_transactions()

        # Clear input fields
        self.date_input.clear()
        self.type_input.clear()
        self.category_input.clear()
        self.amount_input.clear()
        self.description_input.clear()

        self.load_transactions()

    def view_all_transactions(self):
        """ Layout for viewing all transactions """
        layout = QVBoxLayout(self.view_all_transactions_tab)
        self.view_all_transactions_tab.setColumnCount(6)
        self.view_all_transactions_tab.setHorizontalHeaderLabels(
            ["Date", "Type", "Category", "Amount", "Description", " "])
        layout.addWidget(self.view_all_transactions_tab)

        self.load_transactions()

    def load_transactions(self):
        """ Loading all transactions from json file """
        try:
            with open("transactions.json", "r") as file:
                self.transactions = json.load(file)
                self.display_transactions()
        except FileNotFoundError:
            pass

    def display_transactions(self):
        """ Display's all transactions, and delete button in front of each transaction """
        self.view_all_transactions_tab.setRowCount(len(self.transactions))

        for row, transaction in enumerate(self.transactions):
            self.view_all_transactions_tab.setItem(row, 0, QTableWidgetItem(transaction["date"]))
            self.view_all_transactions_tab.setItem(row, 1, QTableWidgetItem(transaction["type"]))
            self.view_all_transactions_tab.setItem(row, 2, QTableWidgetItem(transaction["category"]))
            self.view_all_transactions_tab.setItem(row, 3, QTableWidgetItem(str(transaction["amount"])))
            self.view_all_transactions_tab.setItem(row, 4, QTableWidgetItem(transaction["description"]))

            # Delete for each Transaction
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(partial(self.delete_transaction, row))
            self.view_all_transactions_tab.setCellWidget(row, 5, delete_button)

    def delete_transaction(self, row):
        """ Deletes transaction, save's it, and display's """
        del self.transactions[row]
        self.save_transactions()
        self.display_transactions()

    def save_transactions(self):
        """ Save's transactions in json file """
        with open("transactions.json", "w") as file:
            json.dump(self.transactions, file, indent=4)


