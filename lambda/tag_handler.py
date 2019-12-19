import boto3
import logging
import tag_factory


logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Tags EC2 resource with the owner and PrincipalId tags automatically
def handler(event, context):
    print(event)
    try:
        service = event['source']

        factory = tag_factory.TagFactory()
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
