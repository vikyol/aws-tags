import logging
from tag_factory import TagFactory


# Tags EC2 resource with the owner and PrincipalId tags automatically
def handler(event, context):
    logger = logging.getLogger("tagging")
    logging.basicConfig(format='"[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s')
    logger.setLevel(logging.DEBUG)

    logger.debug(f'{event}')

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
