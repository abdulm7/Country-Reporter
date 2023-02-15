# Abdul Mahmoud
# 1093276
# Jan 21, 2023
# CIS*4010
# Assignment #2
# DynamoDB Assignment

#!/usr/bin/env python3
# Modules
import configparser
import os 
import sys 
import pathlib
import boto3
import csv
import db_functions as dbf
import json
from boto3.dynamodb.conditions import Key, Attr

# table names
NON_ECON = 'non-econ'
ECON = 'econ'

MIN_YEAR = 1960
MAX_YEAR = 2030

def main():
    #
    #  Find AWS access key id and secret access key information
    #  from configuration file
    #
    config = configparser.ConfigParser()
    config.read("S5-S3.conf")
    aws_access_key_id = config["default"]["aws_access_key_id"]
    aws_secret_access_key = config["default"]["aws_secret_access_key"]

    try:

        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        db = session.resource('dynamodb', region_name='ca-central-1')
        db_client = session.client('dynamodb', region_name='ca-central-1')

        print('Connected to DynamoDB!')

        cmd = ""

        # menu / command options
        while cmd.lower() != "quit" and cmd.lower() != "exit" and cmd != '10':
            print("""Menu Options: 
  1. Create DB Tables (Economic & Non-Economic)
  2. Delete All Tables
  3. Load all records from CSV files
  4. Add individual record into a table
  5. Delete individual record from a table
  6. Display a specific table
  7. Create Report A (Country Level)
  8. Create Report B (Global Level)
  9. Add missing information
  10. Quit/Exit""")

            cmd = input("Enter a number: ")
            
            if ( cmd == '1'):
                necon_exist = dbf.check_exists(db_client, NON_ECON)
                econ_exist = dbf.check_exists(db_client, ECON)

                print('\tLoading... (This might take a minute)')

                if necon_exist == False:
                    ret = dbf.create_table(db, NON_ECON, 'country', 'S')
                    if ret == True:
                        print('\tNon-Economic Table successfully created!')
                else:
                    print('\tERROR: table already exists.')

                if econ_exist == False:
                    ret = dbf.create_table(db, ECON, 'country', 'S')
                    if ret == True:
                        print('\tEconomic Table successfully created!')
                else:
                    print('\tERROR: table already exists.')

            elif (cmd == '2'):
                necon_exist = dbf.check_exists(db_client, NON_ECON)
                econ_exist = dbf.check_exists(db_client, ECON)

                print('\tLoading... (This might take a minute)')

                if necon_exist:
                    ret = dbf.delete_table(db, NON_ECON)
                    if ret == True:
                        print("\tSuccessfully delete the Non-Economic ('non-econ') table!")
                else:
                    print('\tERROR: table does not exist')

                if econ_exist:
                    ret = dbf.delete_table(db, ECON)
                    if ret == True:
                        print("\tSuccessfully delete the Economic ('econ') table!")
                else:
                    print('\tERROR: table does not exist')
            elif (cmd == '3'):

                necon_exist = dbf.check_exists(db_client, NON_ECON)
                econ_exist = dbf.check_exists(db_client, ECON)

                print('\tLoading... (This might take a minute)')

                # creating tables
                tables = dbf.create_tables_dict("un_shortlist.csv", "shortlist_area.csv", "shortlist_capitals.csv", 'shortlist_curpop.csv', 'shortlist_languages.csv', 'shortlist_gdppc.csv')
                
                # print(tables[NON_ECON])
                # loading tables into db
                if tables[NON_ECON] != False and necon_exist:
                    dbf.load_tables(db, NON_ECON, tables[NON_ECON])
                    print("\tSuccessfully loaded Non-economic data into 'non-econ' table")
                else:
                    if (necon_exist == False):
                        print("\tERROR: You must create the tables before loading data (Option #1)")
                    else:
                        print("\tERROR: Could not process non-economic files. (Check file names/structure)")
                
                if tables[ECON] != False and econ_exist:
                    dbf.load_tables(db, ECON, tables[ECON])
                    print("\tSuccessfully loaded Economic data into 'econ' table")
                else:
                    if (econ_exist == False):
                        print("\tERROR: You must create the tables before loading data (Option #1)")
                    else:
                        print("\tERROR: Could not process economic files. (Check file names/structure)")
            elif (cmd == '6'):
                valid = False
                choice = 0

                while choice != 1 and choice != 2:
                    print("Which table would you like to display?")
                    print("  1. Non-economic")
                    print("  2. Economic")
                    try:
                        choice = int(input('Select a number: '))
                    except:
                        choice = 0 

                    if choice == 1:
                        try:
                            table = db.Table(NON_ECON)
                            items = table.scan()
                        
                            print(dbf.print_non_econ(items))
                        except:
                            print("\tERROR: Non-economic table does not exist in the database.")


                    elif choice == 2:
                        # printing economic table
                        try:
                            table = db.Table(ECON)
                            items = table.scan()

                            print(dbf.print_econ(items))
                        except:
                            print("\tERROR: Economic table does not exist in the database.")
            
                    else:
                        print("\tERROR: Invalid choice")

            # elif (cmd == '5'):

            #         t = db.Table(NON_ECON)

            #         res = t.delete_item(
            #             Key = {
            #                 'population': "1970"
            #             }
            #         )

            #         print()
            
            elif (cmd == '7'):
                # create report
                print(dbf.create_report_a(db, 'Bosnia and Herzegovina'))
            

    except Exception as e:
        print("ERROR: " + str(e))

main()

    



