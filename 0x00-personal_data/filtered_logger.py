#!/usr/bin/env python3
"""This script imports necessary modules and defines a logging framework
with redaction for personal identifiable information (PII), connects to a
database, fetches user data, and logs the data with sensitive fields redacted.
"""

import logging
import re
from typing import List
import os
import mysql.connector


# List of fields containing personal identifiable information to be redacted
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for logging, which
    redacts specified PII fields.
    """

    # Placeholder for redaction
    REDACTION = "***"
    # Format of the log messages
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    # Separator used in log messages
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the RedactingFormatter with fields to redact.

        Args:
            fields (List[str]): List of PII fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Override the default format method to redact PII fields in the log
        record.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record with PII fields redacted.
        """
        # Get the original formatted message
        msg = super().format(record)

        # Redact the sensitive fields in the message
        redacted_msg = filter_datum(
            self.fields, self.REDACTION, msg, self.SEPARATOR)
        return redacted_msg


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Redact sensitive fields in a log message.

    Args:
        fields (List[str]): List of fields to redact.
        redaction (str): Redaction string.
        message (str): Original log message.
        separator (str): Separator used in the log message.

    Returns:
        str: The log message with sensitive fields redacted.
    """
    # Create a regex pattern to find each field and replace its value
    # with the redaction
    r_p = '|'.join([f'{field}=.*?(?={separator}|$)' for field in fields])
    return re.sub(r_p, lambda m: f"{m.group(0).split('=')[0]}={redaction}",
                  message)


def get_logger() -> logging.Logger:
    """Create and configure a logger.

    Returns:
        logging.Logger: Configured logger with redacting formatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a stream handler for the logger
    stream_handler = logging.StreamHandler()

    # Set the redacting formatter for the handler
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Establish and return a connection to the database.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection.
    """
    # Get database connection details from environment variables
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    if not db_name:
        raise ValueError("Database name must be set in the environment
                         variable")

    # Create and return a connection to the database
    connection_session = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return connection_session


def main():
    """
    Connect to the database, fetch user data, and log the data with
    redacted PII.
    """
    # Get a database connection
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Get the logger
    logger = get_logger()

    for row in rows:
        # Format the log message with user data
        message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]};"
            f"password={row[4]}; ip={row[5]}; last_login={row[6]};"
            f"user_agent={row[7]};"
        )
        # Log the message
        logger.info(message)

    # Close the cursor and database connection
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
