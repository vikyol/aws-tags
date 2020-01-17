# Processes userIdentity in event data.
# https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html

from .tags_db import get_tags_from_db
from .iam_tags import (
    get_role_tags,
    get_user_tags
)


def handle_root(event):
    return "root"


# Invoked by an IAM user
def handle_iam_user(event):
    return event['detail']['userIdentity']['userName']


# Invoked by an AWS Service
def handle_aws_service(event):
    return event['detail']['userIdentity']['invokedBy']


# A federated user invoked an action.
def handle_federated_user(event):
    principal = event['detail']['userIdentity'].get('principalId', None)

    return principal.split(':')[1] if principal else None


# Cross-account action
def handle_aws_account(event):
    return None


def handle_assumed_role(event):
    user_identity = event['detail']['userIdentity']
    # user_name = get_user_name(user_identity)
    # principal_arn = user_identity['sessionContext']['sessionIssuer']['arn']
    # principal_id = get_role_id(user_identity)

    return event['detail']['userIdentity']['sessionContext']['sessionIssuer']['userName']


def handle_saml_user():
    #TODO Handle SAML Federation
    return None


def handle_web_identity_user():
    # TODO Handle Web Identity Federation
    return None


def no_user():
    return {}


# Returns the role id. e.g. AROA6P5R2IBZSNO66ZBOE:erhvik -> AROA6P5R2IBZSNO66ZBOE
def get_role_id(user_identity):
    principal = user_identity.get('principalId', None)
    return principal.split(':')[0] if principal else None


# Returns the user name from principal ID. e.g. AROA6P5R2IBZSNO66ZBOE:erhvik -> erhvik
def get_user_name(user_identity):
    principal = user_identity.get('principalId', None)
    return principal.split(':')[1] if principal else None


# event.detail.userIdentity.type field
user_type = {
    "Root": handle_root,
    "IAMUser": handle_iam_user,
    "AssumedRole": handle_assumed_role,
    "FederatedUser": handle_federated_user,
    "AWSAccount": handle_aws_account,
    "AWSService": handle_aws_service,
    "SAMLUser": handle_saml_user,
    "WebIdentityUser": handle_web_identity_user
}


def get_principal(event):
    return user_type.get(event['detail']['userIdentity']['type'], no_user)(event)


def fetch_tags(event):
    user_type = event['detail']['userIdentity']['type']

    if user_type == 'IAMUser':
        user_name = event['detail']['userIdentity']['userName']
        return get_user_tags(user_name)
    elif user_type == 'AssumedRole':
        # Fetch the tags attached to the IAM role
        role_name = event['detail']['userIdentity']['sessionContext']['sessionIssuer']['userName']
        role_tags = get_role_tags(role_name)

        # Fetch session tags from DynamoDb aws-tags table
        role_id = event['detail']['userIdentity']['principalId']
        session_tags = get_tags_from_db(role_id)
        print("Retrieve session tags from database: {}".format(session_tags))

        tags = list({x['Key']: x for x in role_tags + session_tags}.values())
        print("Merged role and session tags: {}".format(tags))

        return tags
    else:
        print("Not a valid user_type in event: " + user_type)