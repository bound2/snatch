import logging
from enum import Enum


class Level(Enum):
    INFO = 1,
    WARN = 2,
    ERROR = 3


_FORMAT = '%(asctime)-15s %(file_name)-8s %(message)s'


def log(file_name, message, level=Level.INFO, console=True):
    logging.basicConfig(filename='application.log', format=_FORMAT, level=logging.DEBUG)
    params = {'file_name': file_name}
    if level == Level.INFO:
        logging.info(message, extra=params)
    elif level == Level.WARN:
        logging.warn(message, extra=params)
    elif level == Level.ERROR:
        logging.error(message, extra=params)

    if console is True:
        print '{:s}: {:s}'.format(file_name, message)
