#!/usr/bin/env python3
"""0. Regex-ing"""
import re
import logging
from typing import List
import os
import mysql.connector

# PII fields to be redacted
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    # Placeholder for redaction
    REDACTION = "***"
    # Format of the log messages
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    # Separator used in log messages
    SEPARATOR = ";"

    def __init__(self, fields):
        """Initialize the RedactingFormatter with specific fields to redact"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, redacting specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record with sensitive fields redacted.
        """
        # Get the original formatted message
        original_msg = super(RedactingFormatter, self).format(record)

        # Redact the sensitive fields in the message
        return filter_datum(self.fields, self.REDACTION, original_msg,
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Redact sensitive fields in a log message.

    Args:
        fields (List[str]): Fields to redact.
        redaction (str): Redaction string.
        message (str): Original log message.
        separator (str): Separator used in the log message.

    Returns:
        str: The log message with sensitive fields redacted.
    """
    for field in fields:
        # Create a regex pattern to find the field and replace its value with
        # the redaction
        re_pattern = re.sub(f'{field}=.*?{separator}',
                            f'{field}={redaction}{separator}', message)
    return re_pattern


def get_logger() -> logging.Logger:
    """
    Create and configure a logger.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a stream handler for the logger
    stream_handler = logging.StreamHandler()

    # Set the formatter for the handler
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establish and return a connection to the database.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection.
    """
    # Get database connection details from environment variables
    user_name = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    user_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    if not user_name:
        raise ValueError("Database username must be set in the environment
                         variable")

    # Create a connection to the database
    connection_session = mysql.connector.connect(
        user=user_name,
        password=user_password,
        host=db_host,
        database=db_name
    )
    return connection_session


def main():
    """
    Main function to connect to the database and log user data with
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
        original_message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]};"
            f"password={row[4]}; ip={row[5]}; last_login={row[6]};"
            f"user_agent={row[7]};"
        )
        # Log the message
        logger.info(original_message)

    # Close the cursor and database connection
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
