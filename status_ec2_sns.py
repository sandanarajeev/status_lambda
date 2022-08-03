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

    message = "EC2\n"

    ec2 = boto3.resource("ec2", region_name=AWS_REGION)
    ec2_resources = ec2.instances.all()

    for instance in ec2_resources:
        ec2Instance = None
        print("instance", instance)
        if(instance.id == ec2_id):
            ec2Instance = instance
        else:
            tags = instance.tags
            tag = next(
                (tag for tag in tags if tag["Key"] == ec2Key and tag["Value"] == ec2Value), None)
        if(tag != None):
            ec2Instance = instance
        if(ec2Instance):
            message = message + f"""
Instance {ec2Instance.id} information:\n
State: {ec2Instance.state["Name"]}\n"""

    print("ec2Instance", ec2Instance)

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
