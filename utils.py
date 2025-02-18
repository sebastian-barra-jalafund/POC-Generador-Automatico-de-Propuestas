import datetime

def validate_budget(budget_str):
    try:
        budget = float(budget_str)
        if budget <= 0:
            return False, "Budget must be greater than 0"
        return True, budget
    except ValueError:
        return False, "Please enter a valid number for budget"

def validate_date(date_str):
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        if date.date() < datetime.date.today():
            return False, "Date cannot be in the past"
        return True, date
    except ValueError:
        return False, "Invalid date format"

def format_currency(amount):
    return f"{amount:,.2f}"
