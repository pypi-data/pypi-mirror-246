import json

class Analysis:
    """
    Implementation of a Analysis class which loads transaction data
    from a JSON file and stores in an attribute
    """

    def __init__(self,file_path = "userBook.json"):
        self.transactions = self.loadBookData(file_path)

    def loadBookData(self, file_path):
        # Load data from the JSON file
        # The default path for JSON file is 'bookkeeping/userBook.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # Handle file not found error
            print(f"Error: File '{file_path}' not found.")
            return []


        # Extract and combine transaction information
        transactions = []
        try:
            for expense in data.get('expense', []):
                transaction_info = {
                    'type': 'expense',
                    'amount': float(expense.get('amount')),
                    'date': expense.get('date'),
                    'description': expense.get('desc'),
                    'label': expense.get('label')
                }
                transactions.append(transaction_info)

            for income in data.get('income', []):
                transaction_info = {
                    'type': 'income',
                    'amount': float(income.get('amount')),
                    'date': income.get('date'),
                    'description': income.get('desc'),
                    'label': income.get('label')
                }
                transactions.append(transaction_info)
        except (AttributeError, ValueError) as e:
            # Handle attribute or value errors during data extraction
            print(f"Error: Unable to extract data from file '{file_path}'. {e}")
            return []

        return transactions