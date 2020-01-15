import boto3
import logging

import user_identity
from .base import Tagger


class EC2Tagger(Tagger):

    def __init__(self, event):
        super.__init__()
        self.tags = []
        self.event = event

    def tag_resources(self):
        event = self.event
        ec2 = boto3.resource('ec2')

        resources = self.get_resources()

        if resources:
            self.logger.info('Tagging resources ' + ', '.join(resources))
            user = user_identity.get_principal(event)
            tags = self.fetch_tags()

            ec2.create_tags(
                Resources=resources,
                Tags=tags
            )
        else:
            self.logger.warn("No EC2 instance found in the event data")

    def get_resources(self):
        resource_ids = []
        detail = self.event['detail']
        event_name = detail['eventName']
        ec2 = boto3.resource('ec2')

        if event_name == 'RunInstances':
            items = detail['responseElements']['instancesSet']['items']
            for item in items:
                resource_ids.append(item['instanceId'])
            self.logger.info('Number of instances: ' + str(len(resource_ids)))

            instances = ec2.instances.filter(InstanceIds=resource_ids)

            # Find all volumes and elastic network interfaces attached to the instances
            for instance in instances:
                for vol in instance.volumes.all():
                    resource_ids.append(vol.id)
                for eni in instance.network_interfaces:
                    resource_ids.append(eni.id)

        else:
            resource_id = self.get_resource_id()

            self.logger.info("Extracted resource ID {} from {} event".format(resource_id, event_name))
            resource_ids.append(resource_id)

        self.logger.info(resource_ids)
        return resource_ids
