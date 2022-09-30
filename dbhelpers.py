from tkinter import EXCEPTION
import dbcreds
import mariadb


def connect_db():
    try:
        conn = mariadb.connect(password=dbcreds.pasword, user=dbcreds.user,
                               host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        return cursor
    except mariadb.OperationalError as error:
        print("Operational ERROR:", error)
    except EXCEPTION as error:
        print("Unknown ERROR:", error)


def execute_statement(cursor, statement, list_of_args=[]):
    try:
        cursor.execute(statement, list_of_args)
        result = cursor.fetchall()
        return result
    except mariadb.ProgrammingError as error:
        print("Programming ERROR: ", error)
    except mariadb.IntegrityError as error:
        print("Integrity ERROR: ", error)
    except mariadb.DatabaseError as error:
        print("Data ERROR: ", error)
    except Exception as error:
        print("Unexpected ERROR: ", error)


def close_connect(cursor):
    try:
        conn = cursor.connection
        cursor.close()
        conn.close()
    except mariadb.OperationalError as error:
        print("Operational ERROR: ", error)
    except mariadb.InternalError as error:
        print("Internal ERROR: ", error)
    except Exception as error:
        print("Unexpected ERROR: ", error)
