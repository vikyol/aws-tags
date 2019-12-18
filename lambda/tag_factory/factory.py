from .ec2 import EC2Tagger
from .s3 import S3Tagger


class TagFactory:

    def __init__(self):
        self._services = {}
        self.register_service('aws.ec2', EC2Tagger)
        self.register_service('aws.s3', S3Tagger)

    def register_service(self, name, action):
        self._services[name] = action

    def get_tagger(self, event_source):
        return self._services.get(event_source, None)
