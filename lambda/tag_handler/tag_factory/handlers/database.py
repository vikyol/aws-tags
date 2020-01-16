import boto3
from .base import Tagger


class RdsTagger(Tagger):

    def __init__(self, event):
        super().__init__(event)
        self.tags = []
        self.event = event

    def tag_resources(self):
        rds = boto3.resource('rds')

        db_arn = self.get_resource_id()

        if db_arn:
            self.logger.info('Tagging the RDS resource ' + db_arn)
            tags = self.fetch_tags()
            if len(tags) > 0:
                self.logger.info(f'Tagging {arn} with {tags}')
                rds.add_tags_to_resource(
                    ResourceName=db_arn,
                    Tags=tags
                )
            else:
                self.logger.debug("No tag to apply")
        else:
            self.logger.warn("No RDS instance ARN found in the event data")


class DynamoDbTagger(Tagger):

    def __init__(self, event):
        super().__init__(event)
        self.tags = []
        self.event = event

    def tag_resources(self):
        dynamodb = boto3.resource('dynamodb')

        arn = self.get_resource_id()

        if table_arn:
            self.logger.info('Tagging the DynamoDb resource: ' + arn)
            tags = self.fetch_tags()
            if len(tags) > 0:
                self.logger.info(f'Tagging {arn} with {tags}')
                dynamodb.tag_resource(
                    ResourceArn=arn,
                    Tags=tags
                )
            else:
                self.logger.debug("No tag to apply")
        else:
            self.logger.warn("No DynamoDB table ARN found in the event data")

