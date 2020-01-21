import boto3

from .base import Tagger


class LambdaTagger(Tagger):

    def __init__(self, event):
        super().__init__(event)
        self.tags = []
        self.event = event

    def tag_resources(self):
        client = boto3.client('lambda')

        function_arn = self.get_resource_id()

        if function_arn:
            self.logger.info('Tagging the Lambda function ' + function_arn)
            tags = self.fetch_tags_as_dict()

            if len(tags) > 0:
                self.logger.info(f'Tagging {function_arn} with {tags}')
                client.tag_resource(Resource=function_arn, Tags=tags)
            else:
                self.logger.debug("No tag found to apply")
        else:
            self.logger.warning("No function ARN found in the event data")


class ECSTagger(Tagger):

    def __init__(self, event):
        super().__init__(event)
        self.tags = []
        self.event = event

    def tag_resources(self):
        ecs = boto3.client('ecs')

        arn = self.get_resource_id()

        if arn:
            self.logger.info('Tagging the ECS resource: ' + arn)
            tags = self.fetch_tags()

            if len(tags) > 0:
                self.logger.info(f'Tagging {arn} with {tags}')
                response = ecs.tag_resource(resourceArn=arn, tags=tags)
            else:
                self.logger.debug("No tag found to apply")
        else:
            self.logger.warning("No resource ARN found in the event data")


class EKSTagger(Tagger):

    def __init__(self, event):
        super().__init__(event)
        self.tags = []
        self.event = event

    def tag_resources(self):
        eks = boto3.client('eks')

        arn = self.get_resource_id()

        if arn:
            self.logger.info('Tagging the EKS resource: ' + arn)
            tags = self.fetch_tags_as_dict()
            if len(tags) > 0:
                self.logger.info(f'Tagging {arn} with {tags}')
                response = eks.tag_resource(resourceArn=arn, tags=tags)
            else:
                self.logger.debug("No tag found to apply")
        else:
            self.logger.warning("No resource ARN found in the event data")
