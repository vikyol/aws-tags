from aws_cdk import (
    aws_events as _events
)

# A dictionary that keeps <service name>:<actions> mappings
events = dict()


def get_event_pattern(service):
    event_names = events.get(service, None)

    return _events.EventPattern(
        source=["aws." + service],
        detail_type=["AWS API Call via CloudTrail"],
        detail={
            "eventSource": [
                service + ".amazonaws.com"
            ],
            "eventName": event_names
        }
    )


def get_services():
    return events.keys()


events["ec2"] = [
    "AllocateAddress",
    "RunInstances",
    "CreateSnapshot",
    "CreateVolume",
    "CreateImage",
    "CreateVpc",
    "CreateSubnet",
    "CreateNetworkInterface",
    "CreateNatGateway",
    "CreateInternetGateway",
    "CreateVpcPeeringConnection",
    "CreateSecurityGroup",
    "CreateTransitGateway",
    "CreateVpnGateway",
    "CreateCustomerGateway",
    "CreateVpcEndpoint",
    "CreateRouteTable",
    "CreateLaunchTemplate",
    "CreateNetworkAcl",
    "CopySnapshot",
    "CopyImage"

]

events["s3"] = [
    "PutObject",
    "CreateBucket"
]

events["dynamodb"] = [
    "CreateTable"
    "CreateGlobalTable"
]

events["rds"] = [
    "CreateDBCluster",
    "CreateDBClusterSnapshot",
    "CreateDBInstance",
    "CreateDBInstanceReadReplica",
    "CreateDBProxy",
    "CreateDBSecurityGroup",
    "CreateDBSnapshot",
    "CreateGlobalCluster"
]

