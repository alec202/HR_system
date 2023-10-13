"""GUI Module for Employee Information

We provide a default form with common Employee information, then inherit and subclass
to create custom forms for each type.

Ira Woodring and Alec Mirambeau
Winter 2023
"""

import csv
import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QLabel, QLineEdit, QMenu, QHeaderView, QTableView, QMainWindow, QAbstractItemView, \
    QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QComboBox, QApplication, QDialog

from employee import *
from typing import *


class HRTableModel(QAbstractTableModel):
    """The HRTableModel allows us to display our information in a QTableView."""
    def __init__(self, data) -> None:
        """Initialize HRTableModel"""
        super(HRTableModel, self).__init__()
        self._columns = ["ID#", "Type", "Name", "Pay", "Email"]
        self._data = data

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> str:
        """Gives the header info in a format PyQt wants."""
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            # return f"Column {section + 1}"
            return self._columns[section]
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return f"{section + 1}"

    def data(self, index, role) -> str:
        """Returns the data at some table index."""
        if role == Qt.ItemDataRole.DisplayRole:
            e = self._data[index.row()]
            field = e.id_number
            if index.column() == 1:
                field = type(e).__name__
            if index.column() == 2:
                field = e.name
            if index.column() == 3:
                if isinstance(e, Salaried):
                    field = '${:,.2f}'.format(e.yearly)
                else:
                    field = '${:,.2f}'.format(e.hourly)
            if index.column() == 4:
                field = e.email
            return field

    def rowCount(self, index) -> int:
        """Provides the way for PyQt to get our row count."""
        return len(self._data)

    def columnCount(self, index) -> int:
        """Provides the column count, as PyQt expects."""
        return len(self._columns)


class MainWindow(QMainWindow):
    """MainWindow will have menus and a central list widget."""
    def __init__(self, parent=None) -> None:
        """Initializes MainWindow with its data."""
        super().__init__(parent)
        self.setWindowTitle("Employee Management v1.0.0")
        self.resize(800, 600)
        self._data = []
        self.load_file()
        self._model = HRTableModel(self._data)
        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._table.setAlternatingRowColors(True)
        self._header = self._table.horizontalHeader()
        self._header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.setCentralWidget(self._table)
        self._create_menu_bar()
        self._employee_form = None
        self._about_form = AboutForm()

    def _create_menu_bar(self) -> None:
        """Create the menus."""
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = QMenu("&File", self)
        edit_menu = QMenu("&Edit", self)
        help_menu = QMenu("&Help", self)
        self._exit_action = QAction("&Exit")
        self._exit_action.triggered.connect(exit)
        self._load_action = QAction("&Load HR Data")
        self._save_action = QAction("&Save HR Data")
        self._save_action.setShortcut('Ctrl+S')
        file_menu.addAction(self._load_action)
        self._load_action.setShortcut('Ctrl+O')
        self._load_action.triggered.connect(self.load_file)
        file_menu.addAction(self._save_action)
        file_menu.addAction(self._exit_action)
        self._edit_action = QAction("&Edit current employee")
        edit_menu.addAction(self._edit_action)
        self._edit_action.triggered.connect(self.edit_employee)
        self._edit_action.setShortcut('Ctrl+E')
        self._save_action.triggered.connect(self.save_file)
        self._about_action = QAction("About this software")
        self._about_action.triggered.connect(self.show_help)
        help_menu.addAction(self._about_action)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(help_menu)
        self.setMenuBar(menu_bar)

    def show_help(self) -> None:
        """Our 'help' form merely shows who wrote this, the version, and a description."""
        self._about_form.show()

    def data_to_rows(self) -> List[str]:
        """It is sometimes useful for us to have our model data as a list.  This method
        provides that feature."""
        data = []
        for e in self._data:
            row = [e.id_number, type(e).__name__, e.name]
            if isinstance(e, Salaried):
                row.append(str(e.yearly))
            else:
                row.append(str(e.hourly))
            row.append(e.email)
            data.append(row)
        return data

    def refresh_width(self) -> None:
        """Resize our table to fit our data width."""
        self._header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

    def edit_employee(self) -> None:
        """Update an employee object by populating the correct type of form with the selected type of
        employee data."""
        index = self._table.selectionModel().selectedIndexes()
        if not index:
            return
        index = index[0].row()
        if isinstance(self._data[index], Executive):
            self._employee_form = ExecutiveForm(self)
        if isinstance(self._data[index], Manager):
            self._employee_form = ManagerForm(self)
        if isinstance(self._data[index], Permanent):
            self._employee_form = PermanentForm(self)
        if isinstance(self._data[index], Temp):
            self._employee_form = TempForm(self)
        self._employee_form.fill_in(index)
        self._employee_form.show()

    def create_employee(self, employee_data: list) -> Employee:
        """Returns an instance of one of the extended classes of the Employee class.

        Params:
            employee_data (list): A list representing the information of this specific employee.
        """
        if employee_data[0] == "Executive":
            return Executive(employee_data[1], employee_data[2], employee_data[4], employee_data[5])
        elif employee_data[0] == "Manager":
            return Manager(employee_data[1], employee_data[2], employee_data[4], employee_data[5])
        elif employee_data[0] == "Temp":
            return Temp(employee_data[1], employee_data[2], employee_data[4], employee_data[5])
        elif employee_data[0] == "Permanent":
            return Permanent(employee_data[1], employee_data[2], employee_data[4], employee_data[5])

    def load_file(self) -> None:
        """Read a representation of all of our Employees from a file and store in our
        _data variable.  The table will automatically be populated by this variable."""
        with open('./employee.data') as datafile:
            reader = csv.reader(datafile, quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                emp = self.create_employee(row)
                emp.image = row[3]
                self._data.append(emp)

    def save_file(self) -> None:
        """Save a representation of all the Employees to a file."""
        try:
            file = open("./employee.data", "w")
            for worker in self._data:
                file.write(f"{worker.__repr__()}\n")
        finally:
            file.close()


class EmployeeForm(QtWidgets.QWidget):
    """There will never be a generic employee form, but we don't want to repeat code
    so we put it all here.  Each subtype of form will add to it."""
    def __init__(self, parent=None, employee: Employee = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        outer_layout = QVBoxLayout()
        self.layout = QtWidgets.QFormLayout()
        self.setLayout(outer_layout)
        self._id_label = QLabel()
        self.layout.addRow(QLabel("ID#"), self._id_label)
        self._name_edit = QLineEdit()
        self.layout.addRow(QLabel("Name: "), self._name_edit)
        self._pay_edit = QLineEdit()
        # # add the salary row
        # self.layout.addRow(QLabel("Salary: "), self._pay_edit)
        self._email_edit = QLineEdit()
        self.layout.addRow(QLabel("Email address:"), self._email_edit)
        self._image_path_edit = QLineEdit()
        self.layout.addRow(QLabel("Image path:"), self._image_path_edit)
        self._image = QLabel()
        self._image.setPixmap(QPixmap(Employee.IMAGE_PLACEHOLDER))
        # adding the combobox for the exec form to hold the role of the person.
        # self._exec_combobox = QComboBox()
        # self._exec_combobox.addItem(["CEO", "CFO", "CIO"])
        # self.layout.addRow(QLabel("Role: "), self._exec_combobox)
        # Add the combobox for the manager form to hold the department of the person.
        # self._manager_combobox = QComboBox()
        # self._manager_combobox.addItem(["Accounting", "Finance", "HR", "R & D", "Machining"])
        # self.layout.addRow(QLabel("Head of department: "), self._manager_combobox)
        # Manager combobox
        self._manager_combobox = QComboBox()
        self._manager_combobox.addItems(["Accounting", "Finance", "HR", "R & D", "Machining"])
        # Exec combobox
        self._exec_combobox = QComboBox()
        self._exec_combobox.addItems(["CEO", "CFO", "CIO"])
        self._err = False

        self.layout.addWidget(self._image)
        update = QPushButton("Update")
        update.clicked.connect(self.update_employee)
        outer_layout.addLayout(self.layout)
        outer_layout.addWidget(update)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._parent = parent  # missing in student version
        self._employee = employee  # missing in student version

    def update_employee(self) -> None:
        """Change the selected employee's data to the updated values."""
        try:
            self._employee.name = self._name_edit.text()
            self._employee.email = self._email_edit.text()
            self._employee.image = self._image_path_edit.text()
            self._parent.refresh_width()
            self.setVisible(False)
        except ValueError as err:
#             if not self._err:
#                 self._err = True
#                 self.layout.addRow(QLabel(f"{err}"))
#             else:
#                 self.layout.removeRow(-1)
#                 self.layout.addRow(QLabel(f"{err}"))
#                 self._err = False
            self.layout.addRow(QLabel(f"{err}"))
        except:
            self.layout.addRow(QLabel("Only enter valid values please!"))

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        self._employee = self._parent._data[index]
        self.setWindowTitle("Edit " + type(self._employee).__name__ + " Employee Information")
        self._id_label.setText(str(self._employee.id_number))
        self._name_edit.setText(self._employee.name)
        self._email_edit.setText(self._employee.email)
        self._image_path_edit.setText(self._employee.image)
        self._image.setPixmap(QPixmap(self._employee.image))

# Complete the following forms so that they update and fill-in
# their custom information.


class SalariedForm(EmployeeForm):
    """This is the form that will show up for a Salaried employee."""
    def fill_in(self, index) -> None:
        """See base class."""
        super().fill_in(index)
        self.layout.addRow(QLabel("Salary: "), self._pay_edit)
        self._pay_edit.setText(f"{self._employee.yearly:.2f}")

    def update_employee(self) -> None:
        """See base class."""
        try:
            self._employee.yearly = self._pay_edit.text()
            super().update_employee()
        except ValueError:
            self.layout.addRow(QLabel(f"Yearly amount entered must be a number greater than 50,000.00"))
        except:
            self.layout.addRow(QLabel(f"Yearly amount entered must be a number greater than 50,000.00"))


class ExecutiveForm(SalariedForm):
    """This is the form that will show up for an Executive employee."""
    def fill_in(self, index: int) -> None:
        """See base class."""
        super().fill_in(index)
        self.layout.addRow(QLabel("Role: "), self._exec_combobox)
        self._exec_combobox.setCurrentIndex(self._employee.role.value - 1)

    def update_employee(self) -> None:
        """See base class."""
        try:
            self._employee.role = self._exec_combobox.currentIndex() + 1
            super().update_employee()
        except ValueError:
            self.layout.addRow(QLabel(f"Role entered must be a valid role."))
        except:
            self.layout.addRow(QLabel(f"Role entered must be a valid role."))


class ManagerForm(SalariedForm):
    """This is the form that will show up for a Manager employee."""
    def fill_in(self, index: int) -> None:
        """See base class."""
        super().fill_in(index)
        self.layout.addRow(QLabel("Head of department: "), self._manager_combobox)
        self._manager_combobox.setCurrentIndex(self._employee.department.value - 1)

    def update_employee(self) -> None:
        """See base class."""
        try:
            self._employee.department = self._manager_combobox.currentIndex() + 1
            super().update_employee()
        except ValueError:
            self.layout.addRow(QLabel(f"Department entered must be a valid department."))
        except:
            self.layout.addRow(QLabel(f"Department entered must be a valid department."))


class HourlyForm(EmployeeForm):
    """This is the form that will show up for an hourly employee."""
    def fill_in(self, index) -> None:
        """See base class."""
        super().fill_in(index)
        self.layout.addRow(QLabel("Hourly wage: "), self._pay_edit)
        self._pay_edit.setText(f"{self._employee.hourly}")

    def update_employee(self) -> None:
        """See base class."""
        try:
            self._employee.hourly = self._pay_edit.text()
            super().update_employee()
        except ValueError:
            self.layout.addRow(QLabel(f"Hourly wage entered must be a number between 15.00 and 99.99 inclusive."))
        except:
            self.layout.addRow(QLabel(f"Hourly wage entered must be a number between 15.00 and 99.99 inclusive."))


class TempForm(HourlyForm):
    """This is the form that will show up for a temp employee."""
    def fill_in(self, index):
        """See base class."""
        super().fill_in(index)
        self.layout.addRow(QLabel(f"Last day:       {self._employee.last_day}"))


class PermanentForm(HourlyForm):
    """This is the form that will show up for a Permanent employee."""
    def fill_in(self, index):
        """See base class."""
        super().fill_in(index)
        self.layout.addRow(QLabel(f"Hired date:      {self._employee.hired_date}"))


class AboutForm(QtWidgets.QWidget):
    """An About Form just gives information about our app to users who want to see it.  Automatically
    sets itself visible on creation."""
    def __init__(self, *args, **kwargs) -> None:
        """Initializes AboutForm with it's data."""
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("HR Management System"))
        self.layout.addWidget(QLabel("version 1.0.0"))
        self.layout.addWidget(QLabel("A simple system for storing important pieces of information about employees."))
        self.close = QPushButton("Close")
        self.close.clicked.connect(self.close_form)
        self.layout.addWidget(self.close)
        self.setLayout(self.layout)

    def close_form(self) -> None:
        """Hide the form."""
        self.setVisible(False)
