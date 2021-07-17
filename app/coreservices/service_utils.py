import datetime
import pytz


def get_age(created_time):
    """
    This method gets an object of datetime class as argument and returns the time difference between the time in
    argument and current time
    :param created_time:
    :return datetime in string format:
    """
    current_time = datetime.datetime.now(tz=pytz.utc)
    return str(current_time - created_time)
