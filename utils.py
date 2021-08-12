def calculate_time_diff_in_hours(start_dt, end_dt):
    time_diff = end_dt - start_dt
    diff_in_hours = time_diff.total_seconds() / 3600
    return diff_in_hours