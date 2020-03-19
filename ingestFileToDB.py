import sqlite3
import xml.etree.ElementTree as ET
from preprocessingText import cleaning_data


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


def ingestDataToTable(sqliteConnection, cursor, list_columns, xmlRoot):
    """
    Insert Data from bioinformatics_posts_se.xml file into Table "bioinformatics_posts".
    Perform bulk insert operation in a single query.

    :param sqliteConnection: connection object to SQLite Database
    :param cursor: cursor object
    :param list_columns: all possible columns from the XML file - bioinformatics_posts_se.xml
    :param xmlRoot: root element of XML file
    :return: cursor object
    """
    try:
        # Construct sql statement
        sqlite_insert_query = "INSERT INTO bioinformatics_posts ("

        # Specify all column names after the table name
        for column in list_columns:
            sqlite_insert_query += column + ", "

        # Cut the last ", " and add further SQL keywords
        sqlite_insert_query = sqlite_insert_query[: -2] + ") " + "\nVALUES ("

        # Create placeholders (?) for every column value used in parameterized query
        for i in range(len(list_columns)):
            sqlite_insert_query += "?, "

        # Cut the last ", " and add further SQL keywords
        sqlite_insert_query = sqlite_insert_query[: -2] + ");"

        # Create array where all rows from XML file are stored
        recordsToInsert = list()

        # Specify all values after the VALUES keyword
        for child in xmlRoot:
            # Store VALUES from current row in array
            row_values = []
            for attribute in list_columns:
                # Check if current row has all needed columns
                if attribute in child.attrib:
                    if attribute == "Id":
                        # Set INTEGER type for "Id" value
                        row_values.append(int(child.attrib[attribute]))
                    elif attribute == "Body":
                        # Do preprocessing of text in "body" field
                        row_values.append(cleaning_data(child.attrib[attribute]))
                    else:
                        row_values.append(child.attrib[attribute])
                # if some columns in a row are missing, set to None
                else:
                    row_values.append("None")

            recordsToInsert.append(tuple(row_values))

        # add multiple records into the SQLite table
        cursor.executemany(sqlite_insert_query, recordsToInsert)

        # Commit current transaction
        sqliteConnection.commit()

        print("Total", cursor.rowcount, "Records inserted successfully into bioinformatics_posts table")
        # sqliteConnection.commit()

        return cursor

    except sqlite3.Error as error:
        print("Failed to insert multiple records into sqlite table", error)
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

    # INSERT rows from XML file into created table
    cursor = ingestDataToTable(sqliteConnection, cursor, list_columns=all_columns, xmlRoot=root)

    # Close the connection to database
    cursor.close()
    sqliteConnection.close()


if __name__ == "__main__":
    main()
