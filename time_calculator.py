def add_time(start, duration, starting_day=None):
    # Parse the start time
    start_time, period = start.split()
    start_hour, start_minute = map(int, start_time.split(':'))
    if period == 'PM':
        start_hour += 12  # Convert to 24-hour format

    # Parse the duration time
    duration_hour, duration_minute = map(int, duration.split(':'))

    # Calculate total minutes and convert to hours and days
    total_minutes = start_minute + duration_minute
    additional_hour = total_minutes // 60
    final_minutes = total_minutes % 60

    total_hours = start_hour + duration_hour + additional_hour
    final_hour = total_hours % 24
    days_later = total_hours // 24

    # Convert back to 12-hour format
    if final_hour >= 12:
        final_period = 'PM'
        display_hour = final_hour - 12 if final_hour > 12 else 12
    else:
        final_period = 'AM'
        display_hour = final_hour if final_hour != 0 else 12

    # Determine the day of the week if provided
    if starting_day:
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        starting_day_index = days_of_week.index(starting_day.capitalize())
        result_day_index = (starting_day_index + days_later) % 7
        result_day = days_of_week[result_day_index]
    else:
        result_day = None

    # Format the result string
    new_time = f"{display_hour}:{final_minutes:02d} {final_period}"
    if result_day:
        new_time += f", {result_day}"
    if days_later == 1:
        new_time += " (next day)"
    elif days_later > 1:
        new_time += f" ({days_later} days later)"

    return new_time

# Examples to test
print(add_time('3:00 PM', '3:10'))  # 6:10 PM
print(add_time('11:30 AM', '2:32', 'Monday'))  # 2:02 PM, Monday
print(add_time('11:43 AM', '00:20'))  # 12:03 PM
print(add_time('10:10 PM', '3:30'))  # 1:40 AM (next day)
print(add_time('11:43 PM', '24:20', 'tueSday'))  # 12:03 AM, Thursday (2 days later)
print(add_time('6:30 PM', '205:12'))  # 7:42 AM (9 days later)
