#!/usr/bin/env python3
"""importing the necessary modules"""
import logging
import re
from typing import List
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Doc string for the initialization"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        # NotImplementedError
        """This function overides the default format method"""
        message = super().format(record)
        redacted_message = filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)
        return redacted_message


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """function that returns the log message obfuscated:"""
    pattern = '|'.join([f'{field}=.*?(?={separator}|$)' for field in fields])
    return re.sub(pattern, lambda m:
                  f"{m.group(0).split('=')[0]}={redaction}", message)


def get_logger() -> logging.Logger:
    """function takes no arguments and returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ function that returns a connector to the database"""
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    if not db_name:
        raise ValueError("name must be set in the environment variable")

    conn = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )
    return conn


def main():
    """connect to the database"""
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    logger = get_logger()
    for row in rows:
        message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]};"
            f"password={row[4]}; ip={row[5]}; last_login={row[6]};"
            f" user_agent={row[7]};"
        )
        logger.info(message)
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
