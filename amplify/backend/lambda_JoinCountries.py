import json
import boto3

db = boto3.resource('dynamodb', region_name='ca-central-1')
db_client = boto3.client('dynamodb', region_name='ca-central-1')

def lambda_handler(event, context):

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
    return {
        'statusCode': 200,
        'body': json.dumps(reportable_countries)
    }
