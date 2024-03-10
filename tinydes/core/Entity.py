from datetime import datetime

class Entity:
    def __init__(self, entity_type: str, attributes: dict, arrival_time: datetime, service_sequence):
        self.entity_type = entity_type
        self.attributes = attributes
        self.arrival_time = arrival_time
        self.service_sequence = service_sequence  # List of services the entity must go through
        self.waiting_time = 0
        self.current_step = 0  # Tracks the current step in the service sequence

    def next_service(self):
        if self.current_step < len(self.service_sequence):
            return self.service_sequence[self.current_step]
        return None

    def advance_service(self):
        self.current_step += 1
        return self.next_service()