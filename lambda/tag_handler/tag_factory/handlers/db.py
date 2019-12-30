import boto3
import logging

import user_identity


class RdsTagger:
    pass


class DynamoDbTagger:

    def __init__(self, event):
        self.tags = []
        self.event = event

    def tag_resources(self):
        event = self.event
        dynamodb = boto3.resource('dynamodb')

        resources = self.get_resources()

        if resources:
            print('Tagging resources ' + ', '.join(resources))
            user = user_identity.get_principal(event)
            tags = self.fetch_tags()

            dynamodb.tag_resource(
                ResourceArn='string',
                Tags=tags
            )

    def fetch_tags(self):
        # fetch from dynamodb
        tags = user_identity.fetch_tags(self.event)
        tags.append({'Key': 'Owner', 'Value': user_identity.get_principal(self.event)})
        tags.append({'Key': 'PrincipalId', 'Value': self.event['detail']['userIdentity']['principalId']})

        return self.tags

    def get_resources(self):
        event = self.event
        resources = []

        return resources
