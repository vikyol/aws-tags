import unittest
import boto3

from moto import mock_dynamodb2
import unittest
from user_identity import tags_db


class TestGetTagsFromDb(unittest.TestCase):
    @mock_dynamodb2
    def test_get_tags(self):
        user_id = 'test-user'

        db = boto3.resource('dynamodb', 'eu-west-1')

        table = db.create_table(
            TableName='aws-tags',
            KeySchema=[
                {
                    'AttributeName': 'principal_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'principal_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

        table.meta.client.get_waiter('table_exists').wait(TableName='aws-tags')

        table.put_item(
            Item={
                "id": {"S": user_id},
                "tags": {"S": "Test"}
            }
        )

        #res = tags_db.get_tags_from_db(id)
        #self.assertEqual(res, '{"Key":"Project", "Value":"AwsTags"}')


if __name__ == '__main__':
    unittest.main()
