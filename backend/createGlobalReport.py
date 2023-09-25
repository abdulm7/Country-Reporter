import boto3
import simplejson as json
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

NON_ECON = 'non-econ'
ECON = 'econ'

# db = boto3.resource('dynamodb', region_name='ca-central-1')
# db_client = boto3.client('dynamodb', region_name='ca-central-1')

# s3 = boto3.client("s3")
# s3_res = boto3.resource("s3")

def create_report_b(year, db):

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
        output += str(num_ec) + " Economic & " + str(num_nec) + " Non-Economic\n"
    else:
        # if same number of countries 
        output += str(num_ec)
    output +=  "\n----------------------------\n"
    output += "\nTable of Countries Ranked by Population (*largest to smallest*)\n"
    output += "\t{:<40} {:<25} {:<20}\n".format("Country Name", "Population","Rank")

    # printing population table
    p_rank = 1
    for p in sorted_pop:
        output += "\t{:<40} {:<25} {:<20}".format(p['country'], str(p['population']), str(p_rank))
        output += '\n'
        p_rank += 1

    output += "\n\nTable of Countries Ranked by Density (*largest to smallest*)\n"
    output += "\t{:<40} {:<25} {:<20}\n".format("Country Name", "Population Density","Rank")
    # printing population table
    d_rank = 1
    for p in sorted_den:
        output += "\t{:<40} {:<25} {:<20}".format(p['country'], '%.2f' %(float(p['pop_den'])), str(d_rank))
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
                    output += '{:10}'.format(" ")
            output += '|\n'

        output += '\n'
                

    return output

def createGlobalReport(y, s3, db):

    
    ret = create_report_b(year=y, db=db)
    
    # getting current time for log
    now = datetime.now()
    # for file name, using ';' instead of ':' due to OS special character bug
    dt_string = now.strftime("%Y-%2m-%2d;%H;%M;%S")
    fname = "Year_" + y + "_Report_" + dt_string + ".txt"
    bucket_name = 'cr-global-reports'
    
    save_to_s3 = s3.put_object(
        Key=fname,
        Bucket=bucket_name,
        Body=(json.dumps(ret))
    )
    
    return json.dumps(ret)
