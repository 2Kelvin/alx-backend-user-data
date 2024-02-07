#!/usr/bin/env python3
'''Logging in python'''
from typing import List
import re
import logging

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    '''Redacting Formatter class'''

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str,
                 logMessage: str, separator: str) -> str:
    '''returns a log message'''
    for eachField in fields:
        logMessage = re.sub(
            f'{eachField}=.*?{separator}',
            f'{eachField}={redaction}{separator}', logMessage
        )
    return logMessage


def get_logger() -> logging.Logger:
    '''Returns a logger object'''
    userDataLogger = logging.getLogger('user_data')
    userDataLogger.setLevel(logging.INFO)
    userDataLogger.propagate = False
    userstreamHandler = logging.StreamHandler()
    userstreamHandler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    userDataLogger.addHandler(userstreamHandler)
    return userDataLogger
