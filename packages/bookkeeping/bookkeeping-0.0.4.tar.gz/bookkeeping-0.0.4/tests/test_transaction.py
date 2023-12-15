import unittest
from ..src.bookkeeping.management.transaction import Income
from ..src.bookkeeping.management.transaction import Expense
from datetime import datetime
from datetime import date

class TestTransaction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        # Common setup for each test case
        self.income_1 = Income(100.0, "Test Income Transaction 1", "salary income")
        self.income_2 = Income(200.0, "Test Income Transaction 2", "passive income")     
        self.expense_1 = Expense(300.0, "Test Expense Transaction 1", "grocery")
        self.expense_2 = Expense(400.0, "Test Expense Transaction 2", "entertainment")

    def tearDown(self):
        del self.income_1
        del self.income_2
        del self.expense_1
        del self.expense_2

    def test_setDate(self):
        self.income_1.setDate('2014-01-01')
        self.income_2.setDate('2014-01-02')
        self.expense_1.setDate('2014-01-03')
        self.expense_2.setDate('2014-01-04')

        self.assertEqual(self.income_1.date, datetime.strptime(str("2014-01-01"), "%Y-%m-%d").date())
        
        self.assertEqual(self.income_2.date, datetime.strptime(str("2014-01-02"), "%Y-%m-%d").date())
        self.assertEqual(self.expense_1.date, datetime.strptime(str("2014-01-03"), "%Y-%m-%d").date())
        self.assertEqual(self.expense_2.date, datetime.strptime(str("2014-01-04"), "%Y-%m-%d").date())

    def test_setLabel_valid(self):
        self.income_1.setLabel("passive income")
        self.income_2.setLabel("other")
        self.expense_1.setLabel("utility")
        self.expense_2.setLabel("newlabel")

        self.assertEqual(self.income_1.label, "passive income")
        self.assertEqual(self.income_2.label,"other")
        self.assertEqual(self.expense_1.label, "utility")
        self.assertEqual(self.expense_2.label, "newlabel")

    def test_setAmount_valid(self):
        self.income_1.setAmount(1000)
        self.income_2.setAmount(2000)
        self.expense_1.setAmount(3000)
        self.expense_2.setAmount(4000)

        self.assertEqual(self.income_1.amount, 1000)
        self.assertEqual(self.income_2.amount, 2000)
        self.assertEqual(self.expense_1.amount, 3000)
        self.assertEqual(self.expense_2.amount, 4000)

    def test_toDict(self):
        # Test the toDict method
        expected_dict_in_1 = {
            'amount': 100.0,
            'date': date.today().strftime('%Y-%m-%d'),
            'desc': "Test Income Transaction 1",
            'label': "salary income"
        }
        expected_dict_in_2 = {
            'amount': 200.0,
            'date': date.today().strftime('%Y-%m-%d'),
            'desc': 'Test Income Transaction 2',
            'label': "passive income"
        }

        expected_dict_ep_1 = {
            'amount': 300.0,
            'date': date.today().strftime('%Y-%m-%d'),
            'desc': 'Test Expense Transaction 1',
            'label': "grocery"
        }
        expected_dict_ep_2 = {
            'amount': 400.0,
            'date': date.today().strftime('%Y-%m-%d'),
            'desc': "Test Expense Transaction 2",
            'label': "entertainment"
        }
        result_dict_in_1 = self.income_1.toDict()
        result_dict_in_2= self.income_2.toDict()
        result_dict_ep_1= self.expense_1.toDict()
        result_dict_ep_2= self.expense_2.toDict()

        self.assertEqual(result_dict_in_1, expected_dict_in_1)
        self.assertEqual(result_dict_in_2, expected_dict_in_2)
        self.assertEqual(result_dict_ep_1, expected_dict_ep_1)
        self.assertEqual(result_dict_ep_2, expected_dict_ep_2)

    def test_str(self):
        expected_str_in_1 = f"{{'amount': 100.0, 'date': '{date.today().strftime('%Y-%m-%d')}', 'description': 'Test Income Transaction 1', 'label': 'salary income'}}"
        expected_str_in_2 = f"{{'amount': 200.0, 'date': '{date.today().strftime('%Y-%m-%d')}', 'description': 'Test Income Transaction 2', 'label': 'passive income'}}"
        expected_str_ep_1 = f"{{'amount': 300.0, 'date': '{date.today().strftime('%Y-%m-%d')}', 'description': 'Test Expense Transaction 1', 'label': 'grocery'}}"
        expected_str_ep_2 = f"{{'amount': 400.0, 'date': '{date.today().strftime('%Y-%m-%d')}', 'description': 'Test Expense Transaction 2', 'label': 'entertainment'}}"
  
        
        result_str_in_1 = self.income_1.__str__()
        result_str_in_2 = self.income_2.__str__()
        result_str_ep_1 = self.expense_1.__str__()
        result_str_ep_2 = self.expense_2.__str__()

        self.assertEqual(result_str_in_1, expected_str_in_1)
        self.assertEqual(result_str_in_2, expected_str_in_2)
        self.assertEqual(result_str_ep_1, expected_str_ep_1)
        self.assertEqual(result_str_ep_2, expected_str_ep_2)

    @classmethod
    def tearDownClass(cls):
        pass

unittest.main(argv=[''], verbosity=2, exit=False)