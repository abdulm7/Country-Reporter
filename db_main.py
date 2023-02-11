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
        db = boto3.resource('dynamodb')
    
    except Exception as e:
        print("ERROR: " + e)

# reads the "shortlist_curpop.csv" file
# prepares 'json/python dict' to as table for db
def read_curpop_file(filename):
    first = True
    header = []
    cntryCurTable = []
    cntryYearPopTable = []
    with open(filename, 'r', encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            if first:
                header = row
                first = False
            else:
                curCntry = row[0]
                for i in range(1, len(row), 1):
                    if i == 1:
                        cntryCurTable.append({'country': curCntry, 'currency': row[i]})
                    else:
                        cntryYearPopTable.append({'country': curCntry, 'year': header[i], 'population': row[i]})

# 
def read_countries(names_file, area_file, capitals_file):
    first = True
    header = []
    name_info = []
    fNames = open(names_file, 'r', encoding="utf-8-sig")
    fArea = open(area_file, 'r', encoding="utf-8-sig")
    fCapitals = open(capitals_file, 'r', encoding="utf-8-sig")
    
    rNames = list(csv.reader(fNames))
    rArea = list(csv.reader(fArea))
    rCapitals = list(csv.reader(fCapitals))

    headNames = rNames[0]
    headArea = rArea[0]
    headCaptinals = rCapitals[0]

    print(headNames)
    print(headArea)
    print(headCaptinals)

    for i in range(1, len(rNames), 1):
        tmp = {'Country': '', 'ISO3': '', 'Official_name': '', 'ISO2': '', 'Area': '', 'Capital': ''}

        for j in range(0, len(rNames[i]), 1):
            if j == 0:
                tmp['ISO3'] = rNames[i][j]
            elif j == 1:
                tmp['Country'] = rNames[i][j]
            elif j == 2:
                tmp['Official_name'] = rNames[i][j]
            elif j == 3:
                tmp['ISO2'] = rNames[i][j]

        if (len(rArea[i]) > 2):
            if tmp['Country'] == rArea[i][1]:
                tmp['Area'] = rArea[i][2]

        if (len(rCapitals[i]) > 2):
            if tmp['Country'] == rCapitals[i][1]:
                tmp['Capital'] = rCapitals[i][2]

        name_info.append(tmp)
        
    print(str(name_info) + "\n\n")


read_countries("un_shortlist.csv", "shortlist_area.csv", "shortlist_capitals.csv")
read_curpop_file('shortlist_curpop.csv')

            




