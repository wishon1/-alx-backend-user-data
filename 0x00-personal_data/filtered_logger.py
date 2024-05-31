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


def get_logger() -> logging.Logger:
    """function that takes no arguments and returns a logging.Logger object."""
    logger  = logging.getlogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    return logger.addHandler(stream_handler)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connection to the database"""
    user_name = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    user_password = os.getenv('PERSONAL_DATA_HOST', 'localhost')
    db_host = os.getenv('PERSONAL_DATA_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    if not user_name:
        raise ValueError("name must be set in the environment variable")

    connection_seesion = mysql.connection.connect(
        user=user_name,
        password=user_password,
        host=db_host,
        database=db_name
    )
    return connection_session


def main():
    """connect to the database"""
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    logger = get_logger()
    for row in rows:
        original_message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]};"
            f"password={row[4]}; ip={row[5]}; last_login={row[6]};"
            f" user_agent={row[7]};"
        )
        logger.info(original_message)
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
