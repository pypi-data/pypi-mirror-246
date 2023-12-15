import json
from .transaction import Income
from .transaction import Expense

class Book:
    """
    This class represents the Book object that keeps records of 
    all transactions of users
    """

    def __init__(self, filePath = "userBook.json"):
        self.book = {"expense": [],
                     "income": []}
        self.loadData(filePath)

    def saveData(self, filePath = "userBook.json"):
        with open(filePath, 'w') as file:
            json.dump(self.book, file, indent=2)

    def loadData(self, filePath):
        try:
            with open(filePath, 'r') as file:
                self.book = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book = {"expense": [],
                         "income": []}

    def addTran(self, transaction, filePath = "userBook.json"):
        try:
            transactionDict = transaction.toDict()
            if isinstance(transaction, Income):
                self.book["income"].append(transactionDict)
            elif isinstance(transaction, Expense):
                self.book["expense"].append(transactionDict)
            self.saveData(filePath)
            print(f"The below transaction has been added to the book: \n{transactionDict}")

        except Exception as e:
            print(f"Error adding transaction: {e}")

    def searchTran(self, t_type, keyword):
        found = False
        try:
            if not isinstance(t_type, str) or (t_type.lower() not in ["income", "expense"]):
                raise ValueError("Transaction type must be a string ('income' or 'expense').")
            if not isinstance(keyword, str):
                raise ValueError("Keyword must be a string.")
            if t_type in self.book:
                
                for index, item in enumerate(self.book[t_type]):
                        if keyword in item["desc"]:
                            index += 1
                            print(index, item)
                            found = True
                if not found:
                        print(f"{keyword} not found in the {t_type} transaction records.")
                        return False
            else:
                print(f"{t_type} category not found in the book.")
                return False
        except ValueError as ve:
            print(f"Error searching transaction: {ve}")
            return False
        finally:
            return found
    
    def removeTran(self, t_type, index, filePath = "userBook.json"):
        try:
            if not isinstance(t_type, str) or t_type.lower() not in ["income", "expense"]:
                raise ValueError("Transaction type must be a string ('income' or 'expense').")
            index = int(index) - 1
            if not (0 <= index < len(self.book[t_type])):
                raise ValueError("index is out of bounds.")
            
            if t_type in self.book:
                print(f"Removing {self.book[t_type][index]}")
                del self.book[t_type][index]
                print(f"transaction {index + 1} in {t_type} has been removed")
                self.saveData(filePath)
            else:
                print(f"Error: {t_type} category not found in the book.")
        except ValueError as e:
            print(f"Error removing transaction: {e}")

    def clearAll(self, filePath = "userBook.json"):
        self.book["income"] = []
        self.book["expense"] = []
        self.saveData(filePath)
        print("All transactions have been clear in this book")        

    def displayBook(self):
        print(f"All transactions:")
        for t_type in ['income', 'expense']:
            index = 1
            print(f"{t_type}:")
            for transaction in self.book[t_type]:
                print(f"{index}. {transaction}")
                index += 1