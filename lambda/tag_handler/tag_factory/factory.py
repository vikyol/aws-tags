import tag_factory.handlers as handler


class TagFactory:

    def __init__(self):
        self._services = {}
        self.register_service('aws.ec2', handler.EC2Tagger)
        self.register_service('aws.s3', handler.S3Tagger)
        self.register_service('aws.dynamodb', handler.DynamoDbTagger)
        self.register_service('aws.rds', handler.RdsTagger)
        self.register_service('aws.lambda', handler.LambdaTagger)
        self.register_service('aws.eks', handler.EKSTagger)
        self.register_service('aws.ecs', handler.ECSTagger)
        self.register_service('aws.elasticloadbalancing', handler.ELBTagger)
        self.register_service('aws.secretsmanager', handler.SecretsTagger)
        self.register_service('aws.sqs', handler.SQSTagger)
        self.register_service('aws.sns', handler.SNSTagger)

    def register_service(self, name, action):
        self._services[name] = action

    def get_tagger(self, event_source):
        return self._services.get(event_source, None)


