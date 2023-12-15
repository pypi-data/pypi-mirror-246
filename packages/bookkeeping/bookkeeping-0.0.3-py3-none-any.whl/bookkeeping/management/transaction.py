from datetime import datetime
from datetime import date
from .negative_amount_error import NegativeAmountError

class Transaction:
    """
    This class represents Transaction object
    """


    def __init__(self, amount, desc, label=None):
        try:
            self.amount = float(amount)
            if self.amount < 0:
                raise NegativeAmountError              
        except ValueError:
            print("Amount must be a number")
        except NegativeAmountError as e:
            print(f"Error: {e}")
                   

        self.desc = desc
        self.date = date.today()
        self.label = label if label else "other"             

    def setDate(self, newDate):
        try:
            if isinstance(newDate, str):
                self.date = datetime.strptime(str(newDate), "%Y-%m-%d").date()
            else:
                print("The new date must be a string")
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD'.")

    def setLabel(self, newLabel):
        try:
            if isinstance(newLabel, str):
                self.label = newLabel
            else:
                raise ValueError("The new Label must be a string")
        except ValueError as ve:
            print(ve) 

    def setAmount(self, newAmount):
        try:
            # Attempt to convert the input to a float
            float_value = float(newAmount)

            # Check if the float conversion was successful
            if isinstance(float_value, float):
                self.amount = float_value
            else:
                raise ValueError("The new amount must be a number")
        except ValueError as ve:
            print(ve)     

    def toDict(self):
        return {
            'amount': self.amount,
            'date': self.date.strftime('%Y-%m-%d'),
            'desc': self.desc,
            'label': self.label
        }

    def __str__(self):
        return f"{{'amount': {self.amount}, 'date': '{self.date.strftime('%Y-%m-%d')}', 'description': '{self.desc}', 'label': '{self.label}'}}"
    
class Income(Transaction):
    """
    A subclass of Transaction class that represents Income object
    """

    incomeLabels = ["salary income", "passive income", "capital gains", "other"]

    def __init__(self, amount, desc, label=None):
        super().__init__(amount, desc, label)
        if label:
            if label not in Income.incomeLabels:
                Income.incomeLabels.append(label)

class Expense(Transaction):
    """
    A subclass of Transaction class that represents Expense obejct
    """

    expenseLabels = ["utility", "grocery", "transportation", "entertainment", "healthcare", "other"]

    def __init__(self, amount, desc, label=None):
        super().__init__(amount, desc, label)
        if label:
            if label not in Expense.expenseLabels:
                Expense.expenseLabels.append(label)