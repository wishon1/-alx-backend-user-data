#!/usr/bin/env python3
"""0. Regex-ing"""
import re


def filter_datum(fields: str,
                 redaction: str,
                 message: str,
                 separator: str):
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
    # Each field pattern is of the form 'field=[^separator]+',
    # where the value is anything except the separator
    re_pattern = '|'.join(f'{field}=[^ {separator}]+' for field in fields)

    # Use re.sub to replace all occurrences of the fields' values with the
    # redaction string The lambda function replaces the field value while
    # keeping the field name intact
    return re.sub(re_pattern,
                  lambda m: f"{m.group().split('=')[0]}={redaction}", message)
