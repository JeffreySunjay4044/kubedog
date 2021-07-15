import datetime
import pytz


def get_age(created_time):
    current_time = datetime.datetime.now(tz=pytz.utc)
    return str(current_time - created_time)
