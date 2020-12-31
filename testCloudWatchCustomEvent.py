import boto3
import json
from datetime import datetime


def put_cloudwatch_event():
    try:
        client = boto3.client('events', region_name='ap-northeast-1')
        json_input = {"data": "{0} {1}".format('my-source', 'my-target')}
        response = client.put_events(
            Entries=[
                {
                    'Time': datetime.now(),
                    'Source': 'com.test.ssm.to.target',
                    'DetailType': 'MyDetailType',
                    'Resources': ['resource1', 'resource2'],
                    'Detail': json.dumps(json_input)
                }
            ]
        )
        if response['FailedEntryCount'] == 0:
            print(f"Result {json.dumps(json_input)} is in progress")
    except ValueError as err:
        print(str(err))


put_cloudwatch_event()
