class NextServiceScheduler:
    def __init__(self, sim, resource, service_monitor, queue_monitor, wait_monitor):
        self.sim = sim
        self.resource = resource
        self.service_monitor = service_monitor
        self.queue_monitor = queue_monitor
        self.wait_monitor = wait_monitor

    def schedule_next_service(self):
        if not self.resource.queue.is_empty() and self.resource.is_available():
            next_entity = self.resource.queue.dequeue()
            self.queue_monitor.record(len(self.resource.queue.entities))
            self.resource.start_service(self.sim, next_entity, self.service_monitor, self.queue_monitor, self.wait_monitor)
