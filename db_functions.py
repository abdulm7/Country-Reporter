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

        if type(gdp_arr) == list and type(tables['currency'] == dict):
            econ = combine_econ(gdp_arr, tables['currency'])
        else:
            econ = False

        return {'non-econ': non_econ, 'econ': econ}


def print_econ(items):
    output = ""
    for i in items['Items']:
        output += ("\n\tcountry: " + str(i['country'] + '\n'))
        output += ("\tcurrency: " + str(i['currency']) + '\n')
        output += ("\tGPD: \n")
        line_count = 1
        gdp_keys = sorted(i['gdp'].keys())
        for y in gdp_keys:
            if (str(y) in i['gdp']):
                output += "\t\t{:<30}".format("{year: " + str(y) + ", gdp: " + str(i['gdp'][str(y)]) +"}")

                if (line_count % 3 == 0):
                    output += "\n"
            line_count += 1
        if(output[len(output)-1] != '\n'):
            output += '\n'
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
        output += "\t\t{iso2: " + i['aliases']['iso2'] + ','
        output += "\tiso3: " + i['aliases']['iso3'] + ','
        output += " \tofficial: " + i['aliases']['official'] + '}\n'

        # printing population
        output += "\tpopulation: \n"
        line_count = 1
        pop_keys = sorted(i['population'].keys())
        for y in pop_keys:
            if (str(y) in i['population']):
                output += "\t\t{:<40}".format("{year: " + str(y) + ", population: " + str(i['population'][str(y)]) + '}')

                if (line_count % 3 == 0):
                    output += "\n"
            line_count += 1
        if(output[len(output)-1] != '\n'):
            output += '\n'

        output += "------------------------------------------------------------------------------------------------------------------------------------------------------"

    return output

def create_report_a(db, country):

    pop_ranks = {}
    pop_den = {}
    gdp_ranks = {}

    try:
        ne_table = db.Table(NON_ECON)
        e_table = db.Table(ECON)
        ne_res = ne_table.query(
            KeyConditionExpression = Key('country').eq(country)
        )

        e_res = e_table.query(
            KeyConditionExpression = Key('country').eq(country)
        )

        populations = ne_table.scan(
            AttributesToGet = ['country', 'area', 'population']
        )

        gdps = e_table.scan(
            AttributesToGet = ['country', 'gdp']
        )


        if ne_res['Items'] == []:
            return 'ERROR: ' + country + " was not found."

        if e_res['Items'] == []:
            return 'ERROR: ' + country + " was not found."

        # initializing array for all possible years 
        for rec in populations['Items']:
            str_year_arr = rec['population'].keys()

            for y_iter in str_year_arr:
                pop_ranks[str(y_iter)] = []
                pop_den[str(y_iter)] = []

        # storing all populations and population densities 
        # with the corresponding year and country
        for rec in populations['Items']:
            str_year_arr = rec['population'].keys()
    
            for y_iter in str_year_arr:
                pop_ranks[str(y_iter)].append({'country': rec['country'], 'population':int(rec['population'][str(y_iter)])})
                pop_den[str(y_iter)].append({'country': rec['country'], 'pop_den':(int(rec['population'][str(y_iter)])/int(rec['area']))})

        # initializing array for all possible years 
        for rec in gdps['Items']:
            str_year_arr = rec['gdp'].keys()

            for y_iter in str_year_arr:
                gdp_ranks[str(y_iter)] = []

        # storing all populations and population densities 
        # with the corresponding year and country
        for rec in gdps['Items']:
            str_year_arr = rec['gdp'].keys()
    
            for y_iter in str_year_arr:
                gdp_ranks[str(y_iter)].append({'country': rec['country'], 'gdp':int(rec['gdp'][str(y_iter)])})

        # getting ranks for the selected country
        selected_pop_ranks = {}
        selected_den_ranks = {}
        selected_gdp_rank = {}

        # population density dict and population dict will have the same keys
        # since they are initialized in the same loop with the same conditions 
        # so for efficiency will use the same loop
        pop_keys = pop_ranks.keys()
        for key in pop_keys:
            sort_pop_ranks = sorted(pop_ranks[key], key=lambda d: d['population'], reverse=True)
            sort_den_ranks = sorted(pop_den[key], key=lambda d: d['pop_den'], reverse=True)
            pop_rank = 1
            den_rank = 1
            found_pop = False
            found_den = False
            for p in sort_pop_ranks or found_pop:
                if p['country'] == country:
                    selected_pop_ranks[key] = pop_rank
                    found_pop = True
                else:
                    pop_rank += 1
            for d in sort_den_ranks or found_den:
                if d['country'] == country:
                    selected_den_ranks[key] = den_rank
                    found_den = True
                else:
                    den_rank += 1


        gdp_keys = gdp_ranks.keys()
        for key in gdp_keys:
            sort_gdp_ranks = sorted(gdp_ranks[key], key=lambda d: d['gdp'], reverse=True)
            rank = 1
            found = False
            for g in sort_gdp_ranks or found:
                if g['country'] == country:
                    selected_gdp_rank[key] = rank
                    found = True
                else:
                    rank += 1

    except Exception as e:
        # return '\tERROR: could not fetch country.'
        return e
    

    output = "----------------------------\n"
    output += country + '\n'
    output += "Offically known as: " + ne_res['Items'][0]['aliases']['official']
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

    pop_str_years = ne_res['Items'][0]['population'].keys()
    pop_years = [int(str_year) for str_year in pop_str_years]
    pop_min = min(pop_years)
    pop_max = max(pop_years)

    output += "\nCapital City: " + str(ne_res['Items'][0]['capital'])
    output += "\nPopulation\n"
    output += "Table of Population, Population Density, and their respective world ranking for that year, ordered by year:\n\n"
    output += "\t{:<10} {:<15} {:<10} {:<20} {:<15}\n".format("Year", "Population", "Rank", "Population Density", "Rank")
    for y in range(pop_min, pop_max+1):
        if (str(y) in ne_res['Items'][0]['population']):
            output += "\t{:<10} {:<15} {:<10} {:<20} {:<15}\n".format(str(y),str(ne_res['Items'][0]['population'][str(y)]), str(selected_pop_ranks[str(y)]), '%.1f' %(float(ne_res['Items'][0]['population'][str(y)])/float(ne_res['Items'][0]['area'])), str(selected_den_ranks[str(y)]))
        else:
            output += "\t\t" + str(y) + '\n'

    
    output +="\nEconomics"
    output += "\nCurrency: " + str(e_res['Items'][0]['currency'])
    
    gdp_str_years = e_res['Items'][0]['gdp'].keys()
    gdp_years = [int(str_year) for str_year in gdp_str_years]
    gdp_min = min(gdp_years)
    gdp_max = max(gdp_years)
    gdp_txt = ""

    for y in range(gdp_min, gdp_max+1):
        if (str(y) in e_res['Items'][0]['gdp']):
            gdp_txt += "\t{:<20} {:<20} {:<20}\n".format(str(y),str(e_res['Items'][0]['gdp'][str(y)]), str(selected_gdp_rank[str(y)]))
        else:
            gdp_txt += "\t\t" + str(y)
    
    output += "\nTable of GDP per capita (GDPCC) from " + str(gdp_min) +" to " + str(gdp_max) + " and rank within the world for that year:\n\n"
    output += "\t{:<20} {:<20} {:<20}\n".format("Year","GDPPC", "RANK")
    output += gdp_txt
    output +=  "\n----------------------------\n\n"
    

    

    return output


def delete_rec(db, table, rec):
    try:
        table = db.Table(table)
        res = table.delete_item(
            Key={
                'country': rec
            }
        )
        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False
    except:
        return False

def add_rec(db, table, rec):
    if table == NON_ECON:
        item = {
            'country': rec, 
            'aliases': {
                'official': '',
                'iso3': '',
                'iso2': ''
            }, 
            'area': '', 
            'capital': '',
            'languages': [],
            'population': {}
        }
    else:
        item = {
            'country': rec, 
            'currency': '',
            'gdp': {}
        }

    res = load_record(db, table, item)
    if res:
        return True
    else:
        return False

def create_report_b(db, year):

    try:
        ne_table = db.Table(NON_ECON)
        e_table = db.Table(ECON)

        ne_data = ne_table.scan(
            AttributesToGet = ['country', 'area', 'population']
        )

        e_data = e_table.scan(
            AttributesToGet = ['country', 'gdp']
        )
    except Exception as e:
        return e

        # storing all populations and population densities 
    # with the corresponding year and country
    ne_memory = []
    for rec in ne_data['Items']:
        if str(year) in rec['population']:
            ne_memory.append({
                'country': rec['country'], 
                'population':int(rec['population'][str(year)]), 
                'pop_den':(int(rec['population'][str(year)])/int(rec['area']))
                })


    sorted_pop = sorted(ne_memory, key=lambda d: d['population'], reverse=True)

    sorted_den = sorted(ne_memory, key=lambda d: d['pop_den'], reverse=True)

    output =  "\n----------------------------\n"
    output += "Year: " + year
    output += "\nNumber of Countries: "
    num_ec = len(e_data['Items'])
    num_nec = len(ne_data['Items'])
    # accounting for the case of different countries in each table
    if num_ec != num_nec:
        # identify if economic table as different number of countries than non-econ
        output += str(num_ec) + " Economic & " + str(num_nec) + "Non-Economic\n"
    else:
        # if same number of countries 
        output += str(num_ec)
    output +=  "\n----------------------------\n"
    output += "\nTable of Countries Ranked by Population (*largest to smallest*)\n"
    output += "\t{:<40} {:<20} {:<20}\n".format("Country Name", "Population","Rank")

    # printing population table
    p_rank = 1
    for p in sorted_pop:
        output += "\t{:<40} {:<14} {:>10}".format(p['country'], str(p['population']), str(p_rank))
        output += '\n'
        p_rank += 1

    output += "\n\nTable of Countries Ranked by Density (*largest to smallest*)\n"
    output += "\t{:<40} {:<25} {:<20}\n".format("Country Name", "Population Density","Rank")
    # printing population table
    d_rank = 1
    for p in sorted_den:
        output += "\t{:<40} {:10.2f} {:>19}".format(p['country'], p['pop_den'], str(d_rank))
        output += '\n'
        d_rank += 1
    
    output += "\n\nGDP Per Capita for all Countries\n"
    
    decades = []
    for i in e_data['Items']:
        str_years = i['gdp'].keys()
        for s in str_years:
            dec = s[:3] + '0'
            if (int(dec) not in decades):
                decades.append(int(dec))

    sort_econ = sorted(e_data['Items'], key=lambda d: d['country'])
    
    for d in sorted(decades):
        output += "\t" + str(d) + "s Table\n"
        # print header first
        output += "\t|{:<35}".format("Country Name")
        for i in range(d, d+10):
            output += "{:<10}".format(str(i))
        output += '|\n'
        output += '\t'
        # 135 because if you add up all the spacing in the formatting
        # 35 + 10*10 (years 0-9 in each decade)
        for i in range(135):
            output += '-'
        output += '\n'
        # printing data
        for c in sort_econ:
            output += "\t|{:<35}|".format(c['country'])
            
            for i in range(d, d+10):
                if str(i) in c['gdp']:
                    output += "{:<10}".format(c['gdp'][str(i)])
                else:
                    output += '{:100}'.format(" ")
            output += '|\n'

        output += '\n'
                

    return output