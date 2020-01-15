import os
from aws_cdk import (
    core,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_dynamodb as dynamdb,
    aws_sns as sns,
    aws_logs as logs,
    aws_lambda as _lambda,
    aws_cloudtrail as cloudtrail,
    aws_logs_destinations as log_destinations
)


SNS_TOPIC_NAME = "AssumeRoleWithSamlEvent"

# Set to NONE to create a new log group
# Specify a name to import an existing log group
CLOUDTRAIL_LOG_GROUP_NAME = "CloudTrail/DefaultLogGroup"


class AwsSessionStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        env = kwargs['env']

        self.register_session_tags_handler()

        dynamdb.Table(
            scope=self,
            id="dynamodb",
            partition_key=dynamdb.Attribute(
                name="assumed_role_id",
                type=dynamdb.AttributeType.STRING
            ),
            table_name="aws-tags",
            # regions=list(dynamo_regions),
            billing_mode=dynamdb.BillingMode.PAY_PER_REQUEST,
            server_side_encryption=True
        )

        # Keep this workaround until sts:AssumeRoleWithSAML is supported by CloudWatch Event Rules
        self.cwe_saml_workaround()

    def register_session_tags_handler(self):
        event_targets = []
        policy_statement = iam.PolicyStatement(
            resources=['*'],
            actions=[
                "dynamodb:PutItem"
            ],
            effect=iam.Effect.ALLOW
        )

        session_handler = _lambda.Function(
            self, 'AwsSessionTagsLambda',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda/session_handler'),
            handler='session_handler.handler',
            environment={'default_region': os.environ["CDK_DEFAULT_REGION"]}
        )

        session_handler.add_to_role_policy(policy_statement)
        event_targets.append(targets.LambdaFunction(handler=session_handler))

        # Create an event rule to handle sts:assumeRoleWithSAML
        session_pattern = events.EventPattern(
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

        events.Rule(
            scope=self,
            id='AwsTagsSTSRule',
            description='Handles STS AssumeRole* events to retrieve session tags',
            rule_name='AwsTagsSTSRule',
            event_pattern=session_pattern,
            targets=event_targets
        )

    #
    def cwe_saml_workaround(self):
        log_group = None

        # if CLOUDTRAIL_LOG_GROUP_NAME is None:
        #     log_group = logs.LogGroup(self, "LogGroup",
        #                               log_group_name=CLOUDTRAIL_LOG_GROUP_NAME,
        #                               retention=logs.RetentionDays.ONE_WEEK
        #                               )
        #     # Create a trail
        #     trail = cloudtrail.Trail(self, "CloudTrail",
        #                              send_to_cloud_watch_logs=True,
        #                              include_global_service_events=False,
        #                              is_multi_region_trail=False
        #                             )
        #     cloudtrail.Trail.cl
        # else:
        log_group = logs.LogGroup.from_log_group_name(self, "ct-loggroup", log_group_name=CLOUDTRAIL_LOG_GROUP_NAME)

        sns_topic = sns.Topic(self, id=SNS_TOPIC_NAME, topic_name=SNS_TOPIC_NAME)


        saml_handler = _lambda.Function(
            self, 'CweAssumeRoleWithSaml',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda/saml_event_handler'),
            handler='saml_handler.handler',
            environment={'default_region': os.environ["CDK_DEFAULT_REGION"]}
        )

        saml_handler.grant_invoke(iam.ServicePrincipal("logs.amazonaws.com"))

        log_group.add_subscription_filter("SubscriptionForSamlEvents",
                                destination=log_destinations.LambdaDestination(saml_handler),
                                filter_pattern=logs.FilterPattern.string_value("$.eventName", "=", "AssumeRoleWithSAML")
                                )

