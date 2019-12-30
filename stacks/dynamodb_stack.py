from aws_cdk import (
    core,
    aws_dynamodb as _dynamodb,
    # aws_dynamodb_global as _globaldb
)

GLOBAL_SERVICES_REGION = "us-east-1"


class DbStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        dynamo_regions = set()
        dynamo_regions.add(GLOBAL_SERVICES_REGION)
        dynamo_regions.add(kwargs['env'].region)

        #_globaldb.GlobalTable(
        _dynamodb.Table(
            scope=self,
            id="dynamodb",
            partition_key=_dynamodb.Attribute(
                name="assumed_role_id",
                type=_dynamodb.AttributeType.STRING
            ),
            table_name="aws-tags",
            #regions=list(dynamo_regions),
            billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST,
            server_side_encryption=True
        )