import unittest
from unittest.mock import patch
from ..src.bookkeeping.analysis.summary import SummaryAnalysis

"""
Note: In summary.py, unit tests cannot be appropriately applied to displayTrend() and displayByLabel()
because of their functionalities in visualization. 
Therefore, no unit test case for these functions is included in this test class, as agreed upon by the instructor.
"""

class TestSummaryAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up the test class")

    @classmethod
    def tearDownClass(cls):
        print("Tearing down the test class")

    def setUp(self):
        print("Setting up for a test")
        self.analysis_instance = SummaryAnalysis(file_path = "bookkeeping/userBook.json")

    def tearDown(self):
        self.analysis_instance = None
        print("Tearing down after a test")


    def test_checkBalance(self):
        # Test with original balance
        with patch("builtins.print") as mock_print:
            self.analysis_instance.checkBalance()
            mock_print.assert_called_once_with("Overall Balance for 2023-12: 482.0")

        # Test with a positive balance
        self.analysis_instance.transactions = [
            {'type': 'income', 'amount': 100.0, 'date': '2023-12-01', "desc": "source", "label": "salary income"},
            {'type': 'expense', 'amount': 20.0, 'date': '2023-12-05', "desc": "description", "label": "grocery"}
        ]
        with patch("builtins.print") as mock_print:
            self.analysis_instance.checkBalance()
            mock_print.assert_called_once_with("Overall Balance for 2023-12: 80.0")

        # Test with a zero balance
        self.analysis_instance.transactions = []
        with patch("builtins.print") as mock_print:
            self.analysis_instance.checkBalance()
            mock_print.assert_called_once_with("Overall Balance for 2023-12: 0")

        # Test with a negative balance
        self.analysis_instance.transactions = [
            {'type': 'expense', 'amount': 1000.0, 'date': '2023-12-20', "desc": "description", "label": "grocery"}
        ]
        with patch("builtins.print") as mock_print:
            self.analysis_instance.checkBalance()
            mock_print.assert_called_once_with("Overall Balance for 2023-12: -1000.0")


if __name__ == '__main__':
    unittest.main(argv =[''], verbosity=2, exit=False)