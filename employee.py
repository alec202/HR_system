"""Employee Module

Holds very simple information about multiple types of employees at our company.  Our business rules indicate
that we cannot have a generic Employee listed in our system.  We have Salaried and Hourly Employee types,
but cannot have generics of these either.  Our concrete types are Executives and Managers (Salaried),
and Permanent and Temporary (Hourly).  Subtypes may hold custom data (but aren't required to).

Author: Alec Mirambeau
Winter 2023
"""

import abc
from abc import ABC
from enum import Enum
from datetime import datetime


class Role(Enum):
    """Enumerated role class with different class variables.

    Statics:
        ceo: Value of 1
        cfo: Value of 2
        cio: Value of 3"""
    ceo = 1
    cfo = 2
    cio = 3


class Department(Enum):
    """Enumerated department class with its different class variables.

    Statics:
        accounting: Value of 1
        finance: Value of 2
        hr: Value of 3
        r_and_d: Value of 4
        machining: Value of 5
    """
    accounting = 1
    finance = 2
    hr = 3
    r_and_d = 4
    machining = 5


class InvalidRoleException(Exception):
    """An incorrect role was used."""
    def __init__(self, message: str = "Invalid role entered") -> None:
        """Initialize the exception error with the passed message"""
        super().__init__(message)


class InvalidDepartmentException(Exception):
    """An invalid department was used."""
    def __init__(self, message: str = "Invalid Department entered.") -> None:
        """Raise the exception and send the message to the base class."""
        super().__init__(message)


class Employee(ABC):
    """Class to store the information about each employee object.

    Class variables:
        current_id (int): an integer to represent the id number that will be used at this instance
            of an employee object.


    Attributes:
        name (str): A string representing the name of the employee.
        email (str): A string representing the email of this employee.
        id_number (int): An integer representing the id number of this employee.
        image (str): A string to represent the directory to the image of this employee instance."""
    _current_id = 1
    IMAGE_PLACEHOLDER = "./imagesForProject2CIS163/placeholder.png"

    def __init__(self, name: str, email: str) -> None:
        """Initialize the values of this class"""
        self.name = name
        self.email = email
        self.image = Employee.IMAGE_PLACEHOLDER
        self._id_number = Employee._current_id
        Employee._current_id += 1

    def __str__(self) -> str:
        """Returns a string with the id number and name of this employee."""
        return f"{self.id_number}:{self.name}"

    def __repr__(self) -> str:
        """Returns a string to represent this object and it's data."""
        return f"{self.name},{self.email},{self.image}"

    @property
    def id_number(self) -> int:
        """Returns the id number of this employee object."""
        return self._id_number

    # @id_number.setter
    # def id_number(self, new_num) -> None:
    #     """Changes the id number to the passed new_num value.
    #
    #     Params:
    #         new_num (int): An integer to represent the id_number of this employee.
    #
    #     Raises:
    #         ValueError: A non-int or number less than zero was passed into new_num."""
    #     if not isinstance(new_num, int) or new_num < 0:
    #         raise ValueError("ID must be an int greater than zero")
    #     self._id_number = new_num

    @property
    def name(self) -> str:
        """Returns the name of this employee."""
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """Setter for the name attribute.

        Params:
            new_name (str): A string to represent the new name for this current employee.

        Raises:
            ValueError: If the new_name is not a string, or if it's empty.."""
        if not isinstance(new_name, str) or len(new_name) <= 0:
            raise ValueError("Name must be a non-empty string")
        self._name = new_name

    @property
    def email(self) -> str:
        """Returns the string representing the email of this employee."""
        return self._email

    @email.setter
    def email(self, new_email: str) -> None:
        """Method to change this employee's email

        Params:
            new_email (str): A non-empty string to represent the email of this current employee.

        Raises:
            ValueError: An invalid email value was passes as a parameter"""

        if not isinstance(new_email, str) or len(new_email) <= 0 or "@acme-machining.com" not in new_email:
            raise ValueError("Email must be a non-empty string containing '@acme-machining.com'.")
        self._email = new_email

    @property
    def image(self) -> str:
        """Returns the directory path of the image."""
        return self._image

    @image.setter
    def image(self, new_image: str) -> None:
        """Change the image of this employee to the new_image image.

        Params:
            new_image (str): A string holding the directory path of an image.

        Raises:
            ValueError: an empty string, or non-string data type was passed.

        """
        if not isinstance(new_image, str) or len(new_image) == 0:
            raise ValueError("Image must be a non-empty string.")
        self._image = new_image

    @abc.abstractmethod
    def calc_pay(self) -> float:
        """Returns a float representing the pay rate of this employee."""
        pass


class Salaried(Employee):
    """Class to represent the information of a salaried employee.

    Attributes:
        yearly (float): An integer representing the yearly amount this salaried employee makes.
        name (str): A string representing the name of this salaried employee instance.
        email (str): A string representing the email of this salaried employee instance."""

    def __init__(self, name: str, email: str, yearly: str) -> None:
        """Initializes the attributes of the class.

        Params:
            name (str): A string representing the name of this employee
            email (str): A string representing the email of this current employee
            yearly (float): An integer representing the yearly amount this employee makes."""
        super().__init__(name, email)
        self.yearly = float(yearly)

    @property
    def yearly(self) -> float:
        """Returns an integer representing the yearly salary of this salaried instance."""
        return self._yearly

    @yearly.setter
    def yearly(self, yearly_amount: str) -> None:
        """Change the yearly amount to the yearly_amount parameter.

        Params:
            yearly_amount (int): An integer representing the yearly amount for
            this employee instance to make.

        Raises:
            ValueError: yearly_amount parameter was negative or it was over 50,000."""
        yearly_amount = float(yearly_amount)
        if not isinstance(yearly_amount, float) or yearly_amount <= 50_000.00:
            raise ValueError(f"{yearly_amount} isn't a float greater than $50,000")
        self._yearly = yearly_amount

    def calc_pay(self) -> float:
        """Returns a float representing the weekly pay of an employee."""
        return float(self.yearly / 52.0)

    def __repr__(self) -> str:
        """Returns a string representing the information of this salaried instance."""
        return f"{type(self).__name__},{super().__repr__()},{self.yearly:.2f}"


class Hourly(Employee):
    """Class to hold the information of an hourly employee.

    Attributes:
        name (str): A string representing the name of this employee.
        email (str) A string representing the email of this employee.
        hourly (float): A float to represent the pay rate of this employee."""

    def __init__(self, name: str, email: str, hourly_pay: str) -> None:
        """Initialize the values/attributes of this instance.

        Params:
            name (str): A string representing the name of this employee.
            email (str) A string representing the email of this employee.
            hourly_pay (float): A float to represent the pay rate of this employee."""
        super().__init__(name, email)
        self.hourly = float(hourly_pay)

    @property
    def hourly(self) -> float:
        """Returns the hourly pay rate of this employee."""
        return self._hourly

    @hourly.setter
    def hourly(self, new_hourly: str) -> None:
        """Change the hourly rate to the new_hourly param as long as it's a valid value.

        Raises:
            ValueError: A float wasn't passed, or the float was not between 15.00 and 99.00 (inclusive)."""
        new_hourly = float(new_hourly)
        if not isinstance(new_hourly, float) or not 15.00 <= new_hourly <= 99.99:
            raise ValueError("Hourly wage must be a float between 15.00 and 99.00 inclusive.")
        self._hourly = new_hourly

    def calc_pay(self) -> float:
        """Returns a float representing the pay rate of this employee."""
        return float(self.hourly * 40)

    def __repr__(self) -> str:
        """Returns a string to represent this hourly instance."""
        return f"{type(self).__name__},{super().__repr__()},{self.hourly:.2f}"


class Executive(Salaried):
    """Holds the information of an executive employee.

    Attributes:
        role (Role): A Role object to represent the role of this executive.
        yearly (float): An integer representing the yearly amount this salaried employee makes.
        name (str): A string representing the name of this employee instance.
        email (str): A string representing the email of this executive instance."""
    def __init__(self, name: str, email: str, yearly_amount: str, role: str):
        """initialize this instance of Executive with the passed values.

        Params:
            name (str): A string representing the name of this employee instance.
            email (str): A string representing the email of this executive instance.
            yearly_amount (float): An integer representing the yearly amount this salaried employee makes.
            role (Role): a Role instance representing the role of this executive."""
        super().__init__(name, email, yearly_amount)
        self.role = int(role)

    @property
    def role(self) -> Role:
        """Returns a Role instance representing the role of this executive instance."""
        return self._role

    @role.setter
    def role(self, new_role) -> None:
        """Changes the role of this executive instance to the new_role value if it's a valid value.

        Params:
            new_role (Role): A role object representing the role of this executive.

        Raises:
            InvalidRoleException: An invalid role or a non-role instance was passed."""
        all_role_vals = [role.value for role in Role]
        if new_role not in all_role_vals or not isinstance(new_role, int):
            raise InvalidRoleException("The role must be a valid Role object.")
        self._role = Role(new_role)

    def __repr__(self) -> str:
        """Returns a string representing this executive instance's information."""
        return f"{super().__repr__()},{self.role.value}"


class Manager(Salaried):
    """Holds the manager information.

    Attributes:
        yearly (float): An integer representing the yearly amount this salaried employee makes.
        name (str): A string representing the name of this employee instance.
        email (str): A string representing the email of this executive instance.
        department (Department): A Department object representing the department this manager
            belongs to.
        """

    def __init__(self, name: str, email: str, yearly: str, department: str):
        """Initialize the attributes with the passed values if they're valid values.

        Params:
            name (str): A string to represent the name of this Manager instance.
            email (str): An email to represent the email of this Manager instance.
            yearly (float): A float representing the yearly amount of money this Manager
                makes.
            department (Department): A static variable from Department class representing
                the department this manager works in."""
        super().__init__(name, email, yearly)
        self.department = int(department)

    @property
    def department(self) -> Department:
        """Returns the department of this manager instance."""
        return self._department

    @department.setter
    def department(self, new_dept: int) -> None:
        """Change the department value to the new_dept value if it's valid.

        Params:
            new_dept (Department): A department representing the department this employee belongs to.

        Raises:
            InvalidDepartmentException: An invalid department was passed.
                passed."""
        all_depts = [dept.value for dept in Department]
        if new_dept not in all_depts or not isinstance(new_dept, int):
            raise InvalidDepartmentException("Can only be changed to a valid department.")
        self._department = Department(new_dept)

    def __repr__(self) -> str:
        """Returns a string representing the information of this object's instance."""
        return f"{super().__repr__()},{self.department.value}"


class Permanent(Hourly):
    """Holds the information of a permanent employee.

    Attributes:
        name (str): A string representing the name of this employee.
        email (str) A string representing the email of this employee.
        hourly (float): A float to represent the pay rate of this employee.
        hired_date (datetime): A datetime object to represent the date this employee was
            hired.
        """

    def __init__(self, name: str, email: str, hourly_pay: str, hired_date: str) -> None:
        """Initialize the attributes with their corresponding values if their valid.

        Params:
            name (str): A string representing the name of this permanent instance.
            email (str): A string representing the email of this permanent instance.
            hourly_pay (float): A float representing the hourly pay rate of this permanent instance.
            hired_date (datetime): A datetime object to represent the date this permanent employee
                was hired."""
        super().__init__(name, email, hourly_pay)
        self.hired_date = datetime.strptime(hired_date, '%Y-%m-%d %H:%M:%S')

    @property
    def hired_date(self) -> datetime:
        """Returns a datetime object representing the date this employee was hired."""
        return self._hired_date

    @hired_date.setter
    def hired_date(self, date: datetime) -> None:
        """Change the hired date of this employee.

        The hired date is changed to the value passed in by the date parameter.

        Params:
            date (datetime): A datetime object representing the date this employee was hired.

        Raises:
            ValueError: A non-datetime object was passed through the date parameter."""
        if not isinstance(date, datetime):
            raise ValueError("A non-date instance was passed.")
        self._hired_date = date

    def __repr__(self) -> str:
        """Returns a string representation of this permanent instance."""
        return f"{super().__repr__()},{self.hired_date}"


class Temp(Hourly):
    """Holds the information of a temporary employee.

    Attributes:
        name (str): A string representing the name of this employee.
        email (str) A string representing the email of this employee.
        hourly (float): A float to represent the pay rate of this employee.
        last_day (datetime): A datetime instance to represent the last day of this employee."""

    def __init__(self, name: str, email: str, hourly: str, last_day: str) -> None:
        """initializes the attributes with the passed values.

        Params:
            name (str): A string representing the name of this temporary employee.
            email (str): A string representing the email of this employee.
            hourly (float): A float to represent the amount of money this hourly employee makes.
            last_day (datetime): A datetime object that represents the last day of this employee.
            """
        super().__init__(name, email, hourly)
        self.last_day = datetime.strptime(last_day, '%Y-%m-%d %H:%M:%S')

    @property
    def last_day(self) -> datetime:
        """Returns a datetime object representing the last day for this employee."""
        return self._last_day

    @last_day.setter
    def last_day(self, new_date: datetime) -> None:
        """Change the last date to the new_date value if it's valid

        Params:
            new_date (datetime): A datetime object representing the last day of this employee.

        Raises
            ValueError: a non-datetime object was passed"""
        if not isinstance(new_date, datetime):
            raise ValueError("A non-datetime instance was passed.")
        self._last_day = new_date

    def __repr__(self) -> str:
        """Returns a string representing this employee's information."""
        return f"{super().__repr__()},{self.last_day}"




# temp = Temp("temp", "e@acme-machining.com", "45.00", "2023-03-02 12:11:50")
# # print(type(temp.last_day.strftime('%B %d, %Y %H:%M:%S')))
# # print(temp.last_day.strftime('%B %d, %Y %H:%M:%S'))
# # print(type(f"{temp.last_day}"))
# print(temp.name)
# print(temp.__repr__())
# print(type(temp.last_day))
