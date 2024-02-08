#!/usr/bin/env python3
'''Logging in python'''
from typing import List
import re
import logging
import mysql.connector
from os import environ

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
                 message: str, separator: str) -> str:
    '''returns a log message'''
    for eachField in fields:
        logMessage = re.sub(f'{eachField}=.*?{separator}',
                            f'{eachField}={redaction}{separator}', message)
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


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''connect to a database constaining user credentials'''
    usrName = environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    pswrd = environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    theHost = environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db = environ.get('PERSONAL_DATA_DB_NAME')

    dbConnection = mysql.connector.connection.MySQLConnection(
        user=usrName,
        password=pswrd,
        host=theHost,
        database=db
    )
    return dbConnection


def main():
    '''get into database, retrieve and display the data'''
    database = get_db()
    cursor = database.cursor()
    cursor.execute('SELECT * FROM  users;')
    fieldNames = [fName[0] for fName in cursor.description]
    theLogger = get_logger()
    for eachRow in cursor:
        rowStr = ''.join(f'{f}={str(r)}; ' for r,
                         f in zip(eachRow, fieldNames))
        theLogger.info(rowStr.strip())
    cursor.close()
    database.close()


if __name__ == '__main__':
    main()
