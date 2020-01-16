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
        # Use event/resource mappings to fetch the resource ID
        resource_path = Tagger.get_event_resource_mappings()[self.event['detail']['eventName']]
        print(f"Before split {resource_path}")
        # Workaround for conflicting API action names: the same action name with a different resource path
        # The event/resource mapping in this case contains a dictionary of resource identifiers {service:resource_path}
        if isinstance(resource_path, dict):
            self.logger.debug("Resolving the conflict with the event name")
            event_source = self.event['detail']['eventSource']
            print(event_source)
            if event_source:
                source = event_source.split('.')[0]
                print(source)
                resource_path = resource_path[source]
                print(resource_path)
                self.logger.debug(f"Retrieved {resource_path} for {source} service")
                print(f"Retrieved {resource_path} for {source} service")  

        path = resource_path.split(".")

        # Extract the resource ID according to the path provided by the mappings
        resource = self.event[path[0]]
        for p in path[1:]:
            resource = resource[p]

        return resource

    @staticmethod
    def get_event_resource_mappings():
        # Creates a mapping between API actions and resource identifier.
        # It stores either ID or ARN of resources depending on the AWS tagging API
        return dict(
            # EC2
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
            CopyImage="detail.responseElements.imageId",
            # RDS
            CreateDBInstance="detail.responseElements.dbInstance.dbInstanceArn",
            CreateDBInstanceReadReplica="detail.responseElements.dbInstance.dbInstanceArn",
            CreateDBSnapshot="detail.responseElements.dbSnapshot.dbSnapshotArn",
            CreateDBCluster="detail.responseElements.dbCluster.dbClusterArn",
            CreateDBClusterSnapshot="detail.responseElements.dbClusterSnapshot.dbClusterSnapshotArn",
            CreateGlobalCluster="detail.responseElements.dbGlobalCluster.dbGlobalClusterArn",
            # DynamoDB
            CreateTable="detail.responseElements.tableDescription.tableArn",
            CreateGlobalTable="detail.responseElements.globalTableDescription.globalTableArn",
            CreateBackup="detail.responseElements.backupDetails.backupArn",
            # Lambda
            CreateFunction="detail.responseElements.functionArn",
            CreateAlias="detail.responseElements.aliasArn",
            # ECS
            CreateCapacityProvider="detail.responseElements.capacityProvider.capacityProviderArn",
            CreateService="detail.responseElements.service.serviceArn",
            CreateTaskSet="detail.responseElements.taskSet.taskSetArn",
            # EKS
            CreateNodeGroup="detail.responseElements.nodeGroup.nodeGroupArn",
            # ECS /EKS common eventName with a different resource path
            CreateCluster=dict(
                ecs="detail.responseElements.cluster.clusterArn",
                eks="detail.responseElements.cluster.arn"
            )
        )
   