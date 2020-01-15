import boto3
import logging

import user_identity


class EC2Tagger:

    def __init__(self, event):
        self.tags = []
        self.event = event

    def tag_resources(self):
        event = self.event
        ec2 = boto3.resource('ec2')

        resources = self.get_resources()

        if resources:
            print('Tagging resources ' + ', '.join(resources))
            user = user_identity.get_principal(event)
            tags = self.fetch_tags()

            ec2.create_tags(
                Resources=resources,
                Tags=tags
            )

    def fetch_tags(self):
        # fetch from dynamodb
        tags = user_identity.fetch_tags(self.event)
        tags.append({'Key': 'Owner', 'Value': user_identity.get_principal(self.event)})
        tags.append({'Key': 'PrincipalId', 'Value': self.event['detail']['userIdentity']['principalId']})

        return self.tags

    @staticmethod
    def get_event_resource_mappings():
        return dict(
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
            CopyImage="detail.responseElements.imageId")

    def get_resource_id(self):
        resource_path = EC2Tagger.get_event_resource_mappings()[self.event['detail']['eventName']]

        path = resource_path.split(".")

        # Extract the resource ID according to the path provided by event/resource mappings
        resource = self.event[path[0]]
        for p in path[1:]:
            resource = resource[p]

        return resource

    def get_resources(self):
        event = self.event
        resource_ids = []
        detail = event['detail']
        event_name = detail['eventName']
        logger = logging.getLogger("tagging")
        ec2 = boto3.resource('ec2')

        if event_name == 'RunInstances':
            items = detail['responseElements']['instancesSet']['items']
            for item in items:
                resource_ids.append(item['instanceId'])
            logger.info('number of instances: ' + str(len(resource_ids)))

            instances = ec2.instances.filter(InstanceIds=resource_ids)

            # Find all volumes and elastic network interfaces attached to the instances
            for instance in instances:
                for vol in instance.volumes.all():
                    resource_ids.append(vol.id)
                for eni in instance.network_interfaces:
                    resource_ids.append(eni.id)

        else:
            resource_id = self.get_resource_id()

            print("Extracted resource ID {} from {} event".format(resource_id, event_name))
            resource_ids.append(resource_id)

        logger.info(resource_ids)
        return resource_ids
