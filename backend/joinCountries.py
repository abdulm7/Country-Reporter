import json

def joinCountries(db):

    e_table = db.Table('econ')
    ne_table = db.Table('non-econ')
    
    ne_countries = ne_table.scan(
        AttributesToGet = ['country']
    )
    
    e_countries = e_table.scan(
        AttributesToGet = ['country']
    )
    
    reportable_countries = []
    
    for ec in e_countries['Items']:
        for nec in ne_countries['Items']:
            if ec == nec:
                reportable_countries.append(ec['country'])
                
    reportable_countries.sort()
    
    return json.dumps(reportable_countries)
