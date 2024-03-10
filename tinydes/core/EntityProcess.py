from datetime import timedelta
from tinydes.core.Entity import Entity
from tinydes.core.NextServiceScheduler import NextServiceScheduler

class EntityProcess:
    def __init__(self, sim, entity_id, entity_type, resources, arrival_monitor, service_monitor, queue_monitor, wait_monitor):
        self.sim = sim
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.resources = resources
        self.arrival_monitor = arrival_monitor
        self.service_monitor = service_monitor
        self.queue_monitor = queue_monitor
        self.wait_monitor = wait_monitor

    def process(self):
        arrival_time = self.sim.current_time
        service_sequence = []
        entity = Entity(self.entity_type, {"id": self.entity_id, "arrival_time": arrival_time}, arrival_time, service_sequence)
        self.arrival_monitor.record(arrival_time.timestamp())

        resource = min(self.resources, key=lambda r: len(r.queue.entities))

        if resource.is_available():
            self.wait_monitor.record(0)
            resource.start_service(self.sim, entity, self.service_monitor, self.queue_monitor, self.wait_monitor)
        else:
            resource.enqueue_entity(self.sim, entity, self.queue_monitor)
            print(f"{self.entity_type} {self.entity_id} queued at {resource.name} at {arrival_time}")

            next_service_scheduler = NextServiceScheduler(self.sim, resource, self.service_monitor, self.queue_monitor, self.wait_monitor)
            self.sim.schedule_event(timedelta(minutes=0), next_service_scheduler.schedule_next_service)
