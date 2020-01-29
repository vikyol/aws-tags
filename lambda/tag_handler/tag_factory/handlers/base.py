import user_identity
import logging


class Tagger:
    def __init__(self, event):
        self.event = event
        self.logger = logging.getLogger("tagging")

    def fetch_tags(self):
        # Fetch session and IAM tags
        tags = user_identity.fetch_tags(self.event)
        if not tags:
            tags = list()

        # Append the ownership tag, if it does not already exist
        if not ('Key' in tags and 'Value' == 'Owner'):
            tags.append({'Key': 'Owner', 'Value': user_identity.get_principal(self.event)})
            tags.append({'Key': 'PrincipalId', 'Value': self.event['detail']['userIdentity']['principalId']})
        else:
            self.logger.debug("Owner tag already exists")

        return tags

    # Some APIs expect dict() instead of list()
    # Converts list({'Key':'k1', 'Value':'v1}, {'Key':'k2', 'Value':'v2}) to {'k1':'v1', 'k2':'v2'}
    def fetch_tags_as_dict(self):
        tags = self.fetch_tags()
        tags_dict = dict()

        for kv_pair in tags:
            tags_dict[kv_pair['Key']] = kv_pair['Value']

        return tags_dict

    def tag_resources(self):
        pass

    def get_resource_id(self):
        resource_path = None
        # e.g source=aws.sns
        service = self.event['source'].split('.')[1]
        print(f"Invoked get_resource_id for {service}")
        # Use event/resource mappings to fetch the resource ID
        resources = Tagger.get_event_resource_mappings().get(service, None)
        if not resources:
            return None

        # Fetch the resource path for the event
        resource_path = resources[self.event['detail']['eventName']]
        self.logger.debug(f"Retrieved {resource_path} for {service} service")

        path = resource_path.split(".")

        # Extract the resource ID according to the path provided by the mappings
        resource = self.event[path[0]]
        for p in path[1:]:
            if isinstance(resource, dict):
                resource = resource[p]
            else:
                resource = resource[int(p)]

        self.logger.debug(f"Extracted resource id/arn {resource}")
        return resource

    @staticmethod
    def get_event_resource_mappings():
        # Creates a mapping between API actions and resource identifier.
        # It stores either ID or ARN of resources depending on the AWS tagging API
        resources = dict(
            s3=dict(
                CreateBucket="",
                PutObject=""
            ),  # s3 does not use this function
            ec2=dict(
                AllocateAddress="detail.responseElements.allocationId",
                CreateVolume="detail.responseElements.volumeId",
                CreateImage="detail.responseElements.imageId",
                CreateSnapshot="detail.responseElements.snapshotId",
                CreateNetworkInterface="detail.responseElements.networkInterface.networkInterfaceId",
                CreateVpc="detail.responseElements.vpc.vpcId",
                CreateSubnet="detail.responseElements.subnet.subnetId",
                CreateVpcPeeringConnection="detail.responseElements.vpcPeeringConnection.vpcPeeringConnectionId",
                CreateInternetGateway="detail.responseElements.internetGateway.internetGatewayId",
                CreateNatGateway="detail.responseElements.natGateway.natGatewayId",
                CreateTransitGateway="detail.responseElements.transitGateway.transitGatewayId",
                CreateVpnGateway="detail.responseElements.vpnGateway.vpnGatewayId",
                CreateCustomerGateway="detail.responseElements.customerGateway.customerGatewayId",
                CreateVpcEndpoint="detail.responseElements.vpcEndpoint.vpcEndpointId",
                CreateRouteTable="detail.responseElements.routeTable.routeTableId",
                CreateLaunchTemplate="detail.responseElements.launchTemplate.launchTemplateId",
                CreateSecurityGroup="detail.responseElements.groupId",
                CreateNetworkAcl="detail.responseElements.networkAcl.networkAclId",
                CopySnapshot="detail.responseElements.snapshotId",
                CopyImage="detail.responseElements.imageId"
            ),
            rds=dict(
                CreateDBInstance="detail.responseElements.dbInstance.dbInstanceArn",
                CreateDBInstanceReadReplica="detail.responseElements.dbInstance.dbInstanceArn",
                CreateDBSnapshot="detail.responseElements.dbSnapshot.dbSnapshotArn",
                CreateDBCluster="detail.responseElements.dbCluster.dbClusterArn",
                CreateDBClusterSnapshot="detail.responseElements.dbClusterSnapshot.dbClusterSnapshotArn",
                CreateGlobalCluster="detail.responseElements.dbGlobalCluster.dbGlobalClusterArn"
            ),
            dynamodb=dict(
                CreateTable="detail.responseElements.tableDescription.tableArn",
                CreateGlobalTable="detail.responseElements.globalTableDescription.globalTableArn",
                CreateBackup="detail.responseElements.backupDetails.backupArn"
            ),
            ecs=dict(
                CreateCapacityProvider="detail.responseElements.capacityProvider.capacityProviderArn",
                CreateService="detail.responseElements.service.serviceArn",
                CreateTaskSet="detail.responseElements.taskSet.taskSetArn",
                CreateCluster="detail.responseElements.cluster.clusterArn"
            ),
            eks=dict(
                CreateNodeGroup="detail.responseElements.nodeGroup.nodeGroupArn",
                CreateCluster="detail.responseElements.cluster.arn"
            ),
            elasticloadbalancing=dict(
                # response contains a list of LoadBalancers/TargetGroups, just fetch the first one at index 0
                CreateLoadBalancer="detail.responseElements.loadBalancers.0.loadBalancerArn",
                CreateTargetGroup="detail.responseElements.targetGroups.0.targetGroupArn",
            ),
            secretsmanager=dict(
                CreateSecret="detail.responseElements.ARN"
            ),
            sqs=dict(
                CreateQueue="detail.responseElements.queueUrl"
            ),
            sns=dict(
                CreateTopic="detail.responseElements.topicArn"
            ),
            ssm=dict(
                CreateDocument="detail.requestParameters.name",
                CreateOpsItem="detail.responseElements.opsItemId",
                CreatePatchBaseline="detail.responseElements.baselineId",
                CreateMaintenanceWindow="detail.responseElements.windowId",
                PutParameter="detail.requestParameters.name"
            ),
            elasticache=dict(
                CreateSnapshot="detail.responseElements.Snapshot.SnapshotName",
                CopySnapshot="detail.responseElements.Snapshot.SnapshotName",
                CreateCacheCluster="detail.responseElements.CacheCluster.CacheClusterId",
            ),
            athena=dict(
                CreateWorkGroup=""
            ),
            glue=dict(
                CreateDatabase=""
            )
        )
        # lambda is a reserved word in Python, cannot use it in dict constructor
        resources["lambda"] = dict(
                CreateFunction20150331="detail.responseElements.functionArn",
                UpdateFunctionCode20150331v2="detail.responseElements.functionArn"
        )
        return resources
