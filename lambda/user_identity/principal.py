# Processes userIdentity in event data.
# https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html

def get_root(event):
    return "Root"


def get_user(event):
    return event['detail']['userIdentity']['userName']


def get_aws_service(event):
    return event['detail']['userIdentity']['invokedBy']


def get_federated_user(event):
    principal = event['detail']['userIdentity'].get('principalId', None)

    return principal.split(':')[1] if principal else None


def get_aws_account(event):
    return None


def get_role_id(event):
    detail = event['detail']
    principal = detail['userIdentity'].get('principalId', None)
    return principal.split(':')[0]


def get_assumed_role(event):
    return event['detail']['userIdentity']['sessionContext']['sessionIssuer']['userName']


def get_saml_user():
    #TODO Handle SAML Federation
    return None


def get_web_identity_user():
    # TODO Handle Web Identity Federation
    return None


def no_user():
    return ""

# event.detail.userIdentity.type field
user_type = {
    "Root": get_root,
    "IAMUser": get_user,
    "AssumedRole": get_assumed_role,
    "FederatedUser": get_federated_user,
    "AWSAccount": get_aws_account,
    "AWSService": get_aws_service,
    "SAMLUser": get_saml_user,
    "WebIdentityUser": get_web_identity_user
}


def get_principal(event):
    return user_type.get(event['detail']['userIdentity']['type'], no_user)(event)
