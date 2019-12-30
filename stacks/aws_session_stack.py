from aws_cdk import (
    core,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_dynamodb as _dynamodb
)
import os


class AwsSessionStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        env = kwargs['env']

        self.register_session_tags_handler()

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

    def register_session_tags_handler(self):
        event_targets = []
        policy_statement = _iam.PolicyStatement(
            resources=['*'],
            actions=[
                "dynamodb:PutItem"
            ],
            effect=_iam.Effect.ALLOW
        )

        session_handler = _lambda.Function(
            self, 'AwsSessionTagsLambda',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda/session_handler'),
            handler='session_handler.handler',
            environment={'default_region': os.environ["CDK_DEFAULT_REGION"]}
        )

        session_handler.add_to_role_policy(policy_statement)
        event_targets.append(_targets.LambdaFunction(handler=session_handler))

        # Create an event rule to handle sts:assumeRoleWithSAML
        session_pattern = _events.EventPattern(
            source=["aws.sts"],
            detail_type=["AWS API Call via CloudTrail"],
            detail={
                "eventSource": ["sts.amazonaws.com"],
                "eventName": [
                    "AssumeRoleWithSAML",
                    "AssumeRole"
                ]
            }
        )

        _events.Rule(
            scope=self,
            id='AwsTagsSTSRule',
            description='Handles STS AssumeRole* events to retrieve session tags',
            rule_name='AwsTagsSTSRule',
            event_pattern=session_pattern,
            targets=event_targets
        )