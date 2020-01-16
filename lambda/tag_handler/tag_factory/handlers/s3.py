import boto3
import logging

from .base import Tagger


class S3Tagger(Tagger):
    bucket_name: str
    s3_key: str

    def __init__(self, event):
        super().__init__(event)
        self.tags = []
        self.event = event
        self.bucket_name = event['detail']['requestParameters'].get('bucketName', None)
        self.s3_key = event['detail']['requestParameters'].get('key', None)
        self.event_name = event['detail']['eventName']
        self.logger = logging.getLogger("tagging")

    def tag_resources(self):
        event = self.event

        tags = self.fetch_tags()

        if self.event_name == 'CreateBucket':
            s3 = boto3.resource('s3')
            bucket_tagging = s3.BucketTagging(self.bucket_name)
            self.logger.debug("Tagging the S3 bucket " + self.bucket_name)

            response = bucket_tagging.put(
                Tagging={
                    'TagSet': tags
                }
            )
        elif self.event_name == 'PutObject':
            client = boto3.client('s3')
            self.logger.debug("Tagging the S3 object " + self.s3_key)

            response = client.put_object_tagging(
                Bucket=self.bucket_name,
                Key=self.s3_key,
                Tagging={
                    'TagSet': tags
                }
            )
        else:
            self.logger.warning("No tag handler registered for this event: " + self.event_name)


