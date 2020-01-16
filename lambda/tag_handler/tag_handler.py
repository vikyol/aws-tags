import logging
import json
from tag_factory import TagFactory
import sys

logger = logging.getLogger("tagging")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


# Tags EC2 resource with the owner and PrincipalId tags automatically
def handler(event, context):
    print(json.dumps(event))
    try:
        service = event['source']

        factory = TagFactory()
        tagger = factory.get_tagger(service)

        if tagger:
            tagger(event).tag_resources()
            return True
        else:
            logger.warning("No tag handler registered for this service: " + service)
            return False

    except Exception as e:
        logger.error('Something went wrong: ' + str(e))
        return False

if __name__ == '__main__':
    event = {}
    handler(event, None)
