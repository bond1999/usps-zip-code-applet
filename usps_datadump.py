import urllib.request
import urllib.error
import pymysql
import datetime

# Editable Variable: Change these before running the program!
host = 'localhost'
user = 'root'
password = 'root'
database = 'classicmodels'
table_name = "usps_data"            # You do NOT need to create a new table, just the database
use_custom_url = False              # Set this to True if you want to specify a certain YYYY & MM to grab the Zip Code Listing for, and change custom_url variable
custom_url = "https://postalpro.usps.com/storages/YYYY-MM/AREADIST_ZIP5"  # Change YYYY & MM to required Year and Month in the given format (eg. 2022-02)

# Global Variables
url = "https://postalpro.usps.com/storages/" + f"{datetime.datetime.today().year:02d}" + "-" + f"{datetime.datetime.today().month:02d}" + "/AREADIST_ZIP5"


# Function to get download zip codes listing from USPS.com
def uspsDataDownload():
    # Connect to USPS.com to download Zip Code Data with Error Handling
    print("CONNECTING TO USPS.COM (1/2 ATTEMPTS)")
    if use_custom_url:  # Using Custom URL
        try:
            response = urllib.request.urlopen(custom_url + "_0.TXT")
            parser(response)
        except urllib.error.HTTPError:
            print("CUSTOM URL WAS INVALID! (ATTEMPT 1/2)\n")
            print("RE-TRYING WITH ALTERNATIVE URL...")
            try:
                response = urllib.request.urlopen(custom_url + ".TXT")
                parser(response)
            except urllib.error.HTTPError:
                print("CUSTOM URL WAS INVALID! (ATTEMPT 2/2)")
    else:  # Using Default URL
        try:
            response = urllib.request.urlopen(url + "_0.TXT")
            parser(response)
        except urllib.error.HTTPError:
            print("DEFAULT URL WAS INVALID! (ATTEMPT 1/2)\n")
            print("RE-TRYING WITH ALTERNATIVE URL...")
            try:
                response = urllib.request.urlopen(url)
                parser(response)
            except urllib.error.HTTPError:
                print("DEFAULT URL WAS INVALID! (ATTEMPT 2/2)\n")

# Function to parse the HTTP response into a Python List
def parser(response):
    print("SUCCESSFULLY CONNECTED TO USPS.COM\n")
    data = str(response.read(), 'UTF-8').split('\r\n')
    data.pop()  # Getting rid of the last-empty element

    # Parsing data to even out values
    for index, value in enumerate(data):
        data[index] = value.split()
        if len(data[index]) > 5:
            data[index][2] = ' '.join(data[index][2:len(data[index]) - 2:1])
            while len(data[index]) > 5:
                data[index].pop(3)
    print("DATA DUMP DOWNLOADED & PARSED")

    # print(data)                             # Output Data to console (Debugging)
    createDatabaseWEntries(data)

# Function to connect to MariaDB SQL Database and Create Database With Entries
def createDatabaseWEntries(data):
    print("CONNECTING TO MYSQL DATABASE")
    # Connect to MySQL database
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = connection.cursor()
    print("DATABASE LINK ESTABLISHED!\n")

    # Delete previous table and Create new table template called "usps_zip"
    cursor.execute("DROP TABLE IF EXISTS " + table_name)
    print("TABLE " + table_name + " DELETED")

    create_table = "CREATE TABLE " + table_name + """ ( 
             REGION  CHAR(20) NOT NULL, 
             REGION_IND  char(2) NOT NULL, 
             STATES_Z CHAR(20) NOT NULL,
             PRE_ZIP  char(3) NOT NULL, 
             ZIPCODE  int(5) PRIMARY KEY UNIQUE) NOT NULL"""
    cursor.execute(create_table)  # Execute CREATE TABLE command
    print("TABLE " + table_name + " CREATED\n")

    # Data Entry
    print("DATA ENTRY STARTED IN TABLE " + table_name + ", PLEASE WAIT... ")
    for entry in data:
        table_entry = "INSERT INTO " + table_name + " VALUES ('" + str(entry[0]) + "', '"
        table_entry += str(entry[1]) + "', '" + str(entry[2]) + "', '" + str(entry[3]) + "', '"
        table_entry += str(entry[4]) + "')"
        cursor.execute(table_entry)
    print("DATA ENTRY FINISHED WITH " + str(len(data)) + " ENTRIES!")

    connection.commit()
    connection.close()


# Main function to run the program
def main():
    uspsDataDownload()  # Calls createDatabaseNEntries from within
    print("\nCODE STOPPED RUNNING")


# Run Program
main()
