import boto3
import logging
from util import get_user


class EC2Tagger:
    
    def __init__(self):
        self.tags = []
        self.event = None

    def tag_resources(self, event):
        self.event = event
        ec2 = boto3.resource('ec2')

        resources = EC2Tagger.get_resources(event)

        if resources:
            print('Tagging resource ' + resources)
            user = get_user(event)
            tags = self.fetch_tags()

            ec2.create_tags(
                Resources=resources,
                Tags=tags
            )

    def fetch_tags(self):
        # fetch from dynamodb
        self.tags.append({'Key': 'Owner', 'Value': get_user(self.event)})
        self.tags.append({'Key': 'PrincipalId', 'Value': self.event['detail']['userIdentity']['principalId'] })

        return self.tags

    @staticmethod
    def get_resources(event):
        resource_ids = []
        detail = event['detail']
        event_name = detail['eventName']
        logger = logging.getLogger("tagging")

        if event_name == 'CreateVolume':
            resource_ids.append(detail['responseElements']['volumeId'])

        elif event_name == 'RunInstances':
            items = detail['responseElements']['instancesSet']['items']
            for item in items:
                resource_ids.append(item['instanceId'])
            logger.info('number of instances: ' + str(len(resource_ids)))

            instances = ec2.instances.filter(InstanceIds=resource_ids)

            # Find all elastic network interfaces attached to the instances
            for instance in instances:
                for vol in instance.volumes.all():
                    resource_ids.append(vol.id)
                for eni in instance.network_interfaces:
                    resource_ids.append(eni.id)

        elif event_name == 'CreateImage':
            resource_ids.append(detail['responseElements']['imageId'])

        elif event_name == 'CreateSnapshot':
            resource_ids.append(detail['responseElements']['snapshotId'])
        else:
            logger.warning('Not supported action')

        logger.info(resource_ids)
        return resource_ids



