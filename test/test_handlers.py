import unittest
import logging
from tag_factory import TagFactory
from tag_factory.handlers import (
    EC2Tagger,
    ELBTagger
)
from test_util import load_event

logger = logging.getLogger("tagging")
logging.basicConfig(format='"[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s')
logger.setLevel(logging.DEBUG)


class TestEventResources(unittest.TestCase):

    # Assure that resource mappings is not empty
    def test_get_resources(self):
        resources = EC2Tagger.get_event_resource_mappings()
        self.assertTrue(len(resources) > 0)

        services = TagFactory().get_service_list()
        for service in services:
            self.assertIsNotNone(resources.get(service, None), f"{service} has no resource mapping")

    # Should return resource ID/ARN successfully
    def test_get_resource_id(self):
        event = load_event("CreateVolume")
        tagger = EC2Tagger(event)

        resource_id = tagger.get_resource_id()
        self.assertEqual(resource_id, "vol-01a9d867be2fb6d86")

    # If a response contains a list of resources, get_resource_id() should return the first ARN/ID.
    def test_get_list_of_resources(self):
        event = load_event("CreateLoadBalancer")
        load_balancer_arn = event['detail']['responseElements']['loadBalancers'][0]['loadBalancerArn']
        tagger = ELBTagger(event)

        resource_id = tagger.get_resource_id()
        self.assertEqual(resource_id, load_balancer_arn)
