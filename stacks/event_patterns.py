from aws_cdk import (
    aws_events as _events
)


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


# A dictionary that keeps <service name>:<actions> mappings
events = dict(
    ec2=[
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
    ],
    s3=[
        "PutObject",
        "CreateBucket"
    ],
    dynamodb=[
        "CreateTable",
        "CreateGlobalTable",
        "CreateBackup"
    ],
    rds=[
        "CreateDBCluster",
        "CreateDBClusterSnapshot",
        "CreateDBInstance",
        "CreateDBInstanceReadReplica",
        "CreateDBProxy",
        "CreateDBSecurityGroup",
        "CreateDBSnapshot",
        "CreateGlobalCluster"
    ],
    ecs=[
        "CreateCapacityProvider",
        "CreateService",
        "CreateTaskSet",
        "CreateCluster"
    ],
    eks=[
        "CreateNodeGroup",
        "CreateCluster"
    ],
    elasticloadbalancing=[
        "CreateLoadBalancer",
        "CreateTargetGroup"
    ],
    secretsmanager=[
        "CreateSecret"
    ],
    sqs=[
        "CreateQueue"
    ],
    sns=[
        "CreateTopic"
    ],
    ssm=[
        "CreateDocument",
        "CreateOpsItem",
        "CreatePatchBaseline",
        "CreateMaintenanceWindow",
        "PutParameter"
    ]
)

# Lambda is a reserved keyword, so we have to add it separately this way.
events["lambda"] = [
        "CreateFunction20150331",
        "UpdateFunctionCode20150331v2"
]

