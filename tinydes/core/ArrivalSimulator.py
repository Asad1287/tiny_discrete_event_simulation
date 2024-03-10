import heapq
from datetime import datetime, timedelta
from scipy import stats
import numpy as np
from tinydes.core.EntityProcess import EntityProcess
class ArrivalSimulator:
    def __init__(self, sim, resources, arrival_monitor, service_monitor, queue_monitor, wait_monitor, entity_type):
        self.sim = sim
        self.resources = resources
        self.arrival_monitor = arrival_monitor
        self.service_monitor = service_monitor
        self.queue_monitor = queue_monitor
        self.wait_monitor = wait_monitor
        self.entity_type = entity_type
        self.entity_id = 1

    def simulate_arrivals(self):
        while True:
            arrival_delay = abs(np.random.normal(loc=1, scale=1))
            next_arrival_time = self.sim.current_time + timedelta(minutes=arrival_delay)
            if next_arrival_time > self.sim.end_time:
                break
            yield timedelta(minutes=arrival_delay)

            entity_process = EntityProcess(self.sim, self.entity_id, self.entity_type, self.resources,
                                           self.arrival_monitor, self.service_monitor, self.queue_monitor, self.wait_monitor)
            entity_process.process()
            self.entity_id += 1