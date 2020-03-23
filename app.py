from flask import Flask, render_template, request
from ingestFileToDB import getColumnsFromXML
from retrieveDataFromDB import readSqliteTable


app = Flask(__name__)


@app.route("/")
def index():
    # Display the Bioinformatics posts (in chronological order) from the table in SQLite

    # Define names of database, table and the column to order rows by
    DB_NAME = "bioposts.db"
    TABLE_NAME = "bioinformatics_posts"

    # Get the "sorting" URL argument
    sorting_column = request.args.get("sorting")

    # Get the columns names from the XML file
    pathToFile = "./dataset/bioinformatics_posts_se.xml"
    list_columns, _ = getColumnsFromXML(pathToFile)

    # Sort rows based on the input argument "sorting" including "Score" & "ViewCount"
    if sorting_column in list_columns:
        ORDER_COL = sorting_column
    else:
        # Default sorting value - chronological order
        ORDER_COL = "CreationDate"

    # Query the DB to get all the posts in the specified order
    records = readSqliteTable(db_name=DB_NAME, table_name=TABLE_NAME, order_col=ORDER_COL)

    # Get the "search" URL argument
    search_keyword = request.args.get("search")

    # Store records that contain searched keyword in array
    recordsWithKeyword = []

    # Check that the search_keyword is provided
    if search_keyword is not None:
        for record in records:
            # Check if the search_keyword is present in title(12th column) or body(5th column) of each post
            if search_keyword in record[12] or search_keyword in record[5]:
                recordsWithKeyword.append(record)
        # Update the records to display
        records = recordsWithKeyword

    # render the template with the columns and data
    return render_template("tables.html", list_columns=list_columns, records=records)
