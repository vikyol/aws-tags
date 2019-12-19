#!/usr/bin/env python3

from aws_cdk import core

from stacks.awstags_stack import AwsTagsStack


app = core.App()
AwsTagsStack(app,
            "awstags",
            env={'region': 'eu-central-1'},
            tags={
                "CostCenter": "9999",
                "Project": "ABCD",
                "Owner": "Me"
            }
)

app.synth()