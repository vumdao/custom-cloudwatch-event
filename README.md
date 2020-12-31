<p align="center">
  <a href="https://dev.to/vumdao">
    <img alt="Custom CloudWatch Events" src="https://dev-to-uploads.s3.amazonaws.com/i/v31e8t4rtkazjajpbo5q.png" width="500" />
  </a>
</p>
<h1 align="center">
  Custom CloudWatch Events
</h1>


<h3 align="center">
  <div>Create rules to invoke Targets based on Events happening in your AWS environment. </div>
  <div>Use event source with customize an Event Pattern</d>
</h3>


## What’s In This Document 
- [Create cloudwatch event rule](#-Create-cloudwatch-event-rule)
- [Create AWS Systems Manager Document](#-Create-AWS-Systems-Manager-Document)
- [Update IAM role to run SSM document from cloudwatch](#-Update-IAM-role-to-run-SSM-document-from-cloudwatch)
- [Put cloudwatch event to test](#-Put-cloudwatch-event-to-test)


### 🚀 **[Create cloudwatch event rule](#-Create-cloudwatch-event-rule)**
- Build custom event pattern
```
{
  "source": [
    "com.test.ssm.to.target"
  ]
}
```
- Target: SSM Run Command
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/091ber3if66wkgb8wr9m.png)

### 🚀 **[Create AWS Systems Manager Document](#-Create-AWS-Systems-Manager-Document)**
- JSON Content: Write `{{Message}}` content to `{{workingDirectory}}/testSSM.txt"`
```
{
  "schemaVersion": "2.2",
  "description": "Run SSM command",
  "parameters": {
    "Message": {
      "type": "String",
      "description": "Parameter of SSM script",
      "default": ""
    },
    "workingDirectory": {
      "type": "String",
      "description": "Working dir",
      "default": "/tmp/"
    }
  },
  "mainSteps": [
    {
      "action": "aws:runShellScript",
      "name": "runSSMCommand",
      "inputs": {
        "runCommand": [
          "echo {{Message}} > {{workingDirectory}}/testSSM.txt"
        ]
      }
    }
  ]
}
```
- Target type: `/AWS::EC2::Instance`
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/hh9ofpgelwb5ux8r3sig.png)

### 🚀 **[Update IAM role to run SSM document from cloudwatch](#-Update-IAM-role-to-run-SSM-document-from-cloudwatch)**
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "ssm:SendCommand",
            "Effect": "Allow",
            "Resource": [
                "arn:aws:ec2:ap-northeast-1:111111111111:instance/i-0f4a1c3c2ca0a7dee",
                "arn:aws:ssm:ap-northeast-1:111111111111:document/testSSM"
            ]
        }
    ]
}
```

### 🚀 **[Put cloudwatch event to test](#-Put-cloudwatch-event-to-test)**
- Use python script to put event to cloudwatch rule
```
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
```

- Run script
```
Result {"data": "my-source my-target"} is in progress

Process finished with exit code 0
```

- Check result: Access to target instance
```
# cat /tmp/testSSM.txt 
my-source my-target
```