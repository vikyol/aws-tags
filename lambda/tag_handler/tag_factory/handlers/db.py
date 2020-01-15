import boto3
import logging
import user_identity
from .base import Tagger


class RdsTagger(Tagger):

    def __init__(self, event):
        super.__init__()
        self.tags = []
        self.event = event

    def tag_resources(self):
        rds = boto3.resource('rds')

        db_arn = self.get_resource_id()

        if db_arn:
            self.logger.info('Tagging RDS  table ' + db_arn)
            user = user_identity.get_principal(self.event)
            tags = self.fetch_tags()

            rds.add_tags_to_resource(
                ResourceName=db_arn,
                Tags=tags
            )
        else:
            self.logger.warn("No RDS instance ARN found in the event data")


class DynamoDbTagger(Tagger):

    def __init__(self, event):
        super.__init__()
        self.tags = []
        self.event = event

    def tag_resources(self):
        dynamodb = boto3.resource('dynamodb')

        table_arn = self.get_resource_id()

        if table_arn:
            self.logger.info('Tagging DynamoDb  table ' + table_arn)
            user = user_identity.get_principal(self.event)
            tags = self.fetch_tags()

            dynamodb.tag_resource(
                ResourceArn='string',
                Tags=tags
            )
        else:
            self.logger.warn("No DynamoDB table ARN found in the event data")

