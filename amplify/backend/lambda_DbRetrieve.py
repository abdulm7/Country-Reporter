import boto3
from decimal import Decimal
import simplejson as json

db = boto3.resource('dynamodb', region_name='ca-central-1')
db_client = boto3.client('dynamodb', region_name='ca-central-1')
    

def lambda_handler(event, context):

    try:
        # get table name from query string
        table_name = event['queryStringParameters']['table']
        
        
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
        return {
            'statusCode': 200,
            'body': json.dumps({'items': items['Items'], 'years': years}, use_decimal=True)
        }
    except Exception as e:
        return {
        'statusCode': 200,
        'body': "ERROR: " + str(e),
    }
