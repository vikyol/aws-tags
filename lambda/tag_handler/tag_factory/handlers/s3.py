import boto3
import logging

import user_identity


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
            assert(self.s3_key,)
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
            self.logger.debug("No tag handler registered for this event")

    def fetch_tags(self):
        # fetch from dynamodb
        tags = user_identity.fetch_tags(self.event)
        tags.append({'Key': 'Owner', 'Value': user_identity.get_principal(self.event)})
        tags.append({'Key': 'PrincipalId', 'Value': self.event['detail']['userIdentity']['principalId']})

        return self.tags

    def get_resources(self):
        pass

