from .ec2 import EC2Tagger
from .s3 import S3Tagger
from .database import (
    DynamoDbTagger,
    RdsTagger
)
from .compute import (
    LambdaTagger,
    ECSTagger,
    EKSTagger
)

from .elb import ELBTagger
from .secrets import SecretsTagger
from .sqs_sns import (
    SQSTagger,
    SNSTagger
)
