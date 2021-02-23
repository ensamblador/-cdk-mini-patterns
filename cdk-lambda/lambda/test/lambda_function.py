import json
import uuid
import decimal
import os
import boto3


ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, contex):
    print ("invocado", event)
    for rec in event['Records']:
        s3_bucket = rec['s3']['bucket']['name']
        s3_key = rec['s3']['object']['key']
        print (s3_bucket, s3_key)
        my_item = {
            's3_key': s3_key,
            's3_bucket': s3_bucket,
            'id': str(uuid.uuid4()),
            'seguridad': 'NO'
        }
        res = save_item_ddb(my_item)
        print (res)
    return 0


def save_item_ddb(item):
    response = table.put_item(Item=item)
    return response