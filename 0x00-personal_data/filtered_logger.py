#!/usr/bin/env python3
"""0. Regex-ing"""
import re
import logging
from typing import List


# PII fields to be redacted
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """method for initialization of the class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format the specific record as text and filter, values in incoming
        log record using filter_datum
        """
        original_msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, original_msg,
                            self.SEPARATOR)


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    function called filter_datum that returns the log message obfuscated:
    Arguments:
        1. fields: a list of strings representing all fields to obfuscate
        2. redaction: a string representing by what the field will be
                    obfuscated
        3. message: a string representing the log line
        4. separator: a string representing by which character is
                    separating all fields in the log line (message)

    Returns:  returns the log message obfuscated:
    """
    for string in fields:
        re_pattern = re.sub(f'{string}=.*?{separator}',
                            f'{string}={redaction}{separator}', message)
    return re_pattern
