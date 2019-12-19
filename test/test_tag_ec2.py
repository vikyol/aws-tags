from moto import mock_ec2
import boto3

def add_servers(ami_id, count):
    client = boto3.client('ec2', region_name='eu-west-1')
    client.run_instances(ImageId=ami_id, MinCount=count, MaxCount=count)

@mock_ec2
def test_add_servers():
    add_servers('ami-01f14919ba412de34', 1)
    client = boto3.client('ec2', region_name='eu-west-1')
    desc_instances = client.describe_instances()
    print(desc_instances)
    instances = desc_instances['Reservations'][0]['Instances']

    assert len(instances) == 1
    instance1 = instances[0]
    assert instance1['ImageId'] == 'ami-01f14919ba412de34'