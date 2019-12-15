#!/usr/bin/env python3

from aws_cdk import core

from stacks.awstags_stack import AutoTagsStack


app = core.App()
AutoTagsStack(app,
            "autotags",
            env={'region': 'eu-central-1'},
            tags={
                "CostCenter": "",
                "Project": "",
                "Owner": ""
            }
)

app.synth()
