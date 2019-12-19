from aws_cdk import (
    core,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_dynamodb as _dynamodb
)


class AwsTagsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        event_targets = []

        policy_statement = _iam.PolicyStatement(
            resources=['*'],
            actions=[
                "cloudwatch:PutMetricAlarm",
                "cloudwatch:ListMetrics",
                "cloudwatch:DeleteAlarms",
                "ec2:CreateTags",
                "ec2:Describe*",
                "s3:PutBucketTagging",
                "s3:PutObjectTagging"
            ],
            effect=_iam.Effect.ALLOW
        )

        event_handler = _lambda.Function(
            self, 'AwsTaggingLambda',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='tag_handler.handler'
        )
        event_handler.add_to_role_policy(policy_statement)

        event_targets.append(_targets.LambdaFunction(handler=event_handler))

        ec2_pattern = _events.EventPattern(
            source=['aws.ec2'],
            detail_type=["AWS API Call via CloudTrail"],
            detail={
                "eventSource": [
                  "ec2.amazonaws.com"
                ],
                "eventName": [
                    "RunInstances",
                    "CreateSnapshot",
                    "CreateVolume",
                    "CreateImage"
                ]
            }
        )

        _events.Rule(
            scope=self,
            id='AutoTagsEc2Rule',
            description='Handles ec2:RunInstances, ec2:CreateSnapshot, ec2:CreateVolume, ec2:CreateImage events',
            rule_name='AwsTagsEc2Rule',
            event_pattern=ec2_pattern,
            targets=event_targets
        )

        s3_pattern = _events.EventPattern(
            source=['aws.s3'],
            detail_type=["AWS API Call via CloudTrail"],
            detail={
                "eventSource": [
                  "s3.amazonaws.com"
                ],
                "eventName": [
                    "PutObject",
                    "CreateBucket"
                ]
            }
        )

        _events.Rule(
            scope=self,
            id='AutoTagsS3Rule',
            description='Handles s3:CreateBucket and s3:PutObject events',
            rule_name='AwsTagsS3Rule',
            event_pattern=s3_pattern,
            targets=event_targets
        )

        _dynamodb.Table(
            scope=self,
            id="TagsTable",
            table_name="aws-tags",
            partition_key=_dynamodb.Attribute(
                name="principal_id",
                type=_dynamodb.AttributeType.STRING
            ),
            # sort_key=_dynamodb.Attribute(
            #     name="tags",
            #     type=_dynamodb.AttributeType.STRING
            # ),
            billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST,
            server_side_encryption=True
        )