import json
import simplejson as json

def deleteReport(bucketName, objName, s3):

    # exception handling with boto3 api call
    try:
        s3.delete_object(Bucket=bucketName, Key=objName)
        return json.dumps(str(objName) + " Successfully Deleted!!!!")
    
    except Exception as e:
        return json.dumps('ERROR: ' + str(e))

