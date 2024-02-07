#!/usr/bin/env python3
'''Regex-ing'''
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''returns a log message'''
    pattern = r"(?<=" + separator + r")(?:{})(?=" + \
        separator + r")".format("|".join(fields))
    return re.sub(pattern, redaction, message)
