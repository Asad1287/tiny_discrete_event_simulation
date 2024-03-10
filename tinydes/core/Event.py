class Event:
    def __init__(self, event_type, time, entity=None, resource=None):
        self.event_type = event_type
        self.time = time
        self.entity = entity
        self.resource = resource