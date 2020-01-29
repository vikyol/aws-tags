#!/usr/bin/env python3

import os
from aws_cdk import core

from stacks.awstags_stack import AwsTagsStack
from stacks.aws_session_stack import AwsSessionStack
from stacks.dynamodb_stack import DbStack


GLOBAL_SERVICES_REGION = "us-east-1"

app = core.App()

AwsTagsStack(app,
             "aws-tags-stack",
             env=core.Environment(
                 account=os.environ["CDK_DEFAULT_ACCOUNT"],
                 region=os.environ["CDK_DEFAULT_REGION"]
             ),
             tags={
                 "Project": "AwsTags"
             })

AwsSessionStack(app,
                "aws-session-stack",
                env=core.Environment(
                    account=os.environ["CDK_DEFAULT_ACCOUNT"],
                    region=os.environ["CDK_DEFAULT_REGION"]
                ),
                tags={
                    "Project": "AwsTags"
                })

AwsSessionStack(app,
                "aws-session-stack-us",
                env=core.Environment(
                    account=os.environ["CDK_DEFAULT_ACCOUNT"],
                    region=GLOBAL_SERVICES_REGION
                ),
                tags={
                    "Project": "AwsTags"
                })

# DbStack(app,
#         "db-stack",
#         env=core.Environment(
#             account=os.environ["CDK_DEFAULT_ACCOUNT"],
#             region=os.environ["CDK_DEFAULT_REGION"]
#         ),
#         tags={
#             "Project": "AwsTags"
#         })

app.synth()
