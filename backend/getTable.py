from decimal import Decimal
import simplejson as json

def getTable(t, db):
    try:
        # get table name from query string
        table_name = t
        
        # pull table 
        table = db.Table(table_name)
        items = table.scan()
        
        years = []
        
        if (table_name == "non-econ"):
            for i in items['Items']:
                str_years = i['population'].keys()
                for s in str_years:
                    if (int(s) not in years):
                        years.append(int(s))
                

        else:
            for i in items['Items']:
                str_years = i['gdp'].keys()
                for s in str_years:
                    if (int(s) not in years):
                        years.append(int(s))
        years.sort()

        return json.dumps({'items': items['Items'], 'years': years}, use_decimal=True)
    
    except Exception as e:
        return ("ERROR: " + str(e))
    
    