from aws_cdk import (
    core,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _targets,
)
from .event_patterns import (
    get_services,
    get_event_pattern
)


class AwsTagsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        env = kwargs['env']

        self.register_tags_event_handler()

    def register_tags_event_handler(self):
        event_targets = []
        policy_statement = _iam.PolicyStatement(
            resources=['*'],
            actions=[
                "cloudwatch:PutMetricAlarm",
                "cloudwatch:ListMetrics",
                "cloudwatch:DeleteAlarms",
                "dynamodb:GetItem",
                "dynamodb:DescribeTable",
                "iam:ListRoleTags",
                "iam:ListUserTags",
                "ec2:Describe*",
                # Tagging permissions for the supported services
                "ec2:CreateTags",
                "s3:PutBucketTagging",
                "s3:PutObjectTagging",
                "dynamodb:TagResource",
                "rds:AddTagsToResource",
                "lambda:TagResource",
                "ecs:TagResource",
                "eks:TagResource",
                "sns:TagResource",
                "sqs:TagQueue",
                "elasticloadbalancing:AddTags"
            ],
            effect=_iam.Effect.ALLOW
        )
        tagging_handler = _lambda.Function(
            self, 'AwsTaggingLambda',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda/tag_handler'),
            handler='tag_handler.handler'
        )

        # Create an event pattern for each supported service
        tagging_handler.add_to_role_policy(policy_statement)
        event_targets.append(_targets.LambdaFunction(handler=tagging_handler))
        for service in get_services():
            event_pattern = get_event_pattern(service)

            _events.Rule(
                scope=self,
                id=f'AwsTags{service.capitalize()}Rule',
                description=f'Handles {service.capitalize()} write events for tagging resources',
                rule_name=f'AwsTags{service.capitalize()}Rule',
                event_pattern=event_pattern,
                targets=event_targets
            )