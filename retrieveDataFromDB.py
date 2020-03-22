import sqlite3


def readSqliteTable(db_name, table_name, order_col):
    """
    Execute SQLite SELECT Query from Python application to retrieve data from the SQLite table.

    :param db_name: The name of the DataBase
    :param table_name: The name of the Table in <db_name>
    :param order_col: The name of the column to order selecter rows by

    :return: list of the selected rows
    """

    # init the empty array to store all the records from the table
    records = []

    try:
        # Open a connection to an SQLite database
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # Define the SQLite SELECT statement query (by default in chronological order)
        sqlite_select_query = "SELECT * FROM " + table_name + " ORDER BY " + order_col + ";"

        # Execute the SELECT query
        cursor.execute(sqlite_select_query)

        # Get rows from the cursor object
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))

        # Close the Cursor connection
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return records
