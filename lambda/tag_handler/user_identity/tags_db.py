import boto3
from botocore.exceptions import ClientError
import json


# Check if a dynamodb table exists
def table_exists(table_name):
    client = boto3.client('dynamodb')

    try:
        client.describe_table(TableName=table_name)
        return True
    except client.exceptions.ResourceNotFoundException:
        return False


def get_tags_from_db(role_id):
    table_name = "aws-tags"
    client = boto3.client("dynamodb")
    print("GetItem for " + role_id)

    if not table_exists(table_name):
        return []

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    try:
        response = table.get_item(
            Key={
                'assumed_role_id': role_id
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return []
    else:
        print("GetItem successful. Tags: {}".format(response['Item']['tags']))

    tags = json.loads(response['Item']['tags'])

    return tags if tags else []


def write_tags_to_db(role_id, principal_arn, session_tags, expiration):
    dynamodb = boto3.resource('dynamodb')
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



if __name__ == '__main__':
    get_tags_from_db("AROAIJ6IV7WBS64P73R7G:aws-tags")
