<p align="center">
  <a href="https://dev.to/vumdao">
    <img alt="Custom CloudWatch Events" src="https://dev-to-uploads.s3.amazonaws.com/i/3uswygba3lrhi1sq5oc3.png" width="500" />
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
- [Create custom cloudwatch event rule](#-Create-custom-cloudwatch-event-rule)
- [Create AWS Systems Manager Document](#-Create-AWS-Systems-Manager-Document)
- [Update IAM role to run SSM document from cloudwatch](#-Update-IAM-role-to-run-SSM-document-from-cloudwatch)
- [Put cloudwatch event to test](#-Put-cloudwatch-event-to-test)


### 🚀 **[Create custom cloudwatch event rule](#-Create-custom-cloudwatch-event-rule)**
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

**Read More**
- [Pelican-resume with docker-compose and AWS + CDK](https://dev.to/vumdao/pelican-resume-with-docker-compose-and-aws-cdk-33e5)
- [Using Helm Install Botkube Integrate With Slack On EKS](https://dev.to/vumdao/using-helm-install-botkube-integrate-with-slack-on-eks-gmn)
- [Ansible AWS EC2 Dynamic Inventory Plugin](https://dev.to/vumdao/ansible-aws-ec2-dynamic-inventory-plugin-3bme)
- [How To List All Enabled Regions Within An AWS account](https://dev.to/vumdao/list-all-enabled-regions-within-an-aws-account-4oo7)
- [Using AWS KMS In AWS Lambda](https://dev.to/vumdao/using-aws-kms-in-aws-lambda-2jm2)
- [Create AWS Backup Plan](https://dev.to/vumdao/create-aws-backup-plan-a0f)
- [Techniques For Writing Least Privilege IAM Policies](https://dev.to/vumdao/techniques-for-writing-least-privilege-iam-policies-4fc7)
- [EKS Persistent Storage With EFS Amazon Service](https://dev.to/vumdao/eks-persistent-storage-with-efs-amazon-service-14ei)
- [Create k8s Cronjob To Schedule Delete Expired Files](https://dev.to/vumdao/create-k8s-cronjob-to-schedule-delete-expired-files-1i41)
- [Amazon ECR - Lifecycle Policy Rules](https://dev.to/vumdao/amazon-ecr-lifecycle-policy-rules-1l59)
- [Connect Postgres Database Using Lambda Function](https://dev.to/vumdao/connect-postgres-database-using-lambda-function-1mca)
- [Using SourceIp in ALB Listener Rule](https://dev.to/vumdao/using-sourceip-in-alb-listener-rule-377b)
- [Amazon Simple Systems Manager (SSM)](https://dev.to/vumdao/amazon-simple-systems-manager-ssm-2pb0)
- [Invalidation AWS CDN Using Boto3](https://dev.to/vumdao/invalidation-aws-cdn-using-boto3-2k9g)
- [Create AWS Lambda Function Triggered By S3 Notification Event](https://dev.to/vumdao/create-aws-lambda-function-triggered-by-s3-notification-event-9p0)
- [CI/CD Of Invalidation AWS CDN Using Gitlab Pipeline](https://dev.to/vumdao/ci-cd-of-invalidation-aws-cdn-using-gitlab-pipeline-34op)
- [Create CodeDeploy](https://dev.to/vumdao/create-codedeploy-4425)
- [Gitlab Pipeline With AWS Codedeploy](https://dev.to/vumdao/gitlab-pipeline-with-aws-codedeploy-30cl)
- [Create AWS-CDK image container](https://dev.to/vumdao/create-aws-cdk-image-container-43ei)
- [Deploy Python Lambda Functions With Container Image](https://dev.to/vumdao/deploy-python-lambda-functions-with-container-image-5hgj)

<h3 align="center">
  <a href="https://dev.to/vumdao">:stars: Blog</a>
  <span> · </span>
  <a href="https://vumdao.hashnode.dev/">Web</a>
  <span> · </span>
  <a href="https://www.linkedin.com/in/vu-dao-9280ab43/">Linkedin</a>
  <span> · </span>
  <a href="https://www.linkedin.com/groups/12488649/">Group</a>
  <span> · </span>
  <a href="https://www.facebook.com/CloudOpz-104917804863956">Page</a>
  <span> · </span>
  <a href="https://twitter.com/VuDao81124667">Twitter :stars:</a>
</h3>
