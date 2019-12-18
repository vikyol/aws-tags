import boto3
import logging

from .util import get_user

class S3Tagger:

    bucket_name: str
    s3_key: str

    def __init__(self, event):
        self.tags = []
        self.event = event
        self.bucket_name = event['detail']['requestParameters'].get('bucketName', None)
        self.s3_key = event['detail']['requestParameters'].get('key', None)
        self.event_name = event['detail']['eventName']
        self.logger = logging.getLogger("tagging")

    def tag_resources(self):
        event = self.event
        s3 = boto3.resource('s3')

        self.logger.debug("Tagging S3 resources")

        tags = self.fetch_tags()

        if self.event_name == 'CreateBucket':
            bucket_tagging = s3.BucketTagging(self.bucket_name)

            response = bucket_tagging.put(
                Tagging={
                    'TagSet': tags
                }
            )
        elif self.event_name == 'PutObject':
            client = boto3.client('s3')

            response = client.put_object_tagging(
                Bucket=self.bucket_name,
                Key=self.s3_key,
                Tagging={
                    'TagSet': tags
                }
            )
        else:
            self.logger.debug("No tag handler registered for this event")

    def fetch_tags(self):
        # fetch from dynamodb
        self.tags.append({'Key': 'Owner', 'Value': get_user(self.event)})
        principal = self.event['detail']['userIdentity'].get('principalId', None)
        if principal:
            self.tags.append({'Key': 'PrincipalId', 'Value': principal})

        return self.tags

    def get_resources(self):
        pass

