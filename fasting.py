import re

def parse_time(time_str, period=None):
    """
    Parse a time string in HH:MM format.
    If period is provided ('AM' or 'PM'), convert to 24-hour time.
    Returns the number of minutes since midnight.
    """
    # Validate the basic pattern HH:MM
    if not re.match(r'^\d{1,2}:\d{2}$', time_str):
        raise ValueError("Time must be in HH:MM format.")
    hours, minutes = map(int, time_str.split(':'))
    if hours < 0 or minutes < 0 or minutes >= 60:
        raise ValueError("Invalid time. Hours must be non-negative and minutes between 0 and 59.")

    # If using 12-hour format with period indicator
    if period:
        period = period.upper()
        if period not in ["AM", "PM"]:
            raise ValueError("Period must be either AM or PM.")
        if hours > 12 or hours < 1:
            raise ValueError("For 12-hour format, hours must be between 1 and 12.")
        if period == "PM" and hours != 12:
            hours += 12
        elif period == "AM" and hours == 12:
            hours = 0

    else:
        # For 24-hour format, hours must be between 0 and 23.
        if hours > 23:
            raise ValueError("For 24-hour format, hours must be between 0 and 23.")

    return hours * 60 + minutes

def format_time(total_minutes, use_12_hour=False):
    """
    Format minutes-since-midnight to a time string.
    If use_12_hour is True, returns a string in 12-hour format with AM/PM.
    """
    # Normalize to 0-1439 range for display purposes.
    normalized = total_minutes % 1440
    hours = normalized // 60
    minutes = normalized % 60

    if use_12_hour:
        period = "AM" if hours < 12 else "PM"
        display_hour = hours % 12
        display_hour = 12 if display_hour == 0 else display_hour
        return f"{display_hour:02}:{minutes:02} {period}"
    else:
        return f"{hours:02}:{minutes:02}"

def calculate_fasting_start(current_time_str, meal_time_str, fasting_duration_hours,
                            current_period=None, meal_period=None, use_12_hour_output=False):
    """
    Calculates the upcoming fasting start time.
    current_time_str, meal_time_str: strings in HH:MM format.
    current_period and meal_period: optional; if provided, expect "AM"/"PM" for 12-hour format.
    fasting_duration_hours: a positive number representing hours.
    Returns a tuple: (formatted fasting start time, day label: "today" or "tomorrow").
    """
    # Convert input times into minutes-since-midnight.
    current_minutes = parse_time(current_time_str, current_period)
    meal_minutes = parse_time(meal_time_str, meal_period)
    fasting_duration_minutes = int(fasting_duration_hours * 60)

    # Determine the absolute meal time in minutes.
    # Assume current day starts at minute 0.
    # If the meal time (today) is not later than current time or the fasting start would be in the past,
    # assume the meal is on the next day.
    if meal_minutes <= current_minutes:
        meal_absolute = meal_minutes + 1440
    else:
        meal_absolute = meal_minutes

    fasting_start = meal_absolute - fasting_duration_minutes

    # If the fasting start time is still not in the future relative to current time,
    # then assume the meal is on the next day.
    if fasting_start <= current_minutes:
        meal_absolute += 1440
        fasting_start = meal_absolute - fasting_duration_minutes

    # Determine the day label relative to today.
    # Day number 0 means today; 1 means tomorrow.
    day_num = fasting_start // 1440
    if day_num == 0:
        day_label = "today"
    elif day_num == 1:
        day_label = "tomorrow"
    else:
        # For completeness, if it's more than one day ahead.
        day_label = f"in {day_num} days"

    fasting_start_str = format_time(fasting_start, use_12_hour_output)
    return fasting_start_str, day_label

def get_input(prompt):
    """Helper to get non-empty input."""
    value = input(prompt).strip()
    while not value:
        value = input("Input cannot be empty. " + prompt).strip()
    return value

def main():
    print("Welcome to the Fasting Start Time Calculator!\n")
    print("Please enter times in HH:MM format. For 12-hour format, you will also be prompted for AM/PM.\n")

    # Ask the user if they prefer 12-hour or 24-hour input.
    format_choice = get_input("Enter 1 for 12-hour format or 2 for 24-hour format: ")
    use_12_hour_input = format_choice == "1"

    try:
        # Get current time.
        current_time_str = get_input("Enter the current time (HH:MM): ")
        current_period = None
        if use_12_hour_input:
            current_period = get_input("Enter the period for current time (AM/PM): ")

        # Get meal time.
        meal_time_str = get_input("Enter your next meal time (HH:MM): ")
        meal_period = None
        if use_12_hour_input:
            meal_period = get_input("Enter the period for meal time (AM/PM): ")

        # Get fasting duration in hours.
        fasting_duration_input = get_input("Enter the number of hours you want to fast before the meal: ")
        fasting_duration = float(fasting_duration_input)
        if fasting_duration <= 0:
            raise ValueError("Fasting duration must be a positive number.")

    except ValueError as ve:
        print(f"Input error: {ve}")
        return

    # Calculate the fasting start time.
    fasting_start, day_label = calculate_fasting_start(current_time_str, meal_time_str,
                                                       fasting_duration,
                                                       current_period, meal_period,
                                                       use_12_hour_output=use_12_hour_input)
    print(f"\nYou should start fasting at {fasting_start} {day_label}.")

if __name__ == "__main__":
    main()
