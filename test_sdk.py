import boto3

ec2_client = boto3.client('ec2')

ec2_data = ec2_client.describe_instances()

for reservation in ec2_data['Reservations']:
    for instance in reservation['Instances']:
        print(instance['InstanceId'])

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'last_name',
            'KeyType': 'RANGE'
        }
    ]
)


cloudwatch = boto3.client('cloudwatch')

paginator = cloudwatch.get_paginator('describe_alarms')
for response in paginator.paginate(stateValue='INSUFFICIENT_DATA'):
    print(response['MetricAlarms'])
