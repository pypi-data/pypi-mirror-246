import unittest
from unittest.mock import patch, mock_open
from ..src.bookkeeping.analysis.analytics import Analysis
class TestAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting up the test class")

    @classmethod
    def tearDownClass(cls):
        print("Tearing down the test class")

    def setUp(self):
        print("Setting up for a test")
        self.analysis_instance = Analysis(file_path = "userBook.json")
        self.income = [t for t in self.analysis_instance.transactions if t['type'] == 'income']
        self.expense = [t for t in self.analysis_instance.transactions if t['type'] == 'expense']

    def tearDown(self):
        self.analysis_instance = None
        print("Tearing down after a test")

    def test_loadBookData_expense(self):
        # Test loading expense transactions
        expected_expense_count = 30
        expected_first_expense_amount = 132.0
        expected_second_expense_label = "entertainment"

        self.assertEqual(len(self.expense), expected_expense_count)
        self.assertAlmostEqual(self.expense[0]['amount'], expected_first_expense_amount, places=2)
        self.assertEqual(self.expense[1]['label'], expected_second_expense_label)
        self.assertEqual(self.expense[1]['type'], 'expense')

    def test_loadBookData_income(self):
        # Test loading income transactions
        expected_income_count = 33
        expected_first_income_date = "2023-04-10"
        expected_second_income_label = "capital gains"

        self.assertEqual(len(self.income), expected_income_count)
        self.assertEqual(self.income[0]['date'], expected_first_income_date)
        self.assertEqual(self.income[1]['label'], expected_second_income_label)
        self.assertEqual(self.income[1]['type'], 'income')


    def test_loadBookData_file_not_found(self):
        # Mock the open function to simulate file not found and invalid JSON
        with patch("builtins.open", side_effect=[FileNotFoundError("File not found"), mock_open(read_data="This is not a valid JSON"), None]):
            with patch("builtins.print") as mock_print:
                # File not found
                self.analysis_instance = Analysis("nonexistent_file.json")
                transactions_file_not_found = self.analysis_instance.transactions     
                self.assertEqual(transactions_file_not_found, [])
                mock_print.assert_called_once_with("Error: File 'nonexistent_file.json' not found.")



if __name__ == '__main__':
    unittest.main(argv =[''], verbosity=2, exit=False)
