import boto3
import json


def get_tags_from_db(principal):
    client = boto3.client("dynamodb")

    response = client.get_item(
        Key={
            'principal_id': {
                'S': principal
            }
        },
        TableName='aws-tags'
    )

    print(response['Item']['tags']['S'])

    return json.loads(response['Item']['tags']['S'])


if __name__ == '__main__':
    get_tags_from_db("erhan.vikyol@buzzcloud.se")
