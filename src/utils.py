from datetime import datetime


def now_date_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%I:%M %p")
