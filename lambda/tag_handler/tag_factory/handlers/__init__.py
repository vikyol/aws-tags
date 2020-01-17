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

from .secrets import SecretsTagger
