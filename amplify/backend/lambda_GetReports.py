import simplejson as json
import boto3

s3 = boto3.client("s3")
s3_res = boto3.resource("s3")

def lambda_handler(event, context):

    c_bucket_name = 'cr-country-reports'
    g_bucket_name = 'cr-global-reports'

    try:
        # example code
        # response = s3.get_object(Bucket=bucket_name, Key=object_key)
        # object_body = response['Body'].read()
        
        country_bucket = s3_res.Bucket(c_bucket_name)
        global_bucket = s3_res.Bucket(g_bucket_name)
        
        country_reports = []
        global_reports = []

        
        for obj in country_bucket.objects.all():
            tmp = {'file': '', 'creation-date': '', 'body': ''}
            
            tmp['file'] = str(obj.key)
            tmp['creation-date'] = str(obj.last_modified)
            
            # getting report (content/body)
            response = s3.get_object(Bucket=c_bucket_name, Key=str(obj.key))
            tmp['body'] = response['Body'].read()
            
            country_reports.append(tmp)
            
            
        for obj in global_bucket.objects.all():
            tmp = {'file': '', 'creation-date': '', 'body': ''}
            
            tmp['file'] = str(obj.key)
            tmp['creation-date'] = str(obj.last_modified)
            
            # getting global report (content/body)
            response = s3.get_object(Bucket=g_bucket_name, Key=str(obj.key))
            tmp['body'] = response['Body'].read()
            
            global_reports.append(tmp)
            
        return {
            'statusCode': 200,
            'body': json.dumps({'country': country_reports, 'global': global_reports},  use_decimal=True)
        }
    except Exception as e:
        print('Error getting S3 object:', str(e))
        
        return {
            'statusCode': 500,
            'body': 'Error',
        }