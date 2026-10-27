class EventBus:

    def __init__(self):

        self.events = []

    def emit(self, event, data=None):

        self.events.append({
            "event": event,
            "data": data
        })

    def history(self):

        return self.events[-50:]

event_bus = EventBus()