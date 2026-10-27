class EventBus:

    def __init__(self):
        self.events = []

    def emit(self, event, payload=None):

        self.events.append({
            "event": event,
            "payload": payload
        })

    def get_events(self):

        return self.events

event_bus = EventBus()