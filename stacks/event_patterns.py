from aws_cdk import (
    aws_events as _events
)

from tag_factory import handlers


def get_event_pattern(service):
    event_mappings = handlers.EC2Tagger.get_event_resource_mappings()
    events = event_mappings.get(service, None)
    if not events:
        return None

    event_list = list(events.keys())
    return _events.EventPattern(
        source=["aws." + service],
        detail_type=["AWS API Call via CloudTrail"],
        detail={
            "eventSource": [
                service + ".amazonaws.com"
            ],
            "eventName": event_list
        }
    )


def get_services():
    events = handlers.EC2Tagger.get_event_resource_mappings()
    return list(events.keys())
