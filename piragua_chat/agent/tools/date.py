import datetime


def get_todays_date() -> str:
    today = datetime.datetime.now()
    return f"Hoy es {today.strftime('%A')}, {today.strftime('%Y-%m-%d')}"
