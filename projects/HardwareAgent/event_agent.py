import win32evtlog

class EventAgent:

    def recent_events(self):

        server = "localhost"
        logtype = "System"

        hand = win32evtlog.OpenEventLog(
            server,
            logtype
        )

        events = win32evtlog.ReadEventLog(
            hand,
            win32evtlog.EVENTLOG_BACKWARDS_READ |
            win32evtlog.EVENTLOG_SEQUENTIAL_READ,
            0
        )

        result = []

        for event in events[:10]:

            result.append({
                "event_id": event.EventID
            })

        return result