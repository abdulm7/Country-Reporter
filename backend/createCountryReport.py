import json
import boto3
import simplejson as json
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

NON_ECON = 'non-econ'
ECON = 'econ'


def create_report_a(country, db):

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
        
        print("WORKING")


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
    try:
        pop_min = min(pop_years)
        pop_max = max(pop_years) + 1
    except:
        pop_min = 0
        pop_max = 0

    output += "\nCapital City: " + str(ne_res['Items'][0]['capital'])
    output += "\nPopulation\n"
    output += "Table of Population, Population Density, and their respective world ranking for that year, ordered by year:\n\n"
    output += "\t{:<10} {:<15} {:<10} {:<20} {:<15}\n".format("Year", "Population", "Rank", "Population Density", "Rank")
    for y in range(pop_min, pop_max):
        if (str(y) in ne_res['Items'][0]['population']):
            output += "\t{:<10} {:<15} {:<10} {:<20} {:<15}\n".format(str(y),str(ne_res['Items'][0]['population'][str(y)]), str(selected_pop_ranks[str(y)]), '%.2f' %(float(ne_res['Items'][0]['population'][str(y)])/float(ne_res['Items'][0]['area'])), str(selected_den_ranks[str(y)]))
        else:
            output += "\t" + str(y) + '\n'

    
    output +="\nEconomics"
    output += "\nCurrency: " + str(e_res['Items'][0]['currency'])
    
    gdp_str_years = e_res['Items'][0]['gdp'].keys()
    gdp_years = [int(str_year) for str_year in gdp_str_years]


    try:
        gdp_min = min(gdp_years)
        gdp_max = max(gdp_years) + 1
    except:
        gdp_min = 0
        gdp_max = 0
    gdp_txt = ""

    for y in range(gdp_min, gdp_max):
        if (str(y) in e_res['Items'][0]['gdp']):
            gdp_txt += "\t{:<20} {:<20} {:<20}\n".format(str(y),str(e_res['Items'][0]['gdp'][str(y)]), str(selected_gdp_rank[str(y)]))
        else:
            gdp_txt += "\t" + str(y) +'\n'
    
    output += "\nTable of GDP per capita (GDPCC) from " + str(gdp_min) +" to " + str(gdp_max) + " and rank within the world for that year:\n\n"
    output += "\t{:<20} {:<20} {:<20}\n".format("Year","GDPPC", "RANK")
    output += gdp_txt
    output +=  "\n----------------------------\n\n"

    return output
    

def createCountryReport(c, s3, db):
    country = c
    
    ret = create_report_a(country, db)
    
    # getting current time for log
    now = datetime.now()
    # for file name, using ';' instead of ':' due to OS special character bug
    dt_string = now.strftime("%Y-%2m-%2d;%H;%M;%S")
    f_country = country.replace(" ", "_")
    fname = f_country + "_Report_" + dt_string + ".txt"
    bucket_name = 'cr-country-reports'
    
    save_to_s3 = s3.put_object(
        Key=fname,
        Bucket=bucket_name,
        Body=(json.dumps(ret))
    )
    
    return json.dumps(ret)
    

