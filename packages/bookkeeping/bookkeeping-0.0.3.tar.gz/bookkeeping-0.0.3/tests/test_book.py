import unittest
import os
from ..src.bookkeeping.management.transaction import Income, Expense
from ..src.bookkeeping.management.book import Book

import sys
from io import StringIO

class TestBook(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a Book instance for testing
        cls.filePath = "testJSON.json"
        cls.testBook = Book(cls.filePath)

    def setUp(self):
        self.testBook.clearAll(self.filePath)

    def tearDown(self):
        self.testBook.clearAll(self.filePath)

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.filePath)
        except OSError:
            pass
        del cls.filePath
        del cls.testBook
        

    def test_addTran_income(self):
        # Test adding an income transaction
        income_transaction = Income(100.0, "Test Income", "salary income")
        self.testBook.addTran(income_transaction, self.filePath)

        self.assertEqual(len(self.testBook.book["income"]), 1)
        self.assertEqual(self.testBook.book["income"][0]["amount"], 100.0)
        self.assertEqual(self.testBook.book["income"][0]["desc"], "Test Income")
        self.assertEqual(self.testBook.book["income"][0]["label"], "salary income")

    def test_addTran_expense(self):
        # Test adding an expense transaction
        expense_transaction = Expense(50.0, "Test Expense", "grocery")
        self.testBook.addTran(expense_transaction, self.filePath)

        self.assertEqual(len(self.testBook.book["expense"]), 1)
        self.assertEqual(self.testBook.book["expense"][0]["amount"], 50.0)
        self.assertEqual(self.testBook.book["expense"][0]["desc"], "Test Expense")
        self.assertEqual(self.testBook.book["expense"][0]["label"], "grocery")

    def test_searchTran_valid(self):

        income_transaction = Income(200.0, "Test Income", "passive income")
        self.testBook.addTran(income_transaction, self.filePath)
        
        # Capture the output
        capturedOutput = StringIO()          
        sys.stdout = capturedOutput                   
        # Search for the transaction
        output = self.testBook.searchTran("income", "Test Income")                     
        sys.stdout = sys.__stdout__
        
        result = capturedOutput.getvalue()

        self.assertTrue(output)
        self.assertIn("income", result)
        self.assertIn("Test Income", result)
        self.assertIn("passive income", result)
        

    def test_searchTran_invalid(self):
        # Test searching for a transaction that does not exist
        income_transaction = Income(200.0, "Searchable Income", "passive income")
        self.testBook.addTran(income_transaction, self.filePath)
        
        # Capture the output
        capturedOutput = StringIO()          
        sys.stdout = capturedOutput                   
        
        output = self.testBook.searchTran("income", "Non-Existent")                     
        sys.stdout = sys.__stdout__
        
        result = capturedOutput.getvalue()

        self.assertFalse(output)
        self.assertIn("Non-Existent", result)
        self.assertIn("not found", result)
        self.assertIn("income", result)
        

    def test_removeTran_valid(self):
       
        income_transaction = Income(300.0, "Removable Income", "salary income")
        self.testBook.addTran(income_transaction, self.filePath)
        
        capturedOutput = StringIO()          
        sys.stdout = capturedOutput                   
        
        self.testBook.removeTran("income", 1, self.filePath)                     
        sys.stdout = sys.__stdout__
        
        result = capturedOutput.getvalue()

        self.assertEqual(len(self.testBook.book["income"]), 0)
        self.assertIn("income", result)
        self.assertIn("Removable Income", result)
        self.assertIn("salary income", result)

    def test_removeTran_invalid_index(self):
       
        income_transaction = Income(300.0, "Removable Income", "salary income")
        self.testBook.addTran(income_transaction, self.filePath)

       
        capturedOutput = StringIO()          
        sys.stdout = capturedOutput                   
        
        self.testBook.removeTran("income", 2, self.filePath)                     
        sys.stdout = sys.__stdout__
        
        result = capturedOutput.getvalue()

        self.assertEqual(len(self.testBook.book["income"]), 1)
        self.assertIn("index is out of bounds", result)

    def test_clearAll(self):
        
        income_transaction = Income(400.0, "Clearable Income", "passive income")
        expense_transaction = Expense(50.0, "Clearable Expense", "grocery")
        self.testBook.addTran(income_transaction, self.filePath)
        self.testBook.addTran(expense_transaction, self.filePath)

        self.testBook.clearAll(self.filePath)
        
        self.assertEqual(len(self.testBook.book["income"]), 0)
        self.assertEqual(len(self.testBook.book["expense"]), 0)

    def test_displayBook(self):
        
        income_transaction = Income(500.0, "Displayable Income", "salary income")
        expense_transaction = Expense(75.0, "Displayable Expense", "entertainment")
        self.testBook.addTran(income_transaction, self.filePath)
        self.testBook.addTran(expense_transaction, self.filePath)

        captured_output = StringIO()
        sys.stdout = captured_output

        self.testBook.displayBook()

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Displayable Income", output)
        self.assertIn("Displayable Expense", output)

unittest.main(argv=[''], verbosity=2, exit=False)

