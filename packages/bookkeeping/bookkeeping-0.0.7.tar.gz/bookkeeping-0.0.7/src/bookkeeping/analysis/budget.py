from datetime import datetime
import pandas as pd
import pygal
from pygal.style import DefaultStyle
from IPython.display import SVG, display
from .analytics import Analysis
from ..management.negative_amount_error import NegativeAmountError

class BudgetAnalysis(Analysis):
    """
    Implementation of a BudgetAnalysis class which contains methods
    to perform basic analysis that is related to budget
    """

    def __init__(self, file_path = "userBook.json"):
        super().__init__(file_path)
        self.budget = 0  # Initialize budget as 0

    def setBudget(self, type, amount):
        """
        Set a monthly budget

        Args:
            type (int): an integer indicating whether the user would like to 
                    set the budget with the amount number or percentage of income
                    1 for an amount of monthly budget, 2 for a percentage of average income
            amount (float): an amount(>0) or a percentage(0-100)

        Raises:
            ValueError: invalid argument input
        """
        try:
            type = int(type)
            if type == 1:
                self.budget = float(amount)
            elif type == 2:
                if amount < 0:
                    raise NegativeAmountError
                percentage = float(amount)/100
                average_income = sum(t['amount'] for t in self.transactions if t['type']
                                        == 'income') / len(set(t['date'][:7] for t in self.transactions))
                self.budget = percentage * average_income
            else:
                raise ValueError("Please use pre-defined type code")
            print(f"Your set monthly budget is {round(self.budget)} CAD")
        except ValueError as v:
            print(f"Value Error: {v}")
        except ZeroDivisionError as Z:
            print(f"There is no income in this month")    
        except NegativeAmountError as n:
            print(f"Negative Amount Error: {n}")
   

    def overBudgetExpenses(self):
        """ 
        Print the amount of the expenses exceeding budget of this month 
        and all expenses of this month that occur after the point where
        the sum of expenses exceeds set budget
        """
        current_month = datetime.now().strftime('%Y-%m')
        current_month_expense = sum(
            t['amount'] for t in self.transactions if t['date'][:7] == current_month and t['type'] == 'expense')
        try:
            if self.budget != 0:
                over_budget = self.budget-current_month_expense
                if over_budget >= 0:
                    print(
                        f"Expenses in the current month have not exceed the budget, {round(over_budget)} CAD remaining")
                else:
                    print(
                        f"Expenses in the current month have exceeded the budget by {-round(over_budget)} CAD")
            else:
                raise ValueError("Budget has not been set yet")
        except ValueError as ve:
            print(ve)
        finally:    
            post_budget_transactions = self.transactionsAfterBudgetExceeded()
            self.displayTransactions(post_budget_transactions)

    def transactionsAfterBudgetExceeded(self):
        """
        Get all expenses of this month that occur after the point where
        the sum of expenses exceeds set budget

        Returns:
            post_budget_transactions(list): a list of transactions 
        """
        total_expense = 0
        budget_exceeded = False
        post_budget_transactions = []
        current_month = datetime.now().strftime('%Y-%m')

        for transaction in self.transactions:
            if transaction['type'] == 'expense':
                month = transaction['date'][:7]
                if month != current_month:
                    continue
                total_expense += transaction['amount']
                if total_expense > self.budget and not budget_exceeded:
                    budget_exceeded = True
                if budget_exceeded:
                    post_budget_transactions.append(transaction)

            return post_budget_transactions

    def displayTransactions(self, transactions):
        """
        Store the passed-in transactions as a pandas dataframe
        and print them
        """
        # Continue only if there is any transaction to show
        if transactions:
            # Create a DataFrame from the transactions list
            df = pd.DataFrame(transactions)

            # Format the DataFrame for better readability
            df['amount'] = df['amount'].apply(lambda x: f"${x:,.2f}")
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

            # Sort by date for chronological order
            df.sort_values(by='date', inplace=True)

            # Reset index for neatness
            df.reset_index(drop=True, inplace=True)

            print(df)

    def displayOverBudgetTrend(self):
        """ 
        Plot a bar chart to show the monthly trend of expenses exceeding over budget"""
        # Calculate monthly expenses
        budget_monthly_totals = {}
        for transaction in self.transactions:
            transaction_date = datetime.strptime(
                transaction['date'], '%Y-%m-%d')
            month_key = transaction_date.strftime('%Y-%m')
            if month_key not in budget_monthly_totals:
                budget_monthly_totals[month_key] = {
                    'expense': 0, 'overBudget': 0}
            if transaction['type'] == 'expense':
                budget_monthly_totals[month_key]['expense'] += transaction['amount']

        # Calculate the amount of expense over budget for each month
        for month_key, totals in budget_monthly_totals.items():
            totals['overBudget'] = totals['expense'] - self.budget

        # Extract data for plotting
        sorted_months = sorted(budget_monthly_totals.keys())
        overbudget_values = [budget_monthly_totals[month]
                                ['overBudget'] for month in sorted_months]

        # plot a bar chart for trend of expenses over budget
        bar_chart = pygal.Bar(print_values=True, print_values_position='top',
                                value_formatter=lambda x:  '%d' % x,
                                style=DefaultStyle(value_font_size=10))
        bar_chart.title = 'Monthly trend of expenses over budget'
        bar_chart.x_title = 'month'
        bar_chart.y_title = 'amount'
        bar_chart.x_labels = map(str, sorted_months)
        bar_chart.add('overBudget', overbudget_values)
        display(SVG(bar_chart.render(disable_xml_declaration=True)))
