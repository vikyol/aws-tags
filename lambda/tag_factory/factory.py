from ec2 import EC2Tagger
from s3 import S3Tagger


class TagFactory:

    def __init__(self):
        self._services = {}
        self.register_service('ec2.amazonaws.com', EC2Tagger)
        self.register_service('s3.amazonaws.com', S3Tagger)

    def register_service(self, name, action):
        self._services[name] = action

    def get_tagger(self, event_source):
        tagger = self._services.get(event_source)
        if not tagger:
            raise ValueError(format)
        return tagger


