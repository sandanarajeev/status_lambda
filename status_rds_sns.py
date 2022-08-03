#!/usr/bin/env python3

import boto3

AWS_REGION = ""
ec2_id = ""
rds_id = ""
topic_arn = ""

rdsKey = "test"
rdsValue = "abiola-ground"

ec2Key = "test"
ec2Value = "abiola-ground"


def lambda_handler(event, context):

    client = boto3.client("rds", region_name=AWS_REGION)
    response = client.describe_db_instances()

    message = "RDS\n"
    for instance in response["DBInstances"]:
        rdsInstance = None
        if(instance["DBInstanceIdentifier"] == rds_id):
            rdsInstance = instance
        else:
            tags = instance["TagList"]
            tag = next(
                (tag for tag in tags if tag["Key"] == rdsKey and tag["Value"] == rdsValue), None)
            if(tag != None):
                rdsInstance = instance
        if(rdsInstance):
            message = message + f"""
Instance {rdsInstance["DBInstanceIdentifier"]} information:\n
State: {rdsInstance["DBInstanceStatus"]}\n"""

    print("rdsInstance", rdsInstance)

    subject = "Status Mail"
    print("message", message)
    sns = boto3.client("sns", region_name=AWS_REGION)
    sns.publish(TopicArn=topic_arn, Message=message, Subject=subject)

    return {
        "StatusCode": 200,
        "Body": "Success"
    }


# enable for local testing
# lambda_handler(None, None)
