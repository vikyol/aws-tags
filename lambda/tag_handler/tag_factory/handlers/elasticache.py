import boto3

from .base import Tagger


class ElastiCacheTagger(Tagger):

    def __init__(self, event):
        super().__init__(event)
        self.tags = []
        self.event = event

    def tag_resources(self):
        client = boto3.client('elasticache')

        arn = self.get_resource_id()

        if arn:
            self.logger.info('Tagging the ElastiCache resource ' + arn)
            tags = self.fetch_tags()

            if len(tags) > 0:
                self.logger.info(f'Tagging {arn} with {tags}')
                client.add_tags_to_resource(ResourceName=[arn], Tags=tags)
            else:
                self.logger.debug("No tag found to apply")
        else:
            self.logger.warn("No ELB arn found in the event data")