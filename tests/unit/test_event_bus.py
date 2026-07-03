import unittest
from backend.services.coordinator.event_bus import EventBus
from backend.services.coordinator.models import Event


class TestEventBus(unittest.TestCase):
    def test_publish_subscribe(self):
        bus = EventBus()
        events_received = []

        def handler(event: Event):
            events_received.append(event)

        bus.subscribe("test.topic", handler)

        event1 = Event(topic="test.topic", payload={"data": 1})
        bus.publish(event1)

        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0].topic, "test.topic")
        self.assertEqual(events_received[0].payload["data"], 1)

        # Unsubscribe
        bus.unsubscribe("test.topic", handler)
        event2 = Event(topic="test.topic", payload={"data": 2})
        bus.publish(event2)

        self.assertEqual(len(events_received), 1)

    def test_wildcard_subscribe(self):
        bus = EventBus()
        events_received = []

        def handler(event: Event):
            events_received.append(event)

        bus.subscribe("*", handler)

        event1 = Event(topic="any.topic", payload={"data": 1})
        bus.publish(event1)

        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0].topic, "any.topic")


if __name__ == "__main__":
    unittest.main()
