# usps-zip-code-database-dl-application

Developed for TrenData Texas as part of their training under UTD Capstone Project (Team 65)

This script accessed USPS.com to download, parse and store, ALL the ZIP Codes currently linked to the United States Postal Service's directory.



### Requirements

Python 3.10

MariaDB SQL Database or Any other SQL Server Database of your choice

PIP [Optional, to install dependencies]

### Install instructions

1. Download _usps_datadump.py_ and _requirements.txt_
2. Run `pip install -r requirements.txt` to install dependencies
3. Before running the script, change MYSQL server variables [host, user, password, database] and if you want data from a specific YYYY & MM,
    - Edit the script using Text Editor of your choice
    - Editable Variables are Listed on the top, under imports
4. To run the script, use `python usps_datadump.py`
