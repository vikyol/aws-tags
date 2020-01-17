import boto3

from .base import Tagger


class SecretsTagger(Tagger):

    def __init__(self, event):
        super().__init__(event)
        self.tags = []
        self.event = event

    def tag_resources(self):
        client = boto3.client('secretsmanager')

        secret_id = self.get_resource_id()

        if secret_id:
            self.logger.info('Tagging the Lambda function ' + function_arn)
            tags = self.fetch_tags()

            if len(tags) > 0:
                self.logger.info(f'Tagging {secret_id} with {tags}')
                client.tag_resource(SecretId=secret_id, Tags=tags)
            else:
                self.logger.debug("No tag found to apply")
        else:
            self.logger.warn("No function arn found in the event data")

        response = client.tag_resource(
            SecretId=secret_id,
            Tags=tags
        )