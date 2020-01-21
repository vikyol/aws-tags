import boto3

from .base import Tagger


class SQSTagger(Tagger):

    def __init__(self, event):
        super().__init__(event)
        self.tags = []
        self.event = event

    def tag_resources(self):
        client = boto3.client('sqs')

        q_url = self.get_resource_id()

        if q_url:
            self.logger.info('Tagging the SQS queue ' + q_url)
            tags = self.fetch_tags_as_dict()

            if len(tags) > 0:
                self.logger.info(f'Tagging {q_url} with {tags}')
                response = client.tag_queue(
                    QueueUrl=q_url,
                    Tags=tags
                )
            else:
                self.logger.debug("No tag found to apply")
        else:
            self.logger.warning("No queue URL found in the event data")


class SNSTagger(Tagger):

    def __init__(self, event):
        super().__init__(event)
        self.tags = []
        self.event = event

    def tag_resources(self):
        client = boto3.client('sns')

        arn = self.get_resource_id()

        if arn:
            self.logger.info('Tagging the SNS topic ' + arn)
            tags = self.fetch_tags()

            if len(tags) > 0:
                self.logger.info(f'Tagging {arn} with {tags}')
                response = client.tag_resource(
                    ResourceArn=arn,
                    Tags=tags
                )
            else:
                self.logger.debug("No tag found to apply")
        else:
            self.logger.warning("No topic ARN found in the event data")
