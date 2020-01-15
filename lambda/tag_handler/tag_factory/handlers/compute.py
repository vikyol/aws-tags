import boto3
import logging

import user_identity
from .base import Tagger


class LambdaTagger(Tagger):

    def __init__(self, event):
        super.__init__()
        self.tags = []
        self.event = event

    def tag_resources(self):
        client = boto3.resource('lambda')

        function_arn = self.get_resource_id()

        if function_arn:
            print('Tagging Lambda function ' + function_arn)
            user = user_identity.get_principal(self.event)
            tags = self.fetch_tags()

            response = client.tag_resource(Resource=function_arn, Tags=tags)
        else:
            self.logger.warn("No function arn found in the event data")
