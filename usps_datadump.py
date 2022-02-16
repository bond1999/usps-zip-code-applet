import urllib.request
import pymysql

# Global Variables
url = "https://postalpro.usps.com/storages/2022-02/AREADIST_ZIP5_0.TXT"

# Function to get List of players belonging to country/{CC}, CC is the Country Code
def uspsDataDownloadNParse():
    response = urllib.request.urlopen(url)
    data = str(response.read(), 'UTF-8')
    lines = data.split('\r\n')
    lines.pop()                             # Getting rid of the last-empty element
    parser(lines);

def parser(lines):
    for line in lines:
        data = line.split()
        if len(data) > 5:
            data[2] = ' '.join(data[2:len(data)-2:1])
            while len(data) > 5:
                data.pop(3)
        print(data)

def createDatabaseWEntries(data):
    connection = pymysql.connect(host='localhost',user='root',password='root',database='classicmodels')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS usps_zip")
    create_table = """CREATE TABLE usps_zip ( 
             REGION  CHAR(20) NOT NULL PRIMARY KEY UNIQUE, 
             REGION_IND  int(2), 
             STATES_Z CHAR(20),
             PRE_ZIP  int(3), 
             ZIPCODE  int(5) NOT NULL) """
    cursor.execute(create_table)                            # Execute CREATE TABLE command





    connection.commit()
    connection.close()

# Main function to run the program
def main():
    uspsDataDownloadNParse()
    # createDatabaseNEntries()

# Run Program
main()



