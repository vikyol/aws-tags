import boto3
import logging
import tag_factory


logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Tags EC2 resource with the owner and PrincipalId tags automatically
def handler(event, context):
    try:
        event_source = event['detail']['eventSource']

        factory = tag_factory.factory()
        tagger = factory.get_tagger(event_source)

        if tagger:
            tagger.tag_resources(event)
            return True
        else:
            logger.warning("No tag handler for this service: " + event_source)
            return False
    except Exception as e:
        logger.error('Something went wrong: ' + str(e))
        return False
