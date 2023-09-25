import json
import simplejson as json

def getYears(db):
    
    e_table = db.Table('econ')
    ne_table = db.Table('non-econ')
    
    ne_countries = ne_table.scan(
        AttributesToGet = ['population']
    )
    
    e_countries = e_table.scan(
        AttributesToGet = ['gdp']
    )
    
    years = []
        
    for i in ne_countries['Items']:
        str_years = i['population'].keys()
        for s in str_years:
            if (int(s) not in years):
                years.append(int(s))
            
    
    for i in e_countries['Items']:
        str_years = i['gdp'].keys()
        for s in str_years:
            if (int(s) not in years):
                years.append(int(s))
    
    years.sort()

    return json.dumps(years, use_decimal=True)
    
