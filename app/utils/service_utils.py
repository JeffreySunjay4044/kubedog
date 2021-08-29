import datetime
import pytz
from flask import json


def get_age(created_time):
    """
    This method gets an object of datetime class as argument and returns the time difference between the time in
    argument and current time
    :param created_time:
    :return datetime in string format:
    """
    current_time = datetime.datetime.now(tz=pytz.utc)
    return str(current_time - created_time)


def get_json(object):
    """
    This method returns the input object as dictionary, so that it can be converted to json dump easily.
    :return __dict__ of input object
    """
    return json.dumps(object.__dict__)


def get_json_list(object_list):
    """
    This method converts the input list of objects to list of dictionary structure of the object for dumping as json
    :return list of __dict__
    """
    dict_list = []
    for obj in object_list:
        dict_list.append(obj.__dict__)
    return json.dumps(dict_list)
