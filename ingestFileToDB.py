import sqlite3
import xml.etree.ElementTree as ET


def createTableDB(sqliteConnection, list_columns):
    """
    Create Table in SQLite Database to store data from bioinformatics_posts_se.xml file.

    :param sqliteConnection: connection object to SQLite Database
    :param list_columns: all possible columns from the XML file - bioinformatics_posts_se.xml
    :return: cursor object
    """
    try:
        # Create cursor object to execute SQLite queries
        cursor = sqliteConnection.cursor()

        # Construct sql statement
        sqlite_create_table_query = "CREATE TABLE bioinformatics_posts ("

        for column_name in list_columns:
            # Set INTEGER type to column "Id" & make a primary key
            if column_name == "Id":
                sqlite_create_table_query += column_name + " INTEGER" + " PRIMARY KEY" + ","
            else:
                sqlite_create_table_query += column_name + " TEXT" + ","

        # Cut the last "," and add proper ending to sql statement
        sqlite_create_table_query = sqlite_create_table_query[: -1] + ");"

        # Execute a database operation
        cursor.execute(sqlite_create_table_query)
        # Commit current transaction
        sqliteConnection.commit()

        print("SQLite table created successfully")

        return cursor

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
        cursor.close()
        sqliteConnection.close()
        print("SQLite connection is closed")


def main():
    # Relative path to the XML file
    pathToFile = "./dataset/bioinformatics_posts_se.xml"

    # Read in the xml file with ElementTree
    tree = ET.parse(pathToFile)
    root = tree.getroot()

    # Store columns keeping the order
    all_columns = []

    # Iterate over all elements in xml
    for child in root:
        # Store column name in array keeping the order and its uniqueness
        for attribute in child.attrib:
            if attribute not in all_columns:
                all_columns.append(attribute)

    # Open a connection to an SQLite database
    sqliteConnection = sqlite3.connect("bioposts.db")

    print("Successfully Connected to SQLite")

    # Create table in SQLite
    cursor = createTableDB(sqliteConnection, list_columns=all_columns)

    # Close the connection to database
    cursor.close()
    sqliteConnection.close()


if __name__ == "__main__":
    main()
