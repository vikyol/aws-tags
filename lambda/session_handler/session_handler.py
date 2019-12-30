import logging
import boto3
import json
import os
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Tags EC2 resource with the owner and PrincipalId tags automatically
def handler(event, context):
    print(json.dumps(event))
    session_tags = event['detail']['requestParameters'].get('tags', None)
    if not session_tags:
        logger.warning("No session tags in the request")
        return

    # Cloudtrail lowers the case of tag keys, capitalize each key. {'key':'a'} -> {'Key':'a'}
    session_tags = [dict((k.capitalize(), v) for k, v in tags.items()) for tags in session_tags]

    response_elements = event['detail']['responseElements']
    principal_arn = event['detail']['userIdentity']['arn']
    assumed_role_id = response_elements['assumedRoleUser']['assumedRoleId']
    expiration = response_elements['credentials']['expiration']
    # Store extracted tags to Dynamodb
    write_tags_to_db(assumed_role_id, principal_arn, session_tags, expiration)


def write_tags_to_db(role_id, principal_arn, session_tags, expiration):
    region = os.environ.get('default_region', 'eu-north-1')
    dynamodb = boto3.resource('dynamodb', region_name=region)
    print("Saving role_id {} to db".format(role_id))

    try:
        table = dynamodb.Table("aws-tags")
        response = table.put_item(
            Item={
                'assumed_role_id': role_id,
                'tags': json.dumps(session_tags),
                'principal_arn': principal_arn,
                'expiration': expiration
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Session tags for {} saved in database".format(role_id))
