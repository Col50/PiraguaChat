import datetime


def get_todays_date() -> str:
    today = datetime.datetime.now()
    return {
        "year": today.year,
        "month": today.month,
        "day": today.day,
        "dayOfTheWeek": today.strftime("%A"),
    }
