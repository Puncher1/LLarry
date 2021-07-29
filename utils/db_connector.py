import os
import mysql.connector
# end imports

def db_connect():
    """A function that connects to the database."""

    class ModLogDB:
        def __init__(self, connection, mycursor):
            self.connection = connection
            self.mycursor = mycursor

    modlog_db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        use_unicode=True
    )

    mycursor = modlog_db.cursor()
    return ModLogDB(modlog_db, mycursor)