import user_identity
import logging


class Tagger:
    def __init__(self):
        self.event = None
        self.logger = logging.getLogger("tagging")
        self.logger.setLevel(logging.INFO)

    def fetch_tags(self):
        # Fetch session and IAM tags
        tags = user_identity.fetch_tags(self.event)
        # Append ownership tags, if it do not already exist
        tags.append({'Key': 'Owner', 'Value': user_identity.get_principal(self.event)})
        tags.append({'Key': 'PrincipalId', 'Value': self.event['detail']['userIdentity']['principalId']})

        return tags

    def tag_resources(self):
        pass

    def get_resource_id(self):
        # Use event/resource mappings to fetch the resource ID
        resource_path = Tagger.get_event_resource_mappings()[self.event['detail']['eventName']]

        path = resource_path.split(".")

        # Extract the resource ID according to the path provided by the mappings
        resource = self.event[path[0]]
        for p in path[1:]:
            resource = resource[p]

        return resource

    @staticmethod
    def get_event_resource_mappings():
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
        )
