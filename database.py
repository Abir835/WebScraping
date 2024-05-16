import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()


def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user=os.getenv("user"),
        password=os.getenv("password"),
        database="webscraping"
    )
