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
import json

from boto3.dynamodb.conditions import Key, Attr

# Range of possible years (excess does not affect output)
MIN_YEAR = 1960
MAX_YEAR = 2030

# table names
NON_ECON = 'non-econ'
ECON = 'econ'

# to improve report format
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# reading in all "one-to-one" data e.g. name, official name, ISO2, ISO3, Area, & capital
# **Limitation** files must be in the format provided by Dr. Stacey
# takes in the "un_shortlist"
# storing and structuring data to be ready for push to dynamodb
# returns a single table (containing the data referred to above) in JSON/Dict format
def read_names(filename):
    first = True
    header = []
    name_info = []

    with open(filename, 'r', encoding="utf-8-sig") as file:

        reader = csv.reader(file)
        for row in reader:
            tmp = {
                'country': '', 
                'aliases': {
                    'official': '',
                    'iso3': '',
                    'iso2': ''
                }, 
                'area': '', 
                'capital': '',
                'languages': '',
                'population': ''
            }
            if (first):
                first = False
                header = row
            else:
                for i in range(len(row)):
                    if i == 0:
                        tmp['aliases']['iso3'] = row[i]
                    elif i == 1:
                        tmp['country'] = row[i]
                    elif i == 2:
                        tmp['aliases']['official'] = row[i]
                    elif i == 3:
                        tmp['aliases']['iso2'] = row[i]

                name_info.append(tmp)
        
    return name_info

# for files with single data following this structure
# ISO3, Country Name, Data
# e.g. ISO3, Country Name, Area
def read_single(filename):
    first = False
    header = []

    with open(filename, 'r', encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        data = {}
        next(reader)
        for row in reader:
            if (len(row) > 2):
                data[row[1]] = row[2]
            elif (len(row) > 1):
                data[row[1]] = ''
            
    return data

# reads the "shortlist_curpop.csv" file
# splits 'economic' & 'non-economic' data 
# prepares 'json/python dict' to as table for db
# **Limitation** file must be in the format provided by Dr. Stacey
#   e.g Country, Currency, Population 1970, 1971, 1972...
# returns the curreny and population tables as JSON/Dict
def read_cur_pop(filename):
    first = True
    header = []
    currency_arr = {}
    population_arr = {}
    with open(filename, 'r', encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            if first:
                header = row
                # to prevent an index errors assuming file is not correct
                if(len(header) > 2 and 'population' in header[2].lower()):
                    # get rid of word 'Population' in header
                    header[2] = ''.join(filter(str.isdigit, header[2]))
                first = False
            else:
                if (len(row) > 1):
                    currency_arr[row[0]] = ""
                    population_arr[row[0]] = {}
                
                for i in range(1, len(row), 1):
                    if i == 1:
                        currency_arr[row[0]] = row[i]
                    else:
                        if len(row[i]) > 0:
                            population_arr[row[0]][header[i]] = int(row[i])

    return {'currency': currency_arr, 'population': population_arr}

def read_lang(filename):
    try:
        first = True
        lang_arr = {}
        with open(filename, 'r', encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            for row in reader:
                if (len(row) > 2):
                    if first:
                        first = False
                    else:
                        lang_arr[row[1]] = []
                        for i in range(2, len(row)):
                            lang_arr[row[1]].append(row[i])
        
        return lang_arr
    except Exception as e:
        return e


def combine_non_econ(table, languages, populations, area, capitals):

    for c in table:
        if c['country'] in populations:
            c['population'] = populations[c['country']]
        if c['country'] in languages:
            c['languages'] = languages[c['country']]
        if c['country'] in area:
            c['area'] = area[c['country']]
        if c['country'] in capitals:
            c['capital'] = capitals[c['country']]
    
    return table


def read_gdp(filename):
    try:
        first = True
        gdp__arr = []
        with open(filename, 'r', encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            for row in reader:
                tmp = {
                    'country': '',
                    'currency': '',
                    'gdp': {}
                }
                if first:
                    header = row
                    first = False
                else:
                    if (len(row) > 2):
                        tmp['country'] = row[0]
                        for i in range(1, len(row)):
                            if (len(row[i]) > 0):
                                tmp['gdp'][header[i]] = int(row[i])
                        gdp__arr.append(tmp)
                    else:
                        return False
        
        return gdp__arr
    except Exception as e:
        return False

def combine_econ(gdp_table, currency):
    for c in gdp_table:
        if c['country'] in currency:
            c['currency'] = currency[c['country']]
    return gdp_table

            

def create_table (db, name, attr_name, part_type):
    try:
        t = db.create_table(
            TableName = name,
            AttributeDefinitions = [
                {
                    'AttributeName': attr_name,
                    'AttributeType': part_type
                }
            ],
            KeySchema = [
                {
                    'AttributeName': attr_name,
                    'KeyType': 'HASH'
                }
            ],
            ProvisionedThroughput = {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

        t.wait_until_exists()

        return True
    except Exception as e:
        return e


def delete_table (db, table_name):
    try:
        t = db.Table(table_name)
        t.delete()
        t.wait_until_not_exists()

        return True
    except Exception as e:
        return e

def load_record(db, table_name, rec):
    try:
        t = db.Table(table_name)
        res = t.put_item(
            Item = rec
        )
        
        if (res['ResponseMetadata']['HTTPStatusCode'] == 200):
            return True
    except Exception as e:
        return e

def load_tables(db, table_name, data_arr):

    ret = True

    for rec in data_arr:
        ret = load_record(db, table_name, rec)
        if (ret == False):
            break

    return ret


def check_exists(db_client, table_name):
    try:
        db_client.describe_table(TableName=table_name)
        return True
    except:
        return False

def create_tables_dict(f_names, f_area, f_caps, f_cur_pop, f_lang, f_gdp):
        names = read_names(f_names)
        area = read_single(f_area)
        capitals = read_single(f_caps)
        tables = read_cur_pop(f_cur_pop)
        lang_arr = read_lang(f_lang)
        gdp_arr = read_gdp(f_gdp)

        non_econ = []
        econ = []

        if type(lang_arr) == dict and type(names) == list and type(lang_arr) == dict:
            non_econ = combine_non_econ(names, lang_arr, tables["population"], area, capitals)
        else:
            non_econ = False

        # print(non_econ)

        if type(gdp_arr) == list and type(tables['currency'] == dict):
            econ = combine_econ(gdp_arr, tables['currency'])
        else:
            econ = False
        
        # print(non_econ)

        return {'non-econ': non_econ, 'econ': econ}


def print_econ(items):
    output = ""
    for i in items['Items']:
        output += ("\n\tcountry: " + str(i['country'] + '\n'))
        output += ("\tcurrency: " + str(i['currency']) + '\n')
        output += ("\tGPD: \n")
        for y in range(MIN_YEAR, MAX_YEAR):
            if (str(y) in i['gdp']):
                output += "\t\t(year: " + str(y) + " gdp: " + str(i['gdp'][str(y)]) +")\t"

                if (y % 3 == 0):
                    output += "\n"
        output += "------------------------------------------------------------------------------------------------------------------------------------------------------"

    return output

def print_non_econ(items):
    output = ""
    for i in items['Items']:
        # printing country name, capital and area
        output += ("\n\tcountry: " + str(i['country']) + '\n')
        output += ("\tcapital: " + str(i['capital']) + '\n')
        output += ("\tarea: " + str(i['area']) + '\n')

        # printing languages
        output += ("\tlanguages: ")
        idx = 1
        for l in i['languages']:
            if idx == len(i['languages']):
                output += str(l)
            else:
                output += str(l) + ', '
            idx += 1

        # printing aliases data
        output += "\n\taliases: \n"
        output += "\t\tiso2: " + i['aliases']['iso2']
        output += "\tiso3: " + i['aliases']['iso3']
        output += " \tofficial: " + i['aliases']['official'] + '\n'

        # printing population
        output += "\tpopulation: \n"
        for y in range(MIN_YEAR, MAX_YEAR):
            if (str(y) in i['population']):
                output += "\t\t(year: " + str(y) + " population: " + str(i['population'][str(y)]) +")\t"

                if (y % 3 == 0):
                    output += "\n"

        if(output[len(output)-1] != '\n'):
            output += '\n'

        output += "------------------------------------------------------------------------------------------------------------------------------------------------------"
        # output += ("\npopulation"

    return output

def create_report_a(db, country):
    ne_table = db.Table(NON_ECON)
    e_table = db.Table(ECON)

    try:
        ne_res = ne_table.query(
            KeyConditionExpression = Key('country').eq(country)
        )

        e_res = e_table.query(
            KeyConditionExpression = Key('country').eq(country)
        )
    except:
        return 'ERROR: could not fetch country.'

    # try:
    #     all_pop = ne_
    #     Select='SPECIFICT_ATTRIBUTES'

    # print(e_res)

    if ne_res['Items'] == []:
        return 'ERROR: ' + country + " was not found."

    if e_res['Items'] == []:
        return 'ERROR: ' + country + " was not found."
    

    output = "----------------------------\n"
    output += color.BOLD + country + color.END + '\n'
    output += ne_res['Items'][0]['aliases']['official']
    output +=  "\n----------------------------\n"

    output += "Area: " + str(ne_res['Items'][0]['area']) + '\n'
    output += "Languages: "
    idx = 1
    for l in ne_res["Items"][0]['languages']:
        if idx == len(ne_res["Items"][0]['languages']):
            output += str(l)
        else:
            output += str(l) + ', '
            idx += 1
    output += "\nCapital City: " + str(ne_res['Items'][0]['capital'])
    output += color.BOLD + "\nPopulation\n" + color.END
    output += "Table of Population, Population Density, and their respective world ranking for that year, ordered by year:\n\n"
    output += "\t\tYear\t\tPopulation\tRank\tPopulation Density\tRank\n"
    for y in range(MIN_YEAR, MAX_YEAR):
        if (str(y) in ne_res['Items'][0]['population']):
            output += "\t\t" + str(y) + '\t\t' + str(ne_res['Items'][0]['population'][str(y)]) + "\t\t"
            output += "rank" + '\t\t %.1f' %(float(ne_res['Items'][0]['population'][str(y)])/float(ne_res['Items'][0]['area'])) + '\t\t' + 'rank\n'

    
    output += color.BOLD + "\nEconomics" + color.END
    output += "\nCurrency: " + str(e_res['Items'][0]['currency'])
    

    gdp_txt = ""
    earliest = 999999
    latest = 0
    for y in range(MIN_YEAR, MAX_YEAR):
        if (str(y) in e_res['Items'][0]['gdp']):
            gdp_txt += "\t\t"+ str(y) + '\t\t' + str(e_res['Items'][0]['gdp'][str(y)]) +'\t\t' + '\n'
            if y < earliest:
                earliest = y
            if y > latest:
                latest = y
    
    output += "\nTable of GDP per capita (GDPCC) from " + str(earliest) +" to " + str(latest) + " and rank within the world for that year:\n"
    output += "\t\tYear\t\tGDPPC\t\tRANK"
    output += "\n" + gdp_txt
    output +=  "\n----------------------------\n\n"
    

    

    return output


