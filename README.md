
# EC2 CPU Cloudwatch Metrics

ec2-cpu-cloudwatch-metrics is a Python script to get ec2 utilization metrics data of the Client AWS Account and push it to the Master AWS Account Cloudwatch "Custom/EC2" Metrics.

## Prerequisite

Tested with Python3 and Boto3

## Usage

```python
python3 ec2-cpu-cloudwatch-metrics.py <Client Profile> <Master Profile>

example: python3 ec2-cpu-cloudwatch-metrics.py dev prod
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.