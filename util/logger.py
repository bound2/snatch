import logging
import datetime
from enum import Enum


class Level(Enum):
    INFO = 1,
    WARN = 2,
    ERROR = 3


def log(file_name, message, level=Level.INFO, console=True):
    logging.basicConfig(filename='application.log', level=logging.DEBUG)
    current_time = str(datetime.datetime.now())
    log_message = '{:s} {:s} {:s}'.format(current_time, file_name, message)
    if level == Level.INFO:
        logging.info(log_message)
    elif level == Level.WARN:
        logging.warn(log_message)
    elif level == Level.ERROR:
        logging.error(log_message)

    if console is True:
        print log_message
