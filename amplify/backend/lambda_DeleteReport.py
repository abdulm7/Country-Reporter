import json
import boto3

s3 = boto3.client("s3")
s3_res = boto3.resource("s3")

def lambda_handler(event, context):
    # TODO implement
    
    bucketName = event['queryStringParameters']['bucket']
    objName = event['queryStringParameters']['object']
    
            # exception handling with boto3 api call
    try:
        s3.delete_object(Bucket=bucketName, Key=objName)
        return {
            'statusCode': 200,
            'body': json.dumps(str(objName) + " Successfully Deleted!")
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'body': json.dumps('ERROR: ' + str(e))
        }

