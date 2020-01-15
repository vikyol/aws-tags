import boto3
import json
import base64
import gzip
import logging
import os
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    message_encoded = event['awslogs']['data']
    compressed_payload = base64.b64decode(message_encoded)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)
    print("Payload:")
    print(json.dumps(payload))

    logEvents = payload["logEvents"]
    print(logEvents)
    print(logEvents[0])
    process_assume_saml(json.loads(logEvents[0]["message"]))


def process_assume_saml(event):
    print("Processing event: ")
    print(event)

    session_tags = event['requestParameters'].get('tags', None)
    if not session_tags:
        logger.warning("No session tags in the request")
        return

    # Cloudtrail lowers the case of tag keys, capitalize each key. {'key':'a'} -> {'Key':'a'}
    session_tags = [dict((k.capitalize(), v) for k, v in tags.items()) for tags in session_tags]

    response_elements = event['responseElements']
    principal_arn = event['userIdentity']['arn']
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