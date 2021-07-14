import boto3
# import os
# import json
import sys
from datetime import datetime, timedelta

cProfile = sys.argv[1]
mProfile = sys.argv[2]

sessionClient = boto3.session.Session(profile_name = cProfile)
sessionMaster = boto3.session.Session(profile_name = mProfile)
ec2 = sessionClient.resource('ec2')

############## Grabbing the Running EC2 Instances Id's from the Client Account     
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
############## Getting the CPU Utilization CloudWatch Metrics for EC2 Instances from the Client Account
    cloudwatchClient = sessionClient.client('cloudwatch')
    getRequest = cloudwatchClient.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance.id
            }
            ],
            StartTime=datetime.utcnow() - timedelta(days = 14),
            EndTime=datetime.utcnow(),
            Period=300,
            Statistics=['Average']
            )
############### Processing and filtering the data
    filterResponse = getRequest.get('Datapoints',[])
    print (filterResponse)
    cloudwatchMaster = sessionMaster.client('cloudwatch')
############### Pushing the Custom CloudWatch Metric to the Master Account
    for dic in filterResponse:
        putResponse = cloudwatchMaster.put_metric_data(
            MetricData=[
                {
                    'MetricName': 'CPUUtilization',
                    'Dimensions': [
                        {
                        'Name':'InstanceId',
                        'Value': instance.id
                        }
                    ],
                    'Value': dic['Average'],
                    'Timestamp': dic['Timestamp']
                }
            ],
            Namespace = 'Custom/EC2'
        )
