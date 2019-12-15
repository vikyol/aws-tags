from aws_cdk import (
    core,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _targets,
)


class AutoTagsStack(core.Stack):

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
            ],
            effect=_iam.Effect.ALLOW
        )

        event_handler = _lambda.Function(
            self, 'AwsTagging',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='tag_handler.handler'
        )
        event_handler.add_to_role_policy(policy_statement)

        event_targets.append(_targets.LambdaFunction(handler=event_handler))

        pattern = _events.EventPattern(
            source=['aws.ec2'],
            detail_type=[ "AWS API Call via CloudTrail"],
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
            id='AutoTagsRule',
            description='Handles ec2:RunInstances, ec2:CreateSnapshot, ec2:CreateVolume, ec2:CreateImage events',
            rule_name='AutoTagsRule',
            event_pattern=pattern,
            targets=event_targets
        )