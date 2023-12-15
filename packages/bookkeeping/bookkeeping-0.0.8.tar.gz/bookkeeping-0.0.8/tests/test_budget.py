import unittest
from unittest.mock import patch
from analysis.budget import BudgetAnalysis


class TestBudgetAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting up the test class")

    @classmethod
    def tearDownClass(cls):
        print("Tearing down the test class")

    def setUp(self):
        print("Setting up for a test")
        self.analysis_instance = BudgetAnalysis(file_path = "bookkeeping/userBook.json")

    def tearDown(self):
        self.analysis_instance = None
        print("Tearing down after a test")

    def test_setBudget(self):
        # Test setting the budget with a number (type = 1)
        with patch("builtins.print") as mock_print:
            self.analysis_instance.setBudget(500)
            self.assertEqual(self.analysis_instance.budget, 500)
            mock_print.assert_called_once_with("Your set monthly budget is 500 CAD")

        # Test setting the budget with a percentage (type = 2) and original data
        with patch("builtins.print") as mock_print:
            self.analysis_instance.setBudget(20, 2)
            self.assertAlmostEqual(self.analysis_instance.budget, 157, places = 0)
            mock_print.assert_called_once_with("Your set monthly budget is 157 CAD")        


    def test_overBudgetExpenses(self):
        # Test the overBudgetExpenses method with a higher budget
        self.analysis_instance.budget = 500
        with patch("builtins.print") as mock_print:
            self.analysis_instance.overBudgetExpenses()
            mock_print.assert_called_once_with("Expenses in the current month have not exceed the budget, 337 CAD remaining")

        # Test the overBudgetExpenses method with a lower budget
        self.analysis_instance.budget = 100
        with patch.object(self.analysis_instance, 'displayTransactions') as mock_display:
            # Mock the print function
            with patch("builtins.print") as mock_print:
                self.analysis_instance.overBudgetExpenses()

        # Check if the expected output is present in the printed output
        expected_output = "Expenses in the current month have exceeded the budget by 63 CAD"
        mock_print.assert_called_with(expected_output)

        # Check if the 'displayTransactions' method was called
        mock_display.assert_called_once()

        # Check the displayed transactions
        expected_transactions = [
            {'type': 'expense', 'amount': 122.0, 'date': '2023-12-01', 'description': 'description', 'label': 'utility'}
            ]        
        mock_display.assert_called_with(expected_transactions)      

if __name__ == '__main__':
    unittest.main(argv =[''], verbosity=2, exit=False)