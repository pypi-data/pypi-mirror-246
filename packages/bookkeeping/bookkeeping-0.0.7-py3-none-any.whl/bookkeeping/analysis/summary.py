from datetime import datetime
import pygal
from pygal.style import DefaultStyle
from IPython.display import SVG, display
from .analytics import Analysis


class SummaryAnalysis(Analysis):
    """
    Implementation of a SummaryAnalysis class which contains methods
    to perform basic analysis on monthly transactions
    """

    def __init__(self, file_path = "userBook.json"):
        super().__init__(file_path)

    def checkBalance(self):
        """ 
        Calculate overall balance for the current month and print the result 
        """
        current_month = datetime.now().strftime('%Y-%m')
        current_month_transactions = [
            t for t in self.transactions if t['date'][:7] == current_month]
        current_month_balance = sum(
            t['amount'] if t['type'] == 'income' else -t['amount'] for t in current_month_transactions)
        print(f"Overall Balance for {current_month}: {current_month_balance}")

    def displayTrend(self, graph_type):
        """ 
        Plot a line chart or bar chart to represent the monthly 
        trend of income, expenses and balance

        Args:
            graph_type (int): 1 for line chart, 2 for bar chart

        Raises:
            ValueError: invalid argument input for graph_type
        """
        # Calculate monthly totals
        monthly_totals = {}
        for transaction in self.transactions:
            transaction_date = datetime.strptime(
                transaction['date'], '%Y-%m-%d')
            month_key = transaction_date.strftime('%Y-%m')
            if month_key not in monthly_totals:
                monthly_totals[month_key] = {
                    'income': 0, 'expense': 0, 'balance': 0}
            if transaction['type'] == 'income':
                monthly_totals[month_key]['income'] += transaction['amount']
            elif transaction['type'] == 'expense':
                monthly_totals[month_key]['expense'] += transaction['amount']

        # Calculate balance for each month
        for month_key, totals in monthly_totals.items():
            totals['balance'] = totals['income'] - totals['expense']

        # Extract data for plotting
        sorted_months = sorted(monthly_totals.keys())
        income_values = [monthly_totals[month]['income']
                         for month in sorted_months]
        expense_values = [monthly_totals[month]['expense']
                          for month in sorted_months]
        balance_values = [monthly_totals[month]['balance']
                          for month in sorted_months]

        # Plot line chart or bar chart
        chart = None
        try: 
            graph_type = int(graph_type)
            if graph_type == 1:  # line chart
                chart = pygal.Line(print_values=True,
                                    style=DefaultStyle(value_font_size=10))
            elif graph_type == 2:  # bar chart
                chart = pygal.Bar(print_values=True, print_values_position='top',
                                    style=DefaultStyle(value_font_size=10))
            else:
                raise ValueError(
                    "Please use pre-defined type code for graph_type")
            chart.title = 'Monthly trend of expenses, income and balance'
            chart.x_title = 'month'
            chart.y_title = 'amount'
            chart.x_labels = map(str, sorted_months)
            chart.add('Expenses', expense_values)
            chart.add('Income', income_values)
            chart.add('Balance', balance_values)
            display(SVG(chart.render(disable_xml_declaration=True)))
        except ValueError as v:
            print(f"Value Error: {v}")


    def displayByLabel(self, transaction_type, graph_type):
        """ 
        Plot one type of pie chart to represent the constitution
        of income or expenses

        Args:
            transaction_type (str): "income", "expense"
            graph_type (int): 1 for pie chart, 2 for donut chart, 
                            3 for ring chart, 4 for half-pie chart

        Raises:
            ValueError: invalid argument input for transaction_type
            ValueError: invalid argument input for graph_type
        """
        # Calculate totals by label
        label_totals = {'income': {}, 'expense': {}}
        for transaction in self.transactions:
            label_type = transaction['type']
            label = transaction['label']
            if label not in label_totals[label_type]:
                label_totals[label_type][label] = 0
            label_totals[label_type][label] += transaction['amount']

        # Store label composition
        percentage_composition = {
            'income': label_totals['income'], 'expense': label_totals['expense']}
        total_income = sum(label_totals['income'].values())
        for label, amount in label_totals['income'].items():
            percentage_composition['income'][label] = (
                amount / total_income) * 100
        total_expense = sum(label_totals['expense'].values())
        for label, amount in label_totals['expense'].items():
            percentage_composition['expense'][label] = (
                amount / total_expense) * 100

        # Plot a type of pie chart of income or expenses
        pie_chart = None
        try:
            graph_type = int(graph_type)
            if graph_type == 1:  # Pie
                pie_chart = pygal.Pie(print_values=True, style=DefaultStyle(
                    value_font_size=10), value_formatter=lambda x:  '%.2f%%' % float(x))
            elif graph_type == 2:  # Donut
                pie_chart = pygal.Pie(inner_radius=.4, print_values=True, style=DefaultStyle(
                    value_font_size=10), value_formatter=lambda x:  '%.2f%%' % float(x))
            elif graph_type == 3:  # Ring
                pie_chart = pygal.Pie(inner_radius=.75, print_values=True, style=DefaultStyle(
                    value_font_size=10), value_formatter=lambda x:  '%.2f%%' % float(x))
            elif graph_type == 4:  # Half-pie
                pie_chart = pygal.Pie(half_pie=True, print_values=True, style=DefaultStyle(
                    value_font_size=10), value_formatter=lambda x:  '%.2f%%' % float(x))
            else:
                raise ValueError(
                    "Please use pre-defined type code for graph_type")

            transaction_type = str(transaction_type)
            if transaction_type == "income":
                pie_chart.title = 'Constitution of income'
                for key, value in percentage_composition['income'].items():
                    pie_chart.add(key, value)
                display(SVG(pie_chart.render(disable_xml_declaration=True)))
            elif transaction_type == "expense":
                pie_chart.title = 'Constitution of expenses'
                for key, value in percentage_composition['expense'].items():
                    pie_chart.add(key, value)
                display(SVG(pie_chart.render(disable_xml_declaration=True)))
            else:
                raise ValueError(
                    "Please use pre-defined type code for transaction_type")
        except ValueError as v:
            print(f"Value Error: {v}")
