
def calculate_fee(issue_date, return_date):
    duration = (return_date - issue_date).days

    daily_fee = 50
    if duration <= 0:
        return 0
    else:
        return duration * daily_fee