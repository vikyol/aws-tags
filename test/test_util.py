import json

EVENTS_DIR = "events"


def load_event(event_name):
    with open(f"{EVENTS_DIR}/{event_name}.json") as event_data:
        return json.load(event_data)