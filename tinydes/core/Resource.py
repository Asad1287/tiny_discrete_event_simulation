from tinydes.core.Queue import Queue
from datetime import timedelta
class Resource:
    def __init__(self, name, num_servers, service_time_distribution, schedule):
        self.name = name
        self.num_servers = num_servers
        self.service_time_distribution = service_time_distribution
        self.schedule = schedule
        self.queue = Queue()
        self.busy = 0  # Tracks the number of servers currently busy

    def is_available(self):
        return self.busy < self.num_servers

    def start_service(self, simulation, entity, service_monitor, queue_monitor, wait_monitor):
        self.busy += 1

        # Calculate waiting time as the difference between the current time and the entity's arrival time
        wait_time = (simulation.current_time - entity.arrival_time).total_seconds() / 60
        entity.waiting_time = wait_time  # Store waiting time in the entity

        # Record the waiting time using the wait_monitor
        wait_monitor.record(wait_time)

        # Proceed with scheduling the service completion and other logic
        service_time = timedelta(minutes=abs(self.service_time_distribution.generate()[0]))
        print(f"{entity.entity_type} {entity.attributes['id']} starts service at {simulation.current_time} (Waited: {wait_time:.2f} mins)")
        simulation.schedule_event(service_time, lambda: self.finish_service(simulation, entity, service_monitor, queue_monitor, wait_monitor))

        # Update queue length monitoring
        queue_monitor.record(len(self.queue.entities))


    def enqueue_entity(self, simulation, entity, queue_monitor):
         self.queue.enqueue(entity)
         entity.enqueue_time = simulation.current_time  # Record the time when the entity enters the queue
         queue_monitor.record(len(self.queue.entities))


    def finish_service(self, simulation, entity, service_monitor, queue_monitor, wait_monitor):
        self.busy -= 1
        # Corrected to calculate service time directly based on service start and end times
        service_end_time = simulation.current_time
        service_time = (service_end_time - entity.arrival_time).total_seconds() / 60
        service_monitor.record(service_time)
        print(f"{entity.entity_type} {entity.attributes['id']} completes service at {simulation.current_time} - Service time: {service_time:.2f} mins")

        if not self.queue.is_empty():
            next_entity = self.queue.dequeue()
            self.start_service(simulation, next_entity, service_monitor, queue_monitor, wait_monitor)

