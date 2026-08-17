import os

import mysql.connector
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv(override=True)


def get_mysql_connection():
    """
    Create and return a connection to the MySQL source database.
    """

    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )

        print("Connected to MySQL successfully!")
        return conn

    except mysql.connector.Error as e:
        print("Connection failed!")
        print(e)
        return None


def get_connection():
    """
    Backward-compatible connection function.

    Existing extraction scripts use get_connection(),
    while newer code can use get_mysql_connection().
    """

    return get_mysql_connection()


if __name__ == "__main__":
    get_mysql_connection()