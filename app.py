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
    ORDER_COL = "CreationDate"

    # Query the DB to get all the posts in chronological order
    records = readSqliteTable(db_name=DB_NAME, table_name=TABLE_NAME, order_col=ORDER_COL)

    # Get the columns names from the XML file
    pathToFile = "./dataset/bioinformatics_posts_se.xml"
    list_columns, _ = getColumnsFromXML(pathToFile)

    # render the template with the columns and data
    return render_template("tables.html", list_columns=list_columns, records=records)
