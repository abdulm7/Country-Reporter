import boto3
from decimal import Decimal
import simplejson as json
# backend functions (similar to endpoints)
from getTable import getTable
from getYears import getYears
from getReports import getReports
from deleteReport import deleteReport
from joinCountries import joinCountries
from createGlobalReport import createGlobalReport
from createCountryReport import createCountryReport

db = boto3.resource('dynamodb', region_name='ca-central-1')
db_client = boto3.client('dynamodb', region_name='ca-central-1')

s3 = boto3.client("s3")
s3_res = boto3.resource("s3")

def lambda_handler(event, context):
    
    func = event['queryStringParameters']['func'].lower()
    
    if (func == "gettable"):
    
        table_name = event['queryStringParameters']['table']
    
        body = getTable(t=table_name, db=db)
    elif (func == "createglobalreport"):

        year = event['queryStringParameters']['year']

        body = createGlobalReport(y=year, s3=s3, db=db)

    elif (func == "getyears"):

        body = getYears(db=db)

    elif (func == "getreports"):

        body = getReports(s3_res=s3_res, s3=s3)

    elif(func == "deletereport"):

        bucketName = event['queryStringParameters']['bucket']
        objName = event['queryStringParameters']['object']

        body = deleteReport(bucketName, objName, s3)

    elif (func == "joincountries"):

        body = joinCountries(db=db)

    elif (func == "createcountryreport"):

        country = event['queryStringParameters']['country']

        body = createCountryReport(c=country, s3=s3, db=db)

    else:
        body = "ERROR: Function doesn't exist"


    return {
        'statusCode': 200,
        'body': body
    }



