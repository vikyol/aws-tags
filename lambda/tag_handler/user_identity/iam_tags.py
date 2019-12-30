import boto3


# Returns the tags of a role.
def get_role_tags(role_name) -> list:
    iam = boto3.client('iam')

    print("Fetching the tags attached to the role " + role_name)
    response = iam.list_role_tags(RoleName=role_name)
    print(response)

    # {'Tags': [{'Key': 'MyTag', 'Value': 'Yes'}],
    # 'IsTruncated': False,
    # 'ResponseMetadata': {'RequestId': '', 'HTTPStatusCode': 200,
    # 'HTTPHeaders': {'x-amzn-requestid': '', 'content-type': 'text/xml', 'content-length': '325', 'date': ''},
    # 'RetryAttempts': 0}
    # }

    return response['Tags']


# Returns the tags of a user.
def get_user_tags(user_name) -> list:
    iam = boto3.client('iam')

    print("Fetching the tags attached to the user " + user_name)
    response = iam.list_user_tags(UserName=user_name)
    print(response)

    return response['Tags']
