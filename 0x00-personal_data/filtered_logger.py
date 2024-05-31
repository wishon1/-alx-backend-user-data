#!/usr/bin/env python3

"""
Module for handling sensitive user data and logging it in an obfuscated manner.
"""

import logging
import re
from typing import List
from os import getenv
import mysql.connector

# Fields that contain Personally Identifiable Information (PII)
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates PII fields in a log message.

    Args:
        fields (List[str]): The list of fields to obfuscate.
        redaction (str): The string to replace the PII data with.
        message (str): The log message containing PII data.
        separator (str): The character separating the fields in the
        log message.

    Returns:
        str: The obfuscated log message.
    """
    for row in fields:
        msg = re.sub(f'{row}=.*?{separator}', f'{row}={redaction}{separator}',
                     message)
    return msg


def get_logger() -> logging.Logger:
    """
    Configures and returns a logger object for logging user data.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Stream handler for logging
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes and returns a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.

    Raises:
        ValueError: If the database name is not set in the environment
        variables.
    """
    username = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = getenv('PERSONAL_DATA_HOST', 'localhost')
    db_name = getenv('PERSONAL_DATA_DB_NAME')

    if not db_name:
        raise ValueError("Database name must be set in the\
                         environment variable")

    db_session = mysql.connector.connection.MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return db_session


def main():
    """
    Main function to connect to the database, fetch user data, and log it.
    """
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    logger = get_logger()

    for row in rows:
        message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]};"
            f"password={row[4]}; ip={row[5]}; last_login={row[6]};"
            f"user_agent={row[7]};"
        )
        logger.info(message)

    cursor.close()
    db_connection.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """method for  initialization of class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """overides the default format method"""
        mssg = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            mssg, self.SEPARATOR)


if __name__ == "__main__":
    main()
