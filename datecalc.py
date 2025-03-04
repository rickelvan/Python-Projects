from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calculate_new_date(years, start_date=None):
    # If no start date is given, use today's date
    if start_date is None:
        start_date = datetime.today()
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    # Calculate new date by adding/subtracting the number of years
    new_date = start_date + relativedelta(years=years)
    
    return new_date.strftime("%Y-%m-%d")

# User input
years = int(input("Enter the number of years (negative for past, positive for future): "))
custom_date = input("Enter the start date (YYYY-MM-DD) or press Enter to use today: ")

# Compute the new date
result_date = calculate_new_date(years, custom_date if custom_date else None)

print(f"New Date: {result_date}")
